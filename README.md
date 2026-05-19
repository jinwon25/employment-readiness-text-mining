# 대학생 취업 준비 실태 텍스트 마이닝 — 구해줘! 잡스

에브리타임 자유게시판 크롤링과 자체 설문조사를 결합해 대학생의 취업 준비
실태를 텍스트 마이닝으로 분석한 프로젝트. LDA 토픽 모델링과 KoBERT 기반
감정 분류로 학생들이 실제로 어떤 고민을 하고 있는지 추출하고, 학내 취업
지원 방안을 정량적 근거 위에서 제안.

## 진행 기간
2025.04 ~ 2025.06 — 2025 중앙대학교 경영경제대학 학술제 출품작 (팀명: 구해줘! 잡스)

## 역할
팀 프로젝트 — 크롤링·전처리·토픽 모델링·감정 분류·시각화·보고서 작성 흐름 수행

## 데이터
| 데이터 | 규모 | 비고 |
|---|---|---|
| 에브리타임 크롤링 (취업·진로·졸업생 키워드) | 3종 raw csv | 자유게시판 본문·댓글·추천·스크랩 |
| 통합 게시글 + 전처리 결과 | `everytime_df.csv` | 형태소 분석 후 토큰화 완료 |
| 자체 설문조사 응답 | csv | 학술제용 학내 설문 |

> ⚠️ 원본 게시글은 익명이지만 학생 개인 작성 텍스트라 본 저장소에는
> 포함하지 않는다. 구조와 재현 방법은 [`data/README.md`](./data/README.md) 참고.

## 분석 흐름

| 단계 | 노트북 | 내용 |
|---|---|---|
| 0 | `notebooks/00_1차_데이터_탐색.ipynb` | 초기 데이터 점검 |
| 1 | `notebooks/01_메인_분석.ipynb` | 162셀 — 크롤링·전처리·LDA·EDA·가설검정·감정 모델링 |
| 2 | `notebooks/02_부정_토픽_모델링.ipynb` | 부정 감정 게시글에 한정해 별도 LDA |
| 3 | `notebooks/03_감정_분류.ipynb` | KoBERT / kcbert-large 분류기 학습·추론 |

### 검정한 가설 6개
1. 요일별 부정 감정 비율 차이
2. 지역별 부정 감정 비율 차이
3. 시간대별 부정 감정 비율 차이
4. 부정 글과 긍정 글의 단어 사용 차이
5. 본문과 댓글 사이의 단어 사용 차이
6. 추천 받은 글과 일반 글의 단어 사용 차이

## 기술 스택
| 영역 | 도구 |
|---|---|
| 크롤링 | selenium, chromedriver-autoinstaller, beautifulsoup4 |
| 한국어 NLP | KoNLPy, MeCab |
| 토픽 모델링 | gensim (LDA), pyLDAvis |
| 감정 분류 | scikit-learn (TF-IDF + 전통 분류기), HuggingFace transformers (KoBERT, beomi/kcbert-large), PyTorch |
| 시각화 | matplotlib, seaborn, wordcloud, pyLDAvis |
| 데이터 처리 | pandas, numpy |

## 산출물
- 메인 보고서: [`reports/구해줘_잡스.pdf`](./reports/구해줘_잡스.pdf)
- 원페이지 요약: [`reports/원페이지_보고서.pdf`](./reports/원페이지_보고서.pdf)
- 학술제 참가 보고서: [`reports/구해줘_잡스_참가보고서.hwp`](./reports/구해줘_잡스_참가보고서.hwp)
- LDA 토픽 시각화 (전체): [`reports/토픽_모델링_시각화.html`](./reports/토픽_모델링_시각화.html)
- LDA 토픽 시각화 (부정 감정): [`reports/부정_토픽_모델링_시각화.html`](./reports/부정_토픽_모델링_시각화.html)
- 학술제 공고: [`docs/공고_2025_경영경제대학_학술제.pdf`](./docs/공고_2025_경영경제대학_학술제.pdf)

## 디렉토리 구조
```
employment-readiness-text-mining/
├── README.md
├── LICENSE
├── requirements.txt
│
├── crawlers/
│   └── 에타_크롤링.py            # Selenium 기반 에브리타임 크롤러
│
├── notebooks/
│   ├── 00_1차_데이터_탐색.ipynb   # 1차 데이터 점검
│   ├── 01_메인_분석.ipynb          # 메인 분석 (162셀)
│   ├── 02_부정_토픽_모델링.ipynb   # 부정 감정 글 별도 LDA
│   └── 03_감정_분류.ipynb          # KoBERT / kcbert-large 분류
│
├── data/                           # ⚠️ gitignored (원본 텍스트 포함)
│   ├── raw/                        #   에브리타임 크롤링 + 설문 응답 원본
│   ├── processed/                  #   토픽·감정 가공 산출물
│   └── README.md                   #   데이터 구조와 재현 방법
│
├── reports/
│   ├── 구해줘_잡스.pdf
│   ├── 원페이지_보고서.pdf
│   ├── 구해줘_잡스_참가보고서.hwp
│   ├── 토픽_모델링_시각화.html
│   └── 부정_토픽_모델링_시각화.html
│
└── docs/
    └── 공고_2025_경영경제대학_학술제.pdf
```
