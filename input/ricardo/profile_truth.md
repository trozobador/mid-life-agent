# Profile Truth — Ricardo Martins
<!-- 
  FONTE DE VERDADE DO CURRÍCULO
  ───────────────────────────────
  Este arquivo é o guardrail do pipeline de geração de currículo.
  O LLM sempre prioriza as informações daqui sobre os PDFs/DOCX.

  INSTRUÇÕES DE EDIÇÃO:
  - Corrija qualquer informação errada diretamente no texto.
  - Preencha as lacunas marcadas com [PREENCHER].
  - Remova ou mova para a seção "NÃO INCLUIR" o que for falso.
  - Mantenha as datas no formato MM/AAAA.
  - Não apague as seções, mesmo que vazias — deixe-as em branco.

  ATUALIZADO EM 22/08/2026 a partir de cruzamento com o LinkedIn
  (linkedin.com/in/costaricardomartins) e confirmação direta do usuário.
-->

---

## DADOS PESSOAIS

- **Nome completo:** Ricardo Martins
- **E-mail:** ricardo.parallax@gmail.com
- **Telefone:** (34) 98433-1954
- **Cidade:** Uberlândia – MG – Brasil
- **LinkedIn:** https://www.linkedin.com/in/costaricardomartins/
- **CNPJ ativo:** Sim
- **Disponibilidade para trabalho remoto:**  Apenas remoto 
- **Disponibilidade para realocação:**  Sim 

---

## RESUMO PROFISSIONAL

<!-- Escreva aqui o resumo que você quer que apareça no currículo.
     Se deixar em branco, o LLM gera automaticamente a partir das experiências. -->

Profissional de TI com mais de 30 anos de experiência, sendo 15 anos em liderança técnica de projetos complexos. Atuação em empresas de médio e grande porte nos setores financeiro, mineração, call center, consultoria (software house) e metalurgia. Experiência em modernização de backoffices, desenvolvimento de RPAs e aplicações em nuvem (Azure, AWS, Copilot Studio). Grande facilidade em traduzir necessidades de negócio em soluções técnicas robustas e escaláveis, com forte conhecimento em integração de tecnologias. Perfil movido a desafios, resiliente, colaborativo, com foco em solução de problemas e atendimento ao cliente.

---

## FORMAÇÃO ACADÊMICA

<!-- Confirme os dados abaixo. "Cursando" é crítico — evita que o LLM trate como concluído. -->

| Grau | Instituição | Curso | Situação | Ano de conclusão |
|------|-------------|-------|----------|-----------------|
| Bacharelado | Anhanguera | Ciências de Dados | **CURSANDO** | Previsão 02/2027 |
| Bacharelado | Universidade de São Paulo (USP) | Física | Concluído | 1998 (início 1994) |
| Pós-graduação | UFABC | Engenharia em Gestão de Projetos | Concluído | 2015 |

<!-- NOTA: Bacharelado em Física pela USP e o Nanodegree de IA da Udacity (ver seção Certificações)
     apareciam no LinkedIn mas estavam ausentes deste arquivo até 22/08/2026. Confirmados
     diretamente pelo usuário e incluídos. A previsão de conclusão da Anhanguera é 02/2027 —
     o LinkedIn hoje mostra "jun/2029" por erro de preenchimento e precisa ser corrigido lá. -->

---

## CERTIFICAÇÕES

<!-- 
  ATENÇÃO: Revise cada item. Marque com ✅ se confirmado, ❌ se falso/não possui, 🔄 se em andamento.
  O LLM não deve inventar nem omitir certificações desta lista.
-->

