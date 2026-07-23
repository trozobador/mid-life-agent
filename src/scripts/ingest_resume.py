"""
Lê todos os arquivos em input/ (PDF e DOCX), extrai o texto de cada um,
combina tudo e usa o LLM para gerar data/resume.json com o máximo de
informação possível.

Uso:
    python src/scripts/ingest_resume.py
    python src/scripts/ingest_resume.py --provider anthropic
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

import fitz  # PyMuPDF
from docx import Document
from dotenv import load_dotenv

load_dotenv()

# Windows consoles default to cp1252, which can't encode ✓/✗ etc. below.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from prompts.job_application_prompts import JSON_STRUCTURE


# ─── Extração de texto ────────────────────────────────────────────────────────

def extract_pdf(path: Path) -> str:
    doc = fitz.open(str(path))
    return "\n".join(page.get_text() for page in doc)


def extract_docx(path: Path) -> str:
    doc = Document(str(path))
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def is_legacy_doc(path: Path) -> bool:
    """Word 97-2003 binary format (OLE2 Compound File) vs. zip-based .docx."""
    with open(path, "rb") as f:
        return f.read(8) == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"


def extract_legacy_doc(path: Path) -> str:
    """Extract text from a binary .doc via antiword (python-docx can't read these)."""
    try:
        result = subprocess.run(
            ["antiword", str(path)],
            capture_output=True,
            check=True,
        )
    except FileNotFoundError:
        print(f"  [ERRO] '{path.name}' é um .doc binário (Word 97-2003) e o "
              f"conversor 'antiword' não foi encontrado no PATH. Instale-o ou "
              f"salve o arquivo como .docx e tente novamente.")
        return ""
    except subprocess.CalledProcessError as e:
        print(f"  [ERRO] antiword falhou em '{path.name}': {e.stderr.decode(errors='replace')}")
        return ""
    return result.stdout.decode("cp1252", errors="replace")


def extract_file(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return extract_pdf(path)
    elif suffix == ".doc" and is_legacy_doc(path):
        return extract_legacy_doc(path)
    elif suffix in (".docx", ".doc"):
        return extract_docx(path)
    return ""


def collect_input_texts(input_dir: Path) -> dict[str, str]:
    supported = {".pdf", ".docx", ".doc"}
    texts = {}
    for f in sorted(input_dir.iterdir()):
        if f.suffix.lower() in supported:
            text = extract_file(f)
            if text.strip():
                texts[f.name] = text
                print(f"  ✓ {f.name} ({len(text)} chars)")
    return texts


def load_truth_file(input_dir: Path) -> str:
    truth_path = input_dir / "profile_truth.md"
    if truth_path.exists():
        content = truth_path.read_text(encoding="utf-8")
        print(f"  ✓ profile_truth.md (guardrail carregado)")
        return content
    return ""


# ─── Prompt ───────────────────────────────────────────────────────────────────

def build_prompt(texts: dict[str, str], truth: str = "") -> str:
    sections = "\n\n".join(
        f"### Arquivo: {name}\n{text}" for name, text in texts.items()
    )

    truth_block = ""
    if truth:
        truth_block = f"""
## AUTHORITATIVE SOURCE OF TRUTH

The following document was manually curated by the person and is the GROUND TRUTH.
It takes absolute precedence over anything in the resume files below.

CRITICAL RULES when a `profile_truth.md` is provided:
- Any fact stated here overrides the resume files — dates, titles, certifications, levels.
- Items in the "NÃO INCLUIR" section MUST NOT appear anywhere in the output JSON.
- Fields marked [PREENCHER] mean the person hasn't filled them in yet — leave them empty or omit them; do NOT invent values.
- Education marked "CURSANDO" must have no endDate or use the preview year — never treat it as completed.
- Only include certifications explicitly listed here with ✅ or without a status marker.
  Do NOT include certifications marked ❌ or [STATUS] without a confirmed year.

### profile_truth.md
{truth}

---
"""

    return f"""You are an expert resume parser and career data analyst.
{truth_block}
## RESUME FILES

Below are the contents of {len(texts)} resume file(s) belonging to the same person.
They may be different versions of the same resume (general, specialized per role, etc.).

Your task:
1. Read ALL versions carefully.
2. Extract the most complete, accurate picture of this person's career.
3. When the same information appears in multiple versions, use the most detailed one.
4. When specialized versions add skills or highlights not in the general version, INCLUDE them.
5. If a profile_truth.md was provided above, it is the authoritative source — reconcile conflicts in its favor.
6. Output a single, comprehensive resume as a valid JSON object.

Use EXACTLY this JSON schema — do not add or remove top-level keys:
{JSON_STRUCTURE}

Rules:
- Use the actual person's data. Do not invent anything.
- `basics.summary`: write a neutral, comprehensive 3-sentence professional summary.
- `work[].highlights`: include ALL bullet points found across all versions (deduplicated).
- `skills`: merge all skill categories across versions; keep the most complete keyword lists.
- Dates must be in "YYYY-MM" format (e.g., "2020-03"). Use "Present" for current roles.
- Output ONLY the JSON object — no markdown, no explanation, no code fences.

---

{sections}
"""


# ─── LLM call ─────────────────────────────────────────────────────────────────

def call_llm(prompt: str, provider: str) -> str:
    from src.llm_factory import get_llm

    llm = get_llm(provider=provider, temperature=0.1)
    return llm.call(prompt)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Converte currículos de input/ para data/resume.json"
    )
    parser.add_argument(
        "--provider",
        choices=["openai", "anthropic", "gemini", "grok"],
        default=None,
        help="Provedor LLM (padrão: LLM_PROVIDER do .env)",
    )
    parser.add_argument(
        "--person",
        default=os.getenv("PERSON", "ricardo"),
        help="Para quem gerar o resume.json (ex: ricardo, carol). Padrão: PERSON no .env, ou 'ricardo'",
    )
    parser.add_argument(
        "--input-dir",
        default=None,
        help="Diretório com os arquivos de currículo (padrão: input/<person>/)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Caminho do JSON de saída (padrão: data/<person>/resume.json)",
    )
    args = parser.parse_args()

    args.input_dir = args.input_dir or f"input/{args.person}"
    args.output = args.output or f"data/{args.person}/resume.json"

    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        print(f"[ERRO] Diretório '{input_dir}' não encontrado.")
        sys.exit(1)

    print(f"\nLendo arquivos de '{input_dir}/'...")
    texts = collect_input_texts(input_dir)
    if not texts:
        print("[ERRO] Nenhum arquivo PDF ou DOCX encontrado em input/")
        sys.exit(1)

    truth = load_truth_file(input_dir)

    print(f"\nEnviando {len(texts)} arquivo(s) para o LLM...")
    prompt = build_prompt(texts, truth=truth)
    raw = call_llm(prompt, provider=args.provider)

    # Limpa possíveis code fences que o LLM adicione por engano
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1]
    if cleaned.endswith("```"):
        cleaned = cleaned.rsplit("```", 1)[0]
    cleaned = cleaned.strip()

    try:
        resume_data = json.loads(cleaned)
    except json.JSONDecodeError as e:
        print(f"\n[ERRO] O LLM retornou JSON inválido: {e}")
        print("Salvando resposta bruta em data/resume_raw.txt para inspeção...")
        Path("data/resume_raw.txt").write_text(raw, encoding="utf-8")
        sys.exit(1)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(resume_data, indent=2, ensure_ascii=False), encoding="utf-8")

    name = resume_data.get("basics", {}).get("name", "—")
    print(f"\n✓ resume.json gerado com sucesso!")
    print(f"  Nome detectado : {name}")
    print(f"  Experiências   : {len(resume_data.get('work', []))}")
    print(f"  Habilidades    : {len(resume_data.get('skills', []))}")
    print(f"  Certificações  : {len(resume_data.get('certificates', []))}")
    print(f"  Projetos       : {len(resume_data.get('projects', []))}")
    print(f"  Salvo em       : {output_path}")


if __name__ == "__main__":
    main()
