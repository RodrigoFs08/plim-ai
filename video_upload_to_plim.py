import os
import tempfile
from flask import jsonify
from werkzeug.utils import secure_filename
import instaloader
import requests
import google.generativeai as genai
import cv2
import shutil

# Função auxiliar para obter o caminho do arquivo temporário
def get_file_path(filename):
    file_name = secure_filename(filename)
    return os.path.join(tempfile.gettempdir(), file_name)

def upload_video_and_get_description(request):
    if request.method != 'POST':
        return jsonify({'message': 'Método não permitido. Use POST para upload.', 'code': 405}), 405

    if 'profile_name' not in request.form or 'video' not in request.files:
        return jsonify({'message': 'Dados necessários não encontrados na solicitação.', 'code': 400}), 400

    profile_name = request.form['profile_name']
    video_file = request.files['video']

    # Obtem o nome do arquivo e cria um nome de arquivo seguro para upload
    video_filename_uploaded = secure_filename(video_file.filename)
    file_path = './' + video_filename_uploaded
    print(f"Salvando arquivo temporário em: {file_path}")
    print(f"Nome do arquivo de vídeo: {video_filename_uploaded}")

    # Salva o arquivo temporariamente
    video_file.save(file_path)

    # Agora vamos carregar o perfil do Instagram e processar o vídeo
    L = instaloader.Instaloader()
    profile = instaloader.Profile.from_username(L.context, profile_name)

    profile_name = profile.username
    profile_biography = profile.biography

    descricoes = []
    for post in profile.get_posts():
        if len(descricoes) < 10:
            descricoes.append(post.caption)
        else:
            break

    videos_info = []
    for post in profile.get_posts():
        if post.is_video and len(videos_info) < 2:
            videos_info.append((post.video_url, post.caption))
        elif len(videos_info) >= 2:
            break

    lista_videos_descricao = []
    for i, (url, descricao) in enumerate(videos_info, 1):
        video_filename = f"video_{i}.mp4"
        response = requests.get(url)
        with open(video_filename, 'wb') as video_file:
            video_file.write(response.content)
        lista_videos_descricao.append([video_filename, descricao])

    # Inclua o vídeo enviado pelo usuário na lista de vídeos
    lista_videos_descricao.append([video_filename_uploaded, 'Conforme exemplo anterior, elabore uma descrição para o vídeo'])

    # Configurações iniciais para o uso do Google Generative AI
    GOOGLE_API_KEY = "SUA_API_KEY_AQUI"
    genai.configure(api_key=GOOGLE_API_KEY)

    generation_config = {
      "candidate_count": 1,
      "temperature": 0.5,
    }

    safety_settings = {
      'HATE': 'BLOCK_NONE',
      'HARASSMENT': 'BLOCK_NONE',
      'SEXUAL' : 'BLOCK_NONE',
      'DANGEROUS' : 'BLOCK_NONE'
    }

    system_instruction = "O objetivo é gerar uma system instruction para outro modelo que será especializado em gerar descrições atraentes e coerentes para novos vídeos do perfil no Instagram. Mande apenas a system instruction sem título ou observações, com no máximo 400 caracteres, não utilizar links."

    model = genai.GenerativeModel(model_name='gemini-1.5-pro-latest',
                                      generation_config=generation_config,
                                    system_instruction=system_instruction,
                                      safety_settings=safety_settings,)

    # Construção do prompt inicial para o modelo de IA
    prompt = f"Nome do perfil: {profile_name}\n"
    prompt += f"Biografia: {profile_biography}\n\n"

    for i, descricao in enumerate(descricoes, 1):
        prompt += f"\n{i}. {descricao}\n"

    response = model.generate_content(prompt)
    aux_description_model_final = "Esteja pronto para ajustar seu estilo com exemplos de few-shot learning. Mande apenas a descricao, sem titulos ou observacoes"

    plim_ai_instruction = response.text + aux_description_model_final

    # Criando o modelo especializado em gerar descrições atraentes e coerentes para novos vídeos do perfil no Instagram
    model_plim_ai = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                  generation_config=generation_config,
                                  system_instruction=plim_ai_instruction,
                                  safety_settings=safety_settings)

    # Diretório para extração de quadros de vídeo
    FRAME_EXTRACTION_DIRECTORY = "./content/frames"
    FRAME_PREFIX = "_frame"
    def create_frame_output_dir(output_dir):
      if not os.path.exists(output_dir):
        os.makedirs(output_dir)
      else:
        shutil.rmtree(output_dir)
        os.makedirs(output_dir)

    def extract_frame_from_video(video_file_path):
      print(f"Extracting {video_file_path} at 1 frame per second. This might take a bit...")
      create_frame_output_dir(FRAME_EXTRACTION_DIRECTORY)
      vidcap = cv2.VideoCapture(video_file_path)
      fps = vidcap.get(cv2.CAP_PROP_FPS)
      frame_duration = 1 / fps
      output_file_prefix = os.path.basename(video_file_path).replace('.', '_')
      frame_count = 0
      count = 0
      while vidcap.isOpened():
          success, frame = vidcap.read()
          if not success:
              break
          if int(count / fps) == frame_count:
              min = frame_count // 60
              sec = frame_count % 60
              time_string = f"{min:02d}:{sec:02d}"
              image_name = f"{output_file_prefix}{FRAME_PREFIX}{time_string}.jpg"
              output_filename = os.path.join(FRAME_EXTRACTION_DIRECTORY, image_name)
              cv2.imwrite(output_filename, frame)
              frame_count += 1
          count += 1
      vidcap.release()
      print(f"Completed video frame extraction!\n\nExtracted: {frame_count} frames")

    # Função para obter itens distribuídos uniformemente da lista
    def get_uniformly_distributed_items(lst, num_items):
        step = len(lst) / num_items
        return [lst[int(i * step)] for i in range(num_items)]

    class File:
      def __init__(self, file_path: str, display_name: str = None):
        self.file_path = file_path
        if display_name:
          self.display_name = display_name
        self.timestamp = get_timestamp(file_path)

      def set_file_response(self, response):
        self.response = response

    def get_timestamp(filename):
      parts = filename.split(FRAME_PREFIX)
      if len(parts) != 2:
          return None
      return parts[1].split('.')[0]

    uploaded_files = []
    for video in lista_videos_descricao:
        print(f"Processing video: {video[0]}")
        video_file_path = video[0]
        extract_frame_from_video(video_file_path)

        files = os.listdir(FRAME_EXTRACTION_DIRECTORY)
        files = sorted(files)
        files_to_upload = []
        for file in files:
          files_to_upload.append(
              File(file_path=os.path.join(FRAME_EXTRACTION_DIRECTORY, file)))
        print(files_to_upload)
        full_video = False

        print(f'Uploading {len(files_to_upload) if full_video else 10} files. This might take a bit...')

        files_to_upload = get_uniformly_distributed_items(files_to_upload, 10)

        for file in files_to_upload if full_video else files_to_upload:
          print(f'Uploading: {file.file_path}...')
          response = genai.upload_file(path=file.file_path)
          file.set_file_response(response)
          uploaded_files.append([video[0],file.timestamp, file.response])

    print(f"Completed file uploads!\n\nUploaded: {len(uploaded_files)} files")

    instruction_1=[]
    instruction_2=[]
    instruction_3=[]

    for file in uploaded_files:
      if file[0] == 'video_1.mp4':
        instruction_1.append(file[1])
        instruction_1.append(file[2])
      elif file[0] == 'video_2.mp4':
        instruction_2.append(file[1])
        instruction_2.append(file[2])
      elif file[0] == video_filename_uploaded:
        instruction_3.append(file[1])
        instruction_3.append(file[2])

    instruction_1.append(lista_videos_descricao[0][1])
    instruction_2.append(lista_videos_descricao[1][1])

    print(f"Instruction 1: {instruction_1}")
    print(f"Instruction 2: {instruction_2}")
    print(f"Instruction 3: {instruction_3}")

    # Inicialização e comunicação com o modelo Plim AI para geração de descrições
    chat = model_plim_ai.start_chat(history=[
      {
        "role": "user",
        "parts": instruction_1
        },
      {
        "role": "user",
        "parts": instruction_2
      },
      {
        "role": "user",
        "parts": instruction_3
      },
    ])

    # Envia a mensagem final para obter a descrição do vídeo carregado
    try:
        chat.send_message('Conforme exemplo anterior, elabore uma descrição para o vídeo')
        video_description = chat.last.text
    except Exception as e:
        # Em caso de falha na comunicação ou geração com o modelo Plim AI
        return jsonify({
            'message': 'Falha na geração de descrição do vídeo.',
            'code': 500,
            'error': str(e)
        }), 500

    # Resposta bem-sucedida com a descrição gerada para o vídeo
    return jsonify({
        'message': 'Vídeo carregado e descrição gerada com sucesso.',
        'code': 200,
        'video_description': video_description,
        'plim_ai_instruction': plim_ai_instruction
    }), 200
