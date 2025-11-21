#!/usr/bin/env python3
"""
배치 분석 스크립트
- 여러 세션을 한 번에 분석
- 비교 리포트 생성
"""

import json
from pathlib import Path
from analyze_play_session import PlaySessionAnalyzer
from generate_reports import ReportGenerator
import pandas as pd
from datetime import datetime


def find_all_sessions(raw_data_dir):
    """모든 세션 디렉토리 찾기"""
    raw_data_path = Path(raw_data_dir)
    
    # vtt 폴더가 있는 디렉토리만 세션으로 인식
    sessions = []
    for item in raw_data_path.iterdir():
        if item.is_dir() and not item.name.endswith('.zip'):
            vtt_dir = item / "vtt"
            if vtt_dir.exists():
                sessions.append(item)
    
    return sorted(sessions)


def analyze_all_sessions(raw_data_dir="raw_data", output_dir="analysis_results"):
    """모든 세션 분석"""
    sessions = find_all_sessions(raw_data_dir)
    
    print(f"\n{'='*80}")
    print(f"🔍 총 {len(sessions)}개 세션 발견")
    print(f"{'='*80}\n")
    
    results = []
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    for i, session_dir in enumerate(sessions, 1):
        print(f"\n[{i}/{len(sessions)}] 분석 중: {session_dir.name}")
        print("-" * 80)
        
        try:
            # 분석 실행
            analyzer = PlaySessionAnalyzer(session_dir)
            analysis_file = output_path / f"{session_dir.name}_analysis.json"
            result = analyzer.save_analysis(analysis_file)
            results.append(result)
            
            print(f"✅ 완료: {session_dir.name}")
            
        except Exception as e:
            print(f"❌ 오류 발생: {session_dir.name}")
            print(f"   에러: {str(e)}")
            continue
    
    print(f"\n{'='*80}")
    print(f"✨ 전체 분석 완료! ({len(results)}/{len(sessions)} 성공)")
    print(f"{'='*80}\n")
    
    return results


def generate_all_reports(analysis_dir="analysis_results", report_dir="reports"):
    """모든 분석 결과에 대해 레포트 생성"""
    analysis_path = Path(analysis_dir)
    analysis_files = sorted(analysis_path.glob("*_analysis.json"))
    
    print(f"\n{'='*80}")
    print(f"📝 총 {len(analysis_files)}개 레포트 생성 시작")
    print(f"{'='*80}\n")
    
    for i, analysis_file in enumerate(analysis_files, 1):
        print(f"\n[{i}/{len(analysis_files)}] 레포트 생성 중: {analysis_file.stem}")
        print("-" * 80)
        
        try:
            generator = ReportGenerator(analysis_file)
            generator.save_all_reports(report_dir)
            print(f"✅ 완료")
            
        except Exception as e:
            print(f"❌ 오류 발생: {str(e)}")
            continue
    
    print(f"\n{'='*80}")
    print(f"✨ 전체 레포트 생성 완료!")
    print(f"{'='*80}\n")