| Status | Nome da Certificação | Emissor | Ano |
|--------|---------------------|---------|-----|
| ✅ | Microsoft Certified: Power Platform Developer Associate (PL-400) — **emitida 04/2025, EXPIRADA em 04/2026, renovação pendente** | Microsoft | 2025 |
| ✅ | Microsoft Certified: Azure AI Fundamentals (AI-900) | Microsoft | 2025 |
| ✅ | Microsoft Certified: Dynamics 365 Fundamentals (CRM) (MB-910) | Microsoft | 2023 |
| ✅ | Microsoft Certified: Power Platform Fundamentals (PL-900) | Microsoft | 2023 |
| ✅ | Microsoft Certified Technology Specialist: Dynamics CRM 2011 Customization and Configuration | Microsoft | 2013 |
| ✅ | AI Nanodegree | Udacity | 2019 |
| 🔄 A CONFIRMAR | Databricks Fundamentals | Databricks | 2025 |
| 🔄 A CONFIRMAR | AI Agent Fundamentals | Databricks | 2025 |
| 🔄 A CONFIRMAR | Software Engineer (credencial) | HackerRank | 2026 |
| 🔄 A CONFIRMAR | Reinvente seu Trabalho e Carreira com Hacks de IA para Produtividade / Inteligência Artificial: Desafios e Oportunidades para Líderes / Fundamentos de HTTP para Desenvolvedores / Como Escrever Artigos com Maestria / Introdução à Inteligência Artificial (cursos curtos) | LinkedIn Learning | 2025 |

<!-- As linhas "🔄 A CONFIRMAR" vieram do LinkedIn público do usuário (aba Certificações) e não
     estavam neste arquivo. Foram adicionadas para visibilidade do pipeline, mas NÃO devem ser
     tratadas como ✅ confirmadas até o usuário revisar e trocar o status. -->

---

## EXPERIÊNCIA PROFISSIONAL

<!-- 
  Para cada empresa: confirme cargo, datas e bullets.
  Adicione bullets que faltam; delete ou mova para "NÃO INCLUIR" o que for falso.
  Formato de data: MM/AAAA. "Atual" para emprego corrente.
-->

---

### R238
- **Cargo:** Founder - Desenvolvedor especialista em IA
- **Período:** 03/2025 – Atual
- **Regime:** Sócio
- **Local:** Remoto
- **Atividades e resultados:**

