# 🌲 모여봐요 약속의 숲 (MeetWhen) - 약속 날짜 조율 웹앱

> **"언제 만날까?" 더 이상 카톡에서 헤매지 마세요!**  
> 친구들과 모임 날짜를 빠르고 직관적으로 투표하고, 최적의 참석 날짜를 자동으로 계산해 주는 웹 애플리케이션입니다.

![MeetWhen Preview](https://img.shields.io/badge/License-MIT-blue.svg)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-06B6D4?style=flat&logo=tailwindcss&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)

---

## ✨ 주요 기능 (Key Features)

- 🗓️ **후보 날짜 자유 지정**: 약속 생성자가 달력 UI에서 원하는 후보 날짜들을 다중 클릭하여 선택
- 🙋‍♂️ **참가자 3단계 투표**: `🟢 가능` / `🟡 세모 (조율 필요)` / `🔴 불가` 로 세분화하여 일정 투표
- 👑 **최적 추천 날짜 1위 산출**: 참석 인원 및 가중치를 계산하여 가장 완벽한 날짜를 자동으로 찾고 폭죽(Confetti) 이펙트 제공
- 📊 **한눈에 보는 종합 일정 표 (Matrix & Heatmap)**: 전체 참가자의 투표 현황을 그리드 표 형태로 일목요연하게 비교
- 💬 **카카오톡 공유 텍스트 자동 생성**: 버튼 클릭 한 번으로 단톡방 공유용 투표 결과 요약문(`"1위: 8/28(금) - 4명 가능..."`) 클립보드 복사
- 💾 **로컬 데이터 보존 (LocalStorage)**: 별도 서버 없이 브라우저 내에 작성된 투표 및 결과가 안전하게 저장됨
- ⚡ **샘플 데이터 지원**: '샘플 모임 불러오기' 버튼으로 앱의 전체 기능을 1초 만에 테스트 가능

---

## 🚀 시작하기 & 사용 방법 (Getting Started)

### 1. 로컬에서 실행하기 (Local Development)
별도의 빌드 과정 없이 `index.html` 파일을 브라우저로 바로 열거나, 간단한 웹 서버로 실행할 수 있습니다.

```bash
# Python 웹 서버로 실행 (포트 8080)
python3 -m http.server 8080
```
접속 주소: `http://localhost:8080`

---

## 🌐 깃허브 페이지(GitHub Pages) 무료 호스팅 방법

이 프로젝트는 단일 static 웹앱이므로 **GitHub Pages**를 활용하면 서버 비용 전혀 없이 무료로 웹 주소를 만들어 친구들에게 공유할 수 있습니다.

1. 이 저장소를 GitHub에 푸시합니다 (`git push origin main`).
2. GitHub 저장소 페이지의 **[Settings] ➔ [Pages]** 탭으로 이동합니다.
3. **Build and deployment ➔ Source**를 `Deploy from a branch`로 설정합니다.
4. **Branch**를 `main` (또는 `master`) / `/ (root)` 로 선택 후 **[Save]**를 누릅니다.
5. 1~2분 후 `https://<사용자이름>.github.io/<저장소이름>` 형태의 나만의 공유 웹 링크가 완성됩니다!

---

## 🛠️ 기술 스택 (Tech Stack)

- **Frontend**: HTML5, Vanilla JavaScript (ES6+)
- **Styling**: Tailwind CSS (CDN), Custom Glassmorphism UI
- **Icons & UI**: Lucide Icons
- **Animation**: Canvas Confetti
- **Storage**: Browser LocalStorage

---

## 📄 라이선스 (License)

This project is licensed under the [MIT License](LICENSE).
