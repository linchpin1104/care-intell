#!/usr/bin/env python3
"""
놀이 세션 레포트 생성기
- 회사용 레포트 (상세)
- 부모용 레포트 (아이 중심)
- 선생님용 레포트 (교육적 인사이트)
"""

import json
from pathlib import Path
from datetime import datetime


class ReportGenerator:
    """레포트 생성기"""
    
    def __init__(self, analysis_result_path):
        """
        Args:
            analysis_result_path: 분석 결과 JSON 파일 경로
        """
        self.analysis_path = Path(analysis_result_path)
        
        with open(self.analysis_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.meta = self.data['meta_info']
        self.speech_ratio = self.data['speech_ratio']
        self.speech_amount = self.data['child_speech_amount']
        self.emotion = self.data['emotion_analysis']
        self.topics = self.data['topic_keywords']
        self.problem_solving = self.data['problem_solving']
        self.continuity = self.data['topic_continuity']
        self.turn_taking = self.data['turn_taking']
    
    def generate_company_report(self):
        """회사용 상세 레포트 생성 (가장 자세함)"""
        
        report = f"""
{'='*100}
📊 놀이 세션 분석 레포트 (회사용 - 상세)
{'='*100}

생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
분석 데이터: {self.meta['session_name']}

{'='*100}
1️⃣  기본 정보
{'='*100}

📅 세션 날짜: {self.meta.get('date', 'N/A')}
👩‍🏫 선생님: {self.meta.get('teacher_name', 'N/A')}
👶 아동: {self.meta.get('child_name', 'N/A')}
🎂 나이: {self.meta.get('child_age', 'N/A')}
⏱️  세션 시간: {self.meta.get('duration', 'N/A')}

{'='*100}
2️⃣  아동 발화 분석 (Child Speech Analysis)
{'='*100}

📊 발화 비율 (Speech Ratio)
  • 아동 발화 비율: {self.speech_ratio['child_speech_ratio']:.2f}%
  • 선생님 발화 비율: {100 - self.speech_ratio['child_speech_ratio']:.2f}%
  • 아동 발화 횟수: {self.speech_ratio['child_utterance_count']:,}회
  • 선생님 발화 횟수: {self.speech_ratio['teacher_utterance_count']:,}회
  • 총 발화 횟수: {self.speech_ratio['total_utterance_count']:,}회

📝 발화량 (Speech Amount)
  • 아동 총 글자 수: {self.speech_amount['total_characters']:,}자
  • 아동 평균 발화 길이: {self.speech_amount['avg_utterance_length']:.2f}자
  • 아동 최장 발화 길이: {self.speech_amount['longest_utterance']:,}자
  • 아동 최단 발화 길이: {self.speech_amount['shortest_utterance']}자
  • 발화 길이 표준편차: {self.speech_amount['utterance_length_std']:.2f}

💬 단어 비율 (Word Ratio)
  • 아동 단어 비율: {self.speech_ratio['child_word_ratio']:.2f}%
  • 아동 단어 수: {self.speech_ratio['child_words']:,}자
  • 선생님 단어 수: {self.speech_ratio['teacher_words']:,}자

{'='*100}
3️⃣  감정 분석 (Emotion Analysis)
{'='*100}

😊 긍정/부정 비율
  • 긍정 키워드: {self.emotion['positive_count']}개 ({self.emotion['positive_ratio']:.2f}%)
  • 부정 키워드: {self.emotion['negative_count']}개 ({self.emotion['negative_ratio']:.2f}%)
  • 감정 균형: {self.emotion['emotion_balance'].upper()}

🎭 주요 긍정 정서 단어
  {', '.join(self.emotion['positive_keywords'][:20])}

😔 주요 부정 정서 단어
  {', '.join(self.emotion['negative_keywords'][:20]) if self.emotion['negative_keywords'] else '없음'}

{'='*100}
4️⃣  주제 분석 (Topic Analysis)
{'='*100}

🎯 주요 토픽 키워드 (Top 20)
"""
        
        for i, (word, count) in enumerate(self.topics['top_keywords'][:20], 1):
            report += f"  {i:2d}. {word:<10s} {count:4d}회\n"
        
        report += f"""
📚 어휘 다양성
  • 고유 단어 수: {self.topics['unique_words']:,}개
  • 총 단어 수: {self.topics['total_words']:,}개
  • 어휘 다양도 (TTR): {(self.topics['unique_words'] / self.topics['total_words'] * 100):.2f}%

{'='*100}
5️⃣  문제해결 발화 분석 (Problem-Solving Speech)
{'='*100}

🧩 문제해결 지표
  • 문제해결 발화 수: {self.problem_solving['problem_solving_count']}회
  • 문제해결 발화 비율: {self.problem_solving['problem_solving_ratio']:.2f}%

💡 문제해결 발화 예시
"""
        
        for i, example in enumerate(self.problem_solving['examples'], 1):
            report += f"  {i}. \"{example}\"\n"
        
        report += f"""
{'='*100}
6️⃣  주제 지속도 분석 (Topic Continuity)
{'='*100}

🔄 주제 연속성
  • 평균 주제 연속성: {self.continuity['avg_continuity']:.4f}
  • 주제 전환 횟수: {self.continuity['topic_changes']}회
  • 총 세그먼트: {self.continuity['total_segments']}개
  
⚠️  참고: 주제 연속성이 0인 경우 세그먼트 분석이 필요할 수 있습니다.

{'='*100}
7️⃣  대화 교대 분석 (Turn-Taking Analysis)
{'='*100}

🗣️ 턴 테이킹 패턴
  • 총 턴 수: {self.turn_taking['total_turns']:,}회
  • 아동 턴 수: {self.turn_taking['child_turns']:,}회
  • 선생님 턴 수: {self.turn_taking['teacher_turns']:,}회
  • 아동 평균 턴 길이: {self.turn_taking['avg_child_turn_length']:.2f}회
  • 선생님 평균 턴 길이: {self.turn_taking['avg_teacher_turn_length']:.2f}회
  • 턴 균형도: {self.turn_taking['turn_taking_balance']:.2f}

{'='*100}
8️⃣  종합 평가 (Overall Assessment)
{'='*100}
"""
        
        # 종합 평가 로직
        assessments = []
        
        # 발화 비율 평가
        if self.speech_ratio['child_speech_ratio'] >= 45:
            assessments.append("✅ 아동 발화 비율이 양호합니다 (45% 이상)")
        else:
            assessments.append("⚠️  아동 발화 비율이 다소 낮습니다 (45% 미만)")
        
        # 감정 균형 평가
        if self.emotion['positive_ratio'] >= 60:
            assessments.append("✅ 긍정적 감정 표현이 우세합니다")
        elif self.emotion['positive_ratio'] >= 40:
            assessments.append("🟡 긍정/부정 감정이 균형적입니다")
        else:
            assessments.append("⚠️  부정적 감정 표현이 다소 많습니다")
        
        # 문제해결 발화 평가
        if self.problem_solving['problem_solving_ratio'] >= 10:
            assessments.append("✅ 문제해결 발화가 활발합니다 (10% 이상)")
        elif self.problem_solving['problem_solving_ratio'] >= 5:
            assessments.append("🟡 문제해결 발화가 적절합니다 (5-10%)")
        else:
            assessments.append("⚠️  문제해결 발화를 더 유도할 필요가 있습니다 (5% 미만)")
        
        # 어휘 다양성 평가
        ttr = self.topics['unique_words'] / self.topics['total_words'] * 100
        if ttr >= 30:
            assessments.append("✅ 어휘 다양성이 매우 높습니다 (30% 이상)")
        elif ttr >= 20:
            assessments.append("🟡 어휘 다양성이 적절합니다 (20-30%)")
        else:
            assessments.append("⚠️  어휘 다양성을 높일 필요가 있습니다 (20% 미만)")
        
        for assessment in assessments:
            report += f"\n{assessment}"
        
        report += f"""

{'='*100}
🔚 레포트 끝
{'='*100}

분석 시스템: Care Intelligence v1.0
분석 엔진 버전: 2025.11
생성 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return report
    
    def generate_parent_report(self):
        """부모용 레포트 생성 (아이 중심, 쉬운 언어)"""
        
        child_name = self.meta.get('child_name', '아이')
        teacher_name = self.meta.get('teacher_name', '선생님')
        child_age = self.meta.get('child_age', '')
        
        report = f"""
{'='*80}
🎉 {child_name} 놀이 활동 레포트
{'='*80}

안녕하세요, {child_name} 부모님! 👋

{child_name}의 {self.meta.get('date', '')} 놀이 활동을 분석한 결과를 공유드립니다.
{teacher_name} 선생님과 함께한 시간 동안 {child_name}의 여러 모습을 관찰할 수 있었습니다.

{'='*80}
💬 얼마나 많이 이야기했나요?
{'='*80}

{child_name}는 이번 놀이 시간에 총 {self.speech_ratio['child_utterance_count']:,}번 
이야기를 나눴어요! 선생님과의 대화 비율은 {self.speech_ratio['child_speech_ratio']:.1f}%로,
"""
        
        if self.speech_ratio['child_speech_ratio'] >= 50:
            report += f"{child_name}가 적극적으로 대화에 참여했답니다. 😊\n"
        else:
            report += f"선생님의 이야기를 잘 듣고 반응하는 모습을 보였어요. 👂\n"
        
        report += f"""
한 번에 평균 {self.speech_amount['avg_utterance_length']:.0f}자 정도 이야기했는데,
"""
        
        if self.speech_amount['avg_utterance_length'] >= 20:
            report += "문장을 길고 구체적으로 표현하는 능력이 좋아요! ✨\n"
        elif self.speech_amount['avg_utterance_length'] >= 10:
            report += "생각을 적절한 길이로 잘 표현하고 있어요! 👍\n"
        else:
            report += "짧고 명확하게 의사를 전달하고 있어요! 💡\n"
        
        report += f"""
{'='*80}
😊 어떤 감정을 표현했나요?
{'='*80}

{child_name}의 감정 표현을 분석해보니,
"""
        
        if self.emotion['positive_ratio'] >= 60:
            report += f"긍정적인 감정을 많이 표현했어요! ({self.emotion['positive_ratio']:.1f}%) 🌟\n"
        elif self.emotion['positive_ratio'] >= 40:
            report += f"긍정과 부정 감정을 균형있게 표현했어요. 👌\n"
        else:
            report += f"다양한 감정을 솔직하게 표현하는 모습을 보였어요. 🌈\n"
        
        report += f"""
특히 이런 긍정적인 표현들을 자주 사용했어요:
  {', '.join(self.emotion['positive_keywords'][:10])}

"""
        
        if self.emotion['negative_keywords']:
            report += f"""이런 감정 표현도 있었어요:
  {', '.join(self.emotion['negative_keywords'][:5])}
  
💡 감정을 솔직하게 표현하는 것은 건강한 발달의 중요한 부분이에요!
"""
        
        report += f"""
{'='*80}
🎯 무엇에 관심이 있었나요?
{'='*80}

{child_name}가 놀이 시간에 가장 많이 이야기한 주제들이에요:

"""
        
        for i, (word, count) in enumerate(self.topics['top_keywords'][:10], 1):
            report += f"  {i}. {word}\n"
        
        report += f"""
총 {self.topics['unique_words']}개의 서로 다른 단어를 사용했어요.
"""
        
        ttr = self.topics['unique_words'] / self.topics['total_words'] * 100
        if ttr >= 30:
            report += "어휘력이 매우 풍부해요! 📚✨\n"
        elif ttr >= 20:
            report += "다양한 단어를 사용하고 있어요! 📖\n"
        else:
            report += "익숙한 단어로 명확하게 표현하고 있어요! 💬\n"
        
        report += f"""
{'='*80}
🧠 문제해결 능력은 어떤가요?
{'='*80}

{child_name}는 "왜?", "어떻게?", "이렇게 하면?" 같은
문제해결 표현을 {self.problem_solving['problem_solving_count']}번 사용했어요!

예를 들면 이런 말들이 있었어요:
"""
        
        for i, example in enumerate(self.problem_solving['examples'][:3], 1):
            report += f"  • \"{example}\"\n"
        
        if self.problem_solving['problem_solving_ratio'] >= 10:
            report += "\n스스로 생각하고 해결하려는 모습이 돋보여요! 🎯\n"
        elif self.problem_solving['problem_solving_ratio'] >= 5:
            report += "\n궁금한 것을 질문하고 탐구하는 모습이 좋아요! 🔍\n"
        else:
            report += "\n함께 문제를 해결하는 경험이 더 있으면 좋겠어요! 💪\n"
        
        report += f"""
{'='*80}
🌟 종합 평가
{'='*80}
"""
        
        # 긍정적인 평가 중심
        strengths = []
        
        if self.speech_ratio['child_speech_ratio'] >= 45:
            strengths.append(f"✨ {child_name}는 대화에 적극적으로 참여해요!")
        
        if self.emotion['positive_ratio'] >= 50:
            strengths.append(f"😊 긍정적인 감정을 잘 표현해요!")
        
        if self.problem_solving['problem_solving_ratio'] >= 5:
            strengths.append(f"🧩 스스로 생각하고 질문하는 능력이 있어요!")
        
        if ttr >= 20:
            strengths.append(f"📚 다양한 단어를 사용할 줄 알아요!")
        
        if self.turn_taking['avg_child_turn_length'] <= 2:
            strengths.append(f"🗣️ 대화 주고받기를 잘해요!")
        
        if not strengths:
            strengths.append(f"🌱 {child_name}만의 독특한 방식으로 놀이에 참여하고 있어요!")
        
        for strength in strengths:
            report += f"\n{strength}"
        
        report += f"""

{'='*80}
💌 마무리 말씀
{'='*80}

{child_name}는 {teacher_name} 선생님과의 놀이 시간을 통해
자신의 생각과 감정을 표현하고, 새로운 것을 탐구하며 성장하고 있어요.

앞으로도 {child_name}가 자신감을 가지고 
더 많은 것을 표현할 수 있도록 응원해주세요! 💪🌟

궁금하신 점이 있으시면 언제든 선생님께 문의해주세요.

감사합니다. 😊

{'='*80}
레포트 생성일: {datetime.now().strftime('%Y년 %m월 %d일')}
{'='*80}
"""
        
        return report
    
    def generate_teacher_report(self):
        """선생님용 레포트 생성 (교육적 인사이트, 개선 제안)"""
        
        child_name = self.meta.get('child_name', '아동')
        child_age = self.meta.get('child_age', '')
        
        report = f"""
{'='*80}
👩‍🏫 교사용 놀이 분석 레포트
{'='*80}

아동: {child_name} ({child_age})
세션 날짜: {self.meta.get('date', 'N/A')}
분석 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*80}
📊 핵심 지표 요약
{'='*80}

