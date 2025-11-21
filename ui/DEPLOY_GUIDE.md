# 놀이 레포트 웹페이지 배포 가이드

## 방법 1: GitHub Pages (무료, 추천!)

### 준비물
- GitHub 계정
- Git 설치

### 단계별 가이드

#### 1단계: GitHub 저장소 만들기
```bash
# 터미널에서 실행
cd /Users/healin/Downloads/develop/care-intell
git init
git add .
git commit -m "놀이 레포트 시스템 초기 커밋"
```

#### 2단계: GitHub에 저장소 생성
1. https://github.com 접속
2. 우측 상단 '+' → 'New repository' 클릭
3. Repository name: `care-intell` (원하는 이름)
4. Public 선택
5. 'Create repository' 클릭

#### 3단계: GitHub에 푸시
```bash
# GitHub에서 알려준 주소로 연결 (예시)
git remote add origin https://github.com/YOUR_USERNAME/care-intell.git
git branch -M main
git push -u origin main
```

#### 4단계: GitHub Pages 활성화
1. GitHub 저장소 페이지에서 'Settings' 클릭
2. 좌측 메뉴에서 'Pages' 클릭
3. Source: 'Deploy from a branch' 선택
4. Branch: `main` 선택, 폴더: `/ui` 선택
5. 'Save' 클릭

#### 5단계: 접속
- 약 1-2분 후 `https://YOUR_USERNAME.github.io/care-intell/report_preview.html`로 접속 가능!

---

## 방법 2: Vercel (무료, 더 빠름)

### 단계별 가이드

#### 1단계: Vercel 계정 만들기
- https://vercel.com 접속
- GitHub 계정으로 로그인

#### 2단계: 프로젝트 import
1. 'Add New' → 'Project' 클릭
2. GitHub 저장소 연결
3. `care-intell` 저장소 선택
4. 'Deploy' 클릭

#### 3단계: 설정 (선택사항)
- Root Directory: `ui` 로 설정하면 바로 접속 가능

#### 4단계: 접속
- `https://care-intell.vercel.app/report_preview.html` 형식으로 자동 생성!

---

## 방법 3: Netlify (무료, 드래그앤드롭)

### 가장 쉬운 방법!

1. https://netlify.com 접속
2. 'Sites' → 'Add new site' → 'Deploy manually' 클릭
3. `/Users/healin/Downloads/develop/care-intell/ui` 폴더를 드래그앤드롭
4. 완료! 자동으로 URL 생성됨
   - 예: `https://random-name.netlify.app/report_preview.html`

---

## 방법 4: 직접 서버 (회사 서버가 있다면)

### 단순 HTML 호스팅

```bash
# Python 간이 서버 (테스트용)
cd /Users/healin/Downloads/develop/care-intell/ui
python3 -m http.server 8000

# 접속: http://localhost:8000/report_preview.html
```

### Nginx 설정 (프로덕션)
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    root /path/to/care-intell/ui;
    index report_preview.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
```

---

## 주의사항 ⚠️

### 1. 이미지 경로 수정 필요
현재 `report_preview.html`에서:
```html
<img src="../째깍악어-로고.png" alt="째깍악어" class="logo" />
```

웹 배포 시:
```html
<img src="./째깍악어-로고.png" alt="째깍악어" class="logo" />
```

또는 로고를 `ui/` 폴더 안으로 복사:
```bash
cp /Users/healin/Downloads/develop/care-intell/째깍악어-로고.png \
   /Users/healin/Downloads/develop/care-intell/ui/째깍악어-로고.png
```

### 2. CSS 경로 확인
```html
<!-- 현재 -->
<link rel="stylesheet" href="report_preview.css" />
<!-- 이건 그대로 OK! -->
```

---

## 추천 순서

1. **급하다면**: Netlify 드래그앤드롭 (5분)
2. **회사 프로젝트**: GitHub Pages (10분)
3. **자동 배포 원한다면**: Vercel (15분)
4. **자체 서버 있다면**: 직접 호스팅

---

## 다음 단계 제안

배포 후 고려할 사항:
- 🔒 비밀번호 보호 (샘플이지만 내부용이라면)
- 📱 모바일 반응형 최적화
- 🔗 커스텀 도메인 연결 (예: report.care-intell.com)
- 📊 방문자 통계 (Google Analytics)

---

필요하시면 제가 바로 배포 준비를 도와드릴게요!
어떤 방법을 원하시나요?

