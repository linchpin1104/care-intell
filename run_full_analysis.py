"""
전체 분석 및 레포트 생성 워크플로우
- VTT 파일 분석
- 지표 계산
- 3가지 레포트 + 방문일지 생성
"""

import os
import sys
from datetime import datetime
from enhanced_analysis import analyze_session
from report_generator import ReportGenerator


def run_full_pipeline(session_path: str, output_base_dir: str = None):
    """
    전체 파이프라인 실행
    
    Args:
        session_path: 세션 폴더 경로
        output_base_dir: 출력 디렉토리 (기본값: 프로젝트 루트)
    """
    if output_base_dir is None:
        output_base_dir = os.path.dirname(os.path.abspath(__file__))
    
    session_name = os.path.basename(session_path)
    
    print("\n" + "="*70)
    print(f"🚀 전체 분석 파이프라인 시작")
    print("="*70)
    print(f"📁 세션: {session_name}")
    print(f"📂 출력 경로: {output_base_dir}")
    print("="*70 + "\n")
    
    # Step 1: 분석 실행
    print("【STEP 1】 데이터 분석 중...")
    print("-" * 70)
    
    try:
        analysis_dir = os.path.join(output_base_dir, 'analysis_results')
        analyzer, analysis_file = analyze_session(session_path, analysis_dir)
        print(f"✅ 분석 완료: {analysis_file}\n")
    except Exception as e:
        print(f"❌ 분석 실패: {e}")
        return None
    
    # Step 2: 레포트 생성
    print("【STEP 2】 레포트 생성 중...")
    print("-" * 70)
    
    try:
        reports_dir = os.path.join(output_base_dir, 'reports')
        generator = ReportGenerator(analysis_file)
        report_files = generator.save_all_reports(reports_dir)
        print()
    except Exception as e:
        print(f"❌ 레포트 생성 실패: {e}")
        return None
    
    # Step 3: 요약
    print("\n【STEP 3】 완료 요약")
    print("="*70)
    print("\n📊 생성된 파일:")
    print(f"  1. 분석 데이터: {analysis_file}")
    print(f"  2. 부모용 레포트: {report_files['parent']}")
    print(f"  3. 선생님용 레포트: {report_files['teacher']}")
    print(f"  4. 방문일지: {report_files['journal']}")
    print(f"  5. 회사용 레포트: {report_files['company']}")
    
    print("\n📈 핵심 지표:")
    metrics = analyzer.analysis_results
    print(f"  • 아동 발화 비율: {metrics['child_utterance_ratio']:.1%}")
    print(f"  • 아동 발화 수: {metrics['child_utterance_count']}회")
    print(f"  • 평균 발화 길이: {metrics['child_avg_words_per_utterance']:.1f} 단어")
    print(f"  • 문제해결 발화: {metrics['problem_solving_utterances']['child_count']}회")
    print(f"  • 주제 지속도: {metrics['topic_persistence']:.2f}")
    print(f"  • 긍정/부정 비율: {metrics['positive_negative_ratio']:.2f}")
    
    print("\n" + "="*70)
    print("✨ 모든 작업이 완료되었습니다!")
    print("="*70 + "\n")
    
    return {
        'analysis_file': analysis_file,
        'reports': report_files,
        'metrics': metrics
    }


def batch_process_sessions(raw_data_dir: str, output_base_dir: str = None, limit: int = None):
    """
    여러 세션 일괄 처리
    
    Args:
        raw_data_dir: raw_data 디렉토리 경로
        output_base_dir: 출력 디렉토리
        limit: 처리할 세션 수 제한 (None이면 전체)
    """
    if output_base_dir is None:
        output_base_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("\n" + "="*70)
    print("🔄 일괄 처리 모드")
    print("="*70 + "\n")
    
    # 세션 폴더 찾기
    sessions = []
    for item in os.listdir(raw_data_dir):
        item_path = os.path.join(raw_data_dir, item)
        if os.path.isdir(item_path) and not item.endswith('.zip'):
            # VTT 폴더가 있는지 확인
            vtt_path = os.path.join(item_path, 'vtt')
            if os.path.exists(vtt_path):
                sessions.append(item_path)
    
    sessions.sort()
    
    if limit:
        sessions = sessions[:limit]
    
    print(f"📦 발견된 세션: {len(sessions)}개")
    if limit:
        print(f"📝 처리할 세션: {limit}개\n")
    else:
        print(f"📝 모든 세션을 처리합니다.\n")
    
    results = []
    success_count = 0
    fail_count = 0
    
    for i, session_path in enumerate(sessions, 1):
        session_name = os.path.basename(session_path)
        
        print(f"\n{'▶'*3} [{i}/{len(sessions)}] {session_name}")
        print("-" * 70)
        
        try:
            result = run_full_pipeline(session_path, output_base_dir)
            if result:
                results.append({
                    'session': session_name,
                    'status': 'success',
                    'result': result
                })
                success_count += 1
            else:
                results.append({
                    'session': session_name,
                    'status': 'failed',
                    'result': None
                })
                fail_count += 1
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            results.append({
                'session': session_name,
                'status': 'error',
                'error': str(e)
            })
            fail_count += 1
    
    # 최종 요약
    print("\n" + "="*70)
    print("🏁 일괄 처리 완료")
    print("="*70)
    print(f"\n총 {len(sessions)}개 세션 처리:")
    print(f"  ✅ 성공: {success_count}개")
    print(f"  ❌ 실패: {fail_count}개")
    
    if fail_count > 0:
        print("\n실패한 세션:")
        for r in results:
            if r['status'] != 'success':
                print(f"  • {r['session']}: {r.get('error', '알 수 없는 오류')}")
    
    print("\n" + "="*70 + "\n")
    
    return results


def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description='놀이 세션 분석 및 레포트 생성')
    parser.add_argument('--session', type=str, help='단일 세션 폴더 경로')
    parser.add_argument('--batch', action='store_true', help='일괄 처리 모드')
    parser.add_argument('--raw-data-dir', type=str, 
                       default='/Users/healin/Downloads/develop/care-intell/raw_data',
                       help='raw_data 디렉토리 경로')
    parser.add_argument('--output-dir', type=str, help='출력 디렉토리')
    parser.add_argument('--limit', type=int, help='처리할 세션 수 제한')
    
    args = parser.parse_args()
    
    if args.session:
        # 단일 세션 처리
        run_full_pipeline(args.session, args.output_dir)
    elif args.batch:
        # 일괄 처리
        batch_process_sessions(args.raw_data_dir, args.output_dir, args.limit)
    else:
        # 기본: 첫 번째 세션 처리 (테스트)
        session_path = '/Users/healin/Downloads/develop/care-intell/raw_data/20251017-이민정교사-김준우-만4세-02_00_48-65kbps_mono'
        run_full_pipeline(session_path)


if __name__ == '__main__':
    main()




