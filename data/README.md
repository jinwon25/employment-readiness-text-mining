# data/

원본 게시글과 설문 자유응답에는 개인이 작성한 텍스트가 포함되어 있어 저장소에서 추적하지 않습니다. 공개 발표자료에 실린 비식별 집계 결과만 `derived/`에 제공합니다.

## 폴더 구조

### `raw/`
크롤링 원본·설문 응답 원본.

| 파일 | 설명 |
|---|---|
| `everytime_crawling.csv` | 에브리타임 자유게시판 크롤링 (검색어: 취업·진로 관련) |
| `everytime_crawling_200_졸업생.csv` | 졸업생 키워드 검색 결과 |
| `everytime_crawling_200_취업진로.csv` | 취업·진로 키워드 검색 결과 |
| `everytime_df.csv` | raw 3종 통합 + 전처리 결과 (content, comment, like, scrap, date, clean_text, morphs, tokens 등) |
| `설문조사_응답.csv` | 학술제 자체 설문조사 응답 원본 |

### `processed/`
모델링·시각화에 사용한 가공 산출물.

| 파일 | 설명 |
|---|---|
| `topic_df.csv` | LDA 토픽 모델링 결과 (date, topic_text) |
| `emotion_df.csv` | 감정 분석용 텍스트 통합 (date, emotion_text) |
| `감정분석_결과.csv` | 감정 분류 모델 추론 결과 |
| `수동_라벨링.csv` | 감정 라벨 수동 보정본 |
| `설문조사.csv` | 설문 응답 가공본 |

### `derived/`

| 파일 | 설명 |
|---|---|
| `reported_evidence.json` | 발표자료에 공개된 설문·텍스트·모델 집계 결과 |

## 데이터 사용 원칙

1. 계정 소유자의 접근 권한, 플랫폼 약관과 연구윤리를 먼저 확인합니다.
2. 로그인 정보와 원문 텍스트를 Git에 저장하지 않습니다.
3. 실제 게시글을 공개 예시로 그대로 인용하지 않습니다.
4. 게시글 단위 감정 점수를 작성자 개인의 심리 상태로 해석하지 않습니다.

## 원 분석 경로

1. 수집 권한이 있는 경우에만 `crawlers/에타_크롤링.py`로 원자료를 `raw/`에 저장합니다.
2. `notebooks/01_메인_분석.ipynb`의 전처리 흐름으로 `processed/` 데이터를 만듭니다.
3. 감정 분류는 `03_감정_분류.ipynb`, 부정 토픽은 `02_부정_토픽_모델링.ipynb`에서 확인합니다.

기존 노트북은 당시 Colab·로컬 절대경로를 포함한 분석 기록입니다. 공개 집계 결과는 원문 없이 실행되는 `notebooks/portfolio_summary.ipynb`에서 확인할 수 있습니다.
