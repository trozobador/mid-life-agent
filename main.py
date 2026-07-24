import argparse
import os
import shutil
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


DEFAULT_PERSON = os.getenv("PERSON", "ricardo")


def list_people() -> list[str]:
    data_dir = Path("data")
    if not data_dir.exists():
        return []
    return sorted(d.name for d in data_dir.iterdir() if d.is_dir())


def list_roles(person: str) -> list[str]:
    profiles_dir = Path(f"data/{person}/job_profiles")
    if not profiles_dir.exists():
        return []
    return sorted(f.stem for f in profiles_dir.glob("*.txt"))


def prepare_output_dir(person: str, role: str, base_resume_path: str) -> str:
    output_dir = f"outputs/{person}/{role}"
    for subdir in ("json", "latex", "pdf"):
        os.makedirs(os.path.join(output_dir, subdir), exist_ok=True)
    dst = os.path.join(output_dir, "json", "resume.json")
    # If the best-match resume is the output dir itself (re-run), refresh from canonical source
    if os.path.realpath(base_resume_path) == os.path.realpath(dst):
        base_resume_path = f"data/{person}/resume.json"
    shutil.copy(base_resume_path, dst)
    return output_dir


def run_for_role(person: str, role: str, provider: str = None, language: str = "pt-BR"):
    profile_path = f"data/{person}/job_profiles/{role}.txt"
    if not os.path.exists(profile_path):
        print(f"[ERROR] Profile not found: {profile_path}")
        print(f"  Available profiles for '{person}': {', '.join(list_roles(person)) or 'none'}")
        sys.exit(1)

    original_resume_path = f"data/{person}/resume.json"
    output_dir = prepare_output_dir(person, role, base_resume_path=original_resume_path)

    from src.agents.job_application_crew import JobApplicationCrew

    crew = JobApplicationCrew(
        role=role,
        job_profile_path=profile_path,
        output_dir=output_dir,
        provider=provider,
        language=language,
        original_resume_path=original_resume_path,
    )
    return crew.run()


def run_for_job_desc(person: str, job_desc_path: str, provider: str = None, language: str = "pt-BR"):
    path = Path(job_desc_path)
    if not path.exists():
        print(f"[ERROR] Arquivo de vaga não encontrado: {job_desc_path}")
        sys.exit(1)

    from src.scripts.resume_matcher import extract_job_title, find_best_resume

    job_desc = path.read_text(encoding="utf-8")

    role_name = extract_job_title(job_desc)
    print(f"\n{'='*60}")
    print(f"  Pessoa: {person} | Cargo identificado: {role_name}")
    print(f"{'='*60}")

    original_resume_path = f"data/{person}/resume.json"

    # Procura o currículo existente mais aderente a esta vaga (dentre os da mesma pessoa)
    match = find_best_resume(job_desc, outputs_dir=f"outputs/{person}")
    if match:
        match_path, match_score, match_folder = match
        base_resume = match_path
        print(f"\n[INFO] Currículo mais aderente encontrado:")
        print(f"       outputs/{person}/{match_folder}/  (aderência: {match_score:.0%})")
        print(f"[INFO] Usando como ponto de partida para esta vaga.\n")
    else:
        base_resume = original_resume_path
        print(f"\n[INFO] Nenhum currículo existente aderente. Usando currículo original.\n")

    output_dir = prepare_output_dir(person, role_name, base_resume_path=base_resume)

    from src.agents.job_application_crew import JobApplicationCrew

    crew = JobApplicationCrew(
        role=role_name,
        job_profile_path=str(path),
        output_dir=output_dir,
        provider=provider,
        language=language,
        original_resume_path=original_resume_path,
    )
    return crew.run()


def run_legacy(person: str, provider: str = None):
    """Backwards-compatible run using data/<person>/job_desc.txt → outputs/<person>."""
    output_dir = f"outputs/{person}"
    os.makedirs(f"{output_dir}/json", exist_ok=True)
    os.makedirs(f"{output_dir}/latex", exist_ok=True)
    os.makedirs(f"{output_dir}/pdf", exist_ok=True)
    original_resume_path = f"data/{person}/resume.json"
    shutil.copy(original_resume_path, f"{output_dir}/json/resume.json")

    from src.agents.job_application_crew import JobApplicationCrew

    crew = JobApplicationCrew(
        job_profile_path=f"data/{person}/job_desc.txt",
        output_dir=output_dir,
        provider=provider,
        original_resume_path=original_resume_path,
    )
    return crew.run()


