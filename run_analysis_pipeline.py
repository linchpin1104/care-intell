"""
놀이 세션 분석 파이프라인
1. VTT 파일에서 대화 데이터 추출
2. 지표 분석 (발화비율, 주제, 감정 등)
3. 3가지 레포트 생성 (부모용, 선생님용, 회사용)
"""

import sys
from pathlib import Path
import json

# 로컬 모듈 임포트
from analyze_metrics import PlaySessionAnalyzer
from generate_reports_v2 import generate_all_reports


def run_full_analysis(session_path: str, output_dir: str = None):
    """전체 분석 파이프라인 실행"""
    
    session_path = Path(session_path)
    
    if not session_path.exists():
        print(f"❌ 세션 경로를 찾을 수 없습니다: {session_path}")
        return None
    
    print(f"\n{'='*70}")
    print(f"놀이 세션 분석 시작")
    print(f"{'='*70}")
    print(f"세션: {session_path.name}")
    print(f"{'='*70}\n")
    
    # Step 1: 지표 분석
    print("📊 Step 1: 지표 분석 중...")
    analyzer = PlaySessionAnalyzer(str(session_path))
    analysis_result = analyzer.analyze_all()
    
    # 분석 결과 저장
    if output_dir is None:
        output_dir = Path(__file__).parent / "analysis_results"
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(exist_ok=True)
    
    analysis_file = output_dir / f"{session_path.name}_detailed_analysis.json"
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_result, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 분석 결과 저장: {analysis_file}\n")
    
    # Step 2: 레포트 생성
    print("📝 Step 2: 레포트 생성 중...")
    reports_dir = Path(__file__).parent / "reports"
    generate_all_reports(str(analysis_file), str(reports_dir))
    
    print(f"\n{'='*70}")
    print(f"✅ 분석 완료!")
    print(f"{'='*70}")
    print(f"📂 분석 결과: {analysis_file}")
    print(f"📂 레포트: {reports_dir}/")
    print(f"  - {session_path.name}_parent_report.txt (부모용)")
    print(f"  - {session_path.name}_teacher_report.txt (선생님용)")
    print(f"  - {session_path.name}_company_report.txt (회사용)")
    print(f"{'='*70}\n")
    
    return analysis_result


def batch_analyze_all_sessions(raw_data_dir: str, output_dir: str = None):
    """모든 세션 일괄 분석"""
    
    raw_data_dir = Path(raw_data_dir)
    
    if not raw_data_dir.exists():
        print(f"❌ 디렉토리를 찾을 수 없습니다: {raw_data_dir}")
        return
    
    # 세션 디렉토리 찾기 (날짜로 시작하는 디렉토리)
    session_dirs = [d for d in raw_data_dir.iterdir() 
                   if d.is_dir() and d.name[0].isdigit() and len(d.name) > 8]
    
    print(f"\n발견된 세션 수: {len(session_dirs)}")
    print(f"{'='*70}\n")
    
    results = []
    for i, session_dir in enumerate(session_dirs, 1):
        print(f"\n[{i}/{len(session_dirs)}] {session_dir.name}")
        
        try:
            result = run_full_analysis(str(session_dir), output_dir)
            results.append({
                'session': session_dir.name,
                'status': 'success',
                'result': result
            })
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            results.append({
                'session': session_dir.name,
                'status': 'error',
                'error': str(e)
            })
    
    # 전체 요약
    print(f"\n{'='*70}")
    print("📊 일괄 분석 완료")
    print(f"{'='*70}")
    
    success_count = sum(1 for r in results if r['status'] == 'success')
    error_count = len(results) - success_count
    
    print(f"✓ 성공: {success_count}개")
    print(f"✗ 실패: {error_count}개")
    
    if error_count > 0:
        print("\n실패한 세션:")
        for r in results:
            if r['status'] == 'error':
                print(f"  - {r['session']}: {r['error']}")
    
    print(f"{'='*70}\n")
    
    return results


def main():
    """메인 함수"""
    
    if len(sys.argv) > 1:
        # 명령줄 인자로 세션 경로 지정
        session_path = sys.argv[1]
        
        if Path(session_path).is_dir() and not Path(session_path).name[0].isdigit():
            # raw_data 디렉토리가 전달된 경우 일괄 분석
            batch_analyze_all_sessions(session_path)
        else:
            # 특정 세션 분석
            run_full_analysis(session_path)
    else:
        # 기본: 샘플 세션 2개 분석
        raw_data_dir = Path(__file__).parent / "raw_data"
        
        sample_sessions = [
            "20251017-이민정교사-김준우-만4세-02_00_48-65kbps_mono",
            "20251021-임지우교사-송나윤3-만5세-00_21_23-63kbps_mono"
        ]
        
        print("샘플 세션 분석 실행")
        print("(전체 세션을 분석하려면: python run_analysis_pipeline.py <raw_data_dir>)")
        print()
        
        for session_name in sample_sessions:
            session_path = raw_data_dir / session_name
            if session_path.exists():
                run_full_analysis(str(session_path))
            else:
                print(f"⚠ 세션을 찾을 수 없습니다: {session_path}\n")


if __name__ == "__main__":
    main()

