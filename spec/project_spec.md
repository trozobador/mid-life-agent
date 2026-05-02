# Agente da Meia Idade — Especificação do Projeto

## 1. O que foi pedido

Transformar o repositório `mid-life-agent` em um agente inteligente capaz de:

- **Reescrever e reposicionar** o currículo do usuário de acordo com o perfil de cada vaga
- **Gerar N versões** do currículo, uma por perfil-alvo, incluindo (mas não limitado a):
  - Especialista em Microsoft Dynamics
  - Cientista de Dados (Data Scientist)
  - Engenheiro de Dados (Data Engineer)
  - Engenheiro de IA (AI Engineer)
  - (demais perfis configuráveis)
- Suporte a múltiplos provedores de LLM: **OpenAI, Gemini, Grok (xAI) e Anthropic (Claude)**

---

## 2. Conclusões da Análise do Repositório

### Estado Atual

| Componente | Status |
|---|---|
| Framework de agentes | CrewAI (multi-agent, sequential) |
| Agentes existentes | 3: Hiring Manager, Resume Editor, Job Applicant |
| Input | `data/resume.json` + `data/job_desc.txt` |
| Output | JSON → LaTeX → PDF + diff comparativo |
| Refinamento | Loop iterativo até nota ≥ 8.5 |
| CV de exemplo | Cynthia Dwayne (fictício) |

### Gaps Identificados

| Gap | Impacto |
|---|---|
| Sem agente de reposicionamento | Resume apenas otimiza; não reescreve narrativa de carreira |
| Uma vaga por execução | Sem suporte a geração em lote |
| Sem perfis de vaga curados | Job descriptions precisam ser criados manualmente |
| LLM hardcoded (OpenAI default) | Sem abstração para trocar de provedor |
| CLI sem parâmetros | Não aceita `--role`, `--all`, `--provider` |
| CV real ausente | Só existe currículo de exemplo fictício |

---

## 3. LLMs no Projeto

### Ativo
- **OpenAI `gpt-4o`** — padrão implícito do CrewAI quando nenhum `llm=` é especificado nos agentes
- Autenticado via `OPENAI_API_KEY` no `.env`

### Inativo (comentado)
- **Grok** — código presente mas comentado; pacote `langchain-xai` não está em `requirements.txt`

### Não presentes
- Anthropic (Claude) — não configurado
- Google Gemini — não configurado

---

## 4. Estratégia para Atingir o Objetivo

### 4.1 Novo Agente: Career Strategist

Adicionar um **4º agente** com foco exclusivo em reposicionamento de carreira:

```
Agente: Career Strategist
Responsabilidade:
  - Analisar o perfil-alvo da vaga
  - Identificar habilidades transferíveis do currículo original
  - Reescrever o "summary/objetivo profissional" com narrativa alinhada ao cargo
  - Selecionar e priorizar experiências mais relevantes para o perfil
  - Adaptar linguagem e palavras-chave para ATS (Applicant Tracking Systems)
```

### 4.2 Sistema de Job Profiles

Criar `data/job_profiles/` com arquivos `.txt` curados por perfil:

```
data/job_profiles/
├── dynamics_specialist.txt
├── data_scientist.txt
├── data_engineer.txt
├── ai_engineer.txt
└── [adicionar conforme necessário]
```

Cada arquivo contém: título do cargo, responsabilidades esperadas, stack técnica, palavras-chave ATS, soft skills valorizadas.

### 4.3 Outputs Organizados por Perfil

```
outputs/
├── dynamics_specialist/
│   ├── resume.json
│   ├── output_resume.tex
│   └── output_resume.pdf
├── data_scientist/
│   └── ...
└── ai_engineer/
    └── ...
```

### 4.4 CLI com Parâmetros

```bash
# Gerar para um perfil específico
python main.py --role data_scientist

# Gerar para todos os perfis
python main.py --all

# Especificar provedor de LLM
python main.py --role ai_engineer --provider anthropic

# Listar perfis disponíveis
python main.py --list-roles
```

### 4.5 Fluxo dos Agentes (novo)

