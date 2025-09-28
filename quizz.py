import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random 
import math 

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
    /* CORREÇÃO: Força o fundo do app e do container principal para cores claras */
    .stApp {
        background-color: #000000; 
    }
    .main {
        background-color: #ffffff; 
    }
    
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
        color: #333333;
    }
    .result-card h2, .result-card h3, .result-card p {
        color: #333333;
    }
    .result-card strong {
        color: #000000;
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

# --- Sistema de Perguntas e Pontuação (Mantido Coerente) ---

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

IDEOLOGY_POINTS = {
    "Comunista": (-2.0, -1.0),
    "Socialista": (-1.5, -0.5),
    "Social Democrata": (-0.5, 0.0),
    "Anarco-Comunista": (-2.0, -2.0),
    "Centrista": (0.0, 0.0),
    "Social Liberal": (0.5, 0.0),
    "Liberal": (1.5, -0.5),
    "Conservador": (1.0, 1.5),
    "Anarcocapitalista": (2.0, -2.0),
    "Fascista/Nacionalista": (1.5, 2.0)
}

# --- Funções de Lógica de Negócio (Mantido Coerente) ---

def calculate_results(answers):
    """Calcula os resultados baseado nas respostas com normalização correta."""
    economy_score = 0
    social_score = 0
    MAX_SCORE_PER_AXIS = 8.0 

    for answer in answers.values():
        if answer["eixo"] == "economia":
            economy_score += answer["valor"]
        else:
            social_score += answer["valor"]
    
    # Normalização dos scores para a escala -2.0 a +2.0
    economy_normalized = (economy_score / MAX_SCORE_PER_AXIS) * 2.0
    social_normalized = (social_score / MAX_SCORE_PER_AXIS) * 2.0

    return economy_normalized, social_normalized

def determine_ideology(economy, social):
    """Determina a ideologia usando Distância Euclidiana (mais precisa)."""
    best_match = "Centrista"
    min_distance = float('inf')

    user_point = (economy, social)

    for ideology, point in IDEOLOGY_POINTS.items():
        ideology_point = point
        
        distance = math.sqrt(
            (user_point[0] - ideology_point[0])**2 + 
            (user_point[1] - ideology_point[1])**2
        )

        if distance < min_distance:
            min_distance = distance
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

    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-2.2, 2.2)

    # Cores dos Quadrantes
    ax.fill_between([-2.2, 0], 0, 2.2, alpha=0.15, color='red')
    ax.fill_between([-2.2, 0], -2.2, 0, alpha=0.15, color='orange')
    ax.fill_between([0, 2.2], 0, 2.2, alpha=0.15, color='purple')
    ax.fill_between([0, 2.2], -2.2, 0, alpha=0.15, color='green')

    # Plotar pontos de referência das ideologias
    for name, point in IDEOLOGY_POINTS.items():
        ax.scatter(point[0], point[1], marker='x', color='gray', s=50, alpha=0.7)
        if name in ["Centrista", "Comunista", "Fascista/Nacionalista", "Anarcocapitalista"]:
            ax.annotate(name, (point[0], point[1]), 
                        xytext=(5, 5), textcoords='offset points', 
                        fontsize=8, color='gray')

    # Linhas centrais
    ax.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    ax.axvline(x=0, color='black', linestyle='-', alpha=0.5)

    # Ponto do usuário
    ax.scatter(economy, social, color='gold', s=250, edgecolors='black', linewidth=1.5, zorder=5)
    ax.annotate(f'Você: {ideology}', (economy, social), 
                xytext=(10, 10), textcoords='offset points', 
                bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', alpha=0.9, edgecolor='black'),
                fontsize=10)

    ax.set_xlabel('Eixo Econômico\n← Coletivista/Esquerda (-2.0) - Individualista/Direita (+2.0) →', fontsize=12)
    ax.set_ylabel('Eixo Social\n← Libertário (-2.0) - Autoritário (+2.0) →', fontsize=12)
    ax.set_title('Seu Posicionamento Político no Espectro', fontsize=14, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.4)

    return fig

# --- Aplicação Streamlit Principal ---

