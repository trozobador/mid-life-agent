# Plano de Otimização do LinkedIn — Ricardo Martins

**Data da análise:** 22/08/2026
**Perfil analisado:** linkedin.com/in/costaricardomartins
**Fontes cruzadas:** `profile_truth.md` (fonte de verdade), `json/resume.json` (base "ai_engineer", mais completo), `vagas_selecionadas_2026-08-22.md`, LinkedIn ao vivo (Sobre, Experiência, Formação, Competências, Certificações, Atividades)
**Objetivo:** tornar o perfil competitivo para vagas de **Ciência de Dados**, **Arquiteto de IA**, **Desenvolvedor Sênior** e **Dynamics 365 / Power Platform**

---

## 1. Resumo executivo

O LinkedIn atual está bem alinhado ao *pivot* de carreira em três pontos (headline com "Cientista de Dados & ML", atividade de conteúdo consistente e boa, currículo base "ai_engineer" robusto), mas tem **quatro problemas estruturais que prejudicam a credibilidade e o alcance em buscas de recrutador**, na ordem de gravidade:

1. **Datas de experiência sobrepostas e incoerentes** — o LinkedIn mostra três empregos em tempo integral rodando ao mesmo tempo (2020–2022), o que não é fisicamente possível e é o tipo de erro que reprovador de triagem (humano ou ATS) marca como red flag.
2. **Seção "Competências" (Skills) está vazia** — zero habilidades cadastradas na aba dedicada. Isso é gravíssimo porque é o principal campo usado pelos filtros do LinkedIn Recruiter e pela busca de recrutadores.
3. **Seção "Sobre" desatualizada e com erro de copy-paste** — ainda descreve Ricardo só como "Arquiteto Microsoft Dynamics", não menciona IA/Ciência de Dados, tem um parágrafo duplicado, e cita uma métrica (45.000 matrículas) que contradiz o próprio currículo (8 mil alunos).
4. **Formação acadêmica com dado divergente do Profile Truth** e **uma certificação expirada** sendo exibida como válida.

Existe ainda uma informação de alto valor **presente no LinkedIn mas ausente do `profile_truth.md`**: um bacharelado em Física pela USP (1994–1998). Se verdadeiro, é um ativo forte para vagas de Ciência de Dados (base quantitativa) e deveria estar no currículo e no Profile Truth — hoje está "escondido" e nem o pipeline de geração de currículo sabe que existe.

Todas as recomendações abaixo pressupõem que você **confirme os pontos da Seção 2** antes de publicar qualquer alteração — não deve haver invenção de dado novo, apenas reorganização e correção do que já existe.

---

## 2. Achados de consistência (LinkedIn × Profile Truth × Currículos)

### 2.1 Prioridade CRÍTICA — corrigir antes de qualquer outra coisa

