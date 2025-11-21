#!/usr/bin/env python3
"""
놀이 세션 분석 스크립트
- 아동 발화 분석
- 주제/토픽 추출
- 감정 분석
- 상호작용 패턴 분석
"""

import json
import os
import re
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
import statistics

class PlaySessionAnalyzer:
    """놀이 세션 분석기"""
    
    def __init__(self, session_dir):
        """
        Args:
            session_dir: 세션 디렉토리 경로 (예: raw_data/20251017-이민정교사-김준우-만4세-02_00_48-65kbps_mono)
        """
        self.session_dir = Path(session_dir)
        self.session_name = self.session_dir.name
        
        # 디렉토리 구조
        self.vtt_dir = self.session_dir / "vtt"
        self.ai_response_dir = self.session_dir / "ai_response"
        self.feature_dir = self.session_dir / "feature"
        self.meta_path = self.session_dir / "meta.json"
        
        # 분석 결과 저장
        self.meta_info = {}
        self.dialogues = []  # [{speaker, text, start_time, end_time, segment}]
        self.segments = []  # 2분 단위 세그먼트 정보
        
        # 감정 키워드 사전 (한국어)
        self.positive_keywords = [
            '좋아', '재밌', '신기', '멋지', '우와', '와', '예쁘', '행복', 
            '즐거', '웃', '하하', '히히', '응', '네', '감사', '고마워',
            '사랑', '최고', '대박', '굿', '좋다', '괜찮', '그래'
        ]
        
        self.negative_keywords = [
            '싫', '안돼', '아니', '슬퍼', '무서', '아파', '힘들', '짜증',
            '화나', '미워', '나빠', '속상', '우', '엉엉', '안좋', '별로',
            '실망', '걱정', '불안'
        ]
        
        # 문제해결 관련 키워드
        self.problem_solving_keywords = [
            '어떻게', '왜', '방법', '생각', '해결', '찾', '만들', '해봐',
            '해볼까', '하면', '이렇게', '저렇게', '도와', '같이', '함께',
            '이유', '까닭', '그래서', '그러면', '그럼'
        ]
        
    def parse_filename_info(self):
        """파일명에서 메타 정보 추출"""
        # 예: 20251017-이민정교사-김준우-만4세-02_00_48-65kbps_mono
        parts = self.session_name.split('-')
        
        info = {
            'date': parts[0] if len(parts) > 0 else '',
            'teacher_name': '',
            'child_name': '',
            'child_age': '',
            'duration': '',
            'session_name': self.session_name
        }
        
        # 교사 이름 추출 (끝에 "교사"가 붙음)
        for part in parts:
            if '교사' in part:
                info['teacher_name'] = part.replace('교사', '')
                break
        
        # 나이 추출 (만X세)
        for part in parts:
            if '만' in part and '세' in part:
                info['child_age'] = part
                break
        
        # 아이 이름은 교사 다음 파트
        if len(parts) > 2:
            info['child_name'] = parts[2]
        
        # 시간 정보
        if len(parts) > 3:
            time_part = parts[3]
            info['duration'] = time_part
            
        return info
    
    def load_meta_info(self):
        """메타 정보 로드 (있는 경우)"""
        if self.meta_path.exists():
            with open(self.meta_path, 'r', encoding='utf-8') as f:
                self.meta_info = json.load(f)
                # session_name이 없으면 추가
                if 'session_name' not in self.meta_info:
                    self.meta_info['session_name'] = self.session_name
        else:
            self.meta_info = self.parse_filename_info()
        
        return self.meta_info
    
    def parse_vtt_file(self, vtt_path):
        """VTT 파일 파싱"""
        dialogues = []
        
        with open(vtt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # VTT 엔트리 파싱 (타임스탬프 + 텍스트)
        pattern = r'(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})\s*\n\[([^\]]+)\]\s*(.+?)(?=\n\n|\Z)'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for start_time, end_time, speaker, text in matches:
            # 화자 분류
            speaker_type = 'teacher' if ('교사' in speaker or '선생님' in speaker) else 'child'
            
            dialogues.append({
                'start_time': start_time,
                'end_time': end_time,
                'speaker': speaker.strip(),
                'speaker_type': speaker_type,
                'text': text.strip()
            })
        
        return dialogues
    
    def load_all_dialogues(self):
        """모든 VTT 파일에서 대화 로드"""
        all_dialogues = []
        
        # _subtitle.vtt 파일 우선 (후처리된 버전)
        vtt_files = sorted(self.vtt_dir.glob("*_subtitle.vtt"))
        
        if not vtt_files:
            # subtitle.vtt가 없으면 미처리/후처리 버전 사용
            vtt_files = sorted(self.vtt_dir.glob("*.vtt"))
        
        for vtt_file in vtt_files:
            # 세그먼트 시간 정보 추출 (예: 000-002분)
            segment_match = re.search(r'_(\d{3}-\d{3})분', vtt_file.name)
            segment = segment_match.group(1) if segment_match else ''
            
            dialogues = self.parse_vtt_file(vtt_file)
            
            # 세그먼트 정보 추가
            for d in dialogues:
                d['segment'] = segment
                d['segment_file'] = vtt_file.name
            
            all_dialogues.extend(dialogues)
        
        self.dialogues = all_dialogues
        return all_dialogues
    
    def analyze_speech_ratio(self):
        """발화 비율 분석"""
        teacher_count = 0
        child_count = 0
        teacher_words = 0
        child_words = 0
        
        for d in self.dialogues:
            word_count = len(d['text'])
            
            if d['speaker_type'] == 'teacher':
                teacher_count += 1
                teacher_words += word_count
            else:
                child_count += 1
                child_words += word_count
        
        total_count = teacher_count + child_count
        total_words = teacher_words + child_words
        
        return {
            'child_speech_ratio': (child_count / total_count * 100) if total_count > 0 else 0,
            'child_utterance_count': child_count,
            'teacher_utterance_count': teacher_count,
            'total_utterance_count': total_count,
            'child_words': child_words,
            'teacher_words': teacher_words,
            'total_words': total_words,
            'child_word_ratio': (child_words / total_words * 100) if total_words > 0 else 0,
        }
    
    def analyze_child_speech_amount(self):
        """아동 발화양 분석"""
        child_dialogues = [d for d in self.dialogues if d['speaker_type'] == 'child']
        
        if not child_dialogues:
            return {
                'total_utterances': 0,
                'total_characters': 0,
                'avg_utterance_length': 0,
                'longest_utterance': 0,
                'shortest_utterance': 0
            }
        
        utterance_lengths = [len(d['text']) for d in child_dialogues]
        
        return {
            'total_utterances': len(child_dialogues),
            'total_characters': sum(utterance_lengths),
            'avg_utterance_length': statistics.mean(utterance_lengths),
            'longest_utterance': max(utterance_lengths),
            'shortest_utterance': min(utterance_lengths),
            'utterance_length_std': statistics.stdev(utterance_lengths) if len(utterance_lengths) > 1 else 0
        }
    
    def analyze_emotion_keywords(self):
        """감정 키워드 분석"""
        child_texts = [d['text'] for d in self.dialogues if d['speaker_type'] == 'child']
        all_child_text = ' '.join(child_texts)
        
        # 긍정/부정 키워드 카운트
        positive_count = sum(all_child_text.count(keyword) for keyword in self.positive_keywords)
        negative_count = sum(all_child_text.count(keyword) for keyword in self.negative_keywords)
        
        # 구체적인 감정 키워드 추출
        positive_found = [kw for kw in self.positive_keywords if kw in all_child_text]
        negative_found = [kw for kw in self.negative_keywords if kw in all_child_text]
        
        total = positive_count + negative_count
        
        return {
            'positive_count': positive_count,
            'negative_count': negative_count,
            'positive_ratio': (positive_count / total * 100) if total > 0 else 0,
            'negative_ratio': (negative_count / total * 100) if total > 0 else 0,
            'positive_keywords': list(set(positive_found)),
            'negative_keywords': list(set(negative_found)),
            'emotion_balance': 'positive' if positive_count > negative_count else ('negative' if negative_count > positive_count else 'neutral')
        }
    
    def extract_topic_keywords(self, top_n=20):
        """주요 토픽 키워드 추출 (명사 중심)"""
        child_texts = [d['text'] for d in self.dialogues if d['speaker_type'] == 'child']
        all_child_text = ' '.join(child_texts)
        
        # 간단한 명사 추출 (한글 2자 이상 단어)
        words = re.findall(r'[가-힣]{2,}', all_child_text)
        
        # 불용어 제거
        stopwords = ['이거', '저거', '그거', '이게', '저게', '그게', '있어', '없어', '이렇게', '저렇게', '그렇게']
        words = [w for w in words if w not in stopwords]
        
        # 빈도수 계산
        word_freq = Counter(words)
        
        return {
            'top_keywords': word_freq.most_common(top_n),
            'unique_words': len(set(words)),
            'total_words': len(words)
        }
    
    def analyze_problem_solving(self):
        """문제해결 발화 분석"""
        child_dialogues = [d for d in self.dialogues if d['speaker_type'] == 'child']
        
        problem_solving_utterances = []
        for d in child_dialogues:
            text = d['text']
            # 문제해결 키워드가 포함된 발화
            if any(keyword in text for keyword in self.problem_solving_keywords):
                problem_solving_utterances.append(d)
        
        total_child_utterances = len(child_dialogues)
        ps_count = len(problem_solving_utterances)
        
        return {
            'problem_solving_count': ps_count,
            'problem_solving_ratio': (ps_count / total_child_utterances * 100) if total_child_utterances > 0 else 0,
            'examples': [u['text'] for u in problem_solving_utterances[:5]]  # 상위 5개 예시
        }
    
    def analyze_topic_continuity(self):
        """주제 지속도 분석 (세그먼트별 키워드 중복도 기반)"""
        segments = defaultdict(list)
        
        # 세그먼트별로 아동 발화 그룹화
        for d in self.dialogues:
            if d['speaker_type'] == 'child':
                segments[d['segment']].append(d['text'])
        
        segment_keywords = {}
        for seg, texts in segments.items():
            text = ' '.join(texts)
            words = re.findall(r'[가-힣]{2,}', text)
            segment_keywords[seg] = set(words)
        
        # 연속된 세그먼트 간 키워드 중복도 계산
        segment_list = sorted(segment_keywords.keys())
        continuity_scores = []
        
        for i in range(len(segment_list) - 1):
            seg1 = segment_list[i]
            seg2 = segment_list[i + 1]
            
            kw1 = segment_keywords[seg1]
            kw2 = segment_keywords[seg2]
            
            if len(kw1) > 0 and len(kw2) > 0:
                # Jaccard 유사도
                intersection = len(kw1 & kw2)
                union = len(kw1 | kw2)
                continuity = intersection / union if union > 0 else 0
                continuity_scores.append(continuity)
        
        return {
            'avg_continuity': statistics.mean(continuity_scores) if continuity_scores else 0,
            'continuity_std': statistics.stdev(continuity_scores) if len(continuity_scores) > 1 else 0,
            'total_segments': len(segment_list),
            'topic_changes': len([s for s in continuity_scores if s < 0.3])  # 낮은 유사도 = 주제 전환
        }
    
    def analyze_turn_taking(self):
        """턴 테이킹(대화 교대) 분석"""
        turns = []
        prev_speaker_type = None
        current_turn_length = 0
        
        for d in self.dialogues:
            if d['speaker_type'] != prev_speaker_type:
                if prev_speaker_type is not None:
                    turns.append({
                        'speaker_type': prev_speaker_type,
                        'length': current_turn_length
                    })
                prev_speaker_type = d['speaker_type']
                current_turn_length = 1
            else:
                current_turn_length += 1
        
        # 마지막 턴 추가
        if prev_speaker_type is not None:
            turns.append({
                'speaker_type': prev_speaker_type,
                'length': current_turn_length
            })
        
        child_turns = [t['length'] for t in turns if t['speaker_type'] == 'child']
        teacher_turns = [t['length'] for t in turns if t['speaker_type'] == 'teacher']
        
        return {
            'total_turns': len(turns),
            'child_turns': len(child_turns),
            'teacher_turns': len(teacher_turns),
            'avg_child_turn_length': statistics.mean(child_turns) if child_turns else 0,
            'avg_teacher_turn_length': statistics.mean(teacher_turns) if teacher_turns else 0,
            'turn_taking_balance': len(child_turns) / len(turns) if turns else 0
        }
    
    def generate_full_analysis(self):
        """전체 분석 실행"""
        print(f"🔍 분석 시작: {self.session_name}")
        
        # 1. 메타 정보 로드
        meta_info = self.load_meta_info()
        print(f"  - 메타 정보 로드 완료")
        
        # 2. 대화 데이터 로드
        self.load_all_dialogues()
        print(f"  - 대화 데이터 로드 완료: 총 {len(self.dialogues)}개 발화")
        
        # 3. 각종 분석 실행
        analysis_results = {
            'meta_info': meta_info,
            'speech_ratio': self.analyze_speech_ratio(),
            'child_speech_amount': self.analyze_child_speech_amount(),
            'emotion_analysis': self.analyze_emotion_keywords(),
            'topic_keywords': self.extract_topic_keywords(20),
            'problem_solving': self.analyze_problem_solving(),
            'topic_continuity': self.analyze_topic_continuity(),
            'turn_taking': self.analyze_turn_taking(),
            'analyzed_at': datetime.now().isoformat()
        }
        
        print(f"✅ 분석 완료!")
        
        return analysis_results
    
    def save_analysis(self, output_path):
        """분석 결과 저장"""
        results = self.generate_full_analysis()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"💾 분석 결과 저장: {output_path}")
        
        return results