Cloud & Arquitetura Serverless (AWS)
Desenhei e operei arquitetura serverless multi-Lambda em produção (região sa-east-1), com mais de 10 funções Lambda independentes cobrindo geração de conteúdo, curadoria, postagem, limpeza de dados e trading — cada uma com responsabilidade única e agendamento próprio via EventBridge (cron rules, incluindo janelas horárias específicas e recorrência de 3 em 3 horas).
Padronizei IAM com role compartilhada (brigitte-lambdas) e políticas de menor privilégio (managed + inline policies segregadas por recurso — S3, Secrets Manager, DynamoDB), evitando a explosão de roles por função e reduzindo superfície de ataque.
Centralizei segredos em um único AWS Secrets Manager secret por domínio (brigitte/config) consumido por todas as Lambdas via módulo compartilhado, eliminando custo recorrente de secrets duplicados e reduzindo risco de rotação inconsistente de credenciais.
Implementei Infraestrutura como Código com Terraform para provisionamento de Lambdas, tabelas DynamoDB e recursos associados, versionando a infraestrutura junto com o código de aplicação.
Utilizei API Gateway com autenticação por API key para expor endpoints de ingestão de dados de forma segura, desacoplando produtores e consumidores do pipeline.
CI/CD & DevOps
Implementei pipeline de CI no GitHub Actions com lint automatizado (Ruff) em todo Pull Request contra a branch de integração, bloqueando merges com erros de sintaxe/import antes de revisão manual.
Construí pipeline de deploy contínuo em dois estágios (Lambdas → EC2) disparado por push na branch de produção, com dependência explícita entre jobs (o deploy do EC2 só ocorre se o deploy das Lambdas for bem-sucedido).
Adotei autenticação via OIDC (OpenID Connect) entre GitHub Actions e AWS — o runner assume uma IAM Role temporária via JWT assinado, eliminando o uso de credenciais estáticas (access keys) armazenadas em secrets, reduzindo risco de vazamento de credenciais de longa duração.
Automatizei deploy remoto via SSH (chave privada gerenciada como GitHub Secret) para atualização de workloads legadas em EC2, com fallback documentado.
Cada domínio Lambda mantém build script próprio (empacotamento de ZIP com dependências) e Terraform dedicado, permitindo deploys granulares e independentes por função sem acoplamento entre domínios.
Dev IA-First / Engenharia de IA Generativa
Orquestrei múltiplos modelos de LLM em produção, escolhidos deliberadamente por tarefa: Gemini 2.5 Flash (geração de ideias, curadoria de notícias com grounding via Google Search), Claude Sonnet via SDK Anthropic (reescrita de conteúdo com aderência estrita a formato/limite de caracteres e output JSON estruturado), e Grok/xAI (geração de textos para agentes de trading).
Documentei e justifiquei formalmente decisões de migração entre modelos (ex.: troca de modelo por fidelidade de formato e resposta JSON limpa), com rastreamento em issue tracker (Linear) — prática de engenharia, não uso ad-hoc de IA.
Construí pipelines de conteúdo com curadoria humana no loop (human-in-the-loop): IA gera rascunhos, curadoria manual aprova/rejeita em banco editorial (Notion como CMS via API REST), e só então a IA reescreve/expande e publica — reduzindo risco de conteúdo de baixa qualidade indo ao ar de forma autônoma.
Apliquei engenharia de prompt orientada a contrato de dados: parsing defensivo de saída de modelo (remoção de blocos markdown json, validação de schema antes de persistir), tratando LLM como componente não-determinístico de um pipeline determinístico.
Projetei um pipeline de sinalização de tendências (Trend Signal) com múltiplas fontes (Google Trends via scraping não-oficial com fallback resiliente, Reddit API via OAuth) convergindo em um motor de curadoria por IA que pontua e filtra sinais por score de relevância antes de virarem pauta editorial.
Bancos de Dados & Modelagem de Dados
Modelei e mantive schema em PostgreSQL (RDS) para pipeline de ETL, com tabelas multi-tenant (tenant_id) e particionamento lógico por schema de domínio.
Introduzi DynamoDB como primeiro uso de banco NoSQL no ecossistema, com decisão de arquitetura documentada: escolhido especificamente por permitir queries repetidas de "top-N por partição" via Global Secondary Index, mais baratas e rápidas que scans em data lake S3 — e por TTL nativo para expiração automática de dados (60 dias), evitando job de limpeza manual.
Operei S3 como data lake particionado por data (raw/.../YYYY/MM/DD/), com camadas distintas para dados brutos, estado de aplicação e artefatos gerados (imagens, ZIPs de deploy).
Utilizei Notion como banco de dados editorial via API REST (não SDK) para curadoria humana, com convenções de schema (paragraphs coloridos como metadados) consumidas programaticamente por múltiplos processos.
Projetei tabelas de deduplicação com TTL (DynamoDB) para evitar reprocessamento e notificações duplicadas em sistema de mensageria assíncrona.
Arquitetura Orientada a Eventos & Mensageria
Desenhei um hub de comunicação assíncrono baseado em SQS (fila principal + Dead Letter Queue após 3 falhas) para centralizar notificações de todos os agentes do ecossistema, com Lambda consumidora processando em lote (batch de 10 mensagens).
Implementei roteamento por agente e nível de severidade (info/warn retidos em janela de silêncio noturno e entregues em digest matinal agendado via EventBridge; error/critical entregues imediatamente), evitando fadiga de notificação sem perder criticidade.
Migrei agentes de notificação direta (acoplada a Slack SDK) para publish/subscribe desacoplado via fila, permitindo trocar o canal de entrega (Slack → WhatsApp/Messenger no roadmap) sem alterar código dos agentes produtores.
Agentes de Trading Algorítmico (Polymarket — ecossistema Regina)
Desenvolvi múltiplos agentes autônomos de trading (Natasha, Karoline, Kyleph, Emanuelle, Valentina) operando de forma independente sobre o mercado de predição Polymarket, cada um com estratégia e responsabilidade distintas (execução, sinalização, reconciliação de posições).
Ajustei parâmetros de take-profit com base em observação empírica de order book: identifiquei efeito manada acima de um determinado threshold de PnL (outros participantes vendendo no mesmo nível de lucro, derrubando o preço) e reduzi o gatilho de saída de 20% para 10%, com polling de monitoramento acelerado para 2 segundos — decisão de tuning documentada e rastreável, não valor arbitrário.
Implementei reconciliação periódica de posições via EventBridge (regra horária) para manter estado dos agentes consistente com o book real de mercado.
Desenhei fluxo de sinal como filtro de entrada entre agentes (saída de um agente de análise servindo como pré-condição de entrada de um agente de execução), aproximando o sistema de uma arquitetura de pipeline de decisão em camadas em vez de bots isolados.
Apliquei governança operacional deliberada: pausas programadas de agentes específicos via desativação de regras EventBridge para reavaliação de estratégia, sem necessidade de alterar ou remover código — controle de risco tratado como parâmetro operacional, não como incidente.

