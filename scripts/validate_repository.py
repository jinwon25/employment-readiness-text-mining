"""원문 없이 공개 집계와 노트북 공개 범위를 검증합니다."""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def validate_links() -> None:
    for markdown in ROOT.rglob("*.md"):
        text = markdown.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path = target.split("#", 1)[0]
            if path and not (markdown.parent / path).resolve().exists():
                raise AssertionError(f"Broken link in {markdown.relative_to(ROOT)}: {target}")


def validate_python() -> None:
    for folder in ("scripts", "crawlers"):
        for path in (ROOT / folder).glob("*.py"):
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def validate_notebook() -> None:
    path = ROOT / "notebooks" / "portfolio_summary.ipynb"
    notebook = json.loads(path.read_text(encoding="utf-8"))
    code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
    if not code_cells or any(cell.get("execution_count") is None for cell in code_cells):
        raise AssertionError("Representative notebook is not fully executed")
    errors = [
        output
        for cell in code_cells
        for output in cell.get("outputs", [])
        if output.get("output_type") == "error"
    ]
    if errors:
        raise AssertionError(f"Representative notebook contains errors: {errors}")


def validate_evidence() -> None:
    evidence = json.loads((ROOT / "data" / "derived" / "reported_evidence.json").read_text(encoding="utf-8"))
    stress = evidence["survey_stress_distribution_pct"]
    if round(sum(stress.values()), 1) != 100.0:
        raise AssertionError("Stress distribution does not sum to 100%")
    if round(sum(stress[level] for level in ("3", "4", "5")), 1) != 85.4:
        raise AssertionError("Stress level 3+ does not reconcile to 85.4%")
    participation = evidence["program_participation_pct"]
    if round(sum(participation.values()), 1) != 100.0:
        raise AssertionError("Participation distribution does not sum to 100%")
    if len(evidence["final_lda_topics"]) != 4:
        raise AssertionError("Final LDA topic count must be four")


def validate_public_scope() -> None:
    for path in (ROOT / "notebooks").glob("*.ipynb"):
        if path.name == "portfolio_summary.ipynb":
            continue
        notebook = json.loads(path.read_text(encoding="utf-8"))
        for cell in notebook["cells"]:
            if cell.get("cell_type") == "code" and (
                cell.get("outputs") or cell.get("execution_count") is not None
            ):
                raise AssertionError(f"원문 노트북 출력은 비워야 합니다: {path.name}")
    private_artifacts = [ROOT / "reports" / "구해줘_잡스_참가보고서.hwp"]
    exposed = [path.relative_to(ROOT) for path in private_artifacts if path.exists()]
    if exposed:
        raise AssertionError(f"Private application artifacts must not be public: {exposed}")


def main() -> None:
    validate_links()
    validate_python()
    validate_notebook()
    validate_evidence()
    validate_public_scope()
    print("공개 집계·파일 구조·노트북 공개 범위 검증 완료")


if __name__ == "__main__":
    main()
