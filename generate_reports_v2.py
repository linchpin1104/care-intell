"""
3가지 타입 레포트 생성 모듈
1. 부모용 레포트 - 간결하고 이해하기 쉬운 형태
2. 선생님용 레포트 + 방문일지 자동 작성
3. 회사용 레포트 - 모든 데이터 상세 분석
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict


class ReportGenerator:
    """레포트 생성 클래스"""
    
    def __init__(self, analysis_result: Dict):
        self.data = analysis_result
        self.session_info = analysis_result.get('session_info', {})
        
    def generate_parent_report(self) -> str:
        """부모용 레포트 생성"""
        child_name = self.session_info.get('child_name', '아이')
        age = self.session_info.get('age', '')
        date = self.format_date(self.session_info.get('date', ''))
        
        speech_ratio = self.data['speech_ratio']
        utterance = self.data['utterance_volume']
        sentiment = self.data['sentiment']
        topics = self.data['main_topics']
        problem_solving = self.data['problem_solving']
        
        report = f"""
╔════════════════════════════════════════════════════════════╗
                    놀이 활동 리포트 (학부모용)
╚════════════════════════════════════════════════════════════╝

📋 기본 정보
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • 아동명: {child_name} ({age})
  • 관찰일: {date}
  • 선생님: {self.session_info.get('teacher_name', '')}


🎯 이번 놀이 활동
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • 주요 놀이: {', '.join(topics['detected_play_types']) if topics['detected_play_types'] else '자유놀이'}
  • 관심 주제: {', '.join([kw['word'] for kw in topics['top_keywords'][:3]])}


💬 의사소통 발달
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • 말하기 참여도: {self.get_participation_level(speech_ratio['child_utterance_ratio'])}
  • 발화 횟수: {utterance['child_total_utterances']}회
  • 평가: {self.evaluate_speech_ratio(speech_ratio['child_utterance_ratio'])}


🧠 사고력 발달
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • 문제해결 시도: {problem_solving['problem_solving_utterance_count']}회
  • 평가: {self.evaluate_problem_solving(problem_solving['problem_solving_ratio'])}


😊 정서 발달
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • 긍정적 표현: {sentiment['positive_count']}회
  • 부정적 표현: {sentiment['negative_count']}회
  • 정서 상태: {self.evaluate_sentiment(sentiment['sentiment_score'])}


✨ 특별히 관찰된 점
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{self.generate_parent_highlights()}


🏠 가정에서 함께 해보세요
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{self.generate_parent_suggestions()}


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
작성일: {datetime.now().strftime('%Y년 %m월 %d일')}
"""
        return report
    
    def generate_teacher_report(self) -> str:
        """선생님용 레포트 + 방문일지 생성"""
        child_name = self.session_info.get('child_name', '아이')
        age = self.session_info.get('age', '')
        date = self.format_date(self.session_info.get('date', ''))
        
        speech_ratio = self.data['speech_ratio']
        utterance = self.data['utterance_volume']
        topic_consistency = self.data['topic_consistency']
        context_switches = self.data['context_switches']
        problem_solving = self.data['problem_solving']
        sentiment = self.data['sentiment']
        emotion_words = self.data['emotion_words']
        topics = self.data['main_topics']
        
        report = f"""
╔════════════════════════════════════════════════════════════╗
              가정방문 놀이 관찰 일지 (교사용)
╚════════════════════════════════════════════════════════════╝

📋 기본 정보
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • 관찰 아동: {child_name} ({age})
  • 관찰 일시: {date}
  • 관찰 교사: {self.session_info.get('teacher_name', '')}
  • 관찰 시간: {self.session_info.get('duration', '').replace('_', ':')}


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 놀이 내용 및 흐름
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[주요 놀이 유형]
{self.format_play_types(topics['detected_play_types'])}

[놀이 주제 및 관심사]
{self.format_play_topics(topics['top_keywords'][:5])}

