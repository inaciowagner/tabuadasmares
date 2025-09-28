import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random # Importado para embaralhar as questões
import math # Importado para cálculo de distância Euclidiana

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

# --- Sistema de Perguntas e Pontuação ---

# Lista Original de Perguntas (usada para reinicializar)
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

# Sistema de classificação (pontos médios para Distância Euclidiana)
IDEOLOGY_POINTS = {
    # Coordenadas (Eixo Econômico, Eixo Social)
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

# --- Funções de Lógica de Negócio ---

def calculate_results(answers):
    """Calcula os resultados baseado nas respostas com normalização correta."""
    economy_score = 0
    social_score = 0
    
    # 8 questões no total, 4 para cada eixo. Max Score por eixo = 4 * 2 = 8.
    MAX_SCORE_PER_AXIS = 8.0 

    for answer in answers.values():
        if answer["eixo"] == "economia":
            economy_score += answer["valor"]
        else:
            social_score += answer["valor"]
    
    # Normalização dos scores para a escala -2.0 a +2.0
    # Fórmula: (score_atual / max_score_possivel) * 2
    
    # Exemplo: Se todas as 4 perguntas de economia deram -2, o score_atual é -8.
    # Normalizado: (-8 / 8) * 2 = -2.0 (Correto)
    # Exemplo: Se o score_atual é 0: (0 / 8) * 2 = 0.0 (Correto)
    # Exemplo: Se o score_atual é 4: (4 / 8) * 2 = 1.0 (Correto)

    economy_normalized = (economy_score / MAX_SCORE_PER_AXIS) * 2.0
    social_normalized = (social_score / MAX_SCORE_PER_AXIS) * 2.0

    return economy_normalized, social_normalized

def determine_ideology(economy, social):
    """Determina a ideologia usando Distância Euclidiana (mais precisa)."""
    best_match = "Centrista"
    min_distance = float('inf')

    # Ponto do usuário
    user_point = (economy, social)

    for ideology, point in IDEOLOGY_POINTS.items():
        ideology_point = point
        
        # Distância Euclidiana: d = sqrt((x2 - x1)² + (y2 - y1)²)
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

    # Define o grid do gráfico
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-2.2, 2.2)

    # Cores dos Quadrantes (Autoritário/Libertário x Esquerda/Direita)
    ax.fill_between([-2.2, 0], 0, 2.2, alpha=0.15, color='red')    # Autoritário-Esquerda
    ax.fill_between([-2.2, 0], -2.2, 0, alpha=0.15, color='orange') # Libertário-Esquerda
    ax.fill_between([0, 2.2], 0, 2.2, alpha=0.15, color='purple')  # Autoritário-Direita
    ax.fill_between([0, 2.2], -2.2, 0, alpha=0.15, color='green')  # Libertário-Direita
