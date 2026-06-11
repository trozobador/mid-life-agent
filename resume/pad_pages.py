"""
Deterministic post-processor: enriches a generated resume JSON with highlights
from the original until the PDF reaches exactly 2 pages.
"""

import json
import os


def _page_count(output_dir: str) -> int:
    from tools.tools_utils import count_pages_and_lines
    pdf_path = os.path.join(output_dir, "pdf", "output_resume.pdf")
    if not os.path.exists(pdf_path):
        return 0
    pages, _ = count_pages_and_lines(pdf_path)
    return pages


def _regenerate(output_dir: str, json_path: str) -> int:
    from resume.generator import generate
    latex_path = os.path.join(output_dir, "latex", "output_resume.tex")
    pdf_dir = os.path.join(output_dir, "pdf")
    generate(json_path=json_path, latex_path=latex_path, pdf_dir=pdf_dir)
    return _page_count(output_dir)


def _normalize(name: str) -> str:
    return name.strip().lower()


def pad_to_two_pages(output_dir: str, original_path: str = "data/resume.json") -> int:
    """
    Enriches the generated resume with highlights from the original until the PDF
    reaches 2 pages. Returns the final page count.

    Strategy (in order):
      1. For each existing work entry, append unused highlights from the original.
      2. If still 1 page, append missing work entries from the original.
      3. If still 1 page, expand summary with more detail.
    """
    json_path = os.path.join(output_dir, "json", "resume.json")

    with open(json_path, encoding="utf-8") as f:
        generated = json.load(f)
    with open(original_path, encoding="utf-8") as f:
        original = json.load(f)

    # Always regenerate from the current JSON before checking page count
    pages = _regenerate(output_dir, json_path)

    # Build lookup: normalized company name → original work entry
    orig_work_map = {
        _normalize(w.get("name", "")): w
        for w in original.get("work", [])
    }

    # --- Phase 1: add missing highlights in round-robin across all entries -----
    # Build per-job pool of unused original highlights
    pools = []
    for job in generated.get("work", []):
        orig_entry = orig_work_map.get(_normalize(job.get("name", "")))
        if not orig_entry:
            pools.append([])
            continue
        existing = {h.strip() for h in job.get("highlights", [])}
        unused = [
            h for h in orig_entry.get("highlights", [])
            if h.strip() not in existing
        ]
        pools.append(unused)

    exhausted = False
    while pages < 2 and not exhausted:
        exhausted = True
        for i, job in enumerate(generated.get("work", [])):
            if pages >= 2:
                break
            if not pools[i]:
                continue
            exhausted = False
            job.setdefault("highlights", []).append(pools[i].pop(0))
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(generated, f, indent=2, ensure_ascii=False)
            pages = _regenerate(output_dir, json_path)

    if pages >= 2:
        return pages

    # --- Phase 2: add missing work entries from original -----------------------
    gen_companies = {_normalize(w.get("name", "")) for w in generated.get("work", [])}
    for orig_entry in original.get("work", []):
        if pages >= 2:
            break
        if _normalize(orig_entry.get("name", "")) not in gen_companies:
            generated.setdefault("work", []).append(orig_entry)
            gen_companies.add(_normalize(orig_entry.get("name", "")))
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(generated, f, indent=2, ensure_ascii=False)
            pages = _regenerate(output_dir, json_path)

    return pages
