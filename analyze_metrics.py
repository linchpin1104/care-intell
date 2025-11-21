"""
놀이 세션 분석 지표 추출 모듈
- 아동발화비율, 발화양, 주제지속도, 맥락전환도 등 분석
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple
from collections import Counter, defaultdict
import statistics


class PlaySessionAnalyzer:
    """놀이 세션 분석 클래스"""
    
    def __init__(self, session_path: str):
        self.session_path = Path(session_path)
        self.session_name = self.session_path.name
        
        # 경로 설정
        self.vtt_dir = self.session_path / "vtt"
        self.ai_response_dir = self.session_path / "ai_response"
        self.feature_file = self.session_path / "feature" / f"{self.session_name}_features.json"
        
        # 데이터 저장
        self.dialogues = []
        self.audio_features = {}
        
    def parse_vtt_file(self, vtt_path: Path) -> List[Dict]:
        """VTT 파일 파싱"""
        dialogues = []
        
        with open(vtt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # VTT 블록 파싱
        blocks = content.split('\n\n')
        
        for block in blocks:
            if '-->' in block:
                lines = block.strip().split('\n')
                if len(lines) >= 2:
                    time_line = lines[0]
                    text_line = ' '.join(lines[1:])
                    
                    # 화자와 텍스트 분리
                    speaker_match = re.match(r'\[(.*?)\]\s*(.*)', text_line)
                    if speaker_match:
                        speaker = speaker_match.group(1)
                        text = speaker_match.group(2).strip()
                        
                        # 시간 파싱
                        time_match = re.match(r'(\d+:\d+:\d+\.\d+)\s*-->\s*(\d+:\d+:\d+\.\d+)', time_line)
                        if time_match:
                            dialogues.append({
                                'start': time_match.group(1),
                                'end': time_match.group(2),
                                'speaker': speaker,
                                'text': text
                            })
        
        return dialogues
    
    def load_all_vtt_files(self):
        """모든 VTT 파일 로드"""
        print(f"VTT 파일 로딩 중: {self.vtt_dir}")
        
        # _후처리됨.vtt 파일 우선, 없으면 _subtitle.vtt 사용
        vtt_files = sorted(self.vtt_dir.glob("*_후처리됨.vtt"))
        if not vtt_files:
            vtt_files = sorted(self.vtt_dir.glob("*_subtitle.vtt"))
        
        for vtt_file in vtt_files:
            dialogues = self.parse_vtt_file(vtt_file)
            self.dialogues.extend(dialogues)
        
        print(f"총 {len(self.dialogues)}개 발화 로드됨")
    
    def load_audio_features(self):
        """오디오 특징 로드"""
        if self.feature_file.exists():
            with open(self.feature_file, 'r', encoding='utf-8') as f:
                self.audio_features = json.load(f)
            print(f"오디오 특징 로드됨: {self.feature_file.name}")
    
    def identify_speakers(self) -> Tuple[str, str]:
        """화자 구분 (선생님 vs 아이)"""
        speaker_counter = Counter([d['speaker'] for d in self.dialogues])
        
        teacher = None
        child = None
        
        for speaker, count in speaker_counter.items():
            if '선생님' in speaker or '교사' in speaker:
                teacher = speaker
            elif '아이' in speaker:
                child = speaker
        
        return teacher, child
    
    def calculate_child_speech_ratio(self) -> Dict:
        """아동 발화 비율 계산"""
        teacher, child = self.identify_speakers()
        
        child_utterances = [d for d in self.dialogues if d['speaker'] == child]
        teacher_utterances = [d for d in self.dialogues if d['speaker'] == teacher]
        
        total_utterances = len(self.dialogues)
        child_count = len(child_utterances)
        teacher_count = len(teacher_utterances)
        
        child_ratio = child_count / total_utterances if total_utterances > 0 else 0
        
        # 텍스트 길이 기준 비율
        child_text_length = sum(len(d['text']) for d in child_utterances)
        teacher_text_length = sum(len(d['text']) for d in teacher_utterances)
        total_text_length = child_text_length + teacher_text_length
        
        child_text_ratio = child_text_length / total_text_length if total_text_length > 0 else 0
        
        return {
            'child_utterance_count': child_count,
            'teacher_utterance_count': teacher_count,
            'total_utterance_count': total_utterances,
            'child_utterance_ratio': round(child_ratio * 100, 2),  # 퍼센트
            'child_text_length': child_text_length,
            'teacher_text_length': teacher_text_length,
            'child_text_ratio': round(child_text_ratio * 100, 2),  # 퍼센트
            'teacher': teacher,
            'child': child
        }
    
    def calculate_utterance_volume(self) -> Dict:
        """발화량 계산"""
        teacher, child = self.identify_speakers()
        
        child_utterances = [d for d in self.dialogues if d['speaker'] == child]
        
        # 문장 수
        child_sentences = sum(len(d['text'].split('.')) for d in child_utterances)
        
        # 평균 발화 길이
        child_avg_length = statistics.mean([len(d['text']) for d in child_utterances]) if child_utterances else 0
        
        # 단어 수 추정 (한국어는 음절 기준)
        child_word_count = sum(len(d['text'].replace(' ', '')) for d in child_utterances)
        
        return {
            'child_total_utterances': len(child_utterances),
            'child_total_sentences': child_sentences,
            'child_avg_utterance_length': round(child_avg_length, 2),
            'child_total_syllables': child_word_count,
            'child_avg_utterance_per_minute': round(len(child_utterances) / (len(self.dialogues) / 30), 2) if self.dialogues else 0
        }
    
    def analyze_topic_consistency(self) -> Dict:
        """주제 지속도 분석"""
        teacher, child = self.identify_speakers()
        
        # 주요 키워드 추출 (간단한 버전)
        keywords_by_segment = []
        segment_size = 10  # 10개 발화를 하나의 세그먼트로
        
        for i in range(0, len(self.dialogues), segment_size):
            segment = self.dialogues[i:i+segment_size]
            text = ' '.join([d['text'] for d in segment])
            
            # 간단한 키워드 추출 (2-3글자 이상 명사 추정)
            words = re.findall(r'[가-힣]{2,}', text)
            keywords = Counter(words).most_common(5)
            keywords_by_segment.append([k[0] for k in keywords])
        
        # 세그먼트 간 키워드 중복도 계산
        topic_changes = 0
        for i in range(len(keywords_by_segment) - 1):
            current_keywords = set(keywords_by_segment[i])
            next_keywords = set(keywords_by_segment[i+1])
            
            overlap = len(current_keywords & next_keywords)
            if overlap < 2:  # 공통 키워드가 2개 미만이면 주제 전환
                topic_changes += 1
        
        consistency_score = 1 - (topic_changes / len(keywords_by_segment)) if keywords_by_segment else 0
        
        return {
            'total_segments': len(keywords_by_segment),
            'topic_changes': topic_changes,
            'topic_consistency_score': round(consistency_score * 100, 2),  # 퍼센트
            'main_keywords': keywords_by_segment[0] if keywords_by_segment else []
        }
    
    def analyze_context_switches(self) -> Dict:
        """맥락 전환도 분석"""
        teacher, child = self.identify_speakers()
        
        # 연속된 발화에서 화자 전환 횟수
        speaker_switches = 0
        for i in range(len(self.dialogues) - 1):
            if self.dialogues[i]['speaker'] != self.dialogues[i+1]['speaker']:
                speaker_switches += 1
        
        # 평균 연속 발화 길이
        current_speaker = None
        consecutive_counts = []
        current_count = 0
        
        for dialogue in self.dialogues:
            if dialogue['speaker'] == current_speaker:
                current_count += 1
            else:
                if current_count > 0:
                    consecutive_counts.append(current_count)
                current_speaker = dialogue['speaker']
                current_count = 1
        
        if current_count > 0:
            consecutive_counts.append(current_count)
        
        avg_consecutive = statistics.mean(consecutive_counts) if consecutive_counts else 0
        
        return {
            'total_speaker_switches': speaker_switches,
            'switch_rate': round(speaker_switches / len(self.dialogues) * 100, 2) if self.dialogues else 0,
            'avg_consecutive_utterances': round(avg_consecutive, 2),
            'max_consecutive_utterances': max(consecutive_counts) if consecutive_counts else 0
        }
    
    def analyze_problem_solving(self) -> Dict:
        """문제 해결 발화 분석"""
        teacher, child = self.identify_speakers()
        
        # 문제 해결 관련 키워드
        problem_keywords = ['어떻게', '왜', '어디', '무엇', '누가', '언제', 
                           '해볼까', '할까', '하면', '만들', '찾', '생각']
        
        child_utterances = [d for d in self.dialogues if d['speaker'] == child]
        
        problem_solving_count = 0
        problem_solving_utterances = []
        
        for utterance in child_utterances:
            text = utterance['text']
            if any(keyword in text for keyword in problem_keywords):
                problem_solving_count += 1
                problem_solving_utterances.append(text)
        
        ratio = problem_solving_count / len(child_utterances) if child_utterances else 0
        
        return {
            'problem_solving_utterance_count': problem_solving_count,
            'problem_solving_ratio': round(ratio * 100, 2),
            'examples': problem_solving_utterances[:5]  # 상위 5개 예시
        }
    
    def analyze_sentiment(self) -> Dict:
        """긍정/부정 비율 분석"""
        teacher, child = self.identify_speakers()
        
        # 긍정/부정 키워드
        positive_keywords = ['좋아', '재밌', '신나', '예쁘', '멋지', '우와', '좋', '감사', '고마워', '사랑']
        negative_keywords = ['싫어', '안돼', '못', '아니', '안', '슬프', '무서', '아파', '힘들']
        
        child_utterances = [d for d in self.dialogues if d['speaker'] == child]
        
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        for utterance in child_utterances:
            text = utterance['text']
            has_positive = any(keyword in text for keyword in positive_keywords)
            has_negative = any(keyword in text for keyword in negative_keywords)
            
            if has_positive and not has_negative:
                positive_count += 1
            elif has_negative and not has_positive:
                negative_count += 1
            else:
                neutral_count += 1
        
        total = len(child_utterances)
        
        return {
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'positive_ratio': round(positive_count / total * 100, 2) if total > 0 else 0,
            'negative_ratio': round(negative_count / total * 100, 2) if total > 0 else 0,
            'sentiment_score': round((positive_count - negative_count) / total * 100, 2) if total > 0 else 0
        }
    
    def extract_emotion_words(self) -> Dict:
        """주요 정서 단어 추출"""
        teacher, child = self.identify_speakers()
        
        emotion_keywords = {
            '기쁨': ['좋아', '재밌', '신나', '행복', '즐거', '웃'],
            '슬픔': ['슬프', '속상', '아쉬', '우울'],
            '화남': ['화', '짜증', '싫', '미워'],
            '놀람': ['우와', '헐', '대박', '신기'],
            '두려움': ['무서', '겁나', '떨려'],
            '사랑': ['사랑', '좋아해', '예뻐', '귀여']
        }
        
        child_utterances = [d for d in self.dialogues if d['speaker'] == child]
        child_text = ' '.join([d['text'] for d in child_utterances])
        
        emotion_counts = {}
        emotion_examples = {}
        
        for emotion, keywords in emotion_keywords.items():
            count = sum(child_text.count(keyword) for keyword in keywords)
            emotion_counts[emotion] = count
            
            # 예시 추출
            examples = []
            for utterance in child_utterances:
                if any(keyword in utterance['text'] for keyword in keywords):
                    examples.append(utterance['text'])
                    if len(examples) >= 3:
                        break
            emotion_examples[emotion] = examples
        
        return {
            'emotion_counts': emotion_counts,
            'emotion_examples': emotion_examples,
            'dominant_emotion': max(emotion_counts.items(), key=lambda x: x[1])[0] if emotion_counts else None
        }
    
    def extract_main_topics(self) -> Dict:
        """주요 토픽(주제) 추출"""
        # 전체 텍스트에서 빈도수 높은 명사 추출
        all_text = ' '.join([d['text'] for d in self.dialogues])
        
        # 2-4글자 한글 단어 추출
        words = re.findall(r'[가-힣]{2,4}', all_text)
        
        # 불용어 제거 (조사, 어미 등)
        stopwords = ['이거', '저거', '그거', '여기', '저기', '그리고', '그런데', '하지만', 
                    '있어', '없어', '이렇게', '저렇게', '어떻게', '선생님']
        
        words = [w for w in words if w not in stopwords]
        
        # 빈도수 계산
        word_freq = Counter(words)
        top_topics = word_freq.most_common(10)
        
        # 놀이 유형 추정
        play_types = {
            '역할놀이': ['경찰', '의사', '엄마', '아빠', '선생님', '요리', '가게'],
            '구성놀이': ['블록', '레고', '쌓기', '만들기', '건물'],
            '미술놀이': ['그림', '색칠', '그리기', '물감', '크레파스'],
            '게임놀이': ['게임', '놀이', '승부', '이기', '지'],
            '탐색놀이': ['보기', '찾기', '관찰', '실험']
        }
        
        detected_play_types = []
        for play_type, keywords in play_types.items():
            if any(keyword in all_text for keyword in keywords):
                detected_play_types.append(play_type)
        
        return {
            'top_keywords': [{'word': word, 'count': count} for word, count in top_topics],
            'detected_play_types': detected_play_types,
            'total_unique_words': len(set(words))
        }
    
    def analyze_all(self) -> Dict:
        """전체 분석 실행"""
        print(f"\n{'='*60}")
        print(f"분석 시작: {self.session_name}")
        print(f"{'='*60}")
        
        # 데이터 로드
        self.load_all_vtt_files()
        self.load_audio_features()
        
        # 세션 정보 파싱
        session_info = self.parse_session_name()
        
        # 각 지표 계산
        print("\n지표 계산 중...")
        results = {
            'session_info': session_info,
            'audio_features': self.audio_features,
            'speech_ratio': self.calculate_child_speech_ratio(),
            'utterance_volume': self.calculate_utterance_volume(),
            'topic_consistency': self.analyze_topic_consistency(),
            'context_switches': self.analyze_context_switches(),
            'problem_solving': self.analyze_problem_solving(),
            'sentiment': self.analyze_sentiment(),
            'emotion_words': self.extract_emotion_words(),
            'main_topics': self.extract_main_topics()
        }
        
        print("\n✓ 분석 완료!")
        return results
    
    def parse_session_name(self) -> Dict:
        """세션 이름에서 정보 추출"""
        # 예: 20251017-이민정교사-김준우-만4세-02_00_48-65kbps_mono
        parts = self.session_name.split('-')
        
        info = {
            'date': parts[0] if len(parts) > 0 else '',
            'teacher_name': parts[1] if len(parts) > 1 else '',
            'child_name': parts[2] if len(parts) > 2 else '',
            'age': parts[3] if len(parts) > 3 else '',
            'duration': parts[4] if len(parts) > 4 else '',
            'session_name': self.session_name
        }
        
        return info


def main():
    """테스트 실행"""
    # 샘플 세션 분석
    session_path = "/Users/healin/Downloads/develop/care-intell/raw_data/20251017-이민정교사-김준우-만4세-02_00_48-65kbps_mono"
    
    analyzer = PlaySessionAnalyzer(session_path)
    results = analyzer.analyze_all()
    
    # 결과 저장
    output_dir = Path("/Users/healin/Downloads/develop/care-intell/analysis_results")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / f"{analyzer.session_name}_detailed_analysis.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n결과 저장됨: {output_file}")
    
    # 주요 지표 출력
    print(f"\n{'='*60}")
    print("주요 분석 결과")
    print(f"{'='*60}")
    print(f"아동 발화 비율: {results['speech_ratio']['child_utterance_ratio']}%")
    print(f"아동 발화 수: {results['utterance_volume']['child_total_utterances']}회")
    print(f"주제 지속도: {results['topic_consistency']['topic_consistency_score']}점")
    print(f"문제해결 발화 비율: {results['problem_solving']['problem_solving_ratio']}%")
    print(f"감정 점수: {results['sentiment']['sentiment_score']}점")
    print(f"주요 놀이 유형: {', '.join(results['main_topics']['detected_play_types'])}")


if __name__ == "__main__":
    main()

