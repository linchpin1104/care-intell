"""
놀이 세션 레포트 생성기
- 부모용 레포트: 이해하기 쉽고 긍정적
- 선생님용 레포트: 교육적 인사이트와 방문일지
- 회사용 레포트: 상세한 데이터 분석
"""

import os
import json
import numpy as np
from datetime import datetime
from typing import Dict, Any, List


class ReportGenerator:
    """레포트 생성기"""
    
    def __init__(self, analysis_file: str):
        """
        Args:
            analysis_file: enhanced_analysis.py로 생성된 분석 결과 JSON 파일
        """
        with open(analysis_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.metadata = self.data['metadata']
        self.metrics = self.data['metrics']
    
    def generate_parent_report(self) -> str:
        """부모용 레포트 생성 - 따뜻하고 친절한 담당 선생님의 목소리"""
        report = []
        
        child_name = self.metadata['child']
        teacher_name = self.metadata['teacher']
        
        # 헤더
        report.append("╔" + "="*68 + "╗")
        report.append("                        놀이 활동 리포트 (학부모용)                    ")
        report.append("╚" + "="*68 + "╝\n")
        
        # 따뜻한 인사
        report.append(f"안녕하세요, {child_name} 부모님 😊")
        report.append(f"{teacher_name} 선생님입니다.")
        report.append("")
        report.append(f"오늘 {child_name}(이)와 함께한 소중한 시간을 부모님과 나누고 싶어")
        report.append(f"이렇게 글을 남깁니다. 부모님께서 {child_name}(이)의 성장을 함께")
        report.append(f"응원하고 계신다는 것을 알기에, 오늘 관찰한 내용을 자세히 전해드리겠습니다.")
        report.append("")
        report.append("━" * 70)
        report.append("")
        
        # 기본 정보
        report.append("📋 오늘의 만남")
        report.append("━" * 70)
        report.append(f"  • 날짜: {self._format_date(self.metadata['date'])}")
        report.append(f"  • 함께한 시간: {int(self.metrics['total_session_duration']//60)}분")
        report.append("")
        
        # 주요 활동
        report.append("🎯 오늘의 놀이 활동")
        report.append("━" * 70)
        topics = self.metrics.get('main_topics', [])[:5]
        if topics:
            report.append(f"  • 주요 관심 주제: {', '.join([t[0] for t in topics])}")
        
        context_switches = self.metrics.get('context_switches', {})
        topic_dist = context_switches.get('topic_distribution', {})
        if topic_dist:
            main_activities = [k for k, v in sorted(topic_dist.items(), key=lambda x: -x[1])[:3]]
            report.append(f"  • 활동 영역: {', '.join(main_activities)}")
        report.append("")
        
        # 의사소통 발달
        report.append("💬 말하기와 듣기")
        report.append("━" * 70)
        
        child_ratio = self.metrics['child_utterance_ratio']
        child_count = self.metrics['child_utterance_count']
        
        # 참여도 평가 (선생님의 따뜻한 관찰)
        if child_ratio >= 0.5:
            report.append(f"오늘 {child_name}(이)는 정말 말을 많이 했어요! 😊")
            report.append(f"선생님보다도 더 많이 이야기할 정도로 자신의 생각을 표현하는 데")
            report.append(f"주저함이 없었답니다. 이렇게 적극적으로 대화에 참여하는 모습이")
            report.append(f"정말 기특하고 대견했어요.")
        elif child_ratio >= 0.35:
            report.append(f"{child_name}(이)가 선생님과 주고받는 대화가 참 자연스러웠어요.")
            report.append(f"때로는 듣고, 때로는 말하며 균형있게 소통하는 모습에서")
            report.append(f"대화의 즐거움을 느끼는 것 같았어요.")
        else:
            report.append(f"{child_name}(이)는 오늘 선생님의 이야기를 귀 기울여 들어주었어요.")
            report.append(f"말은 많지 않았지만, 눈빛과 표정으로 반응하며")
            report.append(f"충분히 소통하고 있었답니다.")
        
        report.append("")
        
        avg_words = self.metrics['child_avg_words_per_utterance']
        if avg_words >= 5:
            report.append(f"특히 인상적이었던 것은 {child_name}(이)가 짧은 단답형이 아니라")
            report.append(f"평균 {avg_words:.1f}개 단어로 이루어진 문장으로 이야기한다는 거예요.")
            report.append(f"자신의 생각을 자세히 설명하려는 노력이 느껴졌어요.")
        else:
            report.append(f"{child_name}(이)는 간결하지만 명확하게 자신의 의사를 전달했어요.")
            report.append(f"꼭 필요한 말만 골라서 하는 모습이 효율적이었답니다.")
        
        report.append("")
        report.append(f"💬 선생님 메모: 오늘 총 {child_count}번 이야기를 나눴어요!")
        report.append("")
        
        # 사고력 발달
        report.append("🧠 생각하는 힘")
        report.append("━" * 70)
        
        problem_solving = self.metrics.get('problem_solving_utterances', {})
        ps_count = problem_solving.get('child_count', 0)
        
        if ps_count >= 50:
            report.append(f"{child_name}(이)의 호기심은 정말 대단해요! ✨")
            report.append(f"오늘 하루 동안 '왜 그래요?', '어떻게 하는 거예요?' 같은 질문을")
            report.append(f"{ps_count}번이나 했답니다. 이렇게 끊임없이 질문하고 탐구하는 모습에서")
            report.append(f"배움에 대한 열정이 느껴져요. 정말 훌륭해요!")
        elif ps_count >= 20:
            report.append(f"{child_name}(이)는 궁금한 게 생기면 그냥 넘어가지 않아요.")
            report.append(f"'왜 그럴까?', '어떻게 하면 될까?' 하고 선생님께 물어보거나")
            report.append(f"스스로 방법을 찾아보려고 했어요. 이런 탐구하는 자세가")
            report.append(f"앞으로의 성장에 큰 밑거름이 될 거예요.")
        else:
            report.append(f"{child_name}(이)는 오늘 놀이에 집중하며 즐거운 시간을 보냈어요.")
            report.append(f"앞으로 '왜 그럴까?', '어떻게 하면 좋을까?' 같은 질문을")
            report.append(f"자연스럽게 할 수 있도록 선생님이 도와줄게요.")
        
        # 인상 깊었던 질문이나 발화
        examples = problem_solving.get('child_examples', [])[:3]
        if examples:
            report.append("")
            report.append(f"📝 특히 기억에 남는 질문:")
            for ex in examples[:2]:  # 최대 2개만
                report.append(f"   \"{ex}\"")
        report.append("")
        
        # 정서 발달
        report.append("❤️ 마음과 감정")
        report.append("━" * 70)
        
        positive = self.metrics['positive_utterances']
        negative = self.metrics['negative_utterances']
        
        if positive > negative * 1.5:
            report.append(f"오늘 {child_name}(이)는 참 밝고 즐거운 하루를 보냈어요! 😊")
            report.append(f"'좋아요', '재밌어요', '우와!' 같은 긍정적인 표현을 많이 사용하며")
            report.append(f"놀이를 즐기는 모습이 정말 보기 좋았답니다.")
            report.append(f"이렇게 긍정적인 정서는 {child_name}(이)의 소중한 강점이에요.")
        elif positive > negative * 0.7:
            report.append(f"{child_name}(이)는 오늘 안정적인 감정 상태로 놀이를 즐겼어요.")
            report.append(f"때로는 즐겁게 웃고, 때로는 진지하게 생각하며")
            report.append(f"상황에 맞게 자신의 감정을 잘 표현했답니다.")
        else:
            report.append(f"{child_name}(이)는 자신의 감정을 솔직하게 표현해요.")
            report.append(f"좋은 것은 좋다고, 싫은 것은 싫다고 분명히 말하는 모습에서")
            report.append(f"자기 주장이 확실한 아이라는 것을 알 수 있었어요.")
            report.append(f"앞으로는 부정적인 감정도 긍정적으로 표현하는 방법을")
            report.append(f"함께 연습해볼 거예요.")
        
        # 주요 정서 단어
        emotion_kw = self.metrics.get('emotion_keywords', {})
        positive_words = emotion_kw.get('positive', [])
        if positive_words:
            top_positive = [w[0] for w in positive_words[:3]]
            report.append("")
            report.append(f"💕 자주 들린 행복한 말: {', '.join(top_positive)}")
        report.append("")
        
        # 주제 지속도
        report.append("🎨 집중력과 몰입")
        report.append("━" * 70)
        
        persistence = self.metrics.get('topic_persistence', 1.0)
        
        if persistence >= 3.0:
            focus_level = "매우 높음 ⭐⭐⭐"
            focus_comment = "한 가지 활동에 깊이 몰입하는 모습을 보였습니다."
        elif persistence >= 2.0:
            focus_level = "높음 ⭐⭐"
            focus_comment = "활동에 집중하며 지속적으로 참여했습니다."
        else:
            focus_level = "보통 ⭐"
            focus_comment = "다양한 활동을 탐색하며 관심을 보였습니다."
        
        report.append(f"  • 주제 지속도: {focus_level}")
        report.append(f"  • 평가: {focus_comment}")
        report.append("")
        
        # 특별히 관찰된 점
        report.append("✨ 특별히 관찰된 점")
        report.append("━" * 70)
        
        observations = []
        
        if child_ratio >= 0.5:
            observations.append(f"• {self.metadata['child']}(이)가 대화를 주도하며 자신의 생각을 적극적으로 표현했습니다.")
        
        if ps_count >= 30:
            observations.append(f"• 호기심이 많아 '왜?', '어떻게?'라는 질문을 자주 하며 탐구하는 모습이 인상적이었습니다.")
        
        if positive > negative:
            observations.append(f"• 즐겁고 긍정적인 태도로 놀이에 참여했습니다.")
        
        if persistence >= 2.5:
            observations.append(f"• 관심 있는 주제에 깊이 몰입하는 집중력을 보였습니다.")
        
        if not observations:
            observations.append(f"• {self.metadata['child']}(이)가 선생님과 즐겁게 놀이하는 시간을 보냈습니다.")
        
        for obs in observations:
            report.append(obs)
        report.append("")
        
        # 가정 연계 제안
        report.append("🏠 가정에서 함께 해보세요")
        report.append("━" * 70)
        
        suggestions = []
        
        # 주요 관심사 기반 제안
        if topics:
            top_topic = topics[0][0]
            suggestions.append(f"• '{top_topic}'에 관심이 많으니 관련 활동을 함께 해보세요.")
        
        # 사고력 발달 제안
        if ps_count < 20:
            suggestions.append("• '왜 그럴까?', '어떻게 하면 좋을까?' 같은 열린 질문을 활용해보세요.")
        else:
            suggestions.append(f"• {self.metadata['child']}(이)의 호기심을 격려하고 함께 답을 찾아가는 과정을 즐겨보세요.")
        
        # 정서 발달 제안
        if positive < negative:
            suggestions.append("• 긍정적인 표현('좋아', '재밌어', '고마워')을 자주 사용하는 모델링을 보여주세요.")
        
        # 의사소통 제안
        if child_ratio < 0.4:
            suggestions.append(f"• {self.metadata['child']}(이)의 이야기를 경청하고 충분히 대답할 시간을 주세요.")
        else:
            suggestions.append(f"• {self.metadata['child']}(이)의 적극적인 표현을 칭찬해주고 더 자세히 이야기할 수 있도록 격려해주세요.")
        
        for sug in suggestions:
            report.append(sug)
        report.append("")
        
        # 따뜻한 마무리
        report.append("")
        report.append("━" * 70)
        report.append("")
        report.append(f"오늘도 {child_name}(이)와 함께한 시간이 참 소중했어요.")
        report.append(f"부모님께서 궁금하신 점이나 함께 나누고 싶은 이야기가 있으시다면")
        report.append(f"언제든 편하게 연락 주세요. {child_name}(이)의 성장을 함께 응원하며")
        report.append(f"옆에서 돕겠습니다. 😊")
        report.append("")
        report.append(f"감사합니다.")
        report.append("")
        report.append(f"{datetime.now().strftime('%Y년 %m월 %d일')}")
        report.append(f"{self.metadata['teacher']} 선생님 올림 ✨")
        report.append("")
        
        return '\n'.join(report)
    
    def generate_teacher_report(self) -> str:
        """선생님용 레포트 생성 - 아동·놀이·발달 전문가의 객관적 평가"""
        report = []
        
        child_name = self.metadata['child']
        child_age = self.metadata['age']
        
        # 헤더
        report.append("╔" + "="*68 + "╗")
        report.append("                    놀이 관찰 전문가 피드백 (교사용)                    ")
        report.append("╚" + "="*68 + "╝\n")
        
        # 전문가 인사
        report.append("━" * 70)
        report.append("   아동·놀이·발달 분석 전문가 리포트")
        report.append("━" * 70)
        report.append("")
        report.append(f"본 리포트는 {child_name} 아동({child_age})의 놀이 세션을 다각도로 분석하여")
        report.append(f"교사의 전문성 향상과 교수 전략 수립을 지원하기 위해 작성되었습니다.")
        report.append(f"데이터 기반 객관적 평가와 발달심리학적 관점에서의 해석을 제공합니다.")
        report.append("")
        report.append("━" * 70)
        report.append("")
        
        # 기본 정보
        report.append("【세션 개요】")
        report.append("")
        report.append(f"  대상 아동: {child_name} ({child_age})")
        report.append(f"  관찰 일시: {self._format_date(self.metadata['date'])}")
        report.append(f"  담당 교사: {self.metadata['teacher']}")
        report.append(f"  세션 시간: {int(self.metrics['total_session_duration']//60)}분")
        report.append(f"  분석 기준: 누리과정 5개 영역, 발달심리학 이론")
        report.append("")
        
        # 발달 영역별 관찰
        report.append("📊 발달 영역별 상세 분석")
        report.append("━" * 70)
        report.append("")
        
        # 1. 언어 발달 (전문가 평가)
        report.append("【1. 의사소통 발달 분석】")
        report.append("")
        
        child_ratio = self.metrics['child_utterance_ratio']
        child_count = self.metrics['child_utterance_count']
        teacher_count = self.metrics['teacher_utterance_count']
        avg_words = self.metrics['child_avg_words_per_utterance']
        total_words = self.metrics['child_word_count']
        
        report.append("■ 정량적 지표")
        report.append(f"  • 전체 발화: {child_count + teacher_count}회")
        report.append(f"    - 아동: {child_count}회 ({child_ratio:.1%})")
        report.append(f"    - 교사: {teacher_count}회 ({1-child_ratio:.1%})")
        report.append(f"  • 아동 언어 생산량: 총 {total_words}개 단어")
        report.append(f"  • 평균 발화 길이(MLU): {avg_words:.2f} 단어/발화")
        report.append("")
        
        # 전문가 평가
        report.append("■ 발달심리학적 해석")
        if child_ratio >= 0.5:
            report.append(f"  본 아동의 발화 비율({child_ratio:.1%})은 또래 평균을 상회하는 수준으로,")
            report.append(f"  자기주장 표현력과 의사소통 주도성이 우수함을 시사합니다.")
            report.append(f"  Vygotsky의 사회문화적 이론 관점에서 볼 때, 언어를 사고의")
            report.append(f"  도구로 적극 활용하고 있으며, 자기조절 발화가 내재화되는")
            report.append(f"  과정에 있는 것으로 판단됩니다.")
        elif child_ratio >= 0.35:
            report.append(f"  아동-교사 간 발화 비율({child_ratio:.1%}:{1-child_ratio:.1%})이 균형을 이루고 있어")
            report.append(f"  상호주관성(intersubjectivity) 형성이 원활합니다.")
            report.append(f"  턴테이킹(turn-taking) 능력이 발달 단계에 적합한 수준으로")
            report.append(f"  사회적 의사소통 능력이 안정적으로 형성되고 있습니다.")
        else:
            report.append(f"  아동의 발화 비율({child_ratio:.1%})이 상대적으로 낮은 것은")
            report.append(f"  수용언어가 표현언어보다 우세한 발달 단계이거나,")
            report.append(f"  관찰적 학습 전략을 선호하는 개인차로 해석할 수 있습니다.")
        
        report.append("")
        
        # 전문가 권고
        report.append("■ 교수 전략 권고사항")
        if child_ratio < 0.4:
            report.append("  → 비계설정(scaffolding) 강화: 개방형 질문 비율 증가")
            report.append("  → 발화 유도 전략: Wait time 5초 이상 확보")
            report.append("  → 병렬적 대화(parallel talk) 기법 활용 권장")
        elif child_ratio >= 0.5:
            report.append("  → 현재 수준 유지 및 심화 확장")
            report.append("  → 메타언어적 사고 촉진 활동 도입")
            report.append("  → 또래와의 언어적 상호작용 기회 확대")
        else:
            report.append("  → 현재의 균형잡힌 상호작용 패턴 유지")
            report.append("  → 아동의 관심사 기반 대화 확장")
        
        report.append("")
        
        # 2. 인지 발달 (전문가 평가)
        report.append("【2. 인지 발달 분석】")
        report.append("")
        
        problem_solving = self.metrics.get('problem_solving_utterances', {})
        ps_count = problem_solving.get('child_count', 0)
        persistence = self.metrics['topic_persistence']
        context_switches = self.metrics.get('context_switches', {})
        total_switches = context_switches.get('total_switches', 0)
        
        report.append("■ 정량적 지표")
        report.append(f"  • 탐구적 질문 빈도: {ps_count}회")
        report.append(f"  • 주제 지속도 지수: {persistence:.2f} (연속 발화)")
        report.append(f"  • 인지적 전환 빈도: {total_switches}회")
        report.append("")
        
        # Piaget 발달 단계 기준 평가
        report.append("■ Piaget 인지 발달 단계 분석")
        if ps_count >= 50:
            report.append(f"  본 아동은 {child_age}에 해당하는 전조작기(Preoperational Stage)에서")
            report.append(f"  매우 활발한 '왜?'의 시기를 경험하고 있습니다.")
            report.append(f"  탐구적 질문 빈도({ps_count}회)는 연령 규준 상위 10% 수준으로,")
            report.append(f"  인과관계 이해와 가설적 사고가 발달하고 있음을 시사합니다.")
            report.append(f"  이는 구체적 조작기로의 전환을 준비하는 긍정적 신호입니다.")
        elif ps_count >= 20:
            report.append(f"  아동의 탐구 행동({ps_count}회)은 발달 단계에 적합한 수준입니다.")
            report.append(f"  인과관계에 대한 호기심과 문제해결 시도가 관찰되며,")
            report.append(f"  전조작기 특성인 직관적 사고가 점차 논리적 사고로")
            report.append(f"  이행하는 과도기적 특성을 보입니다.")
        else:
            report.append(f"  탐구적 질문 빈도({ps_count}회)가 상대적으로 낮은 것은")
            report.append(f"  환경적 자극의 부족, 또는 사고 과정의 내재화로 해석됩니다.")
            report.append(f"  발문 전략을 통한 인지적 도전 상황 제공이 필요합니다.")
        
        report.append("")
        
        # 주의집중 및 실행기능 평가
        report.append("■ 주의집중 및 실행기능")
        if persistence >= 3.0:
            report.append(f"  주제 지속도({persistence:.2f})가 높아 지속적 주의(sustained attention)")
            report.append(f"  능력이 우수합니다. 한 가지 활동에 깊이 몰입하는 Flow 상태를")
            report.append(f"  경험하고 있으며, 이는 자기조절 능력 발달의 핵심 지표입니다.")
        elif persistence >= 2.0:
            report.append(f"  적절한 수준의 주의집중력({persistence:.2f})을 보이며,")
            report.append(f"  과제 전환과 지속 사이의 균형이 유지되고 있습니다.")
        else:
            report.append(f"  탐색적 행동이 우세하며({persistence:.2f}), 다양한 자극에")
            report.append(f"  반응하는 유연성을 보입니다. 심화 활동을 통한 몰입 경험이 필요합니다.")
        
        report.append("")
        
        # 전문가 권고
        report.append("■ 교수 전략 권고사항")
        if ps_count < 20:
            report.append("  → 인지적 갈등 상황 제공: 예측-관찰-설명(POE) 전략")
            report.append("  → 프로젝트 기반 학습: 장기 탐구 활동 도입")
            report.append("  → 또래 협력 문제해결 과제 제시")
        elif ps_count >= 50:
            report.append("  → 상위 인지 전략 도입: 메타인지적 질문")
            report.append("  → 과학적 탐구 과정 경험: 가설-실험-결론")
            report.append("  → 복잡한 프로젝트 과제로 사고 확장")
        else:
            report.append("  → 현재 수준의 탐구 활동 지속")
            report.append("  → 점진적 인지적 도전 과제 추가")
        
        # 발화 예시
        examples = problem_solving.get('child_examples', [])[:3]
        if examples:
            report.append("")
            report.append("■ 대표 탐구 발화 사례")
            for i, ex in enumerate(examples, 1):
                report.append(f"  {i}) \"{ex}\"")
        
        report.append("")
        
        # 3. 사회정서 발달 (전문가 평가)
        report.append("【3. 사회정서 발달 분석】")
        report.append("")
        
        positive = self.metrics['positive_utterances']
        negative = self.metrics['negative_utterances']
        ratio = self.metrics['positive_negative_ratio']
        
        report.append("■ 정량적 지표")
        report.append(f"  • 긍정 정서 발화: {positive}회")
        report.append(f"  • 부정 정서 발화: {negative}회")
        report.append(f"  • 정서 균형 지수: {ratio:.2f}")
        report.append("")
        
        # Emotional Intelligence 관점 평가
        report.append("■ 정서지능(EQ) 분석")
        if ratio >= 1.5:
            report.append(f"  정서 균형 지수({ratio:.2f})가 높아 정서적 안정성이 우수합니다.")
            report.append(f"  Goleman의 정서지능 모델에서 '자기인식' 및 '자기조절' 영역이")
            report.append(f"  발달 단계를 고려할 때 적절한 수준으로 형성되어 있습니다.")
            report.append(f"  긍정 정서의 표현이 활발하여 또래 관계 형성과 유지에")
            report.append(f"  유리한 정서적 특성을 보입니다.")
        elif ratio >= 0.7:
            report.append(f"  긍정-부정 정서의 균형({ratio:.2f})이 적절하여")
            report.append(f"  정서 조절 능력이 발달하고 있음을 시사합니다.")
            report.append(f"  다양한 정서를 경험하고 표현하는 과정에서")
            report.append(f"  정서적 복원력(emotional resilience)이 형성되고 있습니다.")
        else:
            report.append(f"  부정 정서 표현이 상대적으로 많은 것({ratio:.2f})은")
            report.append(f"  정서 조절 전략(emotion regulation strategies)의")
            report.append(f"  발달이 필요한 시기임을 나타냅니다.")
            report.append(f"  이는 병리적 신호가 아니라 발달 과정의 자연스러운 현상이며,")
            report.append(f"  적절한 교수 전략으로 개선 가능합니다.")
        
        report.append("")
        
        # 정서 어휘 분석
        emotion_kw = self.metrics.get('emotion_keywords', {})
        positive_words = emotion_kw.get('positive', [])
        negative_words = emotion_kw.get('negative', [])
        
        if positive_words or negative_words:
            report.append("■ 정서 어휘 레퍼토리")
            if positive_words:
                top_pos = ', '.join([f"'{w[0]}'({w[1]})" for w in positive_words[:5]])
                report.append(f"  • 긍정 정서어: {top_pos}")
            if negative_words:
                top_neg = ', '.join([f"'{w[0]}'({w[1]})" for w in negative_words[:5]])
                report.append(f"  • 부정 정서어: {top_neg}")
            report.append("")
        
        # 전문가 권고
        report.append("■ 교수 전략 권고사항")
        if ratio < 0.7:
            report.append("  → 긍정적 강화 전략: Praise-to-Criticism 비율 5:1 유지")
            report.append("  → 정서 코칭 접근: 감정 이름 붙이기, 감정 타당화")
            report.append("  → Social-Emotional Learning(SEL) 프로그램 도입")
            report.append("  → 정서 조절 기술 교수: 심호흡, 긍정적 자기대화")
        elif ratio >= 1.5:
            report.append("  → 정서적 강점 활용: 또래 돕기 역할 부여")
            report.append("  → 공감 능력 확장: 타인 감정 이해하기 활동")
            report.append("  → 현재의 긍정적 정서 환경 유지")
        else:
            report.append("  → 균형잡힌 정서 표현 지속 지원")
            report.append("  → 다양한 정서 경험 기회 제공")
        
        report.append("")
        
        # 4. 놀이 특성
        report.append("【놀이 특성】")
        
        topics = self.metrics.get('main_topics', [])[:10]
        if topics:
            report.append("  ✓ 주요 관심 주제:")
            for i, (topic, count) in enumerate(topics[:10], 1):
                report.append(f"     {i}. {topic} ({count}회)")
        
        topic_dist = context_switches.get('topic_distribution', {})
        if topic_dist:
            report.append("  ✓ 놀이 영역 분포:")
            for topic, count in sorted(topic_dist.items(), key=lambda x: -x[1]):
                percentage = count / sum(topic_dist.values()) * 100
                report.append(f"     • {topic}: {percentage:.1f}%")
        
        report.append("")
        
        # 시간대별 참여도
        report.append("【시간대별 참여 패턴】")
        segments = self.metrics.get('time_segments', [])
        
        if segments:
            report.append("  시간대        전체발화    아동발화    참여비율")
            report.append("  " + "-" * 50)
            for seg in segments:
                time_range = f"{seg['start_time']}-{seg['end_time']}"
                report.append(f"  {time_range:12s}  {seg['total_utterances']:4d}회     {seg['child_utterances']:4d}회     {seg['child_ratio']:5.1%}")
        
        report.append("")
        
        # 교육적 제언
        report.append("📝 교육적 제언")
        report.append("━" * 70)
        
        recommendations = []
        
        # 언어 발달 제언
        if child_ratio < 0.4:
            recommendations.append({
                'area': '언어발달',
                'suggestion': '아동의 발화 기회를 더 많이 제공하세요. 교사의 발화를 줄이고 기다림의 시간을 늘려보세요.'
            })
        
        # 인지 발달 제언
        if ps_count < 20:
            recommendations.append({
                'area': '인지발달',
                'suggestion': '문제 상황을 제시하고 아동이 스스로 해결책을 생각하도록 유도하는 활동을 늘려보세요.'
            })
        elif ps_count >= 50:
            recommendations.append({
                'area': '인지발달',
                'suggestion': '탐구심이 높으니 프로젝트 기반 활동으로 깊이있는 학습 기회를 제공하세요.'
            })
        
        # 사회정서 제언
        if positive < negative:
            recommendations.append({
                'area': '사회정서',
                'suggestion': '긍정적 강화를 늘리고, 아동의 긍정적 행동을 구체적으로 언어화해주세요.'
            })
        
        # 놀이 제언
        persistence = self.metrics.get('topic_persistence', 1.0)
        if persistence < 2.0:
            recommendations.append({
                'area': '놀이집중도',
                'suggestion': '한 가지 활동에 더 깊이 몰입할 수 있도록 확장 활동을 제안해보세요.'
            })
        
        for i, rec in enumerate(recommendations, 1):
            report.append(f"{i}. [{rec['area']}] {rec['suggestion']}")
        
        report.append("")
        
        # 다음 계획
        report.append("📅 다음 세션 계획")
        report.append("━" * 70)
        
        if topics:
            top_interest = topics[0][0]
            report.append(f"• {top_interest} 관련 활동 확대")
        
        if ps_count >= 30:
            report.append("• 탐구 활동: 실험, 관찰, 예측 활동")
        else:
            report.append("• 문제해결 활동: 퍼즐, 미션, 프로젝트")
        
        if child_ratio < 0.4:
            report.append("• 아동 주도적 놀이 시간 확대")
        
        report.append("")
        
        # 전문가 종합 의견
        report.append("")
        report.append("━" * 70)
        report.append("【전문가 총평】")
        report.append("━" * 70)
        report.append("")
        
        # 강점과 개선 영역을 데이터 기반으로 정리
        report.append("■ 관찰된 발달적 강점")
        strengths = []
        if child_ratio >= 0.5:
            strengths.append("  • 언어 표현력 및 의사소통 주도성")
        if ps_count >= 30:
            strengths.append("  • 탐구심 및 문제해결 지향성")
        if persistence >= 3.0:
            strengths.append("  • 지속적 주의력 및 과제 몰입도")
        if ratio >= 1.0:
            strengths.append("  • 정서적 안정성 및 긍정적 정서 표현")
        
        if strengths:
            for strength in strengths:
                report.append(strength)
        else:
            report.append("  • 아동의 개별적 특성이 잘 관찰됨")
        
        report.append("")
        report.append("■ 중점 지원 영역")
        needs = []
        if child_ratio < 0.4:
            needs.append("  • 자기표현 기회 확대 및 언어적 자신감 향상")
        if ps_count < 20:
            needs.append("  • 인지적 자극 환경 구성 및 탐구 활동 강화")
        if ratio < 0.7:
            needs.append("  • 정서 조절 전략 학습 및 긍정적 강화")
        if persistence < 2.0:
            needs.append("  • 심화 활동을 통한 지속적 주의력 발달")
        
        if needs:
            for need in needs:
                report.append(need)
        else:
            report.append("  • 전반적으로 균형있는 발달을 보이고 있음")
        
        report.append("")
        report.append("■ 교사 전문성 발달을 위한 제언")
        report.append("  • 본 분석 데이터를 바탕으로 개별화 교육 계획(IEP) 수립")
        report.append("  • 누리과정 5개 영역과 연계한 통합적 접근")
        report.append("  • 지속적 관찰 및 포트폴리오 기록 유지")
        report.append("  • 정기적 전문가 컨설팅을 통한 교수 전략 점검")
        report.append("")
        report.append("━" * 70)
        report.append("")
        report.append(f"본 리포트는 객관적 데이터 분석과 발달심리학 이론에 근거하여 작성되었으며,")
        report.append(f"교사의 전문적 판단을 지원하기 위한 참고 자료로 활용하시기 바랍니다.")
        report.append("")
        report.append(f"분석일: {datetime.now().strftime('%Y년 %m월 %d일')}")
        report.append(f"분석: 아동·놀이·발달 전문가 시스템")
        report.append("")
        
        return '\n'.join(report)
    
    def generate_visit_journal(self) -> str:
        """선생님용 방문일지 생성"""
        report = []
        
        # 헤더
        report.append("╔" + "="*68 + "╗")
        report.append("                           가정 방문 관찰 일지                          ")
        report.append("╚" + "="*68 + "╝\n")
        
        # 기본 정보
        report.append("【기본 정보】")
        report.append(f"  관찰 아동: {self.metadata['child']} ({self.metadata['age']})")
        report.append(f"  관찰 일시: {self._format_date(self.metadata['date'])}")
        report.append(f"  관찰 시간: {int(self.metrics['total_session_duration']//60)}분")
        report.append(f"  관찰 교사: {self.metadata['teacher']}")
        report.append("")
        
        # 놀이 환경
        report.append("【놀이 환경】")
        report.append(f"  장소: 가정 (아동의 집)")
        report.append(f"  참여자: {self.metadata['child']}, {self.metadata['teacher']} 교사")
        report.append("")
        
        # 놀이 내용
        report.append("【놀이 내용 및 활동】")
        
        topics = self.metrics.get('main_topics', [])[:5]
        if topics:
            report.append("  주요 관심 영역:")
            for i, (topic, count) in enumerate(topics, 1):
                report.append(f"    {i}. {topic} 놀이 (언급 {count}회)")
        
        context_switches = self.metrics.get('context_switches', {})
        topic_dist = context_switches.get('topic_distribution', {})
        if topic_dist:
            report.append("  ")
            report.append("  참여한 놀이 유형:")
            for topic, count in sorted(topic_dist.items(), key=lambda x: -x[1]):
                report.append(f"    • {topic} 영역")
        
        report.append("")
        
        # 관찰 내용 - 발달 영역별
        report.append("【발달 영역별 관찰 내용】")
        report.append("")
        
        report.append("1. 신체 운동 발달")
        report.append("   - 놀이 활동에 적극적으로 참여함")
        report.append("")
        
        report.append("2. 의사소통 발달")
        child_ratio = self.metrics['child_utterance_ratio']
        child_count = self.metrics['child_utterance_count']
        avg_words = self.metrics['child_avg_words_per_utterance']
        
        if child_ratio >= 0.5:
            report.append(f"   - 매우 적극적으로 자신의 생각과 느낌을 표현함 (총 {child_count}회 발화)")
            report.append(f"   - 한 번에 평균 {avg_words:.1f}개 단어로 상세하게 표현함")
        elif child_ratio >= 0.35:
            report.append(f"   - 적절하게 자신의 의견을 표현함 (총 {child_count}회 발화)")
        else:
            report.append(f"   - 교사의 질문에 적절히 반응하며 경청함 (총 {child_count}회 발화)")
            report.append("   - 더 많은 언어 표현 기회 제공 필요")
        
        problem_solving = self.metrics.get('problem_solving_utterances', {})
        examples = problem_solving.get('child_examples', [])
        if examples:
            report.append(f"   - 발화 예시: \"{examples[0]}\"")
        
        report.append("")
        
        report.append("3. 사회관계 발달")
        positive = self.metrics['positive_utterances']
        negative = self.metrics['negative_utterances']
        
        if positive > negative:
            report.append("   - 긍정적이고 협력적인 태도로 교사와 상호작용함")
        else:
            report.append("   - 자신의 감정을 솔직하게 표현함")
        
        report.append("   - 교사와의 신뢰 관계를 형성하며 놀이에 참여함")
        report.append("")
        
        report.append("4. 예술경험")
        if '놀이' in str(topic_dist):
            report.append("   - 창의적인 놀이 표현을 시도함")
        report.append("   - 다양한 재료와 도구에 관심을 보임")
        report.append("")
        
        report.append("5. 자연탐구")
        ps_count = problem_solving.get('child_count', 0)
        
        if ps_count >= 30:
            report.append(f"   - 호기심이 많아 '왜?', '어떻게?'라는 질문을 자주 함 ({ps_count}회)")
            report.append("   - 탐구적 태도로 새로운 것을 알아가려는 모습을 보임")
        elif ps_count >= 10:
            report.append(f"   - 궁금한 것을 질문하며 탐구하는 모습을 보임 ({ps_count}회)")
        else:
            report.append("   - 주변 환경에 관심을 가지며 관찰함")
        
        report.append("")
        
        # 특이 사항
        report.append("【특이 사항 및 종합 의견】")
        
        observations = []
        
        if child_ratio >= 0.5:
            observations.append(f"• {self.metadata['child']} 아동은 언어 표현이 매우 활발하고 자신의 생각을 명확히 전달할 수 있음")
        
        persistence = self.metrics.get('topic_persistence', 1.0)
        if persistence >= 2.5:
            observations.append("• 관심 있는 활동에 깊이 집중하며 지속적으로 참여하는 모습이 인상적임")
        
        if ps_count >= 50:
            observations.append("• 탐구심과 호기심이 매우 높아 인지 발달이 또래 대비 우수함")
        
        if positive > negative * 1.5:
            observations.append("• 정서적으로 안정되어 있으며 긍정적인 태도로 활동에 임함")
        
        if not observations:
            observations.append(f"• {self.metadata['child']} 아동은 교사와 즐겁게 놀이 시간을 보냄")
        
        for obs in observations:
            report.append(f"  {obs}")
        
        report.append("")
        
        # 지도 방향
        report.append("【향후 지도 방향】")
        
        directions = []
        
        if child_ratio < 0.4:
            directions.append("• 아동 주도적 놀이 기회를 늘리고, 교사는 관찰자이자 지원자 역할에 집중")
        
        if ps_count < 20:
            directions.append("• 문제 상황을 제시하고 스스로 해결책을 찾도록 유도하는 활동 확대")
        
        if topics:
            top_interest = topics[0][0]
            directions.append(f"• '{top_interest}' 관련 활동을 확장하여 심화 학습 기회 제공")
        
        if positive < negative:
            directions.append("• 긍정적 강화를 통한 자존감 향상 및 정서 안정 지원")
        
        for direction in directions:
            report.append(f"  {direction}")
        
        report.append("")
        
        # 서명
        report.append("━" * 70)
        report.append(f"작성일: {datetime.now().strftime('%Y년 %m월 %d일')}")
        report.append(f"작성자: {self.metadata['teacher']} (서명)               확인: _____________ (서명)")
        report.append("")
        
        return '\n'.join(report)
    
    def generate_company_report(self) -> str:
        """회사용 레포트 생성 (상세 데이터 분석)"""
        report = []
        
        # 헤더
        report.append("╔" + "="*68 + "╗")
        report.append("                     놀이 세션 상세 분석 리포트 (내부용)                ")
        report.append("╚" + "="*68 + "╝\n")
        
        # 세션 메타데이터
        report.append("【세션 메타데이터】")
        report.append("━" * 70)
        report.append(f"  세션 ID: {os.path.basename(self.data.get('metadata', {}).get('date', ''))}")
        report.append(f"  아동: {self.metadata['child']} ({self.metadata['age']})")
        report.append(f"  교사: {self.metadata['teacher']}")
        report.append(f"  일시: {self._format_date(self.metadata['date'])}")
        report.append(f"  총 시간: {self.metrics['total_session_duration']:.1f}초 ({int(self.metrics['total_session_duration']//60)}분 {int(self.metrics['total_session_duration']%60)}초)")
        report.append(f"  분석 시각: {self.data.get('timestamp', 'N/A')}")
        report.append("")
        
        # 핵심 지표 요약
        report.append("【핵심 지표 요약 (KPI)】")
        report.append("━" * 70)
        report.append(f"  ► 아동 발화 비율: {self.metrics['child_utterance_ratio']:.2%}")
        report.append(f"  ► 아동 발화 수: {self.metrics['child_utterance_count']}회")
        report.append(f"  ► 교사 발화 수: {self.metrics['teacher_utterance_count']}회")
        report.append(f"  ► 아동 총 단어 수: {self.metrics['child_word_count']}개")
        report.append(f"  ► 평균 발화 길이: {self.metrics['child_avg_words_per_utterance']:.2f} 단어/발화")
        report.append(f"  ► 아동 말하기 시간: {self.metrics['child_speaking_duration']:.1f}초 ({self.metrics['child_speaking_ratio']:.1%})")
        report.append(f"  ► 주제 지속도: {self.metrics['topic_persistence']:.2f}")
        report.append(f"  ► 문제해결 발화: {self.metrics.get('problem_solving_utterances', {}).get('child_count', 0)}회")
        report.append(f"  ► 긍정/부정 비율: {self.metrics['positive_negative_ratio']:.2f}")
        report.append("")
        
        # 상세 언어 분석
        report.append("【상세 언어 분석】")
        report.append("━" * 70)
        report.append("")
        
        report.append("1. 발화 통계")
        report.append(f"   • 전체 발화: {self.metrics['total_utterance_count']}회")
        report.append(f"   • 아동 발화: {self.metrics['child_utterance_count']}회 ({self.metrics['child_utterance_ratio']:.2%})")
        report.append(f"   • 교사 발화: {self.metrics['teacher_utterance_count']}회 ({1-self.metrics['child_utterance_ratio']:.2%})")
        report.append("")
        
        report.append("2. 단어 사용 분석")
        report.append(f"   • 아동 총 단어: {self.metrics['child_word_count']}개")
        report.append(f"   • 교사 총 단어: {self.metrics['teacher_word_count']}개")
        report.append(f"   • 아동 평균 발화 길이: {self.metrics['child_avg_words_per_utterance']:.2f} 단어/발화")
        
        avg_words = self.metrics['child_avg_words_per_utterance']
        if avg_words >= 5:
            word_assessment = "우수 (상세한 문장 구사)"
        elif avg_words >= 3:
            word_assessment = "양호 (적절한 문장 길이)"
        else:
            word_assessment = "개선 필요 (단어 발화 중심)"
        report.append(f"   • 평가: {word_assessment}")
        report.append("")
        
        report.append("3. 발화 시간 분석")
        report.append(f"   • 아동 말하기 시간: {self.metrics['child_speaking_duration']:.1f}초")
        report.append(f"   • 교사 말하기 시간: {self.metrics['teacher_speaking_duration']:.1f}초")
        report.append(f"   • 아동 발화 시간 비율: {self.metrics['child_speaking_ratio']:.2%}")
        report.append("")
        
        # 인지 분석
        report.append("【인지 발달 분석】")
        report.append("━" * 70)
        
        problem_solving = self.metrics.get('problem_solving_utterances', {})
        ps_child = problem_solving.get('child_count', 0)
        ps_teacher = problem_solving.get('teacher_count', 0)
        
        report.append(f"  • 아동 문제해결 발화: {ps_child}회")
        report.append(f"  • 교사 문제해결 유도: {ps_teacher}회")
        report.append(f"  • 문제해결 참여율: {ps_child / self.metrics['child_utterance_count'] * 100:.1f}%")
        
        if ps_child >= 50:
            ps_level = "매우 높음 (5점/5점)"
        elif ps_child >= 30:
            ps_level = "높음 (4점/5점)"
        elif ps_child >= 15:
            ps_level = "보통 (3점/5점)"
        elif ps_child >= 5:
            ps_level = "낮음 (2점/5점)"
        else:
            ps_level = "매우 낮음 (1점/5점)"
        
        report.append(f"  • 문제해결 수준: {ps_level}")
        
        # 예시
        examples = problem_solving.get('child_examples', [])[:10]
        if examples:
            report.append("  • 문제해결 발화 샘플:")
            for i, ex in enumerate(examples, 1):
                report.append(f"     {i}. \"{ex}\"")
        
        report.append("")
        
        # 주제 분석
        report.append("  • 주제 지속도: {:.2f} (평균 연속 발화 수)".format(self.metrics['topic_persistence']))
        
        persistence = self.metrics['topic_persistence']
        if persistence >= 3.0:
            persist_level = "매우 높음 (깊은 몰입)"
        elif persistence >= 2.0:
            persist_level = "높음 (지속적 참여)"
        else:
            persist_level = "보통 (탐색적 참여)"
        
        report.append(f"  • 집중도 평가: {persist_level}")
        report.append("")
        
        # 맥락 전환 분석
        context_switches = self.metrics.get('context_switches', {})
        total_switches = context_switches.get('total_switches', 0)
        switches_per_min = context_switches.get('switches_per_minute', 0)
        
        report.append(f"  • 총 맥락 전환: {total_switches}회")
        report.append(f"  • 분당 전환율: {switches_per_min:.2f}회/분")
        report.append("")
        
        # 정서 분석
        report.append("【정서 발달 분석】")
        report.append("━" * 70)
        
        positive = self.metrics['positive_utterances']
        negative = self.metrics['negative_utterances']
        ratio = self.metrics['positive_negative_ratio']
        
        report.append(f"  • 긍정적 발화: {positive}회")
        report.append(f"  • 부정적 발화: {negative}회")
        report.append(f"  • 긍정/부정 비율: {ratio:.2f}")
        
        if ratio >= 1.5:
            emotion_score = "5점 (매우 긍정적)"
        elif ratio >= 1.0:
            emotion_score = "4점 (긍정적)"
        elif ratio >= 0.7:
            emotion_score = "3점 (중립)"
        elif ratio >= 0.5:
            emotion_score = "2점 (다소 부정적)"
        else:
            emotion_score = "1점 (부정적)"
        
        report.append(f"  • 정서 상태 점수: {emotion_score}")
        report.append("")
        
        # 정서 키워드 상세
        emotion_kw = self.metrics.get('emotion_keywords', {})
        positive_words = emotion_kw.get('positive', [])
        negative_words = emotion_kw.get('negative', [])
        
        if positive_words:
            report.append("  • 긍정 정서 키워드 (빈도순):")
            for word, count in positive_words[:10]:
                report.append(f"     - '{word}': {count}회")
            report.append("")
        
        if negative_words:
            report.append("  • 부정 정서 키워드 (빈도순):")
            for word, count in negative_words[:10]:
                report.append(f"     - '{word}': {count}회")
            report.append("")
        
        # 주제 분석
        report.append("【주제 및 관심사 분석】")
        report.append("━" * 70)
        
        topics = self.metrics.get('main_topics', [])
        if topics:
            report.append("  주요 키워드 (빈도순 TOP 20):")
            for i, (topic, count) in enumerate(topics, 1):
                percentage = count / self.metrics['child_word_count'] * 100 if self.metrics['child_word_count'] > 0 else 0
                report.append(f"     {i:2d}. {topic:10s} - {count:3d}회 ({percentage:.1f}%)")
            report.append("")
        
        # 놀이 영역 분포
        topic_dist = context_switches.get('topic_distribution', {})
        if topic_dist:
            report.append("  놀이 영역 분포:")
            total_topics = sum(topic_dist.values())
            for topic, count in sorted(topic_dist.items(), key=lambda x: -x[1]):
                percentage = count / total_topics * 100
                bar = "█" * int(percentage / 2)
                report.append(f"     {topic:10s} [{bar:<50s}] {percentage:5.1f}%")
            report.append("")
        
        # 시간대별 분석
        report.append("【시간대별 상세 분석】")
        report.append("━" * 70)
        
        segments = self.metrics.get('time_segments', [])
        if segments:
            report.append("  시간대      전체    아동    교사    아동비율")
            report.append("  " + "-" * 50)
            
            for seg in segments:
                time_range = f"{seg['start_time']}-{seg['end_time']}"
                report.append(
                    f"  {time_range:10s}  {seg['total_utterances']:4d}   "
                    f"{seg['child_utterances']:4d}   {seg['teacher_utterances']:4d}   "
                    f"{seg['child_ratio']:6.1%}"
                )
            
            report.append("")
            
            # 시간대별 트렌드 분석
            ratios = [seg['child_ratio'] for seg in segments]
            avg_ratio = np.mean(ratios)
            std_ratio = np.std(ratios)
            
            report.append("  시간대별 트렌드:")
            report.append(f"     • 평균 아동 참여율: {avg_ratio:.1%}")
            report.append(f"     • 표준편차: {std_ratio:.2f}")
            
            if std_ratio < 0.1:
                trend = "매우 안정적 (일관된 참여)"
            elif std_ratio < 0.2:
                trend = "안정적"
            else:
                trend = "변동 큼 (참여도 편차 존재)"
            
            report.append(f"     • 평가: {trend}")
            report.append("")
        
        # 교육 품질 지표
        report.append("【교육 품질 지표】")
        report.append("━" * 70)
        
        # 종합 점수 계산
        scores = {}
        
        # 1. 아동 주도성 (0-100점)
        child_lead_score = min(self.metrics['child_utterance_ratio'] * 2 * 100, 100)
        scores['아동 주도성'] = child_lead_score
        
        # 2. 언어 표현력 (0-100점)
        expression_score = min(self.metrics['child_avg_words_per_utterance'] / 5 * 100, 100)
        scores['언어 표현력'] = expression_score
        
        # 3. 인지 참여도 (0-100점)
        cognitive_score = min(ps_child / 50 * 100, 100)
        scores['인지 참여도'] = cognitive_score
        
        # 4. 정서 안정성 (0-100점)
        emotion_score_val = min(ratio / 1.5 * 100, 100)
        scores['정서 안정성'] = emotion_score_val
        
        # 5. 집중도 (0-100점)
        focus_score = min(persistence / 3.0 * 100, 100)
        scores['집중도'] = focus_score
        
        # 종합 점수
        total_score = np.mean(list(scores.values()))
        
        for metric, score in scores.items():
            bar = "█" * int(score / 2)
            report.append(f"  {metric:12s} [{bar:<50s}] {score:5.1f}점")
        
        report.append("  " + "-" * 66)
        bar = "█" * int(total_score / 2)
        report.append(f"  {'종합 점수':12s} [{bar:<50s}] {total_score:5.1f}점")
        report.append("")
        
        # 종합 평가
        if total_score >= 80:
            grade = "A+ (매우 우수)"
        elif total_score >= 70:
            grade = "A (우수)"
        elif total_score >= 60:
            grade = "B (양호)"
        elif total_score >= 50:
            grade = "C (보통)"
        else:
            grade = "D (개선 필요)"
        
        report.append(f"  종합 등급: {grade}")
        report.append("")
        
        # 개선 권장 사항
        report.append("【데이터 기반 개선 권장 사항】")
        report.append("━" * 70)
        
        improvements = []
        
        if scores['아동 주도성'] < 60:
            improvements.append({
                'priority': '높음',
                'area': '아동 주도성',
                'current': f"{scores['아동 주도성']:.1f}점",
                'recommendation': '교사 발화 감소, 개방형 질문 증가, 기다림의 시간 확보'
            })
        
        if scores['인지 참여도'] < 60:
            improvements.append({
                'priority': '높음',
                'area': '인지 참여도',
                'current': f"{scores['인지 참여도']:.1f}점",
                'recommendation': '문제해결 상황 제시, 탐구 활동 확대, 프로젝트 기반 학습'
            })
        
        if scores['정서 안정성'] < 60:
            improvements.append({
                'priority': '중간',
                'area': '정서 안정성',
                'current': f"{scores['정서 안정성']:.1f}점",
                'recommendation': '긍정적 강화 증대, 정서 인식 활동, 안정적 관계 형성'
            })
        
        if scores['집중도'] < 60:
            improvements.append({
                'priority': '중간',
                'area': '집중도',
                'current': f"{scores['집중도']:.1f}점",
                'recommendation': '활동 확장 기회 제공, 심화 활동 준비, 적절한 도전 과제'
            })
        
        if not improvements:
            report.append("  ✓ 모든 영역에서 양호한 수준을 보이고 있습니다.")
        else:
            report.append(f"  총 {len(improvements)}개 영역 개선 권장\n")
            for i, imp in enumerate(improvements, 1):
                report.append(f"  [{imp['priority']}] {imp['area']} (현재: {imp['current']})")
                report.append(f"     → {imp['recommendation']}")
                report.append("")
        
        # 푸터
        report.append("━" * 70)
        report.append(f"리포트 생성: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("본 리포트는 내부 분석용으로 외부 공유를 금합니다.")
        report.append("")
        
        return '\n'.join(report)
    
    def _format_date(self, date_str: str) -> str:
        """날짜 포맷팅 (20251017 -> 2025년 10월 17일)"""
        if len(date_str) == 8:
            year = date_str[:4]
            month = date_str[4:6]
            day = date_str[6:8]
            return f"{year}년 {int(month)}월 {int(day)}일"
        return date_str
    
    def save_all_reports(self, output_dir: str = 'reports'):
        """모든 레포트를 파일로 저장"""
        os.makedirs(output_dir, exist_ok=True)
        
        session_name = f"{self.metadata['date']}-{self.metadata['teacher']}교사-{self.metadata['child']}-{self.metadata['age']}"
        
        # 부모용
        parent_report = self.generate_parent_report()
        parent_file = os.path.join(output_dir, f"{session_name}_parent_report.txt")
        with open(parent_file, 'w', encoding='utf-8') as f:
            f.write(parent_report)
        print(f"✅ 부모용 레포트: {parent_file}")
        
        # 선생님용
        teacher_report = self.generate_teacher_report()
        teacher_file = os.path.join(output_dir, f"{session_name}_teacher_report.txt")
        with open(teacher_file, 'w', encoding='utf-8') as f:
            f.write(teacher_report)
        print(f"✅ 선생님용 레포트: {teacher_file}")
        
        # 방문일지
        journal = self.generate_visit_journal()
        journal_file = os.path.join(output_dir, f"{session_name}_visit_journal.txt")
        with open(journal_file, 'w', encoding='utf-8') as f:
            f.write(journal)
        print(f"✅ 방문일지: {journal_file}")
        
        # 회사용
        company_report = self.generate_company_report()
        company_file = os.path.join(output_dir, f"{session_name}_company_report.txt")
        with open(company_file, 'w', encoding='utf-8') as f:
            f.write(company_report)
        print(f"✅ 회사용 레포트: {company_file}")
        
        return {
            'parent': parent_file,
            'teacher': teacher_file,
            'journal': journal_file,
            'company': company_file
        }


if __name__ == '__main__':
    # 테스트
    analysis_file = '/Users/healin/Downloads/develop/care-intell/analysis_results/20251017-이민정교사-김준우-만4세-02_00_48-65kbps_mono_enhanced_analysis.json'
    
    generator = ReportGenerator(analysis_file)
    
    print("\n" + "="*70)
    print("📝 레포트 생성 중...")
    print("="*70 + "\n")
    
    files = generator.save_all_reports()
    
    print("\n" + "="*70)
    print("✅ 모든 레포트 생성 완료!")
    print("="*70)