### BlueCX
- **Cargo:** Desenvolvedor Microsoft Dynamics
- **Período:** 04/2025 – 04/2026
- **Regime:** PJ (CNPJ próprio)
- **Local:** Remoto
- **Setor do cliente:** Cooperativa de crédito (uma das maiores do país)
- **Atividades e resultados:**
Sou responsável por manter e evoluir todo o módulo de eventos de Marketing do Dynamics 365, garantindo estabilidade e alinhamento com as áreas de negócio.

Liderei a implantação do Marketing de Evento no Dynamics 365, alcançando redução de aproximadamente 95% nos bugs reportados relacionados a esse módulo.

Automatizei a integração do Dynamics com sistemas legados via API REST, utilizando autenticação OAuth e serviços em AWS para assegurar segurança, escalabilidade e desempenho.

Treinei e mentorei 3 desenvolvedores backend para atuarem com soluções focadas em Microsoft Dynamics, disseminando boas práticas de arquitetura e desenvolvimento.

Foco principal em Azure AI Service, Azure Cognitive Services, Power Platform, Azure DataFactory e Azure Databricks.

Atuo fortemente com C# e Python em análises e extração de dados, incluindo a criação de um modelo de predição de participação em eventos para otimizar a compra de materiais e investimentos em marketing.

  **Arquitetura de IA (Microsoft/AWS):**
  - Arquitetura de soluções no ecossistema Microsoft Azure e AWS: Copilot Studio, Power Automate, Azure AI Studio, Azure OpenAI Services e serviços de DataLake.
  - Atuação como arquiteto de IA utilizando o stack disponível no Azure, migrando para papel de integrador ou desenvolvedor conforme a necessidade do projeto.

  **Integração de IA:**
  - Integração fluída entre componentes de IA: conectei o Copilot Studio a bancos de vetores (RAG) para tornar o assistente especialista no negócio do cliente.
  - Integração de Azure OpenAI Services com sistemas legados via API REST, garantindo segurança (OAuth), escalabilidade e desempenho.

  **Desenvolvimento de IA Especializada:**
  - Desenvolvimento de modelos de ML integrados ao Copilot e Azure AI para entrega de conhecimento especializado em processos de negócio e industriais — superando a limitação generalista das IAs generativas.
  - Criação de modelo de predição de participação em eventos para otimizar compra de materiais e investimentos de marketing.

  **Gestão e Governança de IA:**
  - Gestão pós-implantação: curadoria de conteúdo, métricas de uso, expansão de funcionalidades e governança de custos de componentes de IA.
  - Experiência em pivotar modelos para manter em produção a solução com melhor custo-benefício.
  - Escalabilidade de agentes: tanto agentes no Copilot Studio quanto agentes RAG operando com Azure OpenAI.

- **Tecnologias utilizadas:** Microsoft Dynamics 365, Customer Insights – Journeys, Power Platform, Copilot Studio, Azure AI Studio, Azure OpenAI Services, Azure DataFactory, Azure Databricks, Azure DataLake, C#, Python

---

### NTT DATA Europe & Latam
- **Cargo:** Arquiteto Microsoft Dynamics
- **Período:** 05/2024 – 04/2025
- **Regime:** CLT
- **Local:** Remoto – Brasil
- **Atividades e resultados:**
- **CLIENTE TIM**
• Liderança de projetos de implementação do Microsoft Dynamics 365 em grandes clientes.
• Conduzi iniciativas de integração com Azure, Power Platform e automações via IA, priorizando performance, segurança e escalabilidade. Essas ações resultaram na padronização de processos de CRM e na redução do retrabalho operacional em vendas de sistemas IoT 5G.
• Ferramenta com IA para recomendar horários e abordagens de contato com leads.

Responsável pelo desenvolvimento de softwares em JavaScript para customização do Microsoft Dynamics e pelo desenho da arquitetura de integrações entre o Dynamics e sistemas legados. Atuação ativa nos ritos do Scrum, apoiando a equipe na solução de problemas. Realização de análise de requisitos técnicos e funcionais, modelagem de dados e validação de documentação. Assegurar a aplicação de boas práticas de desenvolvimento, como TDD, BDD e CI/CD. Gerenciar a comunicação e colaboração entre equipes técnicas e não técnicas. Realizar 1:1 com liderados, visando propor melhorias contínuas nos processos e entregas do time.
- **Tecnologias utilizadas:** Microsoft Dynamics 365, JavaScript, Azure, Power Platform, Scrum, CI/CD
- **CLIENTE ITAU**
Customização do Microsoft Dynamcis para atender a área de apoio ao financiamento de veículos.