1. 아동 발화 참여도: {self.speech_ratio['child_speech_ratio']:.1f}%
2. 평균 발화 길이: {self.speech_amount['avg_utterance_length']:.1f}자
3. 감정 긍정 비율: {self.emotion['positive_ratio']:.1f}%
4. 문제해결 발화: {self.problem_solving['problem_solving_ratio']:.1f}%
5. 어휘 다양도 (TTR): {(self.topics['unique_words'] / self.topics['total_words'] * 100):.1f}%

{'='*80}
🎯 발달 영역별 분석
{'='*80}

【 언어 발달 】
"""
        
        # 언어 발달 분석
        if self.speech_amount['avg_utterance_length'] >= 25:
            report += f"  ✅ 우수: 복문 사용 능력이 발달되어 있음 (평균 {self.speech_amount['avg_utterance_length']:.1f}자)\n"
        elif self.speech_amount['avg_utterance_length'] >= 15:
            report += f"  🟢 양호: 문장 구성 능력이 연령에 적합함 (평균 {self.speech_amount['avg_utterance_length']:.1f}자)\n"
        else:
            report += f"  🟡 주의: 발화 길이가 짧음. 확장 질문 필요 (평균 {self.speech_amount['avg_utterance_length']:.1f}자)\n"
        
        ttr = self.topics['unique_words'] / self.topics['total_words'] * 100
        if ttr >= 30:
            report += f"  ✅ 우수: 어휘 다양성이 매우 높음 (TTR {ttr:.1f}%)\n"
        elif ttr >= 20:
            report += f"  🟢 양호: 어휘 사용이 다양함 (TTR {ttr:.1f}%)\n"
        else:
            report += f"  🟡 주의: 반복 단어 사용. 어휘 확장 활동 권장 (TTR {ttr:.1f}%)\n"
        
        report += f"""