```
[Input: my_resume.json + job_profile.txt]
         │
         ▼
┌─────────────────────┐
│  Career Strategist  │  ← NOVO: reescreve narrativa, seleciona experiências
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│   Hiring Manager    │  ← avalia fit com a vaga (nota 1–10)
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│   Resume Editor     │  ← ajusta formatação, 1 página, ferramentas LaTeX
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│   Job Applicant     │  ← orquestra loop até nota ≥ 8.5
└─────────────────────┘
         │
         ▼
[Output: JSON + LaTeX + PDF por perfil]
```

---

## 5. Estratégia de Compatibilidade Multi-LLM

### Abstração via CrewAI + LangChain

O CrewAI aceita qualquer `llm=` compatível com a interface LangChain. A estratégia é criar um **factory de LLM** que instancia o modelo correto com base em variável de ambiente ou flag de CLI.

### 5.1 Provedores Suportados

| Provedor | Pacote LangChain | Modelo Padrão Sugerido | Variável de Ambiente |
|---|---|---|---|
| OpenAI | `langchain-openai` | `gpt-4o` | `OPENAI_API_KEY` |
| Anthropic | `langchain-anthropic` | `claude-sonnet-4-6` | `ANTHROPIC_API_KEY` |
| Google Gemini | `langchain-google-genai` | `gemini-1.5-pro` | `GOOGLE_API_KEY` |
| Grok | `langchain-xai` | `grok-2-latest` | `XAI_API_KEY` |

### 5.2 LLM Factory (novo módulo: `src/llm_factory.py`)

```python
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm(provider: str = None, temperature: float = 0.4):
    provider = provider or os.getenv("LLM_PROVIDER", "openai")

    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(temperature=temperature, model="gpt-4o")

    elif provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(temperature=temperature, model="claude-sonnet-4-6")

    elif provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(temperature=temperature, model="gemini-1.5-pro")

    elif provider == "grok":
        from langchain_xai import ChatXAI
        return ChatXAI(temperature=temperature, model="grok-2-latest")

    else:
        raise ValueError(f"Provedor não suportado: {provider}")
```

### 5.3 `.env` Unificado

```env
# Provedor ativo (openai | anthropic | gemini | grok)
LLM_PROVIDER=openai

# Chaves de API — preencha apenas a do provedor ativo
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_API_KEY=
XAI_API_KEY=
```

### 5.4 Dependências por Provedor (`requirements.txt`)

```
# Core
crewai>=2.7
langchain
python-dotenv
PyPDF2
crewai-tools

# LLM Providers (instale apenas o que for usar)
langchain-openai          # OpenAI / GPT-4o
langchain-anthropic        # Anthropic / Claude
langchain-google-genai     # Google / Gemini
langchain-xai              # Grok / xAI
```

### 5.5 Considerações por Provedor

| Provedor | Vantagem | Limitação |
|---|---|---|
| OpenAI `gpt-4o` | Melhor qualidade geral, padrão testado | Custo mais alto |
| Anthropic `claude-sonnet-4-6` | Excelente para escrita/reposicionamento | Requer `langchain-anthropic` |
| Google `gemini-1.5-pro` | Contexto longo (1M tokens), custo baixo | Qualidade de escrita ligeiramente inferior |
| Grok `grok-2-latest` | Rápido, atualizado em tempo real com X | Custos de API da xAI |

---

## 6. Próximos Passos

- [ ] Criar `data/my_resume.json` com o currículo real do usuário
- [ ] Criar `data/job_profiles/*.txt` com os perfis-alvo
- [ ] Implementar `src/llm_factory.py`
- [ ] Adicionar agente `Career Strategist` em `job_application_crew.py`
- [ ] Atualizar `prompts/job_application_prompts.py` com `STRATEGIST_PROMPT`
- [ ] Atualizar `main.py` com CLI argparse (`--role`, `--all`, `--provider`)
- [ ] Criar `run_all.py` para execução em lote
- [ ] Atualizar `requirements.txt` com todos os provedores
- [ ] Atualizar `.env` com estrutura multi-provedor
- [ ] Testar com pelo menos 2 provedores diferentes
