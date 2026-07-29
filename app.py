import streamlit as st
import pandas as pd
import numpy as np

# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA (DEVE SER A PRIMEIRA CHAMADA DO STREAMLIT)
# ==============================================================================
st.set_page_config(
    page_title="Smart CG | Diagnóstico Quantitativo de Execução Estratégica",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS personalizada
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        color: #1A365D;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4A5568;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #F7FAFC;
        border-radius: 8px;
        padding: 15px;
        border: 1px solid #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">Smart Consultoria & Governança</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Diagnóstico Objetivo de Maturidade: Governança, Projetos, Processos, Mudanças e Qualidade</p>', unsafe_allow_html=True)
st.divider()

# Sidebar: Dados do Cliente
with st.sidebar:
    st.header("📋 Identificação do Cliente")
    client_name = st.text_input("Empresa / Cliente", "Empresa Exemplo S.A.")
    industry = st.selectbox("Setor de Atuação", [
        "Construção / Engenharia",
        "Indústria",
        "Tecnologia / Logística",
        "Saúde / Hospitalar",
        "Serviços / Varejo",
        "Educação"
    ])
    consultant = st.text_input("Consultor Responsável", "Consultor Smart")
    project_scope = st.selectbox("Porte da Operação", [
        "Pequeno (Até 100 colaboradores)",
        "Médio (100 a 500 colaboradores)",
        "Grande (Acima de 500 colaboradores)"
    ])
    
    st.divider()
    st.markdown("**Alinhamento Metodológico:**")
    st.caption("• Governança: IBGC\n• Projetos: PMI\n• Processos: ABMPP / BPM\n• Gestão de Mudanças: HUCMI\n• Qualidade: QA / PDCA")

# Estrutura com 5 Perguntas por Tópico e Opções Não-Ordenadas
questions = {
    "Pilar 1: Governança Corporativa (IBGC)": [
        {
            "id": "gov_1",
            "text": "1. Qual é o grau de clareza na divisão de papéis entre Sócios, Conselho e Diretoria Executiva?",
            "options": [
                ("Existem papéis definidos informalmente, mas decisões estratégicas frequentemente travam na operação.", 2),
                ("Governança formalizada com Conselho/Comitês, alçadas transparentes e prestação de contas periódica.", 4),
                ("Não há separação; decisões estratégicas e operacionais se misturam no dia a dia.", 1),
                ("Papéis são formalizados (Estatuto/Acordo de Sócios), com reuniões periódicas de alinhamento.", 3)
            ]
        },
        {
            "id": "gov_2",
            "text": "2. Como as metas estratégicas e diretrizes da empresa são desdobradas para o nível tático/operacional?",
            "options": [
                ("Metas desdobradas por área/nível, com acompanhamento sistemático de indicadores e planos de ação.", 4),
                ("Não há metas estruturadas; a gestão reage apenas aos problemas urgentes do dia a dia.", 1),
                ("Existem metas gerais definidas pela diretoria, mas elas não chegam formalmente às equipes.", 2),
                ("Metas são desdobradas anualmente, mas o acompanhamento é esporádico e sem cobrança rígida.", 3)
            ]
        },
        {
            "id": "gov_3",
            "text": "3. Como a organização gerencia riscos de negócio, conformidade e diretrizes éticas?",
            "options": [
                ("Gestão informal focada em exigências básicas (fiscais/trabalhistas) quando cobradas.", 2),
                ("Matriz de Riscos atualizada, compliance estruturado e código de conduta amplamente disseminado.", 4),
                ("Inexistente; riscos são tratados apenas quando viram crises ou prejuízos reais.", 1),
                ("Mapeamento dos principais riscos operacionais/financials com controles internos básicos implementados.", 3)
            ]
        },
        {
            "id": "gov_4",
            "text": "4. Qual é a frequência e a estrutura dos ritos de prestação de contas (reuniões de resultados)?",
            "options": [
                ("Reuniões mensais/trimestrais estruturadas com atas, deliberações e acompanhamento de planos prévios.", 4),
                ("Reuniões pontuais apenas quando surgem problemas graves ou resultados financeiros ruins.", 1),
                ("Encontros informais entre diretores sem pauta fixa ou registro de decisões e compromissos.", 2),
                ("Reuniões mensais com pauta definida, porém sem acompanhamento rígido das ações combinadas.", 3)
            ]
        },
        {
            "id": "gov_5",
            "text": "5. Como é feita a tomada de decisão para investimentos e expansão do negócio?",
            "options": [
                ("Decisões baseadas no 'feeling' do fundador/sócio, sem análise formal de viabilidade.", 1),
                ("Análise financeira básica, mas com forte peso da intuição e pouca consulta à estrutura tática.", 2),
                ("Estudos de viabilidade técnica/financeira realizados para grandes investimentos.", 3),
                ("Comitê formal de aprovação, modelos de valuation/ROI rigorosos e alinhamento total ao planejamento estratégico.", 4)
            ]
        }
    ],
    "Pilar 2: Gestão de Projetos & PMO (PMI)": [
        {
            "id": "proj_1",
            "text": "1. Como os projetos estratégicos e de melhoria são planejados e executados?",
            "options": [
                ("Há metodologia definida para grandes projetos (escopo, cronograma, custo), mas com adesão parcial.", 3),
                ("Usa-se planilhas básicas ou listas de tarefas, mas prazos e custos frequentemente estouram.", 2),
                ("Metodologia padrão institucionalizada (Ágil/Híbrida), com baseline rigoroso e baixo nível de desvios.", 4),
                ("Não há padrão; cada profissional ou área gerencia projetos do seu próprio jeito.", 1)
            ]
        },
        {
            "id": "proj_2",
            "text": "2. Qual é a visibilidade da alta liderança sobre a carteira total de projetos da empresa?",
            "options": [
                ("Dashboards em tempo real (PMO Centralizado) com visibilidade total de prazos, custos e riscos.", 4),
                ("Status dos projetos só é conhecido quando ocorrem atrasos críticos ou estouro de orçamento.", 1),
                ("Relatórios de status formais (Status Report) são gerados periodicamente para a diretoria.", 3),
                ("Cobranças pontuais em reuniões longas e desestruturadas sem relatórios consolidados.", 2)
            ]
        },
        {
            "id": "proj_3",
            "text": "3. Como a empresa gerencia a capacidade de alocação de recursos/pessoas nos projetos?",
            "options": [
                ("Alocação feita no 'feeling'; prioridades mudam a todo momento gerando sobrecarga e retrabalho.", 2),
                ("Equipes ficam recorrentemente sobrecarregadas, sem qualquer controle de capacidade ou horas.", 1),
                ("Gestão da capacidade de recursos (Resource Management) estruturada e alinhada à priorização da estratégia.", 4),
                ("Existe controle básico de recursos, mas conflitos de agenda entre projetos e rotina operacional são comuns.", 3)
            ]
        },
        {
            "id": "proj_4",
            "text": "4. Como são tratados os desvios de escopo, prazo e orçamento durante a execução?",
            "options": [
                ("Mudanças são aceitas informalmente sem análise de impacto, estourando prazos e custos.", 1),
                ("Geralmente percebe-se o atraso no final; faz-se mutirão para tentar entregar com perda de qualidade.", 2),
                ("Desvios são negociados formalmente com os patrocinadores (sponsors) antes de alterar as entregas.", 3),
                ("Processo rigoroso de controle de mudanças (CCB), avaliando impactos e replanejando baselines em tempo hábil.", 4)
            ]
        },
        {
            "id": "proj_5",
            "text": "5. Qual é o grau de encerramento formal e registro de lições aprendidas nos projetos?",
            "options": [
                ("Projeto encerra e a equipe é desmontada imediatamente; o mesmo erro se repete no projeto seguinte.", 1),
                ("Avaliação final informal apenas quando o projeto é considerado um fracasso.", 2),
                ("Relatório básico de encerramento gerado para os projetos de grande porte.", 3),
                ("Rito formal de encerramento, registro estruturado de lições aprendidas e repositório consultável.", 4)
            ]
        }
    ],
    "Pilar 3: Gestão de Processos & BPM (ABMPP)": [
        {
            "id": "proc_1",
            "text": "1. Qual é o nível de padronização e documentação dos processos operacionais críticos?",
            "options": [
                ("Processos-chave mapeados e documentados (Fluxogramas/BPMN), com treinamento de equipes.", 3),
                ("Conhecimento está 'na cabeça' das pessoas (se alguém chave sai, a operação sofre gravemente).", 1),
                ("Arquitetura de processos atualizada, com donos de processo (Process Owners) e melhoria contínua.", 4),
                ("Existem Procedimentos Operacionais Padrão (POPs) antigos ou desatualizados que pouca gente consulta.", 2)
            ]
        },
        {
            "id": "proc_2",
            "text": "2. Qual é a incidência de gargalos, retrabalho e falhas na transição entre departamentos (passagem de bastão)?",
            "options": [
                ("Elevada; retrabalho é diário, áreas acusam umas às outras e o cliente final percebe as falhas.", 1),
                ("Baixa; fluxo contínuo de valor otimizado, sem gargalos críticos e com mentalidade Lean.", 4),
                ("Frequente; as áreas funcionam como 'silos' e a passagem de bastão entre departamentos falha.", 2),
                ("Moderada; problemas pontuais ocorrem, mas são identificados e corrigidos com razoável agilidade.", 3)
            ]
        },
        {
            "id": "proc_3",
            "text": "3. Como a tecnologia e os sistemas de informação estão integrados às rotinas de processo?",
            "options": [
                ("Uso intensivo de planilhas paralelas e retrabalho de digitação manual entre sistemas diferentes.", 2),
                ("Processos automatizados com workflows digitais integrados, eliminando tarefas manuais repetitivas.", 4),
                ("Sistemas centrais (ERP/CRM) cobrem as etapas principais, mas ainda há lacunas com papel/planilhas.", 3),
                ("Processos extremamente manuais, baseados em papel, fichas físicas ou trocas infinitas de e-mail.", 1)
            ]
        },
        {
            "id": "proc_4",
            "text": "4. Existe uma rotina contínua de medição e análise de indicadores de processos (KPIs operacionais)?",
            "options": [
                ("Não há medição; indicadores só são olhados no balanço financeiro final do mês/ano.", 1),
                ("Controle pontual de volume ou entregas em planilhas individuais dos gestores.", 2),
                ("Indicadores operacionais definidos para as principais áreas com acompanhamento mensal.", 3),
                ("Painéis digitais de acompanhamento em tempo real, com metas de eficiência e SLA por processo.", 4)
            ]
        },
        {
            "id": "proc_5",
            "text": "5. Como são implementadas melhorias ou otimizações nos processos de trabalho?",
            "options": [
                ("Melhorias surgem como 'gambiarras' ou arranjos temporários feitos pelos próprios operadores.", 1),
                ("Alterações são feitas apenas quando ocorre uma crise operacional grave.", 2),
                ("Projetos pontuais de melhoria são conduzidos quando demandados pela gerência.", 3),
                ("Cultura de melhoria contínua (Kaizen/Lean), com programa estruturado de sugestões e otimização.", 4)
            ]
        }
    ],
    "Pilar 4: Gestão de Mudanças Organizacionais - GMO (HUCMI)": [
        {
            "id": "chg_1",
            "text": "1. Como as equipes reagem quando a empresa implementa novos sistemas, processos ou reestruturações?",
            "options": [
                ("Adesão razoável após algum tempo de desgaste, atrito e esforço excessivo da liderança.", 3),
                ("Adesão lenta e passiva; as mudanças demoram muito para trazer os resultados esperados.", 2),
                ("Resistência intensa e velada; colaboradores tendem a burlar o novo padrão e voltar ao 'jeito antigo'.", 1),
                ("Cultura ágil e receptiva; mudanças são absorvidas rapidamente com alto engajamento das pessoas.", 4)
            ]
        },
        {
            "id": "chg_2",
            "text": "2. Qual é a estrutura de Comunicação e Treinamento adotada nos projetos de transformação?",
            "options": [
                ("Estratégia completa de GMO: Análise de Impactos, Matriz de Stakeholders, Plano de Comunicação e Capacitação.", 4),
                ("Comunicação informal (e-mails pontuais) e treinamento focado apenas no uso técnico da ferramenta.", 2),
                ("Não há plano; comunicações são feitas em cima da hora e treinamentos são rasos/superficiais.", 1),
                ("Plano de comunicação estruturado e capacitação formal antes da entrada em operação.", 3)
            ]
        },
        {
            "id": "chg_3",
            "text": "3. Qual é o comportamento da liderança média (gerentes/coordenadores) durante mudanças operacionais?",
            "options": [
                ("Líderes cobram a mudança, mas não servem de exemplo ou se omitem na gestão do fator humano.", 2),
                ("Líderes atuam ativamente como patrocinadores (Sponsors) e agentes condutores da transformação.", 4),
                ("Líderes demonstram ceticismo ou criticam abertamente as novas diretrizes para suas equipes.", 1),
                ("Líderes apoiam formalmente e incentivam suas equipes a adotar as novas práticas.", 3)
            ]
        },
        {
            "id": "chg_4",
            "text": "4. Como a organização identifica e trata os impactos e medos individuais gerados por novas tecnologias/processos?",
            "options": [
                ("Mapeamento prévio de impactos por função, com planos de mitigação e acolhimento das angústias.", 4),
                ("Impactos são ignorados; assume-se que as pessoas 'têm obrigação de se adaptar'.", 1),
                ("Conversas pontuais são feitas apenas com as pessoas que demonstram resistência declarada.", 2),
                ("Reuniões de alinhamento são feitas para explicar o motivo da mudança e esclarecer dúvidas.", 3)
            ]
        },
        {
            "id": "chg_5",
            "text": "5. Qual é o nível de sustentação e acompanhamento após a implantação das mudanças (Go-Live)?",
            "options": [
                ("Equipe de projeto sai imediatamente e o processo/sistema é abandonado aos poucos pelas pessoas.", 1),
                ("Suporte básico focado apenas em resolver dúvidas técnicas do sistema.", 2),
                ("Acompanhamento por alguns dias até estabilização inicial dos indicadores.", 3),
                ("Plano de sustentação estruturado, com monitoramento de taxa de adesão, reforço de treinos e reconhecimento.", 4)
            ]
        }
    ],
    "Pilar 5: Garantia da Qualidade & QA": [
        {
            "id": "qa_1",
            "text": "1. Como a empresa garante a qualidade dos produtos, serviços ou entregas antes que cheguem ao cliente final?",
            "options": [
                ("Checklists formais de validação e critérios de aceite claros definidos antes da liberação.", 3),
                ("Garantia da Qualidade (QA) integrada em todas as fases, com auditorias preventivas e testes rigorosos.", 4),
                ("Não há validação formal; os testes ocorrem 'na prática' (o próprio cliente identifica as falhas).", 1),
                ("Verificação visual e pontual no final do processo, sem amostragem ou critérios padronizados.", 2)
            ]
        },
        {
            "id": "qa_2",
            "text": "2. Qual é a postura da empresa diante de não-conformidades, falhas recorrentes e reclamações?",
            "options": [
                ("Erros são corrigidos pontualmente, mas sem investigação detalhada das causas raízes.", 2),
                ("Ciclo PDCA/Análise de Causa Raiz aplicado sistematicamente, prevenindo a reincidência dos erros.", 4),
                ("Apenas 'apaga-se o incêndio'; o mesmo erro se repete várias vezes ao longo do ano.", 1),
                ("Existe registro formal de Não-Conformidades (RNC) e planos de ação para os problemas graves.", 3)
            ]
        },
        {
            "id": "qa_3",
            "text": "3. Como a satisfação e percepção de valor do cliente final são monitoradas?",
            "options": [
                ("Não há pesquisa; só sabemos se o cliente reclama formalmente ou cancela o contrato.", 1),
                ("Feedback colhido de forma informal ou esporádica pelos vendedores/atendentes.", 2),
                ("Pesquisa de satisfação realizada periodicamente (ex: NPS), mas com pouca ação sobre as notas baixas.", 3),
                ("Pesquisa contínua de NPS/CSAT com fluxo automático de tratativa (Fechamento de Loop) para insatisfeitos.", 4)
            ]
        },
        {
            "id": "qa_4",
            "text": "4. Qual é o grau de conformidade e auditoria interna sobre o cumprimento dos padrões estabelecidos?",
            "options": [
                ("Inexistente; não há qualquer checagem se o padrão está sendo cumprido.", 1),
                ("Avisos verbais ocorrem quando o gestor presencia o descumprimento de alguma regra.", 2),
                ("Auditorias internas ou verificações periódicas são realizadas em amostras de entregas.", 3),
                ("Programa de Auditoria Interna estruturado, com métricas de adesão por setor e planos de adequação.", 4)
            ]
        },
        {
            "id": "qa_5",
            "text": "5. Como os fornecedores e parceiros críticos são avaliados quanto à qualidade das entregas?",
            "options": [
                ("Não há avaliação; a compra é decidida apenas pelo menor preço.", 1),
                ("Fornecedores ruins são substituídos apenas quando cometem falhas gravíssimas.", 2),
                ("Existe cadastro homologado e avaliação básica de prazo e preço nas compras.", 3),
                ("Programa de Homologação e Avaliação Periódica de Desempenho de Fornecedores (IQF) estruturado.", 4)
            ]
        }
    ]
}

# Navegação do App
tab_diag, tab_report = st.tabs(["📝 Formulario de Diagnóstico (25 Perguntas)", "📊 Relatório Executivo & Recomendações"])

scores = {}

with tab_diag:
    st.markdown("### Questionário Objetivo de Maturidade Operacional e Gestão")
    st.write("Selecione a opção que reflete com mais precisão o cenário atual da organização. A pontuação é calculada automaticamente.")
    
    with st.form("diagnostic_form"):
        for pillar_name, q_list in questions.items():
            with st.expander(f"📌 {pillar_name}", expanded=True):
                pillar_scores = []
                for q in q_list:
                    labels = [opt[0] for opt in q["options"]]
                    choice = st.radio(
                        q["text"],
                        options=labels,
                        key=q["id"]
                    )
                    score_val = [opt[1] for opt in q["options"] if opt[0] == choice][0]
                    pillar_scores.append(score_val)
                
                raw_avg = np.mean(pillar_scores)
                norm_score = round(((raw_avg - 1) / 3) * 4 + 1, 2)
                scores[pillar_name] = norm_score

        submit_btn = st.form_submit_button("Calcular Maturidade e Gerar Relatório Executivo 🚀")

# ==============================================================================
# LÓGICA DE PESOS DINÂMICOS BASEADA NO SETOR E PORTE
# ==============================================================================
# Ordem dos pilares: [Gov, Proj, Proc, Chg, QA]
if industry in ["Construção / Engenharia", "Indústria"]:
    # Enfase em Processos e Qualidade
    weights = [0.15, 0.20, 0.30, 0.15, 0.20]
elif industry in ["Tecnologia / Logística"]:
    # Ênfase em Projetos e Mudança Organizacional
    weights = [0.15, 0.30, 0.20, 0.20, 0.15]
elif industry in ["Saúde / Hospitalar"]:
    # Ênfase em Qualidade, Processos e Governança
    weights = [0.20, 0.15, 0.25, 0.15, 0.25]
else:
    # Padrão balanceado para Serviços, Varejo, Educação
    weights = [0.15, 0.25, 0.25, 0.20, 0.15]

# Atribuição de Notas Consolidadas
score_gov = scores.get("Pilar 1: Governança Corporativa (IBGC)", 1.0)
score_proj = scores.get("Pilar 2: Gestão de Projetos & PMO (PMI)", 1.0)
score_proc = scores.get("Pilar 3: Gestão de Processos & BPM (ABMPP)", 1.0)
score_chg = scores.get("Pilar 4: Gestão de Mudanças Organizacionais - GMO (HUCMI)", 1.0)
score_qa = scores.get("Pilar 5: Garantia da Qualidade & QA", 1.0)

pill_scores = [score_gov, score_proj, score_proc, score_chg, score_qa]
overall_score = sum(s * w for s, w in zip(pill_scores, weights))
execution_readiness_pct = round(((overall_score - 1) / 4) * 100, 1)

with tab_report:
    st.markdown(f"## 📊 Relatório Executivo de Diagnóstico: {client_name}")
    st.caption(f"**Setor:** {industry} | **Porte:** {project_scope} | **Consultor:** {consultant}")
    st.divider()

    # Cards de KPIs
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Índice de Prontidão para Execução", f"{execution_readiness_pct}%")
    with col2:
        if execution_readiness_pct < 45:
            status = "🔴 Crítico (Alto Risco de Fracasso)"
        elif execution_readiness_pct < 75:
            status = "🟡 Moderado (Risco de Gargalos)"
        else:
            status = "🟢 Avançado (Pronto para Alta Performance)"
        st.metric("Status da Operação", status)
    with col3:
        lowest_pillar = min(scores, key=scores.get)
        st.metric("Gargalo Principal", lowest_pillar.split(":")[1].split("(")[0].strip())

    st.subheader("1. Maturidade Calculada por Pilar (Ajustada ao Setor)")
    
    # Tabela de Resultados Dinâmica
    formatted_weights = [f"{int(w*100)}%" for w in weights]
    df_scores = pd.DataFrame({
        "Pilar de Atuação Smart": [p.split(":")[1].strip() for p in scores.keys()],
        "Nota Obtida (1-5)": list(scores.values()),
        "Nível Operacional": [
            "Inexistente / Reativo" if v < 2.2 else "Parcial / Informal" if v < 3.5 else "Padronizado / Estruturado" if v < 4.5 else "Otimizado / Referência"
            for v in scores.values()
        ],
        "Peso Estratégico (Ponderado)": formatted_weights
    })
    st.dataframe(df_scores, use_container_width=True)

    st.subheader("2. Análise Técnica de Gargalos Operacionais")
    
    # Alertas genéricos por nota
    if score_proj < 3.0 or score_proc < 3.0:
        st.error("""
        **🚨 Alerta de Gargalo Operacional (Execução em Risco):**
        A organização apresenta fragilidades no acompanhamento de projetos ou na padronização de processos.
        Iniciativas estratégicas tendem a sofrer estouros orçamentários, atrasos e alto volume de retrabalho.
        """)
    
    if score_chg < 3.0:
        st.warning("""
        **⚠️ Alerta de Fator Humano e Gestão de Mudança (GMO):**
        Baixa capacidade de absorção cultural para novos sistemas e metodologias. Alto risco de resistência passiva.
        """)

    # Alerta específico adaptado ao SETOR
    if industry in ["Construção / Engenharia", "Indústria"] and (score_proc < 3.5 or score_qa < 3.5):
        st.error(f"**🏭 Sensibilidade Setorial ({industry}):** A baixa padronização de processos ou controle de qualidade em operações intensivas gera forte margem de desperdício financeiro e falhas diretas em canteiros/linhas de produção.")
    elif industry in ["Tecnologia / Logística"] and score_proj < 3.5:
        st.error(f"**⚡ Sensibilidade Setorial ({industry}):** A falta de rigor no PMO prejudica diretamente a capacidade de entrega no prazo (SLA) e gera estouro contínuo na capacidade das equipes.")

    st.subheader("3. Escopo Comercial Recomendado (Atuação Smart CG)")
    
    # Recomendações adaptadas ao PORTE DA EMPRESA
    is_large = "Grande" in project_scope
    is_medium = "Médio" in project_scope
    
    recs = []
    if score_gov < 3.8:
        tag = "Enterprise (Governança Corporativa e Conselho)" if is_large else "Estruturação de Ritos e Alçadas"
        recs.append(f"• **Governança & Ritos de Gestão - {tag}:** Implementação de Matriz RACI, acionamento de comitês executivos e rituais formais de acompanhamento de resultados.")
        
    if score_proj < 3.8:
        tag = "PMO Corporativo / EPM" if is_large else ("PMO Tático de Projetos" if is_medium else "PMO Enxuto / Ágil")
        recs.append(f"• **Estruturação de PMO ({tag}):** Padronização do ciclo de vida dos projetos, visibilidade executiva em tempo real e treinamento de gestores.")
        
    if score_proc < 3.8:
        tag = "Arquitetura e Automação BPMN" if is_large else "Mapeamento e Otimização AS-IS / TO-BE"
        recs.append(f"• **Mapeamento & Otimização de Processos ({tag}):** Mapeamento de fluxos críticos, eliminação de gargalos/retrabalho e definição de POPs/workflows.")
        
    if score_chg < 3.8:
        recs.append("• **Plano Integrado de Gestão de Mudanças (HUCMI):** Análise de impactos por função, matriz de stakeholders e plano de comunicação/capacitação.")
        
    if score_qa < 3.8:
        recs.append("• **Garantia da Qualidade (QA & PDCA):** Implantação de auditorias internas de processo, tratamento de RNC (causa raiz) e rotinas de melhoria.")

    for r in recs:
        st.write(r)

    st.divider()
    st.caption("Aplicação desenvolvida para diagnóstico comercial e técnico da Smart Consultoria & Governança.")