---

### Sistema Educacional Brasileiro S.A. (SEB)
- **Cargo:** Arquiteto de Soluções Dynamics e Azure
- **Período:** 06/2022 – 09/2023
- **Regime:** [PREENCHER: CLT / PJ]
- **Local:** [PREENCHER: Remoto / Presencial]
- **Atividades e resultados:**
  - Reimplantação do Microsoft Dynamics, reduzindo erros em Plugins e Flow.
  - Code Review, ritos do Scrum, análise de performance da equipe.
  - Prova de conceito das integrações e entrega de relatórios para Stakeholders e OKRs.
  - Criação de sistema de vendas de matrículas intuitivo, reduzindo burocracia de contratação de Up Selling sem necessidade dos pais comparecerem à unidade escolar.
  - Negociação de budget diretamente com stakeholders para garantir o andamento do projeto.
- **Tecnologias utilizadas:** Microsoft Dynamics 365, Azure, Power Platform, [PREENCHER]
- **Para aproximadamente 18 unidades que mantriculou 8 mil alunos** (número confirmado — ver seção "NÃO INCLUIR" sobre o número divergente de 45.000 usado hoje no LinkedIn)

---

### Adentis Portugal
- **Cargo:** Microsoft Dynamics 365 Specialist and System Architect
- **Período:** 01/2020 – 05/2022
- **Regime:** [PREENCHER: CLT / PJ / Contrato local PT]
- **Local:** Portugal (experiência no exterior)
- **Atividades e resultados:**
  - Desenvolvimento de novas funcionalidades e suporte em projetos em toda a Europa.
  - Criação de app para leitura de notas fiscais físicas usando Computer Vision, integrado a sistema de análise de risco de crédito.
- **Tecnologias utilizadas:** Microsoft Dynamics 365, Computer Vision, Azure C#]
- **Portugal, Alemanhã e Dinamarca**

---

### Algar Tech
- **Cargo:** Especialista Dynamics
- **Período:** 08/2015 – 01/2020
- **Regime:** CLT
- **Local:** Uberlândia – MG
- **Setor:** Call center / Telecomunicações
- **Atividades e resultados:**
 Resultados: 
• Revitalização completa do BackOffice com Dynamics 365;
• Desenvolvimento de ferramenta interna de RPA com .NET Core e Selenium, atendendo mais de 8 milhões de interações/mês.

Responsável por estabilizar o ambiente existente para reduzir os erros e aumentar a produtividade das equipes de Backoffice existentes no Call Center do banco Bradesco. Desenvolver uma customização padrão do Dynamics para uso em todas as operações internas da Algar visando reduzir o custo e o tempo de instalação.

Revitalização do BackOffice utilizando Dynamics da Algar Tech. Nesse projeto eu refiz toda a solução utilizada substituindo entidades personalizadas por entidades nativas da ferramenta, esse movimento elevou a confiabilidade do produto e reduziu muito o custo das melhorias seguintes.  

Ferramenta de RPA - Devido as caracteristicas de uso de multiplos sistemas em operações de backoffice a empresa tinha um elevado custo com licenciamento de ferramentas de RPA (ex: Automation Anywhere), eu recebi a missão de criar uma ferramenta internamente para minimizar esse custo então desenvolvi uma ferramenta utilizando C#, .Net Core e Selenium para esse fim, hoje a ferramenta atende um volume de aproximadamente 8 milhões de interações mensais. 

Foco principal em Azure AI Service, Azure Cognitive services, Power plataform, Azure DataFactory e Azure Databricks

Tecnologias:
Dynamics 365, Power Platform, C#, .NET Core, JavaScript, HTML5, Selenium, Azure DataLake, Azure Computer Vision, Azure Cloud Services.
- **Projetos notáveis neste período:**
  - Ferramenta de RPA Interna (ano exato: 2018)
  - Revitalização do BackOffice (ano exato: 2017)
- **Tecnologias utilizadas:** Microsoft Dynamics, .NET, C#, Selenium e uma automação proprietária para sistemas COBOL