def generate_comparison_report(analysis_dir="analysis_results"):
    """비교 리포트 생성"""
    analysis_path = Path(analysis_dir)
    analysis_files = sorted(analysis_path.glob("*_analysis.json"))
    
    print(f"\n{'='*80}")
    print(f"📊 비교 리포트 생성 중... ({len(analysis_files)}개 세션)")
    print(f"{'='*80}\n")
    
    # 데이터 수집
    comparison_data = []
    
    for analysis_file in analysis_files:
        with open(analysis_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        meta = data['meta_info']
        speech_ratio = data['speech_ratio']
        speech_amount = data['child_speech_amount']
        emotion = data['emotion_analysis']
        topics = data['topic_keywords']
        problem_solving = data['problem_solving']
        turn_taking = data['turn_taking']
        
        comparison_data.append({
            '세션명': meta['session_name'],
            '날짜': meta.get('date', 'N/A'),
            '선생님': meta.get('teacher_name', 'N/A'),
            '아동': meta.get('child_name', 'N/A'),
            '나이': meta.get('child_age', 'N/A'),
            '아동발화비율(%)': round(speech_ratio['child_speech_ratio'], 1),
            '아동발화횟수': speech_ratio['child_utterance_count'],
            '평균발화길이': round(speech_amount['avg_utterance_length'], 1),
            '긍정비율(%)': round(emotion['positive_ratio'], 1),
            '부정비율(%)': round(emotion['negative_ratio'], 1),
            '고유단어수': topics['unique_words'],
            '어휘다양도(%)': round(topics['unique_words'] / topics['total_words'] * 100, 1),
            '문제해결비율(%)': round(problem_solving['problem_solving_ratio'], 1),
            '총턴수': turn_taking['total_turns'],
            '턴균형도': round(turn_taking['turn_taking_balance'], 2)
        })
    
    # DataFrame 생성
    df = pd.DataFrame(comparison_data)
    
    # CSV 저장
    csv_file = Path("reports") / "comparison_report.csv"
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    print(f"✅ CSV 저장: {csv_file}")
    
    # 텍스트 리포트 생성
    report = f"""
{'='*100}
📊 전체 세션 비교 분석 리포트
{'='*100}

생성 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
분석 대상: 총 {len(comparison_data)}개 세션

{'='*100}
1️⃣  기본 통계
{'='*100}

총 세션 수: {len(comparison_data)}개
분석 기간: {df['날짜'].min()} ~ {df['날짜'].max()}
선생님 수: {df['선생님'].nunique()}명
아동 수: {df['아동'].nunique()}명

{'='*100}
2️⃣  아동 발화 분석
{'='*100}

📊 아동 발화 비율
  • 평균: {df['아동발화비율(%)'].mean():.1f}%
  • 최소: {df['아동발화비율(%)'].min():.1f}% ({df.loc[df['아동발화비율(%)'].idxmin(), '아동']})
  • 최대: {df['아동발화비율(%)'].max():.1f}% ({df.loc[df['아동발화비율(%)'].idxmax(), '아동']})
  • 표준편차: {df['아동발화비율(%)'].std():.1f}%

📝 평균 발화 길이
  • 평균: {df['평균발화길이'].mean():.1f}자
  • 최소: {df['평균발화길이'].min():.1f}자 ({df.loc[df['평균발화길이'].idxmin(), '아동']})
  • 최대: {df['평균발화길이'].max():.1f}자 ({df.loc[df['평균발화길이'].idxmax(), '아동']})

{'='*100}
3️⃣  감정 분석
{'='*100}

😊 긍정 비율
  • 평균: {df['긍정비율(%)'].mean():.1f}%
  • 최소: {df['긍정비율(%)'].min():.1f}% ({df.loc[df['긍정비율(%)'].idxmin(), '아동']})
  • 최대: {df['긍정비율(%)'].max():.1f}% ({df.loc[df['긍정비율(%)'].idxmax(), '아동']})

😔 부정 비율
  • 평균: {df['부정비율(%)'].mean():.1f}%
  • 최소: {df['부정비율(%)'].min():.1f}% ({df.loc[df['부정비율(%)'].idxmin(), '아동']})
  • 최대: {df['부정비율(%)'].max():.1f}% ({df.loc[df['부정비율(%)'].idxmax(), '아동']})

{'='*100}
4️⃣  인지 발달
{'='*100}

📚 어휘 다양도 (TTR)
  • 평균: {df['어휘다양도(%)'].mean():.1f}%
  • 최소: {df['어휘다양도(%)'].min():.1f}% ({df.loc[df['어휘다양도(%)'].idxmin(), '아동']})
  • 최대: {df['어휘다양도(%)'].max():.1f}% ({df.loc[df['어휘다양도(%)'].idxmax(), '아동']})

🧩 문제해결 발화
  • 평균: {df['문제해결비율(%)'].mean():.1f}%
  • 최소: {df['문제해결비율(%)'].min():.1f}% ({df.loc[df['문제해결비율(%)'].idxmin(), '아동']})
  • 최대: {df['문제해결비율(%)'].max():.1f}% ({df.loc[df['문제해결비율(%)'].idxmax(), '아동']})

{'='*100}
5️⃣  상위/하위 순위
{'='*100}

🏆 아동 발화 비율 상위 3명:
"""
    
    top_3_speech = df.nlargest(3, '아동발화비율(%)')
    for i, row in enumerate(top_3_speech.itertuples(), 1):
        report += f"  {i}. {row.아동} ({row.나이}) - {row.아동발화비율:}%\n"
    
    report += f"""
🏆 어휘 다양도 상위 3명:
"""
    
    top_3_vocab = df.nlargest(3, '어휘다양도(%)')
    for i, row in enumerate(top_3_vocab.itertuples(), 1):
        report += f"  {i}. {row.아동} ({row.나이}) - {row.어휘다양도:}%\n"
    
    report += f"""
🏆 문제해결 발화 상위 3명:
"""
    
    top_3_ps = df.nlargest(3, '문제해결비율(%)')
    for i, row in enumerate(top_3_ps.itertuples(), 1):
        report += f"  {i}. {row.아동} ({row.나이}) - {row.문제해결비율:}%\n"
    
    report += f"""
{'='*100}
6️⃣  나이별 비교
{'='*100}
"""
    
    age_groups = df.groupby('나이').agg({
        '아동발화비율(%)': 'mean',
        '평균발화길이': 'mean',
        '긍정비율(%)': 'mean',
        '어휘다양도(%)': 'mean',
        '문제해결비율(%)': 'mean'
    }).round(1)
    
    report += "\n" + age_groups.to_string()
    
    report += f"""

{'='*100}
7️⃣  선생님별 비교
{'='*100}
"""
    
    teacher_groups = df.groupby('선생님').agg({
        '아동발화비율(%)': 'mean',
        '평균발화길이': 'mean',
        '긍정비율(%)': 'mean',
        '어휘다양도(%)': 'mean',
        '문제해결비율(%)': 'mean',
        '아동': 'count'
    }).round(1)
    teacher_groups.columns = ['평균아동발화비율', '평균발화길이', '평균긍정비율', '평균어휘다양도', '평균문제해결비율', '세션수']
    
    report += "\n" + teacher_groups.to_string()
    
    report += f"""

{'='*100}
8️⃣  전체 평가
{'='*100}

✅ 전체적으로 아동들의 발화 참여도가 평균 {df['아동발화비율(%)'].mean():.1f}%로 양호합니다.
✅ 감정 표현이 긍정적인 경향을 보입니다 (평균 긍정 비율 {df['긍정비율(%)'].mean():.1f}%).
"""
    
    if df['문제해결비율(%)'].mean() < 5:
        report += "⚠️  전반적으로 문제해결 발화 비율이 낮으므로, 탐구 활동 강화가 필요합니다.\n"
    
    report += f"""
{'='*100}
🔚 레포트 끝
{'='*100}
"""
    
    # 텍스트 리포트 저장
    txt_file = Path("reports") / "comparison_report.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 텍스트 리포트 저장: {txt_file}")
    print(f"\n{report}")
    
    return df


def main():
    """메인 함수"""
    import sys
    
    print("\n" + "="*80)
    print("🚀 놀이 세션 배치 분석 시스템")
    print("="*80)
    
    # 1. 모든 세션 분석
    print("\n📍 단계 1: 세션 분석")
    analyze_all_sessions()
    
    # 2. 모든 레포트 생성
    print("\n📍 단계 2: 레포트 생성")
    generate_all_reports()
    
    # 3. 비교 리포트 생성
    print("\n📍 단계 3: 비교 분석")
    generate_comparison_report()
    
    print("\n" + "="*80)
    print("✨ 모든 작업 완료!")
    print("="*80)
    print("\n결과 확인:")
    print("  - 분석 결과: analysis_results/ 폴더")
    print("  - 개별 레포트: reports/ 폴더")
    print("  - 비교 리포트: reports/comparison_report.txt 및 .csv")
    print()


if __name__ == "__main__":
    main()

