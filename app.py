from flask import Flask, render_template, request, jsonify, session
from chat import enviar_para_gemini 
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    # Cada usuário tem seu próprio histórico na sessão
    if 'historico' not in session:
        session['historico'] = []
    
    dados = request.get_json()
    msg_usuario = dados.get("message")
    
    if not msg_usuario:
        return jsonify({"response": "Mensagem vazia!"})
    
    resposta_ia = enviar_para_gemini(msg_usuario, session['historico'])
    session.modified = True
    
    return jsonify({"response": resposta_ia})

if __name__ == '__main__':
    app.run(debug=True)