| # | Achado | LinkedIn | Profile Truth / Currículo | Ação recomendada |
|---|--------|----------|----------------------------|-------------------|
| 1 | **Sobreposição de empregos em tempo integral** | SEB: jan/2020–set/2023 · Adentis Portugal: jan/2021–mai/2022 · Algar Tech: ago/2015–**2021** — os três se sobrepõem por até 2 anos | Sequência sem sobreposição: Algar Tech 08/2015–01/2020 → Adentis 01/2020–05/2022 → SEB 06/2022–09/2023 | Corrigir as datas de início/fim de Algar Tech, Adentis e SEB no LinkedIn para bater com o Profile Truth (regime CLT/PJ e local ainda têm campos `[PREENCHER]` no Profile Truth — preencha-os primeiro) |
| 2 | **R238 (fundação da empresa própria)** | mar/2025 – atual | Profile Truth diz "04/2022 – 0/2026" (data final malformada) | O texto do "Sobre" da própria experiência R238 no LinkedIn narra um pivot recente ("Depois de mais de uma década... decidi migrar"), o que é coerente com mar/2025, não com 2022. Corrija o Profile Truth para a data real de fundação — hoje ele contradiz o próprio LinkedIn |
| 3 | **NTT DATA — data de saída** | mai/2024 – **abr/2025** | 05/2024 – **01/2025** | Diferença de 3 meses. Confirme a data real (rescisão/último dia) e alinhe as duas fontes |
| 4 | **BlueCX — datas** | mai/2025 – mai/2026 | 04/2025 – 04/2026 | Diferença de ~1 mês em início e fim; alinhar |
| 5 | **Formação — Anhanguera (Ciências de Dados)** | jun/2025 – **jun/2029** ("cursando") | "CURSANDO — Previsão **02/2027**" | Diferença de 2 anos na previsão de conclusão. Um recrutador que veja "conclusão em 2029" pode descartar a candidatura para vagas que pedem graduação completa em Data Science; confirme a grade real do curso e corrija ambos os lugares |
| 6 | **Bacharelado em Física — USP (1994–1998)** | Aparece na aba Formação do LinkedIn | **Não consta em nenhum lugar do Profile Truth nem dos currículos** | Confirme se é real. Se sim, é um diferencial forte para Ciência de Dados (fundamentação quantitativa) e deve ser adicionado ao Profile Truth e destacado no currículo/resumo, não deixado só no LinkedIn |
| 7 | **AI Nanodegree — Udacity (2019)** | Aparece na aba Formação do LinkedIn, com certificado em PDF anexado | **Não consta no Profile Truth** (que só lista as 5 certificações Microsoft) | Confirme e adicione ao Profile Truth — é uma certificação relevante e antiga (2019) que reforça que o interesse em IA não é recente, e sim de longa data — bom argumento contra objeção de "está migrando de área agora do nada" |
| 8 | **Certificação Power Platform Developer Associate (PL-400) EXPIRADA** | "Emitido em abr/2025 · **Expirou em abr/2026**" | Listado como ✅ válida, sem menção a expiração | Hoje (ago/2026) a certificação está vencida e aparece assim publicamente. Renove o quanto antes — é a certificação mais citada na headline (PL-400) e nas vagas de maior aderência (Power Platform) |
| 9 | **Contradição de métrica: matrículas SEB** | "Sobre" do LinkedIn diz **45.000 matrículas anuais** | Profile Truth / currículo dizem **8 mil alunos** em 18 unidades | Uma das duas está errada. Verifique o número real e corrija nos dois lugares — números de impacto divergentes entre LinkedIn e currículo são o tipo de coisa que recrutador confere em entrevista |

### 2.2 Prioridade ALTA — lacunas de preenchimento (não são erros, são vazios)

