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
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visualizador de Códigos de Barras</title>
    <!-- Carrega o Tailwind CSS para estilização moderna e responsiva -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Configuração do Tailwind para usar a fonte Inter e cores personalizadas -->
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                    },
                    colors: {
                        'primary': '#4f46e5',
                        'primary-dark': '#4338ca',
                        'secondary': '#f97316',
                    }
                }
            }
        }
    </script>
    <style>
        /* Estilos personalizados para o código de barras (opcional, mas adiciona um toque visual) */
        .barcode-img {
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            border: 2px solid #e5e7eb;
            transition: transform 0.3s ease;
        }
        .barcode-img:hover {
            transform: scale(1.02);
        }
    </style>
</head>
<body class="bg-gray-50 min-h-screen flex items-center justify-center font-sans p-4">

    <!-- Container Principal do Aplicativo -->
    <div id="app-container" class="w-full max-w-4xl bg-white shadow-2xl rounded-xl p-6 md:p-10 transition-all duration-300">
        
        <header class="text-center mb-8">
            <h1 class="text-3xl md:text-4xl font-extrabold text-primary-dark tracking-tight">
                Visualizador de Códigos de Barras
            </h1>
            <p class="text-gray-500 mt-2 text-lg" id="subtitle">Selecione um item abaixo:</p>
        </header>

        <!-- Conteúdo principal será renderizado aqui -->
        <main id="content-area">
            <!-- Conteúdo dinâmico será injetado pelo JavaScript -->
        </main>
    </div>

    <script>
        // Lista de 12 itens atualizada com os dados do PDF fornecido
        const items = [
            { name: "Desativar conferência de peso", id: "1012047530002547" },
            { name: "Executa função", id: "1012049890002547" },
            { name: "Desconto no item anterior", id: "1012047730002547" },
            { name: "Alterar digital", id: "1012049920002547" },
            { name: "Pagamento outros", id: "1012047740002547" },
            { name: "Fechar caixa", id: "1012050020002547" },
            { name: "Abrir multiplicação", id: "1012047850002547" },
            { name: "Relatório gerencial por usuário", id: "1012050230002547" },
            { name: "Reimprimir últimos comprovantes", id: "1012047880002547" },
            { name: "Desligar PDV", id: "1012050400002547" },
            { name: "Tarar balança de conferência", id: "1012048930002547" },
            { name: "Reiniciar PDV", id: "1012050410002547" }
        ];

        const contentArea = document.getElementById('content-area');
        const subtitle = document.getElementById('subtitle');
        const defaultSubtitle = "Selecione um item abaixo:";

        /**
         * Gera a URL de uma imagem placeholder para simular um código de barras.
         * O Placehold.co simula a imagem com o texto do ID fornecido.
         * * @param {string} barcodeId O ID do código de barras a ser exibido.
         * @returns {string} A URL da imagem.
         */
        function generateBarcodeUrl(barcodeId) {
            // Aumentamos a largura para acomodar o número longo.
            // URL: 600x200, fundo preto, texto branco.
            return `https://placehold.co/600x200/000000/FFFFFF?text=${encodeURIComponent(barcodeId)}`;
        }

        /**
         * Renderiza a página de menu inicial com os 12 botões.
         */
        function renderMenu() {
            subtitle.textContent = defaultSubtitle;
            contentArea.innerHTML = ''; // Limpa o conteúdo anterior

            // Cria um grid responsivo para os botões
            const grid = document.createElement('div');
            // Ajustamos o layout para 2 colunas em telas pequenas e 3 em telas maiores, pois os nomes são mais longos
            grid.className = 'grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4'; 

            items.forEach((item, index) => {
                const button = document.createElement('button');
                button.textContent = `${index + 1}. ${item.name}`;
                button.className = 'p-4 bg-primary text-white rounded-lg shadow-md hover:bg-primary-dark transition duration-150 ease-in-out font-semibold text-sm md:text-base transform hover:scale-[1.03] focus:outline-none focus:ring-4 focus:ring-primary/50 text-left';
                
                // Adiciona o evento de clique para ir para a página de detalhe
                button.addEventListener('click', () => renderDetail(item));

                grid.appendChild(button);
            });

            contentArea.appendChild(grid);
        }

        /**
         * Renderiza a página de detalhe com a imagem do código de barras.
         * @param {object} item O objeto do item (name e id).
         */
        function renderDetail(item) {
            subtitle.textContent = `Visualizando: ${item.name}`;
            contentArea.innerHTML = ''; // Limpa o conteúdo anterior

            const barcodeUrl = generateBarcodeUrl(item.id);

            // Container para centralizar o conteúdo vertical e horizontalmente
            const detailContainer = document.createElement('div');
            detailContainer.className = 'flex flex-col items-center justify-center space-y-8 py-8 animate-fadeIn';
            detailContainer.style.animation = 'fadeIn 0.5s ease-out'; // Define a animação

            // Descrição do Item
            const itemDescription = document.createElement('h2');
            itemDescription.className = 'text-2xl font-bold text-gray-700 text-center';
            itemDescription.textContent = item.name;

            // Título do Código de Barras
            const codeTitle = document.createElement('h3');
            codeTitle.className = 'text-xl font-mono text-gray-600';
            codeTitle.textContent = `Código: ${item.id}`;

            // Imagem do Código de Barras (Este é o elemento <img> que você queria)
            const barcodeImage = document.createElement('img');
            barcodeImage.src = barcodeUrl;
            barcodeImage.alt = `Código de Barras para ${item.name}`;
            // Classe 'barcode-img' aplica a estilização personalizada
            barcodeImage.className = 'barcode-img w-full max-w-md h-auto rounded-md'; 

            // Botão Voltar
            const backButton = document.createElement('button');
            backButton.textContent = '← Voltar ao Menu Principal';
            backButton.className = 'p-3 px-6 bg-secondary text-white rounded-lg shadow-lg hover:bg-orange-600 transition duration-150 ease-in-out font-bold focus:outline-none focus:ring-4 focus:ring-secondary/50';
            backButton.addEventListener('click', renderMenu);

            detailContainer.append(itemDescription, codeTitle, barcodeImage, backButton);
            contentArea.appendChild(detailContainer);
        }

        // Estilo CSS para a animação (adicionado via JS para manter o arquivo único)
        const style = document.createElement('style');
        style.textContent = `
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .animate-fadeIn {
                animation: fadeIn 0.5s ease-out;
            }
        `;
        document.head.appendChild(style);

        // Inicia a aplicação na tela de menu
        window.onload = renderMenu;

    </script>
</body>
</html>
""")

if __name__ == "__main__":
    main()
