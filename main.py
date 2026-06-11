import argparse
import os
import shutil
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def list_roles() -> list[str]:
    profiles_dir = Path("data/job_profiles")
    if not profiles_dir.exists():
        return []
    return sorted(f.stem for f in profiles_dir.glob("*.txt"))


def prepare_output_dir(role: str, base_resume_path: str = "data/resume.json") -> str:
    output_dir = f"outputs/{role}"
    for subdir in ("json", "latex", "pdf"):
        os.makedirs(os.path.join(output_dir, subdir), exist_ok=True)
    dst = os.path.join(output_dir, "json", "resume.json")
    # If the best-match resume is the output dir itself (re-run), refresh from canonical source
    if os.path.realpath(base_resume_path) == os.path.realpath(dst):
        base_resume_path = "data/resume.json"
    shutil.copy(base_resume_path, dst)
    return output_dir


def run_for_role(role: str, provider: str = None, language: str = "pt-BR"):
    profile_path = f"data/job_profiles/{role}.txt"
    if not os.path.exists(profile_path):
        print(f"[ERROR] Profile not found: {profile_path}")
        print(f"  Available profiles: {', '.join(list_roles()) or 'none'}")
        sys.exit(1)

    output_dir = prepare_output_dir(role)

    from src.agents.job_application_crew import JobApplicationCrew

    crew = JobApplicationCrew(
        role=role,
        job_profile_path=profile_path,
        output_dir=output_dir,
        provider=provider,
        language=language,
    )
    return crew.run()


def run_for_job_desc(job_desc_path: str, provider: str = None, language: str = "pt-BR"):
    path = Path(job_desc_path)
    if not path.exists():
        print(f"[ERROR] Arquivo de vaga não encontrado: {job_desc_path}")
        sys.exit(1)

    from src.scripts.resume_matcher import extract_job_title, find_best_resume

    job_desc = path.read_text(encoding="utf-8")

    role_name = extract_job_title(job_desc)
    print(f"\n{'='*60}")
    print(f"  Cargo identificado: {role_name}")
    print(f"{'='*60}")

    # Procura o currículo existente mais aderente a esta vaga
    match = find_best_resume(job_desc, outputs_dir="outputs")
    if match:
        match_path, match_score, match_folder = match
        base_resume = match_path
        print(f"\n[INFO] Currículo mais aderente encontrado:")
        print(f"       outputs/{match_folder}/  (aderência: {match_score:.0%})")
        print(f"[INFO] Usando como ponto de partida para esta vaga.\n")
    else:
        base_resume = "data/resume.json"
        print(f"\n[INFO] Nenhum currículo existente aderente. Usando currículo original.\n")

    output_dir = prepare_output_dir(role_name, base_resume_path=base_resume)

    from src.agents.job_application_crew import JobApplicationCrew

    crew = JobApplicationCrew(
        role=role_name,
        job_profile_path=str(path),
        output_dir=output_dir,
        provider=provider,
        language=language,
    )
    return crew.run()


def run_legacy(provider: str = None):
    """Backwards-compatible run using data/job_desc.txt → outputs/."""
    os.makedirs("outputs/json", exist_ok=True)
    os.makedirs("outputs/latex", exist_ok=True)
    os.makedirs("outputs/pdf", exist_ok=True)
    shutil.copy("data/resume.json", "outputs/json/resume.json")

    from src.agents.job_application_crew import JobApplicationCrew

    crew = JobApplicationCrew(
        job_profile_path="data/job_desc.txt",
        output_dir="outputs",
        provider=provider,
    )
    return crew.run()


def main():
    parser = argparse.ArgumentParser(
        prog="mid-life-agent",
        description="Agente da Meia Idade — Reposicionamento de Currículo com IA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py --role data_scientist
  python main.py --role ai_engineer --provider anthropic
  python main.py --job                          # usa input/job_desc.md
  python main.py --job input/vaga_senior.md     # aponta para outro arquivo
  python main.py --all
  python main.py --all --provider gemini
  python main.py --list-roles
        """,
    )
    parser.add_argument(
        "--role",
        metavar="ROLE",
        help="Perfil alvo (ex: data_scientist, ai_engineer). Arquivo em data/job_profiles/<role>.txt",
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
        const="input/job_desc.md",
        help="Arquivo .md com a descrição da vaga (padrão: input/job_desc.md)",
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
        help="Listar perfis de vaga disponíveis em data/job_profiles/",
    )

    args = parser.parse_args()

    if args.list_roles:
        roles = list_roles()
        if roles:
            print("Perfis disponíveis:")
            for r in roles:
                print(f"  - {r}")
        else:
            print("Nenhum perfil encontrado em data/job_profiles/")
            print("Crie arquivos .txt nesse diretório para cada perfil-alvo.")
        return

    if args.all:
        roles = list_roles()
        if not roles:
            print("[ERROR] Nenhum perfil encontrado em data/job_profiles/")
            sys.exit(1)
        print(f"Executando para {len(roles)} perfil(s): {', '.join(roles)}\n")
        for role in roles:
            print(f"\n{'='*60}")
            print(f"  Processando: {role}")
            print(f"{'='*60}\n")
            run_for_role(role, provider=args.provider, language=args.lang)
        return

    if args.role:
        run_for_role(args.role, provider=args.provider, language=args.lang)
        return

    if args.job is not None:
        run_for_job_desc(args.job, provider=args.provider, language=args.lang)
        return

    # Default: legacy mode with data/job_desc.txt
    print("Nenhum --role especificado. Usando data/job_desc.txt (modo legado).")
    run_legacy(provider=args.provider)


if __name__ == "__main__":
    main()