def main():
    """메인 함수 - 샘플 분석"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python analyze_play_session.py <session_directory>")
        print("\n예시:")
        print("  python analyze_play_session.py raw_data/20251017-이민정교사-김준우-만4세-02_00_48-65kbps_mono")
        sys.exit(1)
    
    session_dir = sys.argv[1]
    
    # 분석기 생성
    analyzer = PlaySessionAnalyzer(session_dir)
    
    # 분석 실행 및 저장
    output_dir = Path("analysis_results")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / f"{analyzer.session_name}_analysis.json"
    results = analyzer.save_analysis(output_file)
    
    # 결과 요약 출력
    print("\n" + "="*80)
    print("📊 분석 결과 요약")
    print("="*80)
    
    print(f"\n👤 기본 정보:")
    print(f"  - 선생님: {results['meta_info'].get('teacher_name', 'N/A')}")
    print(f"  - 아동: {results['meta_info'].get('child_name', 'N/A')}")
    print(f"  - 나이: {results['meta_info'].get('child_age', 'N/A')}")
    
    print(f"\n💬 발화 분석:")
    sr = results['speech_ratio']
    print(f"  - 아동 발화 비율: {sr['child_speech_ratio']:.1f}%")
    print(f"  - 아동 발화 횟수: {sr['child_utterance_count']}회")
    print(f"  - 선생님 발화 횟수: {sr['teacher_utterance_count']}회")
    
    print(f"\n📝 아동 발화량:")
    ca = results['child_speech_amount']
    print(f"  - 총 발화 횟수: {ca['total_utterances']}회")
    print(f"  - 총 글자 수: {ca['total_characters']}자")
    print(f"  - 평균 발화 길이: {ca['avg_utterance_length']:.1f}자")
    
    print(f"\n😊 감정 분석:")
    ea = results['emotion_analysis']
    print(f"  - 긍정 키워드: {ea['positive_count']}개 ({ea['positive_ratio']:.1f}%)")
    print(f"  - 부정 키워드: {ea['negative_count']}개 ({ea['negative_ratio']:.1f}%)")
    print(f"  - 감정 균형: {ea['emotion_balance']}")
    print(f"  - 주요 긍정 키워드: {', '.join(ea['positive_keywords'][:10])}")
    
    print(f"\n🎯 주제 분석:")
    tk = results['topic_keywords']
    print(f"  - 고유 단어 수: {tk['unique_words']}개")
    print(f"  - Top 10 키워드:")
    for i, (word, count) in enumerate(tk['top_keywords'][:10], 1):
        print(f"    {i}. {word} ({count}회)")
    
    print(f"\n🧩 문제해결 발화:")
    ps = results['problem_solving']
    print(f"  - 문제해결 발화 수: {ps['problem_solving_count']}회")
    print(f"  - 문제해결 발화 비율: {ps['problem_solving_ratio']:.1f}%")
    
    print(f"\n🔄 주제 지속도:")
    tc = results['topic_continuity']
    print(f"  - 평균 연속성: {tc['avg_continuity']:.2f}")
    print(f"  - 주제 전환 횟수: {tc['topic_changes']}회")
    print(f"  - 총 세그먼트: {tc['total_segments']}개")
    
    print(f"\n🗣️ 대화 교대:")
    tt = results['turn_taking']
    print(f"  - 총 턴 수: {tt['total_turns']}회")
    print(f"  - 아동 평균 턴 길이: {tt['avg_child_turn_length']:.1f}회")
    print(f"  - 선생님 평균 턴 길이: {tt['avg_teacher_turn_length']:.1f}회")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    main()