【 사회정서 발달 】
"""
        
        # 사회정서 발달 분석
        if self.emotion['positive_ratio'] >= 70:
            report += f"  ✅ 우수: 긍정적 정서 표현이 활발함\n"
        elif self.emotion['positive_ratio'] >= 50:
            report += f"  🟢 양호: 정서 표현이 균형적임\n"
        else:
            report += f"  🟡 주의: 부정 정서 표현 빈도 관찰 필요\n"
        
        if self.turn_taking['turn_taking_balance'] >= 0.4 and self.turn_taking['turn_taking_balance'] <= 0.6:
            report += f"  ✅ 우수: 대화 주고받기가 균형적임 ({self.turn_taking['turn_taking_balance']:.2f})\n"
        else:
            report += f"  🟡 주의: 대화 주도성 조절 필요 ({self.turn_taking['turn_taking_balance']:.2f})\n"
        
        report += f"""
【 인지 발달 】
"""
        
        # 인지 발달 분석
        if self.problem_solving['problem_solving_ratio'] >= 10:
            report += f"  ✅ 우수: 문제해결 사고가 활발함 ({self.problem_solving['problem_solving_ratio']:.1f}%)\n"
        elif self.problem_solving['problem_solving_ratio'] >= 5:
            report += f"  🟢 양호: 탐구적 질문을 함 ({self.problem_solving['problem_solving_ratio']:.1f}%)\n"
        else:
            report += f"  🟡 주의: 사고 확장 질문 유도 필요 ({self.problem_solving['problem_solving_ratio']:.1f}%)\n"
        
        report += f"""
{'='*80}
🎲 놀이 패턴 분석
{'='*80}

