import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import urllib.request
import requests
from PIL import Image
from io import BytesIO

st.markdown("<h1 style='text-align: center; color: grey;'>Variação do Preço por Barril do Petróleo Bruto Brent</h1>", unsafe_allow_html=True)

opcoes_abas = ['Introdução Tech Challenge 4', 'Analise Preço Petroleo']
aba_selecionada = st.sidebar.selectbox('Escolha uma aba', opcoes_abas)

image_url = 'https://github.com/TorNDark/TechChallenge_Fase4/blob/main/Imagem_Capa.jpeg?raw=true'

response = requests.get(image_url)
image = Image.open(BytesIO(response.content))

st.image(image,
         width=30,
         output_format='PNG',
         use_container_width=True,
)

if aba_selecionada == 'Introdução Tech Challenge 4':
    st.markdown("<h1 style='text-align: center; color: grey;'>Introdução Tech Challenge 4</h1>", unsafe_allow_html=True)
    paragraphs = [
        "Analisar os dados de preço do petróleo Brent, que pode ser encontrado no site do Ipea.",
        "Essa base de dados histórica envolve duas colunas: data e preço (em dólares).",
        "Um grande cliente do segmento pediu para que fosse desenvolvido dashboards interativo e que gere insights relevantes para tomada de decisão.",
        "Além disso, desenvolver um modelo de Machine Learning para fazer o forecasting do preço do petróleo e um modelo de Deploy (nesse caso estamos usando o Streamlit).",
        "",
        "No Streamlit há duas abas: a primeira explicando o Tech Challenge e a segunda com os Dados do Projeto",
        "",
    ]

    for paragraph in paragraphs:
        st.write(paragraph)
    st.write('Clique [aqui](http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view) para acessar os dados do IPEA')
    st.write('Clique [aqui](https://youtu.be/yjUcNPZyu8s) para acessar o link de como foi feito o projeto, no youtube')
    st.write("Clique [aqui](https://github.com/TorNDark/TechChallenge_Fase4.git) e acesse todo o conteúdo do trabalho no GitHub")

    

