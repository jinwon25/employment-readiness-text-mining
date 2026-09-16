"""Create the privacy-safe representative portfolio notebook."""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "notebooks" / "portfolio_summary.ipynb"


def build() -> Path:
    cells = [
        new_markdown_cell(
            """# 취업 준비 과정의 감정 데이터 분석과 지원 제도 설계

이 노트북은 개인정보가 포함된 게시글·설문 원문 대신 학술제 발표자료에 공개된 집계 결과를 사용해 프로젝트의 핵심 판단을 보여 줍니다. 원 모델 학습 과정은 `00`–`03` 노트북에 보존되어 있습니다."""
        ),
        new_markdown_cell(
            """## 분석 질문

1. 학생들이 취업 준비에서 체감하는 부담은 어느 정도인가?
2. 학내 프로그램이 있어도 참여하지 않는 접근성 간극이 존재하는가?
3. 커뮤니티 반응과 부정 강도는 어떤 관계를 보이는가?
4. 이 결과를 어떤 지원 제도와 운영 KPI로 연결할 수 있는가?"""
        ),
        new_code_cell(
            """from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path.cwd().resolve()
if not (ROOT / 'data').exists():
    ROOT = ROOT.parent

evidence = json.loads((ROOT / 'data/derived/reported_evidence.json').read_text(encoding='utf-8'))
evidence['scope']"""
        ),
        new_markdown_cell("## 1. 설문에서 확인한 부담과 접근성 간극"),
        new_code_cell(
            """stress = pd.Series(evidence['survey_stress_distribution_pct'], name='share_pct').rename_axis('stress_level')
participation = pd.Series(evidence['program_participation_pct'], name='share_pct').rename_axis('status')
display(stress.to_frame())
display(participation.to_frame())
print(f\"Stress level 3+: {stress.loc[['3', '4', '5']].sum():.1f}%\")"""
        ),
        new_code_cell(
            """fig, axes = plt.subplots(1, 2, figsize=(11, 4))
stress.plot.bar(ax=axes[0], color=['#CBD5E1', '#94A3B8', '#60A5FA', '#2563EB', '#1E3A8A'])
axes[0].set(title='Job-search stress', xlabel='Level (1=low, 5=high)', ylabel='Share (%)')
participation.plot.bar(ax=axes[1], color=['#60A5FA', '#F59E0B'])
axes[1].set(title='Campus career program participation', xlabel='', ylabel='Share (%)')
for axis in axes:
    axis.grid(axis='y', alpha=.2)
plt.tight_layout()
plt.show()"""
        ),
        new_markdown_cell(
            """스트레스 수준 3 이상이 85.4%였고 프로그램 미참여 응답은 62.7%였습니다. 편의 표본이므로 전체 학생 비율로 일반화하기보다, 지원 프로그램을 더 쉽게 발견하고 신청하게 만드는 문제가 존재한다는 탐색 근거로 사용합니다."""
        ),
        new_markdown_cell("## 2. 커뮤니티 반응과 부정 강도"),
        new_code_cell(
            """popular = evidence['popular_post_comparison']
popular_summary = pd.Series({
    'general_posts': popular['general_mean_negative_intensity'],
    'popular_top_10_pct': popular['popular_top_10_pct_mean_negative_intensity'],
}, name='mean_negative_intensity')
display(popular_summary.to_frame())
print(f\"t={popular['t_statistic']:.3f}, p={popular['p_value']:.3f}\")

axis = popular_summary.plot.bar(figsize=(7, 4), color=['#94A3B8', '#EF4444'])
axis.set(title='Negative intensity by community response group', xlabel='', ylabel='Mean model score', ylim=(0, .58))
axis.grid(axis='y', alpha=.2)
plt.tight_layout()
plt.show()"""
        ),
        new_markdown_cell(
            """인기 상위 10% 글에서 부정 강도가 더 높게 관측됐지만, 글 길이·주제·작성 시기와 감정 모델 오차를 통제한 결과는 아닙니다. 따라서 부정성이 인기를 유발한다는 인과 해석 대신, 반응이 큰 고민 주제를 프로그램 수요 탐색에 활용할 수 있다는 수준으로 해석합니다."""
        ),
        new_markdown_cell("## 3. 감정 분류와 토픽 모델링의 공개 근거"),
        new_code_cell(
            """model = pd.Series(evidence['sentiment_model'], name='value')
display(model.to_frame())
topics = pd.DataFrame(evidence['final_lda_topics'])
topics[['topic', 'label', 'keywords']]"""
        ),
        new_markdown_cell(
            """감정 분류는 672건을 537/135로 나눠 학습했고, 저장된 최선의 검증 loss는 3 epoch의 0.600입니다. Accuracy·Macro-F1이 남아 있지 않아 분류 성능을 확정하지 않습니다. 최종 발표의 4토픽은 지원 수요를 구성하는 탐색적 주제로 사용합니다."""
        ),
        new_markdown_cell(
            """## 4. 의사결정 연결

| 발견 | 제도 설계 | 운영 KPI |
|---|---|---|
| 프로그램 미참여 62.7% | 모바일 탐색·시기별 알림·신청 단계 단축 | 상세 조회율, 신청 전환율, 완료 시간 |
| 공채 시즌 부정 글 증가 | 9월 전 서류·면접 지원, 2월 전 인턴 준비 노출 | 참석률, 완료율, 재참여율 |
| 고민 주제의 이질성 | 직무 정보·1:1 케어·경험 보강·상담 연결 분기 | 유형별 신청률, 만족도, 상담 연결률 |
| 반응이 큰 부정 고민 | 익명 집계로 수요 감지 | 주제별 문의량, 지원 콘텐츠 이용률 |

군집은 개인 심리 진단이 아니라 게시글 단위 지원 수요를 정리한 운영 프레임입니다. AI 챗봇 역시 프로그램 탐색과 전문 상담 연결에 한정합니다."""
        ),
        new_markdown_cell(
            """## 결론

- 취업 스트레스와 프로그램 미참여가 함께 관측돼 ‘제도의 존재’보다 ‘발견과 접근’이 중요한 문제로 나타났습니다.
- 커뮤니티 텍스트는 시기와 고민 주제를 파악하는 수요 신호로 활용할 수 있습니다.
- 감정 점수와 군집은 탐색 도구이며, 개인 상태 진단이나 인과 주장에 사용하지 않습니다.
- 실제 도입은 프로그램 탐색→신청→참여 퍼널과 사용자 경험 지표로 평가해야 합니다."""
        ),
    ]
    notebook = new_notebook(
        cells=cells,
        metadata={
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3"},
        },
    )
    nbformat.write(notebook, OUTPUT)
    return OUTPUT


if __name__ == "__main__":
    print(build())
