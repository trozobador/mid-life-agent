# Memória do Projeto: Agente da Meia Idade

## Informações Gerais
- **Nome do Projeto**: Agente da Meia Idade
- **Diretório do Repositório**: `mid-life-agent`
- **Objetivo Principal**: Sistema multi-agente que reposiciona o currículo do usuário para diferentes vagas do mercado, prepara para entrevistas e (futuro) gerencia posicionamento no LinkedIn.

## Usuário
- **Nome**: Ricardo Martins
- **Email**: ricardo.parallax@gmail.com
- **Localização**: Uberlândia, MG
- **Perfil**: Profissional de TI com 30+ anos de experiência, sendo 15 anos em liderança técnica
- **Perfis alvo**: AI Engineer, Cientista de Dados, Engenheiro de Dados, Arquiteto de Sistemas Inteligentes
- **Arquivos de currículo real**: pasta `input/ricardo/`

## Multi-pessoa
- Desde 2026-07-23 o projeto suporta gerar currículos para mais de uma pessoa (ex: `ricardo`, `carol`, `gabrielly`), cada uma com dados isolados em `input/<pessoa>/`, `data/<pessoa>/`, `outputs/<pessoa>/`.
- 2026-07-24: estrutura preparada para a Gabrielly (`input/gabrielly/README.md` + `profile_truth.md` em branco, `data/gabrielly/job_profiles/README.md`) — aguardando que ela envie os arquivos reais do currículo (PDF/DOCX) para rodar `ingest_resume.py --person gabrielly`.
- Pessoa ativa por padrão: `PERSON` no `.env` (atualmente `ricardo`). Trocar via `--person <nome>` na CLI.
- **Why**: o Ricardo pediu uma forma de gerar/chavear o currículo da Carol sem misturar dados dela com os dele.
- **How to apply**: qualquer novo script ou caminho hardcoded para currículo/vaga/output deve receber `person` como parâmetro em vez de assumir um único usuário.

## Arquitetura Implementada
- **5 agentes CrewAI** (sequential): Career Strategist → Hiring Manager → Resume Editor → Job Applicant → Interview Coach
- **Multi-LLM**: `src/llm_factory.py` — OpenAI, Anthropic, Gemini, Grok (via `LLM_PROVIDER` no .env)
- **CLI**: `python main.py --person <nome> --role <perfil> --provider <llm> --all --list-roles --list-people`
- **Ingestion**: `python src/scripts/ingest_resume.py --person <nome>` — lê `input/<pessoa>/` (PDF+DOCX) e gera `data/<pessoa>/resume.json`
- **Job profiles curados**: `data/<pessoa>/job_profiles/` (ricardo: data_scientist, ai_engineer, data_engineer, dynamics_specialist, product_manager)
- **Outputs por perfil**: `outputs/<pessoa>/<role>/json|latex|pdf/` + `outputs/<pessoa>/<role>/interview_prep.md`
- **Venv**: `.venv` (Python 3.12 via uv)

## Convenções
- O sistema NUNCA fabrica experiências — apenas reordena, reescreve e reposiciona o que é real
- `data/<pessoa>/resume.json` é a fonte única de verdade (currículo completo) de cada pessoa
- `input/` e `outputs/` passaram a ser commitados no repositório (removidos do .gitignore) — cuidado ao adicionar dados sensíveis de terceiros

## Roadmap Futuro
- Módulo de posicionamento LinkedIn (monitorar perfil, sugerir posts, alinhar com vagas)
- Busca automática de vagas (LinkedIn, Indeed) e análise de aderência do currículo