elif aba_selecionada == 'Analise Preço Petroleo':
    st.markdown("<h1 style='text-align: center; color: grey;'>Analise Preço Petroleo</h1>", unsafe_allow_html=True)

    paragraphs = [
        "Análise da Flutuação do Preço do Petróleo ao Longo do Tempo.",
        "O estudo examina o preço do petróleo em diferentes períodos. É possível ajustar as datas de referência e observar a tabela e o gráfico correspondentes à variação do preço conforme a data selecionada."
    ]

    for paragraph in paragraphs:
        st.write(paragraph)

    # Carregar o arquivo CSV usando pandas
    df = pd.read_csv("https://raw.githubusercontent.com/TorNDark/TechChallenge_Fase4/refs/heads/main/preco_petroleo_ipea_base_2015_2025.csv", sep=';', encoding='latin1')

    # Exibir os dados no Streamlit

    data_inicial_padrao = pd.to_datetime('2020-01-04').date()
    data_final_padrao = pd.to_datetime('2025-02-10').date()

    data_inicial = st.date_input("Data Inicial", value=data_inicial_padrao, min_value=data_inicial_padrao)
    data_final = st.date_input("Data Final", value=data_final_padrao, max_value=pd.to_datetime('2025-02-10').date())


    df.rename(columns={'Data': 'data', 'Preco': 'preco'}, inplace=True)
    df['preco'] = df['preco'].astype(str).str.replace(',', '.')
    df['preco'] = df['preco'].astype(float)
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y').dt.date # Specifica o formato correto

    df_filtrado = df[(df['data'] >= data_inicial) & (df['data'] <= data_final)]

    x = df_filtrado['data']
    y = df_filtrado['preco']

    plt.plot(df_filtrado['data'], df_filtrado['preco'])
    plt.xlabel('Data')
    plt.ylabel('Preço')
    plt.title('Preço ao longo dos anos')
   

    st.pyplot(plt)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.write('## Prevendo o valor do barril de Petróleo')
    paragraphs = [
        "Para prever os valores do barril do Petróleo estudamos alguns modelos tradicionais de Machine Learning, como Arvore de decisão (Decision Tree), Linear Regression e Arima.",
        "A melhor previsão, entre eles, foi do Arima, com um MAPE de 5%.",
        "As maiores variações de períodos curtos, interferem muito no modelo de previsão."
    ]

    for paragraph in paragraphs:
        st.write(paragraph, format='markdown')

    url_predicao = "https://github.com/TorNDark/TechChallenge_Fase4/blob/main/Modelo_Arima.png?raw=true"
    st.image(url_predicao, use_container_width =True, caption="Gráfico de Predição Arima")

    st.markdown("<hr>", unsafe_allow_html=True)

    st.write('### Potenciais Causadores de Oscilações no Preço do Petróleo')
    paragraphs = [
        "Alguns outros causadores de oscilações no preço do petróleo nos últimos anos, e como isso pode impactar diretamente e indiretamente o valor do petróleo mundial",
        "   1 - Geopolítica: Conflitos e tensões internacionais, como as sanções ao Irã e à Rússia, têm um impacto direto nos preços do petróleo.",
        "   2 - Oferta e Demanda: A produção da OPEP+ e a demanda global por energia influenciam significativamente os preços.",
        "   3 - Eventos Econômicos Globais: Crises econômicas, como a pandemia de COVID-19, podem causar quedas abruptas na demanda e, consequentemente, nos preços.",
        "   4 - Avanços Tecnológicos: A extração de óleo de xisto nos EUA, por exemplo, aumentou a oferta global e impactou os preços."

    ]

    for paragraph in paragraphs:
        st.write(paragraph, format='markdown')


    st.write('Fonte: Código Python disponível no Github')
    st.write('Clique [aqui](https://github.com/TorNDark/TechChallenge_Fase4/blob/main/TechChallengerPetroleoFIAP_v3.ipynb)')

    st.write('<hr>', unsafe_allow_html=True)
    st.write('### Resultados Detalhados')
    paragraphs = [
        "Os resultados detalhados de desempenho dos modelos mostram que o modelo ARIMA teve erros menores em comparação com os modelos de regressão linear e árvore de decisão.",
        "Por exemplo, em 22 de novembro de 2024, o erro do modelo ARIMA foi de -4.883, enquanto o erro da regressão linear foi de -12.129204 e o da árvore de decisão foi de -6.10.",
        "Em resumo, a combinação de diferentes técnicas de machine learning, com destaque para o modelo ARIMA, nos permitiu obter previsões robustas e precisas dos preços do petróleo.",
        "Esses insights são essenciais para a tomada de decisões estratégicas no mercado de petróleo."

    ]


    for paragraph in paragraphs:
        st.write(paragraph, format='markdown')

    st.markdown("<hr>", unsafe_allow_html=True)

    st.write('## Dashboard Power Bi')
    paragraphs = [
        'O Dashboard abaixo mostra as variações do preço do petróleo ao longo dos anos e também explica as variações.',
        'Para acessar todos os recursos, clique no link e baixar o arquivo do Power Bi.'
    ]

    for paragraph in paragraphs:
        st.write(paragraph)

    img_url = "https://github.com/TorNDark/TechChallenge_Fase4/blob/main/dash_power_bi.png?raw=true"

    st.image(img_url, use_container_width=True, caption="Foto do Dashboard Power Bi")

    st.write('Clique [aqui](https://github.com/TorNDark/TechChallenge_Fase4/blob/main/An%C3%A1lise%20Pre%C3%A7o%20do%20Petr%C3%B3leo_01.pbix) para abrir o arquivo Power BI no Github')

    st.markdown("<hr>", unsafe_allow_html=True)





