# Agente da Meia Idade
![images/logo.jpeg](images/logo.jpeg)

Apresentando o Agente da Meia Idade, sua equipe pessoal de avanço de carreira movida a inteligência artificial.

Imagine ter um gerente de contratação de alto nível, um editor de currículos especialista, um estrategista de carreira e um candidato a emprego inteligente trabalhando incansavelmente para aperfeiçoar seu currículo. É exatamente isso que o Agente da Meia Idade faz!

O sistema guiado por IA recebe seu currículo inicial e o processa através de uma série de agentes inteligentes. O **Estrategista de Carreira** analisa a vaga alvo, reescreve a sua narrativa e seleciona as experiências mais relevantes. O gerente de contratação avalia o currículo criticamente, o editor o refina e otimiza, e o candidato a emprego orquestra tudo para fazê-lo se destacar. Este processo iterativo se repete até o seu currículo atingir uma nota de excelência (≥ 8.5).

O Agente da Meia Idade não apenas edita; ele reposiciona o seu currículo e o transforma em uma ferramenta poderosa. Ele garante que seu currículo caiba em uma página, destaque suas qualificações mais relevantes e esteja perfeitamente alinhado aos requisitos da vaga. Você pode **gerar múltiplas versões** do seu currículo em lote para diferentes perfis (ex: Cientista de Dados, Engenheiro de IA, Especialista Microsoft Dynamics, etc.).

Principais vantagens do Agente da Meia Idade:

1. **Geração Multi-Perfil**: Suporta a geração de currículos em lote, criando uma versão otimizada e dedicada para cada perfil de vaga que você definir.
2. **Suporte Multi-LLM**: Funciona de forma integrada com OpenAI (GPT-4o), Anthropic (Claude), Google Gemini e Grok (xAI). Escolha o provedor de IA que preferir.
3. **Reposicionamento de Carreira**: O novo agente "Career Strategist" adapta seu resumo profissional e prioriza suas habilidades e experiências de acordo com o foco da vaga, ajustando a narrativa.
4. **Open-source**: O sistema inteiro é de código aberto, permitindo transparência e contribuições da comunidade.
5. **Totalmente personalizável**: Suporta formatos LaTeX e JSON, oferecendo controle completo sobre o resultado final.
6. **Sem histórias falsas**: A IA não inventa experiências ou habilidades; ela extrai, seleciona e realça estrategicamente suas melhores experiências reais.
7. **Seleção Inteligente**: Se você tem um histórico extenso, o Agente da Meia Idade seleciona automaticamente as experiências e projetos com maior aderência (match) à vaga, mantendo o currículo conciso e impactante.

Deixe a IA revolucionar a sua busca por emprego e abrir as portas para a carreira dos seus sonhos!

## Screenshots 

### Antes vs Depois

![images/before_after.png](images/before_after.png)

### Diff no estilo GitHub

![images/github_like_diff.png](images/github_like_diff.png)

## Instruções de Configuração

1. **Configurar Chaves de API**:
   - Defina a chave de API do seu provedor de LLM preferido no arquivo `.env`. O projeto suporta a alternância fluida entre os modelos:
     ```env
     # Provedor ativo (openai | anthropic | gemini | grok)
     LLM_PROVIDER=openai
     
     OPENAI_API_KEY="sua_chave_da_openai"
     ANTHROPIC_API_KEY="sua_chave_da_anthropic"
     GOOGLE_API_KEY="sua_chave_do_google_gemini"
     XAI_API_KEY="sua_chave_da_xai"
     ```

2. **Múltiplas Pessoas (Multi-perfil)**:
   - O projeto suporta gerar currículos para mais de uma pessoa (ex: `ricardo`, `carol`), cada uma com seus próprios dados isolados:
     - `input/<pessoa>/` — currículos originais (PDF/DOCX) e `profile_truth.md`
     - `data/<pessoa>/resume.json` — currículo consolidado (fonte única de verdade)
     - `data/<pessoa>/job_profiles/` — perfis de vaga-alvo
     - `outputs/<pessoa>/<role>/` — currículos gerados
   - A pessoa ativa por padrão vem de `PERSON` no `.env` (ex: `PERSON=ricardo`). Use `--person <nome>` em qualquer comando para trocar (ex: `--person carol`).
   - Para adicionar uma nova pessoa, crie as pastas `input/<pessoa>/` e `data/<pessoa>/job_profiles/` e rode `python src/scripts/ingest_resume.py --person <pessoa>`.
   - Liste as pessoas configuradas com `python main.py --list-people`.

3. **Perfis de Vaga (Job Profiles)**:
   - Crie arquivos `.txt` com as descrições/perfis das vagas no diretório `data/<pessoa>/job_profiles/` (ex: `data_scientist.txt`, `ai_engineer.txt`, `dynamics_specialist.txt`).

4. **Currículo JSON Original**:
   - Edite o currículo base no arquivo `data/<pessoa>/resume.json`. Ele será a fonte única de dados para todas as variações geradas dessa pessoa.
   - Utilize a estrutura JSON padrão (já fornecida no repositório) para cadastrar dados básicos, experiências, educação, habilidades, certificações, projetos e idiomas.

5. **Instalação das Dependências**:
   - Instale as bibliotecas necessárias executando:
     ```bash
     pip install -r requirements.txt
     ```
   - *Atenção: Os pacotes `langchain` específicos (ex: `langchain-openai`, `langchain-anthropic`) devem estar instalados de acordo com o provedor em uso.*

6. **Executar os Agentes (CLI)**:
   - A ferramenta de linha de comando permite gerar currículos facilmente:
   - **Para gerar para um perfil específico (pessoa padrão do `.env`):**
     ```bash
     python main.py --role data_scientist
     ```
   - **Para gerar para outra pessoa:**
     ```bash
     python main.py --person carol --role data_scientist
     ```
   - **Para gerar currículos para TODOS os perfis listados em lote:**
     ```bash
     python main.py --all
     python main.py --all --person carol
     ```
   - **Para testar outro provedor de LLM em tempo de execução:**
     ```bash
     python main.py --role ai_engineer --provider anthropic
     ```
   - **Para listar os perfis configurados disponíveis:**
     ```bash
     python main.py --list-roles --person carol
     ```
   - **Para listar as pessoas configuradas:**
     ```bash
     python main.py --list-people
     ```

7. **Verificar os Resultados**:
   - Os currículos gerados (JSON, LaTeX e PDF) estarão organizados separadamente por pessoa e perfil alvo na pasta `outputs/`.
   - Exemplo: `outputs/ricardo/data_scientist/output_resume.pdf`.

8. **Comparar Currículos**:
   - Para visualizar exatamente o que a IA otimizou no seu CV original, rode o script de comparação:
     ```bash
     python src/scripts/run_compare_pdf.py
     ```
   - Um arquivo comparativo `outputs/pdf/compare_diff.pdf` será gerado com o diff estilo GitHub.