| # | Seção | Situação atual | Impacto |
|---|-------|------------------|---------|
| 10 | **Competências (Skills)** | Aba "Competências" **completamente vazia** — 0 itens. Apenas 5 competências genéricas aparecem "pineladas" no card Sobre (Microsoft Dynamics CRM, AWS, C#, SQL, Computação em nuvem) | É o pior gap do perfil. O algoritmo de busca do LinkedIn Recruiter filtra por essa lista. Hoje o perfil **não aparece** em buscas por "Python", "Power BI", "RAG", "LLM", "Machine Learning", "Dataverse" etc., mesmo tendo experiência real nisso |
| 11 | **Certificações não sincronizadas** | Faltam no LinkedIn: MB-910 (Dynamics 365 Fundamentals), PL-900 (Power Platform Fundamentals), certificação Dynamics CRM 2011 (2013) — todas listadas no Profile Truth. Sobram no LinkedIn (fora do Profile Truth): AI-900, 2 certificados Databricks (dez/2025), "Software Engineer" HackerRank (jul/2026), 3 cursos curtos do LinkedIn Learning sobre IA/produtividade | Reconciliar: adicionar as que faltam no LinkedIn e preencher a lacuna `[PREENCHER: outras certificações]` do Profile Truth com as que já existem no LinkedIn e são reais |
| 12 | **Projetos / Featured** | Zero projetos cadastrados. O próprio LinkedIn sugere: "Adicione projetos que destaquem suas competências" | Existem pelo menos 4 projetos concretos e bem documentados no currículo (Brigitte — pipeline editorial multi-LLM; agentes de trading Polymarket; RAG no Copilot Studio da BlueCX; ferramenta de RPA da Algar Tech) que não aparecem em lugar nenhum visível do perfil |
| 13 | **"Aberto a" (Open to Work)** | Cargos-alvo cadastrados: Analista de sistemas sênior, Arquiteto de soluções, Desenvolvedor de Dynamics, Desenvolvedor líder de projeto | Não inclui nenhum termo de "Ciência de Dados", "Data Scientist", "AI Architect/Arquiteto de IA" ou "Power Platform" — exatamente os 4 alvos que você quer priorizar agora. O filtro de vagas que o LinkedIn usa para te recomendar e te mostrar a recrutadores está desalinhado do seu objetivo atual |
| 14 | **Confirmação de cargo atual pendente** | O próprio LinkedIn está perguntando: "Seu cargo atual é Founder & CEO at R238?" | Enquanto não confirmado, o perfil pode estar exibindo o status de emprego de forma inconsistente para quem visita — resolver esse prompt |

### 2.3 Prioridade MÉDIA

| # | Achado | Detalhe |
|---|--------|---------|
| 15 | **Localização da SEB corrompida** | Aparece como "Рибейран-Прету, SP" (caracteres cirílicos misturados) em vez de "Ribeirão Preto, SP" — erro de digitação/autocomplete, precisa correção visual |
| 16 | **Headline pode ganhar termos-chave de Ciência de Dados/IA generativa** | Atual: "AI & Dynamics Developer \| Tech Lead \| Cientista de Dados & ML \| Arquiteto de Soluções \| Multicloud \| PL-400 \| C# \| React \| Backend" — boa densidade de palavras-chave, mas falta "Ciência de Dados" por extenso, "IA Generativa", "RAG" ou "Azure OpenAI", termos que recrutadores de Data Science/IA buscam literalmente |
| 17 | **Idioma** | Profile Truth deixa em aberto se o inglês B2 inclui conversação (`[PREENCHER]`). Vagas remotas internacionais (ex.: item #7 da lista de vagas selecionadas, Nortal) exigem inglês avançado com overlap de fuso EUA — vale clarificar o nível real antes de aplicar para essas |
| 18 | **Métricas possivelmente infladas no currículo "ai_engineer"** | Frases como "respostas 30% mais precisas e contextuais", "reduzindo alucinações em 25%", "impactar mais de 500 mil clientes" (BlueCX) não têm lastro claro no Profile Truth nem foram confirmadas por você na seção "❌ NÃO INCLUIR" (que está vazia/não preenchida) | Antes de usar esse currículo para aplicações de Ciência de Dados/Arquiteto de IA — onde esse tipo de claim é mais escrutinado — revise se esses números são reais, aproximados ou devem ser suavizados (ex.: "buscando reduzir alucinações via prompt engineering" em vez de "reduzindo em 25%") |

---

## 3. Plano de ação por seção do LinkedIn

### 3.1 Headline (título)

**Atual:**
> AI & Dynamics Developer | Tech Lead | Cientista de Dados & ML | Arquiteto de Soluções | Multicloud | PL-400 | C# | React | Backend

**Proposta (ajustar para os 4 alvos: Ciência de Dados, Arquiteto de IA, Dev Sênior, Dynamics/Power Platform):**
> Arquiteto de Soluções de IA & Dynamics 365 | Ciência de Dados & Machine Learning | Power Platform | RAG/LLM em Produção (Azure OpenAI) | 15+ anos em Liderança Técnica

Motivo: mantém as palavras que já rankeiam bem (Dynamics, IA, Arquiteto), remove itens de baixo retorno para os 4 alvos (React, Backend genérico) e adiciona termos de alta busca em vagas de Ciência de Dados/Arquiteto de IA (RAG, LLM, Azure OpenAI) que hoje só aparecem "escondidos" na experiência.

### 3.2 Sobre (About)

Reescrever do zero — o texto atual: (a) descreve um cargo antigo ("Arquiteto Microsoft Dynamics" na SEB) como se fosse a identidade central, (b) tem um parágrafo literalmente duplicado, (c) usa a métrica de matrículas que conflita com o currículo, (d) não menciona nenhuma palavra do universo de IA generativa/Ciência de Dados além de "IA generativa" citada de passagem.

Estrutura sugerida (a redigir com você, com números validados):
1. Abertura com identidade atual: 30+ anos de TI / 15 em liderança técnica, migração deliberada para Ciência de Dados e Engenharia de IA, hoje operando sistemas de IA em produção (não é promessa, é prática — cite a R238).
2. Um parágrafo de prova técnica: Dynamics 365/Power Platform em nível avançado + IA generativa aplicada (RAG, Copilot Studio, Azure OpenAI) + fundamentos (Física/USP, se confirmado, e cursando Ciências de Dados).
3. Um parágrafo de resultado de negócio, com números **conferidos** (não os dois conflitantes).
4. Lista curta de stack (a mesma lógica do atual, mas sem duplicar o parágrafo de paixão).
5. Call to action objetivo, coerente com "Buscando emprego": tipos de vaga e modalidade (100% remoto).

### 3.3 Competências (Skills) — maior ganho de esforço/impacto

Cadastrar (usando como base o `ai_engineer/resume.json`, que já está organizado em blocos), priorizando o que aparece nas descrições de vaga de cada um dos 4 alvos:

- **Ciência de Dados / ML:** Python, Machine Learning, Pandas, NumPy, Scikit-Learn, Modelagem Preditiva, Análise de Dados, Estatística
- **IA Generativa / Arquiteto de IA:** LLMs, RAG (Retrieval-Augmented Generation), Prompt Engineering, Azure OpenAI Service, Copilot Studio, Vector Databases, LangChain, Agentes Autônomos, Azure AI Studio, Azure Cognitive Services
- **Dynamics 365 / Power Platform:** Microsoft Dynamics 365 (CE/CRM), Power Platform, Power Apps, Power Automate, Power BI, Dataverse, Customer Insights – Journeys
- **Desenvolvimento Sênior:** C#, .NET, JavaScript/TypeScript, APIs REST, Azure Functions, Azure DevOps, CI/CD, Git, Arquitetura de Software

Fixar como "Principais competências" (as 3 que aparecem no topo do card Sobre) uma combinação que cubra os 4 alvos ao mesmo tempo — sugestão: **Dynamics 365, Python/Machine Learning, Azure OpenAI/RAG**. Hoje as 5 fixadas (Dynamics CRM, AWS, C#, SQL, Cloud) não têm nada de Ciência de Dados/IA, o que é o oposto do objetivo declarado.

### 3.4 Experiência — reescrever bullets com foco duplo (Dynamics + IA/Dados)

Para cada vaga recente (BlueCX, NTT DATA), os bullets já existentes são bons, mas devem:
- Ter as datas corrigidas conforme Seção 2.1.
- Abrir cada cargo com uma frase que amarre à narrativa de Ciência de Dados/IA, não só Dynamics (ex.: já existe isso na BlueCX — replicar na NTT DATA e Algar Tech, que hoje são descritas só como Dynamics/RPA sem menção a dados).
- Usar métricas conferidas (ver item 18 da Seção 2).

Para as vagas mais antigas (Algar Tech, Adentis, SEB, CAST, AlfaPeople, L3), considerar resumir mais (menos linhas), já que o peso de relevância para os 4 alvos atuais é menor — mas sem apagar, pois sustentam os "15 anos de liderança técnica" do resumo.

### 3.5 Formação e Certificações

- Corrigir a data de previsão de conclusão da Anhanguera (02/2027, conforme Profile Truth, ou a data real confirmada).
- Adicionar USP (Física) e Udacity (AI Nanodegree) ao Profile Truth **depois de confirmados**, e garantir que fiquem visíveis e destacados no currículo voltado a Ciência de Dados (uma graduação em Física é um argumento forte de "fundamentação quantitativa" que poucos concorrentes de Dynamics têm).
- Renovar a certificação PL-400/Power Platform Developer Associate (expirada).
- Adicionar ao LinkedIn as certificações MB-910, PL-900 e Dynamics CRM 2011 (2013), hoje ausentes lá.
- Preencher a lacuna `[STATUS] | [PREENCHER: outras certificações]` do Profile Truth com Databricks (x2), AI-900 (confirmar mês real — LinkedIn e `ai_engineer/resume.json` divergem: mar/2025 vs dez/2025), HackerRank e os cursos LinkedIn Learning, marcando status ✅/❌ conforme instrução do próprio arquivo.

### 3.6 Projetos / Featured

Adicionar como "Projetos" (seção de destaque do LinkedIn) pelo menos:
1. **Brigitte** — pipeline de automação editorial multi-LLM em produção na AWS (mostra IA aplicada + engenharia de dados/eventos).
2. **Integração Copilot Studio + RAG** (BlueCX) — mostra Arquiteto de IA na prática.
3. **Modelo preditivo de participação em eventos** (BlueCX) — mostra Ciência de Dados aplicada a negócio.
4. **Ferramenta de RPA** (Algar Tech, 8M interações/mês) — mostra escala e Dynamics/automação.

Isso também resolve o alerta que o próprio LinkedIn está exibindo ("Adicione projetos que destaquem suas competências").

### 3.7 "Aberto a" (Open to Work)

Atualizar a lista de cargos-alvo para refletir os 4 focos pedidos:
- Cientista de Dados / Data Scientist
- Arquiteto de Soluções de IA / AI Solutions Architect
- Desenvolvedor(a) Sênior (manter, já cadastrado como "Desenvolvedor líder de projeto" — trocar por termo mais buscado)
- Desenvolvedor(a) / Consultor(a) Dynamics 365 & Power Platform (já parcialmente coberto — reforçar com "Power Platform" explícito, hoje só "Desenvolvedor de Dynamics" está lá)

Resolver também o prompt pendente de confirmação do cargo atual (Founder & CEO – R238), decidindo conscientemente se ele deve aparecer como cargo principal atual ou como projeto paralelo, já que o resto do perfil sinaliza busca ativa de emprego CLT/PJ.

### 3.8 Conteúdo / Atividade (ponto forte a manter e ampliar)

Os posts recentes têm bom engajamento (um deles com 40 mil+ impressões) e já reforçam a narrativa de "uso de IA no dia a dia como dev sênior" — isso é um ativo real de marca pessoal. Recomendação: fixar (pin) o post de melhor desempenho no topo do perfil e, periodicamente, publicar conteúdo específico sobre Ciência de Dados/Arquitetura de IA (não só opinião sobre uso de IA por devs) para atrair a rede certa para os 4 alvos — hoje os posts são mais sobre cultura de engenharia do que sobre Dados/ML propriamente.

---

## 4. Itens que precisam da SUA confirmação antes de qualquer publicação

Estes não devem ser assumidos como verdade nem publicados sem sua validação — servem para você revisar e me devolver as respostas (ou editar direto no `profile_truth.md`, que é a fonte de verdade do pipeline):

1. Bacharelado em Física pela USP (1994–1998) — é real? Incluir no Profile Truth?
2. AI Nanodegree pela Udacity (2019) — é real? Incluir no Profile Truth?
3. Datas exatas de Algar Tech, Adentis Portugal e SEB (hoje sobrepostas no LinkedIn) — qual sequência e datas estão corretas?
4. Data de fundação real da R238 (2022 conforme Profile Truth ou 2025 conforme LinkedIn/narrativa do "Sobre" da própria experiência)?
5. Data de saída real da NTT DATA (jan/2025 conforme Profile Truth ou abr/2025 conforme LinkedIn)?
6. Número real de matrículas no projeto SEB (8 mil, conforme currículo, ou 45.000, conforme "Sobre" do LinkedIn)?
7. Previsão real de conclusão da Anhanguera (02/2027 conforme Profile Truth ou jun/2029 conforme LinkedIn)?
8. As métricas "30% mais precisas", "25% de redução de alucinações" e "500 mil clientes impactados" (currículo `ai_engineer`) são reais/aproximadas, ou devem ser suavizadas para vagas de Ciência de Dados/Arquiteto de IA, onde esse tipo de claim costuma ser testado em entrevista técnica?
9. Nível real de inglês (conversação, além de leitura/escrita B2) — relevante para as vagas remotas internacionais já mapeadas.

---

## 5. Checklist priorizado

**Crítico (fazer primeiro, antes de aplicar para qualquer vaga nova):**
- [ ] Corrigir datas sobrepostas de Algar Tech / Adentis / SEB no LinkedIn
- [ ] Preencher a aba "Competências" do LinkedIn (zero hoje)
- [ ] Reescrever a seção "Sobre" (remover parágrafo duplicado e métrica não conferida)
- [ ] Renovar certificação PL-400/Power Platform Developer Associate (expirada)
- [ ] Confirmar os 9 pontos da Seção 4 e atualizar `profile_truth.md`

**Alto impacto:**
- [ ] Atualizar headline
- [ ] Adicionar seção de Projetos/Featured (4 projetos sugeridos)
- [ ] Atualizar "Aberto a" com os 4 cargos-alvo corretos
- [ ] Sincronizar certificações entre Profile Truth e LinkedIn (adicionar as que faltam nos dois lados)
- [ ] Resolver o prompt pendente "confirmar cargo atual"

**Complementar:**
- [ ] Corrigir localização da SEB (texto corrompido)
- [ ] Fixar o post de melhor desempenho no topo
- [ ] Planejar 2–3 posts futuros com foco em Ciência de Dados/Arquitetura de IA (não só opinião sobre devs usando IA)
- [ ] Definir nível real de inglês e revisar aderência às vagas que exigem overlap com EUA

---

*Este plano não altera nada automaticamente — é um roteiro para você (ou para mim, com sua aprovação item a item) editar o LinkedIn e o `profile_truth.md`. Nenhum número novo foi inventado: todas as divergências listadas vêm de comparação direta entre o que já está publicado no LinkedIn e o que já está nos seus próprios arquivos.*