---

### CAST Informática SA
- **Cargo:** Desenvolvedor .NET
- **Período:** 04/2014 – 08/2015
- **Local:** Presencial
- **Atividades e resultados:**
  - Atuei como terceirizado em projeto de longa duração no Ministério das Relações Exteriores, cobrindo tanto manutenção/evolução de sistemas internos quanto modernização de aplicações legadas.
  - Migrei uma aplicação legada em VB.NET/Microsoft Access para C#, com migração do banco de dados para Oracle — incluindo o levantamento da lógica de negócio da aplicação original em VB/Access antes de reescrevê-la.
  - Desenvolvi projeto de permissionamento (autenticação/autorização) usando OAuth para os sistemas internos do órgão, com C# e Angular, banco de dados SQL Server.
  - Trabalhei com bancos Oracle e SQL Server no mesmo ambiente, incluindo consultas e modelagem de dados.
- **Tecnologias utilizadas:** VB.NET, Microsoft Access, C#, Angular, Oracle, SQL Server, OAuth

---

### AlfaPeople
- **Cargo:** Arquiteto .NET
- **Período:** 02/2013 – 04/2014
- **Local:** Presencial
- **Atividades:**
  - Desenvolvi inumeros projetos de integração entre o Microsoft Dynamics 2011 e sistemas externos
  - Desenvolvi um portal de atendimento ao Cliente acoplado ao Dynamics que servia para permitir que clientes externos e internos usassem uma ferramenta para abrir e acompanhar tickets que eram tratados no dynamics. 
  - Desenvolvi uma ferramenta de importação de dados não estruturados para o microsoft dynamics
  - Ferramentas usadas: C# e Javascript

---

### L3 Informática
- **Cargo:** Arquiteto de Soluções
- **Período:** 10/2009 – 12/2012
- **Local:** Presencial
- **Atividades:**
  - - Desenvolvi inumeros projetos de integração entre o Microsoft Dynamics 2011 e sistemas externos

---

### Experiências anteriores a 2009

<!-- Se houver experiências relevantes antes de 10/2009, liste aqui. -->

- [PREENCHER ou deixar em branco]

---

## COMPETÊNCIAS TÉCNICAS

<!-- 
  Nível: Avançado / Intermediário / Básico / Não possuo (remover se não possuo)
  Não invente tecnologias — liste apenas o que você realmente usa/usou.
-->

### CRM & Microsoft Ecosystem
| Tecnologia | Nível | Observação |
|-----------|-------|------------|
| Microsoft Dynamics 365 (CRM/CE) | Avançado | |
| Power Platform (geral) | Avançado | |
| Power Automate | Avançado | |
| Power Apps | Avançado | |
| Power BI | Avançado | |
| Copilot Studio (ex-Power Virtual Agents) | Avançado | |
| Dynamics 365 Customer Insights | Avançado | |
| Dynamics 365 Customer Insights – Journeys | Avançado | |
| Dynamics 365 Finance & Operations (F&O) | [PREENCHER] | [Experiência real ou não?] |

### Linguagens de Programação
| Tecnologia | Nível | Observação |
|-----------|-------|------------|
| C# / .NET | Avançado | |
| JavaScript | Avançado | |
| TypeScript | [PREENCHER] | |
| Python | [PREENCHER: Avançado / Intermediário / Básico] | |

### Cloud & DevOps
| Tecnologia | Nível | Observação |
|-----------|-------|------------|
| Azure Functions | Avançado | |
| Azure Logic Apps | Avançado | |
| Azure DevOps | Avançado | |
| AWS | Avançado | |
| Docker | Intermediário | |
| Git / GitHub | Avançado | |
| CI/CD | Avançado | |
| TDD / BDD | Avançado | |

### Banco de Dados
| Tecnologia | Nível | Observação |
|-----------|-------|------------|
| SQL Server | Avançado | |
| [PREENCHER: outros BDs usados] | | |

