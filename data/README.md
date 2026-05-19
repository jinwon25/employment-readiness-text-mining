# data/

원본 게시글 텍스트가 포함되어 있어 본 저장소에서는 추적하지 않는다.
분석을 직접 재현하려면 동일 구조로 데이터를 채워야 한다.

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

## 재현 방법
1. `crawlers/에타_크롤링.py` 로 에브리타임 자유게시판 데이터 수집 → `raw/everytime_crawling*.csv`
2. `notebooks/구해줘_잡스_분석.ipynb` 전처리 셀로 raw → processed 변환
3. 토픽 모델링·감정 분석 노트북 순차 실행