[놀이 지속성]
• 주제 전환 횟수: {topic_consistency['topic_changes']}회
• 주제 지속도: {topic_consistency['topic_consistency_score']}점
• 평가: {self.evaluate_topic_consistency(topic_consistency['topic_consistency_score'])}


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. 언어 및 의사소통 발달 관찰
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[발화 참여도]
• 전체 발화 중 아동 비율: {speech_ratio['child_utterance_ratio']}%
• 아동 발화 횟수: {speech_ratio['child_utterance_count']}회
• 교사 발화 횟수: {speech_ratio['teacher_utterance_count']}회
• 텍스트 기준 비율: {speech_ratio['child_text_ratio']}%

[발화 특성]
• 평균 발화 길이: {utterance['child_avg_utterance_length']}자
• 총 음절 수: {utterance['child_total_syllables']}
• 평가: {self.evaluate_utterance_volume(utterance)}

[상호작용 패턴]
• 화자 전환 횟수: {context_switches['total_speaker_switches']}회
• 평균 연속 발화: {context_switches['avg_consecutive_utterances']}회
• 최대 연속 발화: {context_switches['max_consecutive_utterances']}회
• 평가: {self.evaluate_interaction(context_switches)}


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. 인지 및 사고력 발달 관찰
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[문제해결력]
• 문제해결 시도 발화: {problem_solving['problem_solving_utterance_count']}회
• 문제해결 발화 비율: {problem_solving['problem_solving_ratio']}%
• 발화 예시:
{self.format_examples(problem_solving.get('examples', [])[:3])}


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. 정서 및 사회성 발달 관찰
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[정서 표현]
• 긍정 표현: {sentiment['positive_count']}회 ({sentiment['positive_ratio']}%)
• 부정 표현: {sentiment['negative_count']}회 ({sentiment['negative_ratio']}%)
• 정서 점수: {sentiment['sentiment_score']}점

[주요 정서 키워드]
{self.format_emotion_keywords(emotion_words)}

[주도적 정서]
• {emotion_words.get('dominant_emotion', '중립적')} 정서가 주로 관찰됨


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5. 종합 평가 및 교육적 제언
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[강점]
{self.generate_strengths()}

[발달 지원 영역]
{self.generate_development_areas()}

[교육적 제언]
{self.generate_teacher_suggestions()}


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
6. 방문 소감 및 특이사항
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{self.generate_teacher_notes()}


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
작성일: {datetime.now().strftime('%Y년 %m월 %d일')}
작성자: {self.session_info.get('teacher_name', '')}
"""
        return report
    
    def generate_company_report(self) -> str:
        """회사용 상세 분석 레포트 생성"""
        child_name = self.session_info.get('child_name', '아이')
        age = self.session_info.get('age', '')
        date = self.format_date(self.session_info.get('date', ''))
        
        report = f"""
╔════════════════════════════════════════════════════════════╗
            놀이 세션 상세 분석 리포트 (사업자용)
╚════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 세션 개요
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • 세션명: {self.session_info.get('session_name', '')}
  • 아동명: {child_name} ({age})
  • 관찰일: {date}
  • 교사명: {self.session_info.get('teacher_name', '')}
  • 세션 길이: {self.session_info.get('duration', '')}


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 오디오 품질 지표 (Audio Features)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{self.format_audio_features()}


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬 발화 분석 (Speech Analysis)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[아동 발화 비율]
{json.dumps(self.data['speech_ratio'], ensure_ascii=False, indent=2)}

[발화량 분석]
{json.dumps(self.data['utterance_volume'], ensure_ascii=False, indent=2)}


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 주제 및 맥락 분석 (Topic & Context Analysis)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[주제 지속도]
{json.dumps(self.data['topic_consistency'], ensure_ascii=False, indent=2)}

