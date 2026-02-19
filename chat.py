import requests
import datetime
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega o .env

API_KEY = os.getenv('GEMINI_API_KEY')
if not API_KEY:
    raise ValueError("GEMINI_API_KEY não encontrada no .env")

# 1. Configurações
MODELO = 'gemini-3-flash-preview'
URL_BASE = f'https://generativelanguage.googleapis.com/v1beta/models/{MODELO}:generateContent?key={API_KEY}'


def enviar_para_gemini(mensagem_usuario, historico):
    # Pegando a hora exata no momento da função
    hora_atual = datetime.datetime.now().strftime("%H:%M:%S")


    # 2. Instruções de Sistema dinâmicas
    SYSTEM_PROMPT = f"""
    Você é um assistente técnico da TechPorto, seu objetivo é sanar dúvidas na área da tecnologia.
    REGRAS:
    1. Seja objetivo, mas forneça informações completas.
    2. Use listas para facilitar a leitura.
    3. Vá direto ao ponto técnico.
    4. Quero que você seja completo e extremamente versátil na área da tecnologia.
    5.Não deixe o usuário trocar de assunto, você é um assistente de tecnologia.
    6. Você tem acesso ao horário atual: {hora_atual}, mas SÓ mencione a hora se o usuário perguntar "que horas são".
    """


    # Adiciona a mensagem do usuário ao histórico
    historico.append({
        "role": "user",
        "parts": [{"text": mensagem_usuario}]
    })
   
    # Montagem do Payload 
    payload = {
        "system_instruction": {
            "parts": [{"text": SYSTEM_PROMPT}]
        },
        "contents": historico,
        "generationConfig": {
            "maxOutputTokens": 1000,
            "temperature": 0.3
        }
    }


    try:
        headers = {'Content-Type': 'application/json'}
        resposta = requests.post(URL_BASE, json=payload, headers=headers, timeout=30)
        
        if resposta.status_code == 429:
                return "O sistema está um pouco sobrecarregado (Muitas requisições). Aguarde 1 minuto e tente novamente."
    
        if resposta.status_code == 503:
            return "O servidor do Google está sobrecarregado agora. Aguarde 30 segundos e tente novamente."
       
        if resposta.status_code != 200:
            print(f"❌ Erro da API: {resposta.status_code}")
            print(f"Resposta completa: {resposta.text}")
            return f"Erro na API (Status {resposta.status_code}). Verifique o console."
       
        dados = resposta.json()
       
        if 'candidates' in dados and dados['candidates']:
            texto_ia = dados['candidates'][0]['content']['parts'][0]['text']
           
            historico.append({
                "role": "model",
                "parts": [{"text": texto_ia}]
            })
            return texto_ia
        else:
            print(f"❌ Resposta sem candidates: {dados}")
            return "A IA não gerou uma resposta válida."


    except Exception as e:
        print(f"Erro de conexão: {e}")
        return "Erro de conexão: Verifique o console."
