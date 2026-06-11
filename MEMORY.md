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
- **Arquivos de currículo real**: pasta `input/` (no .gitignore)

## Arquitetura Implementada
- **5 agentes CrewAI** (sequential): Career Strategist → Hiring Manager → Resume Editor → Job Applicant → Interview Coach
- **Multi-LLM**: `src/llm_factory.py` — OpenAI, Anthropic, Gemini, Grok (via `LLM_PROVIDER` no .env)
- **CLI**: `python main.py --role <perfil> --provider <llm> --all --list-roles`
- **Ingestion**: `python src/scripts/ingest_resume.py` — lê `input/` (PDF+DOCX) e gera `data/resume.json`
- **Job profiles curados**: `data/job_profiles/` (data_scientist, ai_engineer, data_engineer, dynamics_specialist, product_manager)
- **Outputs por perfil**: `outputs/<role>/json|latex|pdf/` + `outputs/<role>/interview_prep.md`
- **Venv**: `.venv` (Python 3.12 via uv)

## Convenções
- O sistema NUNCA fabrica experiências — apenas reordena, reescreve e reposiciona o que é real
- `data/resume.json` é a fonte única de verdade (currículo completo)
- `input/` está no .gitignore — nunca commitar dados pessoais
- `outputs/*/` está no .gitignore — artefatos gerados localmente

## Roadmap Futuro
- Módulo de posicionamento LinkedIn (monitorar perfil, sugerir posts, alinhar com vagas)
- Busca automática de vagas (LinkedIn, Indeed) e análise de aderência do currículo