주요 관심 주제 (상위 5개):
"""
        
        for i, (word, count) in enumerate(self.topics['top_keywords'][:5], 1):
            report += f"  {i}. {word} ({count}회)\n"
        
        report += f"""
→ 이 주제들을 활용한 확장 활동 계획을 권장합니다.

문제해결 발화 예시:
"""
        
        for i, example in enumerate(self.problem_solving['examples'][:5], 1):
            report += f"  {i}. \"{example}\"\n"
        
        report += f"""
→ 이러한 질문에 대한 스캐폴딩 전략을 고려하세요.

{'='*80}
💡 교육적 제안 사항
{'='*80}
"""
        
        suggestions = []
        
        # 발화 참여도 기반 제안
        if self.speech_ratio['child_speech_ratio'] < 40:
            suggestions.append({
                'area': '발화 참여 증진',
                'issue': f'아동 발화 비율이 {self.speech_ratio["child_speech_ratio"]:.1f}%로 낮음',
                'suggestion': '개방형 질문 비중 늘리기, 대기 시간(wait time) 5초 이상 확보'
            })
        
        # 발화 길이 기반 제안
        if self.speech_amount['avg_utterance_length'] < 10:
            suggestions.append({
                'area': '언어 확장',
                'issue': f'평균 발화 길이가 {self.speech_amount["avg_utterance_length"]:.1f}자로 짧음',
                'suggestion': '확장(expansion) 및 확대(extension) 기법 사용, "그리고?", "왜?" 질문 추가'
            })
        
        # 어휘 다양성 기반 제안
        if ttr < 20:
            suggestions.append({
                'area': '어휘 확장',
                'issue': f'어휘 다양도(TTR)가 {ttr:.1f}%로 낮음',
                'suggestion': '새로운 어휘 도입, 동의어/반의어 놀이, 그림책 활용'
            })
        
        # 문제해결 기반 제안
        if self.problem_solving['problem_solving_ratio'] < 5:
            suggestions.append({
                'area': '사고력 증진',
                'issue': f'문제해결 발화가 {self.problem_solving["problem_solving_ratio"]:.1f}%로 낮음',
                'suggestion': '가설 설정 유도, "어떻게 하면?" 질문, 원인-결과 탐구 활동'
            })
        
        # 감정 표현 기반 제안
        if self.emotion['positive_ratio'] < 40:
            suggestions.append({
                'area': '정서 지원',
                'issue': f'부정 정서 표현 비율이 {self.emotion["negative_ratio"]:.1f}%',
                'suggestion': '감정 읽기 및 공감 반응, 긍정적 강화, 정서 조절 전략 모델링'
            })
        
        if not suggestions:
            report += "\n✅ 전반적으로 발달이 양호합니다. 현재 상호작용 전략을 유지하세요.\n"
        else:
            for i, sug in enumerate(suggestions, 1):
                report += f"""
{i}. [{sug['area']}]
   ⚠️  현황: {sug['issue']}
   💡 제안: {sug['suggestion']}
