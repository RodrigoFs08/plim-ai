from flask import Flask, request, jsonify
from video_upload_to_plim import upload_video_and_get_description
from plim_ai_chatbot import plim_ai_chatbot
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

@app.route('/upload_video_to_plim_ai', methods=['POST'])
def handle_upload():
    print('Recebendo solicitação de upload...')
    return upload_video_and_get_description(request)

@app.route('/plim_ai_chatbot', methods=['POST'])
def handle_chat():
    print('Recebendo solicitação de chat...')
    dados = request.json
    return plim_ai_chatbot(dados)

if __name__ == '__main__':
    app.run(debug=True)