def main():
    parser = argparse.ArgumentParser(
        prog="mid-life-agent",
        description="Agente da Meia Idade — Reposicionamento de Currículo com IA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Exemplos de uso:
  python main.py --person carol --role data_scientist
  python main.py --role ai_engineer --provider anthropic     # usa PERSON do .env (padrão: {DEFAULT_PERSON})
  python main.py --job                          # usa input/<person>/job_desc.md
  python main.py --job input/vaga_senior.md     # aponta para outro arquivo
  python main.py --all
  python main.py --all --person carol
  python main.py --list-roles --person carol
  python main.py --list-people
        """,
    )
    parser.add_argument(
        "--person",
        metavar="PERSON",
        default=DEFAULT_PERSON,
        help=f"Para quem gerar o currículo (ex: ricardo, carol). Padrão: PERSON no .env, ou '{DEFAULT_PERSON}'",
    )
    parser.add_argument(
        "--role",
        metavar="ROLE",
        help="Perfil alvo (ex: data_scientist, ai_engineer). Arquivo em data/<person>/job_profiles/<role>.txt",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Gerar currículo otimizado para TODOS os perfis disponíveis em lote",
    )
    parser.add_argument(
        "--provider",
        metavar="PROVIDER",
        choices=["openai", "anthropic", "gemini", "grok"],
        help="Provedor de LLM (padrão: valor de LLM_PROVIDER no .env, ou openai)",
    )
    parser.add_argument(
        "--job",
        metavar="PATH",
        nargs="?",
        const="__default__",
        help="Arquivo .md com a descrição da vaga (padrão: input/<person>/job_desc.md)",
    )
    parser.add_argument(
        "--lang",
        metavar="LANG",
        default="pt-BR",
        help="Idioma do currículo gerado: 'pt-BR' (padrão) ou 'en' para inglês",
    )
    parser.add_argument(
        "--list-roles",
        action="store_true",
        help="Listar perfis de vaga disponíveis em data/<person>/job_profiles/",
    )
    parser.add_argument(
        "--list-people",
        action="store_true",
        help="Listar pessoas disponíveis (subpastas em data/)",
    )

    args = parser.parse_args()
    person = args.person

    if args.list_people:
        people = list_people()
        if people:
            print("Pessoas disponíveis:")
            for p in people:
                print(f"  - {p}")
        else:
            print("Nenhuma pessoa encontrada em data/")
        return

    if args.list_roles:
        roles = list_roles(person)
        if roles:
            print(f"Perfis disponíveis para '{person}':")
            for r in roles:
                print(f"  - {r}")
        else:
            print(f"Nenhum perfil encontrado em data/{person}/job_profiles/")
            print("Crie arquivos .txt nesse diretório para cada perfil-alvo.")
        return

    if args.all:
        roles = list_roles(person)
        if not roles:
            print(f"[ERROR] Nenhum perfil encontrado em data/{person}/job_profiles/")
            sys.exit(1)
        print(f"Executando para {person} — {len(roles)} perfil(s): {', '.join(roles)}\n")
        for role in roles:
            print(f"\n{'='*60}")
            print(f"  Processando: {role}")
            print(f"{'='*60}\n")
            run_for_role(person, role, provider=args.provider, language=args.lang)
        return

    if args.role:
        run_for_role(person, args.role, provider=args.provider, language=args.lang)
        return

    if args.job is not None:
        job_path = f"input/{person}/job_desc.md" if args.job == "__default__" else args.job
        run_for_job_desc(person, job_path, provider=args.provider, language=args.lang)
        return

    # Default: legacy mode with data/<person>/job_desc.txt
    print(f"Nenhum --role especificado. Usando data/{person}/job_desc.txt (modo legado).")
    run_legacy(person, provider=args.provider)


if __name__ == "__main__":
    main()