[맥락 전환도]
{json.dumps(self.data['context_switches'], ensure_ascii=False, indent=2)}


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧠 인지 발달 분석 (Cognitive Analysis)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[문제해결 발화]
{json.dumps(self.data['problem_solving'], ensure_ascii=False, indent=2)}


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
😊 정서 분석 (Sentiment Analysis)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[긍정/부정 비율]
{json.dumps(self.data['sentiment'], ensure_ascii=False, indent=2)}

[정서 단어 분석]
{json.dumps(self.data['emotion_words'], ensure_ascii=False, indent=2)}


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎨 주요 토픽 분석 (Topic Modeling)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{json.dumps(self.data['main_topics'], ensure_ascii=False, indent=2)}


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 종합 점수 (Overall Scores)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{self.calculate_overall_scores()}


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 데이터 품질 체크
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{self.check_data_quality()}


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
작성일: {datetime.now().strftime('%Y년 %m월 %d일 %H시 %M분')}
분석 버전: v2.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        return report
    
    # ========== 유틸리티 함수 ==========
    
    def format_date(self, date_str: str) -> str:
        """날짜 포맷팅"""
        if len(date_str) == 8:
            return f"{date_str[:4]}년 {date_str[4:6]}월 {date_str[6:8]}일"
        return date_str
    
    def get_participation_level(self, ratio: float) -> str:
        """참여도 레벨"""
        if ratio >= 50:
            return "매우 적극적 ⭐⭐⭐"
        elif ratio >= 40:
            return "적극적 ⭐⭐"
        elif ratio >= 30:
            return "보통 ⭐"
        else:
            return "소극적"
    
    def evaluate_speech_ratio(self, ratio: float) -> str:
        """발화 비율 평가"""
        if ratio >= 50:
            return "아이가 매우 적극적으로 대화에 참여하고 자신의 생각을 잘 표현했습니다."
        elif ratio >= 40:
            return "아이가 적극적으로 대화에 참여했으며, 자기 주도적인 모습을 보였습니다."
        elif ratio >= 30:
            return "아이가 대화에 참여했으나, 좀 더 자신의 의견을 표현하도록 격려가 필요합니다."
        else:
            return "아이의 발화를 더 이끌어내고 경청하는 시간이 필요합니다."
    
    def evaluate_problem_solving(self, ratio: float) -> str:
        """문제해결 평가"""
        if ratio >= 20:
            return "호기심이 많고 스스로 문제를 해결하려는 시도가 활발합니다."
        elif ratio >= 10:
            return "적절한 수준의 문제해결 시도를 보입니다."
        else:
            return "문제해결 상황을 더 많이 제공하면 좋겠습니다."
    
    def evaluate_sentiment(self, score: float) -> str:
        """감정 평가"""
        if score > 10:
            return "매우 긍정적이고 즐거운 시간을 보냈습니다 😊"
        elif score > 0:
            return "대체로 긍정적인 정서를 보였습니다"
        elif score > -10:
            return "중립적인 정서를 보였습니다"
        else:
            return "다소 부정적인 표현이 있었습니다"
    
    def generate_parent_highlights(self) -> str:
        """부모용 하이라이트"""
        highlights = []
        
        speech_ratio = self.data['speech_ratio']['child_utterance_ratio']
        if speech_ratio >= 45:
            highlights.append("• 대화에 매우 적극적으로 참여하는 모습이 인상적이었습니다.")
        
        problem_solving = self.data['problem_solving']['problem_solving_ratio']
        if problem_solving >= 15:
            highlights.append("• 스스로 생각하고 문제를 해결하려는 시도가 많았습니다.")
        
        sentiment = self.data['sentiment']['sentiment_score']
        if sentiment > 10:
            highlights.append("• 놀이 내내 즐겁고 긍정적인 모습을 보였습니다.")
        
        if not highlights:
            highlights.append("• 선생님과 함께 즐거운 시간을 보냈습니다.")
        
        return '\n'.join(highlights)
    
    def generate_parent_suggestions(self) -> str:
        """부모용 제안"""
        suggestions = []
        topics = self.data['main_topics']
        
        if topics['detected_play_types']:
            play_type = topics['detected_play_types'][0]
            suggestions.append(f"• {play_type}에 관심이 많으니 관련 활동을 함께 해보세요.")
        
        suggestions.append("• 아이의 이야기를 경청하고 질문을 통해 생각을 확장해보세요.")
        suggestions.append("• '왜 그럴까?', '어떻게 하면 좋을까?' 같은 열린 질문을 활용해보세요.")
        
        return '\n'.join(suggestions)
    
    def format_play_types(self, play_types: list) -> str:
        """놀이 유형 포맷팅"""
        if not play_types:
            return "• 자유놀이"
        return '\n'.join([f"• {pt}" for pt in play_types])
    
    def format_play_topics(self, topics: list) -> str:
        """놀이 주제 포맷팅"""
        if not topics:
            return "• 특정 주제 없음"
        return '\n'.join([f"• {t['word']} ({t['count']}회 언급)" for t in topics])
    
    def evaluate_topic_consistency(self, score: float) -> str:
        """주제 지속도 평가"""
        if score >= 70:
            return "한 가지 놀이 주제에 깊이 있게 집중하는 모습을 보였습니다."
        elif score >= 50:
            return "적절한 수준의 주제 전환을 보이며 놀이했습니다."
        else:
            return "다양한 놀이를 시도했으나 집중 시간이 짧았습니다."
    
    def evaluate_utterance_volume(self, utterance: dict) -> str:
        """발화량 평가"""
        count = utterance['child_total_utterances']
        if count >= 100:
            return "매우 활발한 언어 표현을 보였습니다."
        elif count >= 50:
            return "적절한 수준의 언어 표현을 보였습니다."
        else:
            return "언어 표현을 더 이끌어낼 필요가 있습니다."
    
    def evaluate_interaction(self, context_switches: dict) -> str:
        """상호작용 평가"""
        switch_rate = context_switches['switch_rate']
        if switch_rate >= 50:
            return "교사와 활발한 상호작용을 하며 대화를 주고받았습니다."
        elif switch_rate >= 30:
            return "적절한 상호작용 패턴을 보였습니다."
        else:
            return "일방적인 대화 패턴이 관찰되었습니다."
    
    def format_examples(self, examples: list) -> str:
        """예시 포맷팅"""
        if not examples:
            return "  (예시 없음)"
        return '\n'.join([f"  - \"{ex}\"" for ex in examples])
    
    def format_emotion_keywords(self, emotion_words: dict) -> str:
        """정서 키워드 포맷팅"""
        counts = emotion_words.get('emotion_counts', {})
        result = []
        for emotion, count in counts.items():
            if count > 0:
                result.append(f"• {emotion}: {count}회")
        return '\n'.join(result) if result else "• 특별한 정서 키워드 없음"
    
    def generate_strengths(self) -> str:
        """강점 생성"""
        strengths = []
        
        if self.data['speech_ratio']['child_utterance_ratio'] >= 40:
            strengths.append("• 언어 표현력: 적극적인 의사소통 능력을 보임")
        
        if self.data['problem_solving']['problem_solving_ratio'] >= 15:
            strengths.append("• 문제해결력: 호기심과 탐구심이 뛰어남")
        
        if self.data['sentiment']['sentiment_score'] > 5:
            strengths.append("• 정서 발달: 긍정적이고 안정적인 정서 상태")
        
        if self.data['topic_consistency']['topic_consistency_score'] >= 60:
            strengths.append("• 집중력: 놀이에 대한 집중력과 몰입도가 높음")
        
        if not strengths:
            strengths.append("• 놀이 활동에 참여하는 모습을 보임")
        
        return '\n'.join(strengths)
    
    def generate_development_areas(self) -> str:
        """발달 지원 영역"""
        areas = []
        
        if self.data['speech_ratio']['child_utterance_ratio'] < 30:
            areas.append("• 자발적 언어 표현 기회 확대")
        
        if self.data['problem_solving']['problem_solving_ratio'] < 10:
            areas.append("• 문제해결 상황 제공 및 사고 확장 질문")
        
        if self.data['topic_consistency']['topic_consistency_score'] < 50:
            areas.append("• 놀이 지속 시간 확장 및 집중력 향상")
        
        if not areas:
            areas.append("• 현재 발달 수준 유지 및 강화")
        
        return '\n'.join(areas)
    
    def generate_teacher_suggestions(self) -> str:
        """교사용 제안"""
        suggestions = []
        
        speech_ratio = self.data['speech_ratio']['child_utterance_ratio']
        if speech_ratio < 35:
            suggestions.append("• 아동의 발화를 기다리고 경청하는 시간을 늘려보세요.")
            suggestions.append("• 개방형 질문을 통해 아동의 생각을 이끌어내세요.")
        
        problem_solving = self.data['problem_solving']['problem_solving_ratio']
        if problem_solving < 10:
            suggestions.append("• '왜?', '어떻게?' 등의 질문으로 사고를 확장해보세요.")
            suggestions.append("• 문제 상황을 제시하고 아동의 해결책을 기다려보세요.")
        
        if not suggestions:
            suggestions.append("• 현재의 상호작용 방식을 유지하며 아동의 주도성을 지원하세요.")
            suggestions.append("• 아동의 관심사를 파악하고 확장할 수 있는 자료를 준비하세요.")
        
        return '\n'.join(suggestions)
    
    def generate_teacher_notes(self) -> str:
        """교사 소감"""
        child_name = self.session_info.get('child_name', '아이')
        topics = self.data['main_topics']['detected_play_types']
        
        notes = f"{child_name} 아동은 "
        
        if topics:
            notes += f"{topics[0]}을 중심으로 "
        
        sentiment_score = self.data['sentiment']['sentiment_score']
        if sentiment_score > 10:
            notes += "즐겁고 적극적으로 놀이에 참여했습니다. "
        elif sentiment_score > 0:
            notes += "긍정적인 태도로 놀이에 참여했습니다. "
        else:
            notes += "놀이 활동에 참여했습니다. "
        
        speech_ratio = self.data['speech_ratio']['child_utterance_ratio']
        if speech_ratio >= 40:
            notes += "자신의 생각과 느낌을 적극적으로 표현하는 모습이 인상적이었습니다."
        else:
            notes += "다음 방문에서는 아동의 발화를 더 이끌어내는 시도가 필요합니다."
        
        return notes
    
    def format_audio_features(self) -> str:
        """오디오 특징 포맷팅"""
        features = self.data.get('audio_features', {})
        if not features:
            return "  (오디오 특징 데이터 없음)"
        
        result = []
        result.append(f"  • VAD Ratio (음성 활동 비율): {features.get('vad_ratio', 0):.2%}")
        result.append(f"  • SNR (신호 대 잡음비): {features.get('snr', 0):.2f} dB")
        result.append(f"  • Speech Rate: {features.get('speech_rate_frames', 0):.2f} frames/sec")
        result.append(f"  • F0 Mean (평균 음높이): {features.get('f0_mean', 0):.2f} Hz")
        result.append(f"  • F0 Range (음높이 범위): {features.get('f0_range', 0):.2f} Hz")
        result.append(f"  • Clipping Ratio: {features.get('clipping_ratio', 0):.2%}")
        
        return '\n'.join(result)
    
    def calculate_overall_scores(self) -> str:
        """종합 점수 계산"""
        scores = {
            '언어 발달': self.data['speech_ratio']['child_utterance_ratio'],
            '사고력': self.data['problem_solving']['problem_solving_ratio'] * 5,  # 스케일 조정
            '정서 안정': max(0, min(100, 50 + self.data['sentiment']['sentiment_score'])),
            '놀이 집중도': self.data['topic_consistency']['topic_consistency_score'],
            '상호작용': self.data['context_switches']['switch_rate']
        }
        
        result = []
        for category, score in scores.items():
            bar = '█' * int(score / 10) + '░' * (10 - int(score / 10))
            result.append(f"  {category:12s}: {bar} {score:5.1f}점")
        
        avg_score = sum(scores.values()) / len(scores)
        result.append(f"\n  {'종합 평균':12s}: {avg_score:5.1f}점")
        
        return '\n'.join(result)
    
    def check_data_quality(self) -> str:
        """데이터 품질 체크"""
        checks = []
        
        total_utterances = self.data['speech_ratio']['total_utterance_count']
        checks.append(f"  • 총 발화 수: {total_utterances}개 - {'✓ 충분' if total_utterances >= 50 else '⚠ 부족'}")
        
        snr = self.data.get('audio_features', {}).get('snr', 0)
        checks.append(f"  • 음질 (SNR): {snr:.1f}dB - {'✓ 양호' if snr >= 10 else '⚠ 개선 필요'}")
        
        vad_ratio = self.data.get('audio_features', {}).get('vad_ratio', 0)
        checks.append(f"  • 음성 비율: {vad_ratio:.1%} - {'✓ 정상' if vad_ratio >= 0.3 else '⚠ 낮음'}")
        
        unique_words = self.data['main_topics']['total_unique_words']
        checks.append(f"  • 어휘 다양성: {unique_words}개 - {'✓ 풍부' if unique_words >= 100 else '⚠ 제한적'}")
        
        return '\n'.join(checks)


