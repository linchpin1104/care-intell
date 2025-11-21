# 빠른 시작 가이드

## 🚀 5분 안에 시작하기

### 1단계: 환경 설정
```bash
cd /Users/healin/Downloads/develop/care-intell
pip install pandas
```

### 2단계: 샘플 분석 실행
```bash
# 단일 세션 분석
python3 analyze_play_session.py "raw_data/20251017-이민정교사-김준우-만4세-02_00_48-65kbps_mono"

# 레포트 생성
python3 generate_reports.py "analysis_results/20251017-이민정교사-김준우-만4세-02_00_48-65kbps_mono_analysis.json"
```

### 3단계: 결과 확인
```
reports/
├── 20251017-이민정교사-김준우-만4세-02_00_48-65kbps_mono_company_report.txt   # 회사용
├── 20251017-이민정교사-김준우-만4세-02_00_48-65kbps_mono_parent_report.txt    # 부모용
└── 20251017-이민정교사-김준우-만4세-02_00_48-65kbps_mono_teacher_report.txt   # 선생님용
```

---

## 🎯 주요 명령어

### 전체 세션 일괄 처리 (권장)
```bash
python3 batch_analyze.py
```
이 명령어 하나로:
- ✅ 모든 세션 분석
- ✅ 모든 레포트 생성  
- ✅ 비교 분석 리포트 생성

### 개별 작업
```bash
# 1. 단일 세션 분석만
python3 analyze_play_session.py "raw_data/[세션명]"

# 2. 기존 분석으로 레포트만 생성
python3 generate_reports.py "analysis_results/[세션명]_analysis.json"
```

---

## 📊 결과물 확인

### 분석 결과 (JSON)
```
analysis_results/
└── [세션명]_analysis.json    # 모든 지표 데이터
```

### 레포트 (TXT)
```
reports/
├── [세션명]_company_report.txt     # 회사용 (상세)
├── [세션명]_parent_report.txt      # 부모용 (쉬운 표현)
├── [세션명]_teacher_report.txt     # 선생님용 (교육적 제안)
├── comparison_report.txt            # 전체 비교 분석
└── comparison_report.csv            # 비교 데이터 (엑셀 가능)
```

---

## 💡 주요 지표 설명

| 지표 | 의미 | 좋은 범위 |
|------|------|----------|
| 아동발화비율 | 대화 참여도 | 45-60% |
| 평균발화길이 | 언어 표현력 | 15-25자 |
| 긍정비율 | 정서 안정성 | 60% 이상 |
| 어휘다양도 (TTR) | 어휘 풍부함 | 25-35% |
| 문제해결비율 | 인지 참여도 | 5-15% |

---

## 🔧 문제 해결

### pandas 설치 오류
```bash
pip3 install pandas
# 또는
python3 -m pip install pandas
```

### 파일 경로 오류
- 경로에 공백이나 특수문자가 있으면 따옴표로 감싸세요
- 예: `"raw_data/폴더명"`

### 분석 결과가 이상한 경우
- VTT 파일에 화자 태그가 있는지 확인
- 예: `[이민정 선생님]`, `[김준우 아이]`

---

## 📞 도움말

더 자세한 내용은 다음 문서를 참고하세요:
- `README.md`: 전체 시스템 설명
- `PROJECT_SUMMARY.md`: 프로젝트 요약
- 이미지 참고: 제공하신 지표 정의 표

---

**Happy Analyzing! 🎉**

