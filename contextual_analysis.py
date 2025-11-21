"""
맥락 기반 대화 분석 시스템
- VTT 파일의 의미적 분석
- AI 기반 대화 내용 요약 및 발달적 순간 추출
- 계층적 요약 (청크 → 전체)
"""

import os
import json
import re
from typing import List, Dict, Any
from datetime import datetime


class ContextualDialogueAnalyzer:
    """맥락 기반 대화 분석기"""
    
    def __init__(self, session_path: str):
        """
        Args:
            session_path: 세션 폴더 경로
        """
        self.session_path = session_path
        self.session_name = os.path.basename(session_path)
        self.vtt_path = os.path.join(session_path, 'vtt')
        
        # 메타데이터 파싱
        self.metadata = self._parse_session_name()
        
        # 대화 데이터
        self.dialogues = []
        self.chunk_summaries = []
        self.final_summary = {}
    
    def _parse_session_name(self) -> Dict[str, str]:
        """세션 이름에서 메타데이터 추출"""
        parts = self.session_name.split('-')
        return {
            'date': parts[0] if len(parts) > 0 else '',
            'teacher': parts[1].replace('교사', '') if len(parts) > 1 else '',
            'child': parts[2] if len(parts) > 2 else '',
            'age': parts[3] if len(parts) > 3 else '',
        }
    
    def load_vtt_files(self, chunk_minutes: int = 10) -> List[Dict[str, Any]]:
        """
        VTT 파일들을 청크 단위로 묶어서 로드
        
        Args:
            chunk_minutes: 청크 크기 (분 단위)
        
        Returns:
            청크별 대화 리스트
        """
        print(f"📂 VTT 파일 로드 중: {self.vtt_path}")
        
        # VTT 파일 목록 (후처리된 파일 우선)
        vtt_files = []
        for filename in sorted(os.listdir(self.vtt_path)):
            if filename.endswith('.vtt'):
                # 시간 정보 추출 (예: 010-012분)
                time_match = re.search(r'(\d{3})-(\d{3})분', filename)
                if time_match:
                    start_min = int(time_match.group(1))
                    end_min = int(time_match.group(2))
                    
                    # 우선순위: 후처리됨 > subtitle > 미처리
                    if '_후처리됨' in filename:
                        priority = 3
                    elif '_subtitle.vtt' in filename and '_미처리' not in filename and '_후처리됨' not in filename:
                        priority = 2
                    elif '_미처리' in filename:
                        priority = 1
                    else:
                        priority = 2  # 기본값
                    
                    vtt_files.append({
                        'filename': filename,
                        'start_min': start_min,
                        'end_min': end_min,
                        'priority': priority
                    })
        
        # 중복 제거 (후처리 우선)
        time_slots = {}
        for vtt in vtt_files:
            key = (vtt['start_min'], vtt['end_min'])
            if key not in time_slots or vtt['priority'] > time_slots[key]['priority']:
                time_slots[key] = vtt
        
        selected_files = sorted(time_slots.values(), key=lambda x: x['start_min'])
        
        # 청크로 그룹화
        chunks = []
        current_chunk = {
            'start_min': 0,
            'end_min': chunk_minutes,
            'dialogues': []
        }
        
        for vtt in selected_files:
            filepath = os.path.join(self.vtt_path, vtt['filename'])
            
            # VTT 파일 읽기
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 대화 추출
            dialogues = self._parse_vtt_content(content)
            
            # 청크에 추가
            if vtt['start_min'] < current_chunk['end_min']:
                current_chunk['dialogues'].extend(dialogues)
            else:
                # 새 청크 시작
                if current_chunk['dialogues']:
                    chunks.append(current_chunk)
                current_chunk = {
                    'start_min': vtt['start_min'],
                    'end_min': vtt['start_min'] + chunk_minutes,
                    'dialogues': dialogues
                }
        
        # 마지막 청크 추가
        if current_chunk['dialogues']:
            chunks.append(current_chunk)
        
        print(f"✅ {len(selected_files)}개 파일을 {len(chunks)}개 청크로 그룹화")
        
        return chunks
    
    def _parse_vtt_content(self, content: str) -> List[Dict[str, Any]]:
        """VTT 내용 파싱"""
        dialogues = []
        
        pattern = r'(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})\s*\n\[(.*?)\]\s*(.*?)(?=\n\n|\Z)'
        matches = re.finditer(pattern, content, re.DOTALL)
        
        for match in matches:
            speaker = match.group(3).strip()
            text = match.group(4).strip()
            
            speaker_type = 'teacher' if '선생님' in speaker or '교사' in speaker else 'child'
            
            dialogues.append({
                'speaker': speaker,
                'speaker_type': speaker_type,
                'text': text
            })
        
        return dialogues
    
    def create_chunk_prompt(self, chunk: Dict[str, Any]) -> str:
        """청크 분석을 위한 프롬프트 생성"""
        
        dialogues_text = []
        for d in chunk['dialogues']:
            speaker_label = "선생님" if d['speaker_type'] == 'teacher' else "아이"
            dialogues_text.append(f"[{speaker_label}] {d['text']}")
        
        prompt = f"""다음은 {self.metadata['teacher']} 선생님과 {self.metadata['child']} 아동({self.metadata['age']})의 
{chunk['start_min']}-{chunk['end_min']}분 구간 놀이 대화입니다.

# 대화 내용
{chr(10).join(dialogues_text[:200])}  # 최대 200개 발화만

# 분석 요청
다음 관점에서 이 구간의 대화를 분석해주세요:

1. **주요 놀이 활동**: 어떤 놀이를 했나요?
2. **의미있는 상호작용**: 교육적으로 중요한 순간은?
3. **언어 발달 순간**: 특별한 언어 사용, 어휘 학습, 문장 구조 발달
4. **인지 발달 순간**: 문제해결, 탐구, 질문, 추론
5. **정서 사회성**: 감정 표현, 협력, 갈등 해결
6. **핵심 에피소드**: 가장 인상적인 장면 1-2개 (구체적 대화 인용)

간결하게 요약해주세요 (300자 이내).
"""
        
        return prompt
    
    def analyze_chunk_with_ai(self, chunk: Dict[str, Any]) -> Dict[str, Any]:
        """
        청크를 AI로 분석 (실제로는 API 호출)
        
        현재는 프롬프트만 생성하고, 실제 API 호출은 별도 구현 필요
        """
        prompt = self.create_chunk_prompt(chunk)
        
        # TODO: 실제 Claude API 호출
        # response = anthropic.messages.create(...)
        
        # 지금은 구조만 반환
        return {
            'time_range': f"{chunk['start_min']}-{chunk['end_min']}분",
            'prompt': prompt,
            'dialogue_count': len(chunk['dialogues']),
            # 'ai_summary': response.content  # 실제 API 응답
        }
    
    def generate_prompts_for_manual_analysis(self, output_dir: str = 'contextual_prompts'):
        """
        수동 분석을 위한 프롬프트 파일 생성
        (API 키 없이도 사용 가능하도록)
        """
        os.makedirs(output_dir, exist_ok=True)
        
        chunks = self.load_vtt_files(chunk_minutes=10)
        
        prompts = []
        for i, chunk in enumerate(chunks, 1):
            analysis = self.analyze_chunk_with_ai(chunk)
            prompts.append(analysis)
            
            # 개별 프롬프트 파일 저장
            prompt_file = os.path.join(
                output_dir, 
                f"{self.session_name}_chunk{i:02d}_{analysis['time_range']}.txt"
            )
            
            with open(prompt_file, 'w', encoding='utf-8') as f:
                f.write(analysis['prompt'])
                f.write("\n\n" + "="*70)
                f.write(f"\n발화 수: {analysis['dialogue_count']}개")
        
        # 통합 요약본
        summary_file = os.path.join(output_dir, f"{self.session_name}_all_prompts.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump({
                'session': self.session_name,
                'metadata': self.metadata,
                'total_chunks': len(prompts),
                'prompts': prompts
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ {len(prompts)}개 청크 프롬프트 생성 완료")
        print(f"📁 출력 폴더: {output_dir}")
        print(f"\n💡 사용 방법:")
        print(f"   1. 각 프롬프트 파일을 Claude/GPT에 수동으로 입력")
        print(f"   2. AI 응답을 받아서 저장")
        print(f"   3. 모든 요약을 통합하여 최종 분석")
        
        return prompts


def analyze_session_contextually(session_path: str, output_dir: str = 'contextual_prompts'):
    """세션의 맥락적 분석 프롬프트 생성"""
    
    print(f"\n{'='*70}")
    print(f"🎯 맥락 기반 분석 시작: {os.path.basename(session_path)}")
    print(f"{'='*70}\n")
    
    analyzer = ContextualDialogueAnalyzer(session_path)
    prompts = analyzer.generate_prompts_for_manual_analysis(output_dir)
    
    print(f"\n{'='*70}")
    print(f"✅ 완료!")
    print(f"{'='*70}\n")
    
    return prompts


if __name__ == '__main__':
    # 테스트 - 2시간 세션
    session_path = '/Users/healin/Downloads/develop/care-intell/raw_data/20251017-이민정교사-김준우-만4세-02_00_48-65kbps_mono'
    
    prompts = analyze_session_contextually(session_path)
    
    print(f"\n📊 생성된 프롬프트: {len(prompts)}개")
    
    if prompts:
        print(f"\n첫 번째 프롬프트 미리보기:")
        print("=" * 70)
        print(prompts[0]['prompt'][:500] + "...")
    else:
        print("\n⚠️ 프롬프트가 생성되지 않았습니다.")