def main():
    st.markdown('<h1 class="main-header">🏛️ Quiz Político</h1>', unsafe_allow_html=True)
    st.markdown("### Descubra seu espectro político e inclinação ideológica")

    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'quiz_complete' not in st.session_state:
        st.session_state.quiz_complete = False
        
    if 'shuffled_questions' not in st.session_state:
        st.session_state.shuffled_questions = QUESTIONS_LIST.copy()
        random.shuffle(st.session_state.shuffled_questions)

    questions = st.session_state.shuffled_questions
    total_questions = len(questions)

    progress_value = (st.session_state.current_question) / total_questions
    st.progress(progress_value)
    st.write(f"Pergunta {st.session_state.current_question + 1} de {total_questions}")

    if not st.session_state.quiz_complete:
        current_q = questions[st.session_state.current_question]

        st.subheader(f"Pergunta {st.session_state.current_question + 1}: {current_q['question']}")

        option_keys = list(current_q['options'].keys())
        random.shuffle(option_keys)
        
        radio_key = f"question_{current_q['id']}_{st.session_state.current_question}"

        default_option = None
        if current_q['id'] in st.session_state.answers:
            for key, value in current_q['options'].items():
                if value == st.session_state.answers[current_q['id']]:
                    default_option = key
                    break

        selected_option = st.radio(
            "Selecione sua resposta:",
            options=option_keys,
            index=option_keys.index(default_option) if default_option else 0,
            key=radio_key
        )

        col1, col2 = st.columns([1, 1])

        with col1:
            if st.session_state.current_question > 0:
                if st.button("← Voltar"):
                    st.session_state.answers[current_q['id']] = current_q['options'][selected_option]
                    st.session_state.current_question -= 1
                    st.rerun()

        with col2:
            if st.button("Próxima →" if st.session_state.current_question < total_questions - 1 else "Finalizar Quiz"):
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

        economy_score, social_score = calculate_results(st.session_state.answers)
        ideology = determine_ideology(economy_score, social_score)
        spectrum = determine_spectrum(economy_score)

        spectrum_class = ""
        if spectrum == "Esquerda":
            spectrum_class = "left-wing"
        elif spectrum == "Centro":
            spectrum_class = "center-wing"
        else:
            spectrum_class = "right-wing"

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class="result-card {spectrum_class}">
                <h2>📊 Seu Resultado</h2>
                <h3>Espectro: <strong>{spectrum}</strong></h3>
                <h3>Inclinação: <strong>{ideology}</strong></h3>
                <p><strong>Eixo Econômico (X):</strong> {economy_score:.2f} (← Coletivista | Individualista →)</p>
                <p><strong>Eixo Social (Y):</strong> {social_score:.2f} (← Libertário | Autoritário →)</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            fig = plot_results(economy_score, social_score, ideology)
            st.pyplot(fig)

        # Descrição detalhada
        st.subheader("📖 Explicação do Resultado")

        ideology_descriptions = {
            "Comunista": "Busca uma sociedade sem classes e a abolição da propriedade privada e do Estado, com forte controle coletivo da economia.",
            "Socialista": "Defende a socialização dos meios de produção e uma economia planificada com forte Estado de bem-estar social e progressismo social.",
            "Social Democrata": "Combina democracia política com economia mista, Estado de bem-estar social e uma abordagem equilibrada de políticas sociais.",
            "Anarco-Comunista": "Oposição a todas as formas de governo e defesa de uma sociedade sem classes, sem Estado e com autogestão dos meios de produção.",
            "Centrista": "Posição moderada que busca equilíbrio entre diferentes correntes, priorizando o pragmatismo e o consenso.",
            "Social Liberal": "Defende liberdades individuais e de mercado, mas com intervenção estatal para garantir justiça social e direitos civis amplos.",
            "Liberal": "Ênfase na liberdade individual, economia de mercado (livre mercado) e Estado mínimo (Mínimo Socialmente Necessário).",
            "Conservador": "Valoriza a tradição, ordem social hierárquica e manutenção das instituições, geralmente com foco na livre iniciativa econômica.",
            "Anarcocapitalista": "Defende a abolição do Estado e o controle total da sociedade pelo mercado e contratos privados, incluindo serviços de segurança.",
            "Fascista/Nacionalista": "Defende um Estado totalitário, nacionalismo extremo, corporativismo econômico e forte repressão à oposição e à diferença."
        }

        st.write(f"Sua **Inclinação Principal** é: **{ideology}**")
        st.write(f"**{ideology}**: {ideology_descriptions.get(ideology, 'Descrição não disponível.')}")

        if st.button("🔄 Refazer Quiz"):
            st.session_state.answers = {}
            st.session_state.current_question = 0
            st.session_state.quiz_complete = False
            del st.session_state.shuffled_questions 
            st.rerun()

if __name__ == "__main__":
    main()