"""
        
        report += f"""
{'='*80}
📚 누리과정 연계
{'='*80}

이번 놀이 활동은 다음 누리과정 영역과 연계됩니다:

• 의사소통 영역: 말하기, 듣기, 읽기, 쓰기 기초
• 사회관계 영역: 더불어 생활하기, 사회에 관심 갖기
• 자연탐구 영역: 탐구과정 즐기기
"""
        
        if self.problem_solving['problem_solving_ratio'] >= 5:
            report += "• 특히 '탐구과정 즐기기' 측면에서 강점이 관찰됨\n"
        
        report += f"""
{'='*80}
🔄 다음 세션 계획 제안
{'='*80}

1. 이번 세션의 주요 관심사({self.topics['top_keywords'][0][0]})를 활용한 확장 활동
2. """
        
        if self.speech_amount['avg_utterance_length'] < 15:
            report += "발화 확장을 위한 스토리텔링 활동\n3. "
        else:
            report += "주제 심화를 위한 프로젝트 접근\n3. "
        
        if self.emotion['positive_ratio'] >= 60:
            report += "긍정적 정서를 바탕으로 도전적 과제 제시\n"
        else:
            report += "정서적 안정감 형성을 위한 협동 놀이\n"
        
        report += f"""
{'='*80}
✅ 교사 체크리스트
{'='*80}