### IA & Dados
| Tecnologia | Nível | Observação |
|-----------|-------|------------|
| Machine Learning (supervisionado/não supervisionado) | Avançado | Modelos de predição integrados ao Copilot e Azure AI |
| IA Generativa / LLMs | Avançado | Azure OpenAI Services, Copilot Studio, RAG com bancos de vetores |
| Agentes inteligentes | Avançado | Agentes Copilot Studio e agentes RAG com OpenAI |
| Azure AI Studio | Avançado | Arquitetura e desenvolvimento de soluções de IA |
| Azure OpenAI Services | Avançado | |
| Azure Cognitive Services | Avançado | |
| Computer Vision | Intermediário | Usado no projeto Adentis (leitura de notas fiscais) |
| Copilot Studio | Avançado | Incluindo integração com bancos de vetores para especialização de domínio |
| Azure DataLake | Avançado | |
| Azure DataFactory | Avançado | |
| Azure Databricks | Intermediário | |
| Scikit-Learn | Intermediário | |
| Pandas / NumPy | Intermediário | |

### Ferramentas
| Tecnologia | Nível | Observação |
|-----------|-------|------------|
| Visual Studio | Avançado | |
| Visual Studio Code | Avançado | |
| Selenium | Intermediário | Testes e RPA |
| Figma | Intermediário | |
| Postman / Insomnia | Intermediário | |
| React | [PREENCHER: Básico / Intermediário / Nunca usei] | |

---

## IDIOMAS

| Idioma | Nível | Observação |
|--------|-------|------------|
| Português | Nativo | |
| Inglês | B2 | Leitura, escrita e conversação |
| [PREENCHER: outros] | | |

---

## PROJETOS PESSOAIS / EXTRACURRICULARES

<!-- Liste projetos fora do emprego formal — GitHub, freelance, estudos aplicados, etc. -->

- [PREENCHER: nome do projeto, tecnologias usadas, link se houver, resultado]
- [PREENCHER]

---

## INFORMAÇÕES ADICIONAIS

- CNPJ ativo: Sim
- [PREENCHER: disponibilidade de viagem, fuso horário preferido para reuniões, etc.]

---

## ❌ NÃO INCLUIR — INFORMAÇÕES FALSAS OU IMPRECISAS

<!--
  SEÇÃO CRÍTICA: Liste aqui tudo que o LLM inventou ou distorceu e NÃO deve aparecer
  no currículo gerado. O pipeline usará esta lista como blocklist.
  
  Exemplos do que registrar:
  - Certificação que o LLM inseriu e você não possui
  - Métrica inventada (ex: "reduziu 40% o tempo de processamento" sem base real)
  - Cargo ou empresa com nome errado
  - Data errada que mudaria a leitura da sua carreira
-->

- **"45.000 matrículas anuais"** — usado hoje na seção "Sobre" do LinkedIn para o projeto SEB. O número correto e confirmado é **8 mil alunos em 18 unidades** (ver seção Experiência Profissional > SEB). Corrigir no LinkedIn.
- **Métricas do currículo `ai_engineer/resume.json` para a BlueCX**: "respostas 30% mais precisas e contextuais", "reduzindo alucinações em 25%" e "impactar mais de 500 mil clientes" — são aproximadas/não confirmadas com precisão. Por decisão do usuário (22/08/2026), o pipeline deve **suavizar essa linguagem** (ex.: "buscando reduzir alucinações via prompt engineering avançado", sem o percentual fixo) até que números exatos sejam validados. Não usar esses três percentuais/valor específicos em currículos ou no LinkedIn enquanto não confirmados.
- **Datas sobrepostas de Algar Tech / Adentis Portugal / SEB no LinkedIn** — o LinkedIn hoje mostra os três períodos se sobrepondo (ex.: SEB jan/2020–set/2023 simultâneo a Adentis jan/2021–mai/2022 e a Algar Tech ago/2015–2021). A sequência correta é a deste arquivo: Algar Tech 08/2015–01/2020 → Adentis Portugal 01/2020–05/2022 → SEB 06/2022–09/2023. Corrigir no LinkedIn.
- **Previsão de conclusão da Anhanguera (Ciências de Dados) mostrada como "jun/2029" no LinkedIn** — incorreta. A previsão correta é **02/2027** (ver Formação Acadêmica). Corrigir no LinkedIn.
- **Data de fundação da R238 mostrada como "04/2022" na versão anterior deste arquivo** — corrigida nesta revisão para **03/2025**, conforme confirmado pelo usuário e coerente com o histórico do LinkedIn.

---

<!-- 
  DICA: Após editar este arquivo, rode:
    make ingest
  para regenerar o data/resume.json com as correções aplicadas.
-->