def generate_all_reports(analysis_json_path: str, output_dir: str = None):
    """분석 결과에서 3가지 레포트 모두 생성"""
    
    # 분석 결과 로드
    with open(analysis_json_path, 'r', encoding='utf-8') as f:
        analysis_data = json.load(f)
    
    # 출력 디렉토리 설정
    if output_dir is None:
        output_dir = Path(analysis_json_path).parent.parent / "reports"
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(exist_ok=True)
    
    # 레포트 생성기
    generator = ReportGenerator(analysis_data)
    
    # 세션 이름
    session_name = analysis_data['session_info']['session_name']
    
    # 1. 부모용 레포트
    parent_report = generator.generate_parent_report()
    parent_file = output_dir / f"{session_name}_parent_report.txt"
    with open(parent_file, 'w', encoding='utf-8') as f:
        f.write(parent_report)
    print(f"✓ 부모용 레포트 생성: {parent_file}")
    
    # 2. 선생님용 레포트 + 방문일지
    teacher_report = generator.generate_teacher_report()
    teacher_file = output_dir / f"{session_name}_teacher_report.txt"
    with open(teacher_file, 'w', encoding='utf-8') as f:
        f.write(teacher_report)
    print(f"✓ 선생님용 레포트 생성: {teacher_file}")
    
    # 3. 회사용 레포트
    company_report = generator.generate_company_report()
    company_file = output_dir / f"{session_name}_company_report.txt"
    with open(company_file, 'w', encoding='utf-8') as f:
        f.write(company_report)
    print(f"✓ 회사용 레포트 생성: {company_file}")
    
    print(f"\n모든 레포트가 생성되었습니다: {output_dir}")


def main():
    """테스트 실행"""
    # 샘플 분석 결과로 레포트 생성
    analysis_file = "/Users/healin/Downloads/develop/care-intell/analysis_results/20251017-이민정교사-김준우-만4세-02_00_48-65kbps_mono_detailed_analysis.json"
    
    if Path(analysis_file).exists():
        generate_all_reports(analysis_file)
    else:
        print(f"분석 파일을 찾을 수 없습니다: {analysis_file}")
        print("먼저 analyze_metrics.py를 실행하여 분석 데이터를 생성하세요.")


if __name__ == "__main__":
    main()

