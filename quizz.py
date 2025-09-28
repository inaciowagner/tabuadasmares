import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random # Importação adicionada para embaralhar as questões

# --- Configuração da Página e Estilos ---

# Configuração da página
st.set_page_config(
    page_title="Quiz Político - Descubra sua Posição",
    page_icon="🏛️",
    layout="wide"
)

# Estilo CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-card {
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        color: #333333;  /* Texto escuro para melhor contraste */
    }
    .result-card h2, .result-card h3, .result-card p {
        color: #333333;  /* Garante que todos os textos fiquem escuros */
    }
    .result-card strong {
        color: #000000;  /* Texto mais escuro para elementos strong */
    }
    .left-wing {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        color: #333333;
    }
    .center-wing {
        background-color: #f3e5f5;
        border-left: 5px solid #9c27b0;
        color: #333333;
    }
    .right-wing {
        background-color: #e8f5e8;
        border-left: 5px solid #4caf50;
        color: #333333;
    }
    /* Estilo específico para textos dentro dos cards */
    .result-card h2 {
        color: #1a1a1a !important;
        margin-bottom: 1rem;
    }
    .result-card h3 {
        color: #2d2d2d !important;
        margin-bottom: 0.5rem;
    }
    .result-card p {
        color: #333333 !important;
        margin-bottom: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Sistema de Perguntas e Pontuação ---

# A lista original de perguntas é mantida aqui, mas será embaralhada na função main()
QUESTIONS_LIST = [
    {
        "id": 1,
        "question": "Qual é a sua visão sobre o papel do Estado na economia?",
        "options": {
            "O Estado deve controlar os meios de produção": {"eixo": "economia", "valor": -2},
            "O Estado deve regular fortemente a economia": {"eixo": "economia", "valor": -1},
            "Estado e mercado devem coexistir com regulamentação moderada": {"eixo": "economia", "valor": 0},
            "O Estado deve intervir minimamente na economia": {"eixo": "economia", "valor": 1},
            "O mercado deve ser completamente livre": {"eixo": "economia", "valor": 2}
        }
    },
    {
        "id": 2,
        "question": "Como você vê as políticas sociais e direitos civis?",
        "options": {
            "Devemos promover mudanças radicais e quebrar estruturas tradicionais": {"eixo": "social", "valor": -2},
            "Devemos avançar rapidamente em direção a maior igualdade social": {"eixo": "social", "valor": -1},
            "Devemos buscar equilíbrio entre progresso e tradição": {"eixo": "social", "valor": 0},
            "Devemos preservar valores e estruturas tradicionais": {"eixo": "social", "valor": 1},
            "Devemos retornar a valores tradicionais e hierarquias naturais": {"eixo": "social", "valor": 2}
        }
    },
    {
        "id": 3,
        "question": "Qual é sua posição sobre propriedade privada?",
        "options": {
            "A propriedade privada deve ser abolida": {"eixo": "economia", "valor": -2},
            "Propriedade coletiva deve predominar sobre a privada": {"eixo": "economia", "valor": -1},
            "Devem coexistir propriedade pública e privada": {"eixo": "economia", "valor": 0},
            "Propriedade privada com algumas limitações sociais": {"eixo": "economia", "valor": 1},
            "Propriedade privada deve ser absoluta e irrestrita": {"eixo": "economia", "valor": 2}
        }
    },
    {
        "id": 4,
        "question": "Como você vê a organização do poder político?",
        "options": {
            "Devemos abolir completamente o Estado": {"eixo": "social", "valor": -2},
            "Poder deve ser radicalmente descentralizado e comunitário": {"eixo": "social", "valor": -1},
            "Devemos equilibrar democracia representativa com participativa": {"eixo": "social", "valor": 0},
            "Estado forte com democracia representativa": {"eixo": "social", "valor": 1},
            "Estado muito forte com liderança autoritária": {"eixo": "social", "valor": 2}
        }
    },
    {
        "id": 5,
        "question": "Qual é sua visão sobre justiça social e desigualdade?",
        "options": {
            "Devemos eliminar completamente as classes sociais": {"eixo": "economia", "valor": -2},
            "Redistribuição radical de riqueza através de impostos progressivos": {"eixo": "economia", "valor": -1},
            "Políticas sociais moderadas para reduzir desigualdades": {"eixo": "economia", "valor": 0},
            "Oportunidades iguais, mas aceitação de desigualdades naturais": {"eixo": "economia", "valor": 1},
            "Desigualdade é natural e necessária para o progresso": {"eixo": "economia", "valor": 2}
        }
    },
    {
        "id": 6,
        "question": "Como você vê questões de identidade nacional e imigração?",
        "options": {
            "Abolir fronteiras e nações": {"eixo": "social", "valor": -2},
            "Multiculturalismo radical e fronteiras abertas": {"eixo": "social", "valor": -1},
            "Políticas equilibradas de imigração com integração": {"eixo": "social", "valor": 0},
            "Preservação cultural e controle de imigração": {"eixo": "social", "valor": 1},
            "Nacionalismo forte e restrição total da imigração": {"eixo": "social", "valor": 2}
        }
    },
    {
        "id": 7,
        "question": "Qual é sua posição sobre serviços públicos?",
        "options": {
            "Todos os serviços devem ser públicos e gratuitos": {"eixo": "economia", "valor": -2},
            "Estado de bem-estar social amplo com serviços públicos majoritários": {"eixo": "economia", "valor": -1},
            "Mistura de serviços públicos e privados": {"eixo": "economia", "valor": 0},
            "Serviços privados com algum apoio estatal": {"eixo": "economia", "valor": 1},
            "Privatização total de todos os serviços": {"eixo": "economia", "valor": 2}
        }
    },
    {
        "id": 8,
        "question": "Como você vê a relação entre religião e Estado?",
        "options": {
            "Religião deve ser completamente abolida": {"eixo": "social", "valor": -2},
            "Estado laico radical com separação completa": {"eixo": "social", "valor": -1},
            "Estado laico com respeito às tradições religiosas": {"eixo": "social", "valor": 0},
            "Estado com influência de valores religiosos tradicionais": {"eixo": "social", "valor": 1},
            "Estado baseado em princípios religiosos": {"eixo": "social", "valor": 2}
        }
    }
]

# Sistema de classificação (mantido o original)
ideologies = {
    "Socialista": {"economia": [-2, -1], "social": [-2, 0]},
    "Comunista": {"economia": [-2, -2], "social": [-2, -1]},
    "Anarquista": {"economia": [-2, 0], "social": [-2, -2]},
    "Social Democrata": {"economia": [-1, 0], "social": [-1, 1]},
    "Social Liberal": {"economia": [0, 1], "social": [-1, 1]},
    "Centrista": {"economia": [-0.5, 0.5], "social": [-0.5, 0.5]},
    "Liberal": {"economia": [1, 2], "social": [-1, 1]},
    "Conservador": {"economia": [0, 2], "social": [1, 2]},
    "Fascista": {"economia": [0, 2], "social": [2, 2]}
}

# --- Funções de Lógica de Negócio ---

def calculate_results(answers):
    """Calcula os resultados baseado nas respostas"""
    economy_score = 0
    social_score = 0
    total_questions = len(answers)

    # Verifica se há respostas para evitar divisão por zero, embora neste caso
    # só será chamada quando o quiz estiver completo.
    if total_questions == 0:
        return 0, 0
    
    # O número de questões por eixo é o total de questões dividido por 2 (4 para cada eixo)
    num_questions_per_axis = total_questions / 2

    for answer in answers.values():
        if answer["eixo"] == "economia":
            economy_score += answer["valor"]
        else:
            social_score += answer["valor"]

    # Normalizar scores para escala -2 a 2
    # Divide pelo número de questões por eixo para ter uma média de valor
    economy_normalized = economy_score / num_questions_per_axis
    social_normalized = social_score / num_questions_per_axis

    return economy_normalized, social_normalized

def determine_ideology(economy, social):
    """Determina a ideologia baseado nos scores"""
    best_match = "Centrista"
    best_score = float('inf')

    for ideology, ranges in ideologies.items():
        economy_range = ranges["economia"]
        social_range = ranges["social"]

        # Calcula a distância do ponto (economy, social) para o centro do range ideal
        # Para simplificar, vamos usar a distância do ponto para o ponto médio do range
        # e a distância Manhattan (soma das distâncias absolutas nos eixos)
        
        # Ponto médio do range econômico
        eco_mid = (economy_range[0] + economy_range[1]) / 2
        # Ponto médio do range social
        social_mid = (social_range[0] + social_range[1]) / 2
        
        # Distância do ponto do usuário ao ponto médio da ideologia
        eco_dist = abs(economy - eco_mid)
        social_dist = abs(social - social_mid)

        total_dist = eco_dist + social_dist

        # Critério de seleção: se a distância total for menor OU (se for igual, prefere o que está mais próximo do centro social)
        if total_dist < best_score:
            best_score = total_dist
            best_match = ideology
        # Desempate simples, pode ser refinado
        elif total_dist == best_score:
            # Preferir o que está mais próximo da média da escala (0)
            current_mid_dist = abs(eco_mid) + abs(social_mid)
            best_mid_dist = abs((ideologies[best_match]["economia"][0] + ideologies[best_match]["economia"][1]) / 2) + \
                            abs((ideologies[best_match]["social"][0] + ideologies[best_match]["social"][1]) / 2)
            
            if current_mid_dist < best_mid_dist:
                 best_match = ideology


    return best_match

def determine_spectrum(economy_score):
    """Determina o espectro político (esquerda, centro, direita)"""
    if economy_score < -0.5:
        return "Esquerda"
    elif economy_score > 0.5:
        return "Direita"
    else:
        return "Centro"

def plot_results(economy, social, ideology):
    """Cria gráfico dos resultados"""
    fig, ax = plt.subplots(figsize=(10, 8))

    # Define o grid do gráfico
    # Os eixos do quiz são de -2 a 2, mas plotamos um pouco mais para margem
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-2.2, 2.2)

    # Áreas coloridas (Quadrantes)
    # Esquerda (Economia < 0), Direita (Economia > 0)
    # Libertário (Social < 0), Autoritário (Social > 0)
    
    # Quadrante Superior Esquerdo (Autoritário-Esquerda)
    ax.fill_between([-2.2, 0], 0, 2.2, alpha=0.15, color='red')
    # Quadrante Inferior Esquerdo (Libertário-Esquerda)
    ax.fill_between([-2.2, 0], -2.2, 0, alpha=0.15, color='orange')
    # Quadrante Superior Direito (Autoritário-Direita)
    ax.fill_between([0, 2.2], 0, 2.2, alpha=0.15, color='purple')
    # Quadrante Inferior Direito (Libertário-Direita)
    ax.fill_between([0, 2.2], -2.2, 0, alpha=0.15, color='green')


    # Linhas centrais
    ax.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    ax.axvline(x=0, color='black', linestyle='-', alpha=0.5)

    # Ponto do usuário
    ax.scatter(economy, social, color='gold', s=250, edgecolors='black', linewidth=1.5, zorder=5)
    ax.annotate(f'Você: {ideology}', (economy, social), 
                xytext=(10, 10), textcoords='offset points', 
                bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', alpha=0.8, edgecolor='black'))

    ax.set_xlabel('Eixo Econômico\n← Coletivista/Esquerda - Individualista/Direita →', fontsize=12)
    ax.set_ylabel('Eixo Social\n← Libertário - Autoritário →', fontsize=12)
    ax.set_title('Seu Posicionamento Político', fontsize=14, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.4)

    return fig

# --- Aplicação Streamlit Principal ---

def main():
    st.markdown('<h1 class="main-header">🏛️ Quiz Político</h1>', unsafe_allow_html=True)
    st.markdown("### Descubra seu espectro político e inclinação ideológica")

    # Inicializar session state
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'quiz_complete' not in st.session_state:
        st.session_state.quiz_complete = False
    # Inicializar a lista de questões embaralhadas
    if 'shuffled_questions' not in st.session_state or st.session_state.quiz_complete:
        st.session_state.shuffled_questions = QUESTIONS_LIST.copy()
        # Embaralha as questões usando random.shuffle()
        random.shuffle(st.session_state.shuffled_questions)


    questions = st.session_state.shuffled_questions
    total_questions = len(questions)

    # Mostrar progresso
    progress_value = (st.session_state.current_question) / total_questions
    st.progress(progress_value)
    st.write(f"Pergunta {st.session_state.current_question + 1} de {total_questions}")

    if not st.session_state.quiz_complete:
        # Mostrar pergunta atual
        # Pega a pergunta da lista embaralhada
        current_q = questions[st.session_state.current_question]

        st.subheader(f"Pergunta {st.session_state.current_question + 1}: {current_q['question']}")

        # Opções de resposta (Usa o ID original da questão para chavear a resposta)
        
        # Embaralha as opções para evitar a tendência de escolha
        option_keys = list(current_q['options'].keys())
        random.shuffle(option_keys)
        
        # Define a chave de radio com o ID da pergunta e o índice atual para garantir unicidade na rerodagem
        radio_key = f"question_{current_q['id']}_{st.session_state.current_question}"

        selected_option = st.radio(
            "Selecione sua resposta:",
            options=option_keys, # Usa as opções embaralhadas
            key=radio_key
        )

        col1, col2 = st.columns([1, 1])

        with col1:
            if st.session_state.current_question > 0:
                # Botão de voltar
                if st.button("← Voltar"):
                    st.session_state.current_question -= 1
                    st.rerun()

        with col2:
            # Salva a resposta antes de avançar
            if st.button("Próxima →" if st.session_state.current_question < total_questions - 1 else "Finalizar Quiz"):
                # Salvar resposta usando o ID original da pergunta como chave para rastreamento
                st.session_state.answers[current_q['id']] = current_q['options'][selected_option]

                if st.session_state.current_question < total_questions - 1:
                    st.session_state.current_question += 1
                else:
                    st.session_state.quiz_complete = True
                st.rerun()

    else:
        # --- Mostrar Resultados ---
        st.balloons()
        st.success("🎉 Quiz Concluído! Aqui estão seus resultados:")

        # Calcular resultados
        economy_score, social_score = calculate_results(st.session_state.answers)
        ideology = determine_ideology(economy_score, social_score)
        spectrum = determine_spectrum(economy_score)

        # Determinar classe CSS baseada no espectro
        spectrum_class = ""
        if spectrum == "Esquerda":
            spectrum_class = "left-wing"
        elif spectrum == "Centro":
            spectrum_class = "center-wing"
        else:
            spectrum_class = "right-wing"

        # Mostrar resultados principais
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class="result-card {spectrum_class}">
                <h2>📊 Seu Resultado</h2>
                <h3>Espectro: <strong>{spectrum}</strong></h3>
                <h3>Inclinação: <strong>{ideology}</strong></h3>
                <p><strong>Eixo Econômico:</strong> {economy_score:.2f} (Intervalo: -2 a +2)</p>
                <p><strong>Eixo Social:</strong> {social_score:.2f} (Intervalo: -2 a +2)</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            # Gráfico
            fig = plot_results(economy_score, social_score, ideology)
            st.pyplot(fig)

        # Descrição detalhada
        st.subheader("📖 Explicação do Resultado")

        ideology_descriptions = {
            "Socialista": "Defende a socialização dos meios de produção e uma economia planificada com forte Estado de bem-estar social.",
            "Comunista": "Busca uma sociedade sem classes através da abolição da propriedade privada e do Estado, com economia totalmente coletivizada.",
            "Anarquista": "Oposição a todas as formas de governo hierárquico e defesa da autogestão e organização voluntária.",
            "Social Democrata": "Combina democracia política com economia mista e forte Estado de bem-estar social dentro do capitalismo.",
            "Social Liberal": "Defende liberdades individuais com alguma intervenção estatal para garantir justiça social.",
            "Centrista": "Posição moderada que busca equilíbrio entre diferentes correntes políticas.",
            "Liberal": "Ênfase na liberdade individual, economia de mercado e Estado limitado.",
            "Conservador": "Valoriza tradição, ordem social hierárquica e manutenção das instituições estabelecidas.",
            "Fascista": "Defende Estado totalitário, nacionalismo extremo e supressão da oposição política."
        }

        st.write(f"**{ideology}**: {ideology_descriptions.get(ideology, 'Descrição não disponível.')}")
        st.markdown(f"Seu resultado: **{ideology}** é o mais próximo do seu ponto no espectro político de acordo com as respostas.")


        # Botão para refazer
        if st.button("🔄 Refazer Quiz"):
            # Reseta todos os estados, inclusive a lista de perguntas embaralhadas (que será gerada novamente)
            st.session_state.answers = {}
            st.session_state.current_question = 0
            st.session_state.quiz_complete = False
            # Remove a lista antiga para que uma nova seja embaralhada ao rerodarmos
            if 'shuffled_questions' in st.session_state:
                del st.session_state.shuffled_questions 
            st.rerun()

if __name__ == "__main__":
    main()
