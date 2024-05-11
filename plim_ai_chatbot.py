from flask import jsonify

def plim_ai_chatbot(request):

    # Configurações iniciais
    import google.generativeai as genai

    GOOGLE_API_KEY="SUA_API_KEY_AQUI"
    genai.configure(api_key=GOOGLE_API_KEY)
    generation_config = {
    "candidate_count": 1,
    "temperature": 0.5,
    }

    safety_settings={
        'HATE': 'BLOCK_NONE',
        'HARASSMENT': 'BLOCK_NONE',
        'SEXUAL' : 'BLOCK_NONE',
        'DANGEROUS' : 'BLOCK_NONE'
        }

    plim_ai_instruction = request["plim_ai_instruction"]

    chat_history = request['chat_history']

    print(f"chat_history: {chat_history}")

    # Lista para guardar os dicionários estruturados
    structured_list = []

    # Iterar sobre os itens e seus índices
    for index, item in enumerate(chat_history):
        # Alternar entre "model" e "user" com base na paridade do índice
        role = "model" if index % 2 == 0 else "user"
        
        # Criar o dicionário e adicionar à lista estruturada
        structured_list.append({
            "role": role,
            "parts": item
        })
    chat_history = structured_list

    prompt = request['prompt']

    # Criando o modelo especializado em gerar descrições atraentes e coerentes para novos vídeos do perfil no Instagram
    model_plim_ai = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                generation_config=generation_config,
                                system_instruction=plim_ai_instruction,
                                safety_settings=safety_settings)

    chat = model_plim_ai.start_chat(history=chat_history)

  # Envia o prompt do usuario
    try:
        chat.send_message(prompt)
        chat_message = chat.last.text
    except Exception as e:
        # Em caso de falha na comunicação ou geração com o modelo Plim AI
        return jsonify({
            'message': 'Falha na comunicacao com o modelo Plim AI.',
            'code': 500,
            'error': str(e)
        }), 500

    # Resposta bem-sucedida com a resposta do chat 
    return jsonify({
        'message': 'resposta obtida com sucesso.',
        'code': 200,
        'chat_message': chat_message,
    }), 200
