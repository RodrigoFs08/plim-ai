

# Plim AI

<p align="center">
  <img src="https://i.ibb.co/X89LWXs/Whats-App-Image-2024-05-10-at-18-38-41.jpg" alt="Logo do Plim AI" width="200" height="200">
</p>

Plim AI é um serviço inovador desenvolvido para o desafio de imersão em IA da Alura com a Google. Este projeto permite a geração automática de descrições para vídeos, utilizando dados extraídos de perfis públicos do Instagram. O serviço utiliza o modelo Gemini do Google para criar instruções sistemáticas que, através de um processo de few-shot learning, geram descrições precisas e contextualizadas para cada vídeo.

## Como Funciona

1. **Front-End**: Desenvolvido em React, o front-end é onde os usuários podem inserir o nome do perfil do Instagram e fazer upload de seus vídeos.
2. **Back-End**: Api contruída em Python com endpoints responsáveis por extrair dados do Instagram e criar as system instructions e prompts few shots para o modelo Gemini e interações com chatbot. O modelo então gera uma descrição inicial que pode ser ajustada interativamente através do chat.

<p align="center">
  <img src="https://i.ibb.co/ZNmt9r8/diagramaplimai-drawio.png" alt="Logo do Plim AI" width="800" height="400">
</p>

<p align="center">
  <img src="https://i.ibb.co/JBRKvjz/Captura-de-Tela-2024-05-11-a-s-21-02-55.png" alt="Logo do Plim AI" width="300" height="400">
</p>

<p align="center">
  <img src="https://i.ibb.co/gSGNWJz/Captura-de-Tela-2024-05-11-a-s-21-04-43.png" alt="Logo do Plim AI" width="300" height="400">
</p>

<p align="center">
  <img src="https://i.ibb.co/ZKKKnBr/Captura-de-Tela-2024-05-11-a-s-21-04-53.png" alt="Logo do Plim AI" width="300" height="400">
</p>

## Objetivo

O Plim AI visa oferecer uma ferramenta ágil e eficiente para profissionais de mídia social e marketing, melhorando a qualidade e a relevância das descrições de vídeo, e assim, potencializando o engajamento do público.

## Como Rodar o Projeto

### Configuração do Back-End

1. **Instalação das Dependências**: No diretório do back-end do projeto, instale as dependências necessárias executando:

`pip install -r requirements.txt`

2. **Execução do Servidor**: Após a instalação das dependências, inicie o servidor do back-end executando:

`python app.py`

Isso iniciará o servidor na porta padrão ou na especificada no script `app.py`.

### Configuração do Front-End

1. **Instalação das Dependências do Front-End**: Entre no diretório `plim_ai_front` e instale as dependências do projeto React utilizando:

`npm install`

2. **Execução do Front-End**: Após a instalação, inicie o servidor de desenvolvimento do front-end com:

`npm start`

Isso abrirá o aplicativo React no navegador, geralmente em `http://localhost:3000`.

### Uso do Serviço

Após ter o back-end e o front-end em execução, você pode começar a utilizar o Plim AI inserindo o nome do perfil do Instagram desejado e fazendo upload dos vídeos através da interface do usuário no front-end. O sistema processará os dados e retornará as descrições geradas para cada vídeo.
