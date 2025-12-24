# Pianote (Audio/Video to MIDI)

AI 기반 피아노 음원 및 동영상 자동 변환 프로그램입니다. ByteDance의 SOTA(State-of-The-Art) 모델을 탑재하여 초정밀 미디 추출이 가능합니다.

## 주요 기능
- **고해상도 변환**: 화음 및 페달링 정보가 포함된 고화질 MIDI 추출
- **동영상 지원**: 영상 파일에서 자동으로 음원을 추출하여 변환
- **웹 인터페이스**: 브라우저 기반의 직관적인 업로드 및 다운로드 시스템

## 지원되는 파일 형식

### 오디오 (Audio)
- `.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg`, `.aiff`

### 동영상 (Video)
- `.mp4`, `.mov`, `.avi`, `.mkv`, `.wmv`, `.flv`, `.webm`

## 실행 방법

1. 의존성 라이브러리 설치:
   ```bash
   pip install -r requirements.txt
   ```
2. 서버 실행:
   ```bash
   python app.py
   ```
3. 브라우저 접속:
   - `http://127.0.0.1:5000`

## 주의사항
- 첫 실행 시 SOTA 모델 파일(약 165MB)이 준비되어 있어야 합니다.
- 고해상도 연산을 위해 CPU 성능에 따라 변환에 수십 초~수 분이 소요될 수 있습니다.

---
© 2025 Pianote Project
