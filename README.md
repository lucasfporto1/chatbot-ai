# Chatbot AI — assistente técnico com Gemini

Chat web simples em Flask que responde dúvidas de tecnologia (hardware, software e áreas afins) usando a API do Google Gemini. É um projeto de estudo.

## O que ele faz

- Interface de chat no navegador (`Templates/index.html`).
- Backend em Flask (`app.py`) com a rota `POST /get_response`.
- `chat.py` monta o pedido para a API REST do Gemini com:
  - **system prompt** que define o papel (assistente técnico), o tom (objetivo, com listas) e que o assistente deve se manter no assunto de tecnologia;
  - **histórico da conversa** enviado a cada mensagem, para o modelo manter o contexto;
  - hora atual injetada no prompt, usada só se o usuário perguntar as horas;
  - tratamento de erros da API (429 e 503 com mensagens amigáveis, timeout de 30 s).

## Stack

Python, Flask, requests, python-dotenv, HTML/CSS/JavaScript e a API REST do Gemini.

## Como rodar

```bash
python -m venv venv
venv\Scripts\activate        # Windows  (Linux/macOS: source venv/bin/activate)
pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz com a sua chave:

```
GEMINI_API_KEY=sua_chave_aqui
```

```bash
python app.py
```

Abra `http://localhost:5000`.

## Limitações conhecidas

Este projeto é simples de propósito e não é um sistema pronto para produção:

- **Não é RAG:** ele não consulta documentos próprios; as respostas vêm só do conhecimento do modelo.
- O histórico fica na sessão do Flask (cookie), então conversas longas podem estourar o limite de tamanho do cookie.
- A chave secreta da sessão é gerada a cada início do servidor, então as sessões se perdem ao reiniciar.
- Não há testes automatizados nem limite de requisições por usuário.

## Próximos passos

- Guardar o histórico no servidor (ex.: Redis ou banco de dados).
- Adicionar recuperação de documentos (RAG) para respostas baseadas em fontes.
- Testes e avaliação das respostas.
