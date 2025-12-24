# pianote implementation plan

피아노 음원 파일을 분석하여 미디 파일로 변환하고 최종적으로 악보를 생성하는 프로그램

## 주요 도구 및 라이브러리

- 언어: Python
- 엔진: Spotify Basic Pitch
- 오디오 처리: Librosa
- 파일 변환: Mido
- 악보 연동: music21, MusicXML

## SOTA 엔진 도입 (ByteDance)

정확도를 극한으로 높이기 위해 다음의 고해상도 모델들을 검토함:
- **ByteDance Piano Transcription**: 현재 피아노 독주 분야에서 전 세계 최고 수준의 정확도(Onset F1 score 96.7% 이상)를 자랑하며, 페달 정보까지 정교하게 추출함
