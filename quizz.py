import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

# Sistema de perguntas e pontuação
questions = [
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

# Sistema de classificação
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

def calculate_results(answers):
    """Calcula os resultados baseado nas respostas"""
    economy_score = 0
    social_score = 0
    total_questions = len(answers)
    
    for answer in answers.values():
        if answer["eixo"] == "economia":
            economy_score += answer["valor"]
        else:
            social_score += answer["valor"]
    
    # Normalizar scores para escala -2 a 2
    economy_normalized = (economy_score / (total_questions/2)) / 2
    social_normalized = (social_score / (total_questions/2)) / 2
    
    return economy_normalized, social_normalized

def determine_ideology(economy, social):
    """Determina a ideologia baseado nos scores"""
    best_match = "Centrista"
    best_score = float('inf')
    
    for ideology, ranges in ideologies.items():
        economy_range = ranges["economia"]
        social_range = ranges["social"]
        
        # Calcula distância dos ranges ideais
        economy_dist = min(abs(economy - economy_range[0]), abs(economy - economy_range[1]))
        social_dist = min(abs(social - social_range[0]), abs(social - social_range[1]))
        
        total_dist = economy_dist + social_dist
        
        if total_dist < best_score:
            best_score = total_dist
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
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2.5)
    
    # Áreas coloridas
    ax.fill_between([-2.5, 0], -2.5, 2.5, alpha=0.2, color='red', label='Esquerda Econômica')
    ax.fill_between([0, 2.5], -2.5, 2.5, alpha=0.2, color='blue', label='Direita Econômica')
    ax.fill_between([-2.5, 2.5], 0, 2.5, alpha=0.2, color='purple', label='Autoritário')
    ax.fill_between([-2.5, 2.5], -2.5, 0, alpha=0.2, color='green', label='Libertário')
    
    # Linhas centrais
    ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax.axvline(x=0, color='black', linestyle='-', alpha=0.3)
    
    # Ponto do usuário
    ax.scatter(economy, social, color='gold', s=200, edgecolors='black', zorder=5)
    ax.annotate(f'Você: {ideology}', (economy, social), 
                xytext=(10, 10), textcoords='offset points', 
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    ax.set_xlabel('Eixo Econômico\n← Esquerda (Coletivista) - Direita (Individualista) →')
    ax.set_ylabel('Eixo Social\n← Libertário - Autoritário →')
    ax.set_title('Seu Posicionamento Político')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return fig

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
    
    # Mostrar progresso
    progress = st.session_state.current_question / len(questions)
    st.progress(progress)
    st.write(f"Pergunta {st.session_state.current_question + 1} de {len(questions)}")
    
    if not st.session_state.quiz_complete:
        # Mostrar pergunta atual
        current_q = questions[st.session_state.current_question]
        
        st.subheader(f"Pergunta {current_q['id']}: {current_q['question']}")
        
        # Opções de resposta
        selected_option = st.radio(
            "Selecione sua resposta:",
            options=list(current_q['options'].keys()),
            key=f"question_{current_q['id']}"
        )
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.session_state.current_question > 0:
                if st.button("← Voltar"):
                    st.session_state.current_question -= 1
                    st.rerun()
        
        with col2:
            if st.button("Próxima →" if st.session_state.current_question < len(questions) - 1 else "Finalizar Quiz"):
                # Salvar resposta
                st.session_state.answers[current_q['id']] = current_q['options'][selected_option]
                
                if st.session_state.current_question < len(questions) - 1:
                    st.session_state.current_question += 1
                else:
                    st.session_state.quiz_complete = True
                st.rerun()
    
    else:
        # Mostrar resultados
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
                <h3>Espectro: {spectrum}</h3>
                <h3>Inclinação: {ideology}</h3>
                <p><strong>Eixo Econômico:</strong> {economy_score:.2f}</p>
                <p><strong>Eixo Social:</strong> {social_score:.2f}</p>
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
        
        # Botão para refazer
        if st.button("🔄 Refazer Quiz"):
            st.session_state.answers = {}
            st.session_state.current_question = 0
            st.session_state.quiz_complete = False
            st.rerun()

if __name__ == "__main__":
    main()