□ 아동의 발화를 충분히 기다리기 (5초 이상)
□ 확장 질문 사용하기 ("왜?", "어떻게?", "그리고?")
□ 아동의 관심사 파악 및 기록
□ 긍정적 피드백 제공
□ 다음 세션 활동 계획 수립
□ 학부모 소통 계획

{'='*80}
레포트 생성 일시: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}
분석 시스템: Care Intelligence v1.0
{'='*80}
"""
        
        return report
    
    def save_all_reports(self, output_dir="reports"):
        """3가지 레포트를 모두 생성하고 저장"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        session_name = self.meta['session_name']
        
        # 1. 회사용 레포트
        company_report = self.generate_company_report()
        company_file = output_path / f"{session_name}_company_report.txt"
        with open(company_file, 'w', encoding='utf-8') as f:
            f.write(company_report)
        print(f"✅ 회사용 레포트 저장: {company_file}")
        
        # 2. 부모용 레포트
        parent_report = self.generate_parent_report()
        parent_file = output_path / f"{session_name}_parent_report.txt"
        with open(parent_file, 'w', encoding='utf-8') as f:
            f.write(parent_report)
        print(f"✅ 부모용 레포트 저장: {parent_file}")
        
        # 3. 선생님용 레포트
        teacher_report = self.generate_teacher_report()
        teacher_file = output_path / f"{session_name}_teacher_report.txt"
        with open(teacher_file, 'w', encoding='utf-8') as f:
            f.write(teacher_report)
        print(f"✅ 선생님용 레포트 저장: {teacher_file}")
        
        return {
            'company': company_file,
            'parent': parent_file,
            'teacher': teacher_file
        }


def main():
    """메인 함수"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python generate_reports.py <analysis_result.json>")
        print("\n예시:")
        print("  python generate_reports.py analysis_results/20251017-이민정교사-김준우-만4세-02_00_48-65kbps_mono_analysis.json")
        sys.exit(1)
    
    analysis_file = sys.argv[1]
    
    # 레포트 생성기
    generator = ReportGenerator(analysis_file)
    
    # 모든 레포트 생성
    print("\n" + "="*80)
    print("📝 레포트 생성 시작")
    print("="*80 + "\n")
    
    report_files = generator.save_all_reports()
    
    print("\n" + "="*80)
    print("✨ 레포트 생성 완료!")
    print("="*80)
    print(f"\n회사용: {report_files['company']}")
    print(f"부모용: {report_files['parent']}")
    print(f"선생님용: {report_files['teacher']}")
    print()


if __name__ == "__main__":
    main()

