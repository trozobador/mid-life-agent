# Memória do Projeto: Agente da Meia Idade

## Informações Gerais
- **Nome do Projeto**: Agente da Meia Idade (anteriormente conhecido como CV Agents)
- **Diretório do Repositório**: `mid-life-agent`
- **Objetivo Principal**: Um sistema multi-agente inteligente que reposiciona e reescreve o currículo original do usuário de acordo com múltiplos perfis de vagas-alvo.

## Regras Críticas e Convenções
1. **Nomenclatura Obrigatória**: O sistema deve ser SEMPRE chamado de **Agente da Meia Idade**. Qualquer referência anterior a "CV Agent" ou "CV Agents" foi descontinuada e deve ser evitada no código, documentação e comunicação.
2. **Arquitetura Multi-LLM**: O projeto deve suportar de forma transparente múltiplos provedores (OpenAI, Anthropic, Google Gemini e Grok) através do uso do LangChain e variáveis de ambiente unificadas.
3. **Estrutura de Agentes**: O fluxo baseia-se em 4 agentes, incluindo a adição fundamental do **Career Strategist**, responsável por alinhar a narrativa e os objetivos do currículo com os requisitos específicos da vaga.

## Próximos Passos (Roadmap da Especificação)
- Implementar a nova estrutura no código fonte (`main.py`, `job_application_crew.py`).
- Implementar o LLM Factory (`llm_factory.py`).
- Criar templates de job profiles (`data/job_profiles/`).
- Atualizar a CLI para suportar os novos parâmetros (`--role`, `--all`, `--provider`).
