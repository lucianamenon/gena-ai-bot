from flask import Flask, request, jsonify
import os
import logging
import json
from utils import normalize_brazilian_phone


# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import examples

app = Flask(__name__)

from whatsapp_client import WhatsAppClient, create_client_from_env
whatsapp_client = create_client_from_env()

# Chave de verificação do webhook (você deve definir isso como variável de ambiente)
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    """
    Endpoint para verificação do webhook pelo WhatsApp.
    O WhatsApp envia uma solicitação GET com um token de desafio para verificar o endpoint.
    """
    # Parâmetros que o WhatsApp envia
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    logger.info(f"Recebida solicitação de verificação: mode={mode}, token={token}")
    
    # Verificar se o token corresponde ao nosso token de verificação
    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            logger.info("Verificação de webhook bem-sucedida!")
            return challenge, 200
        else:
            logger.warning("Falha na verificação do webhook")
            return "Falha na verificação", 403
    
    return "Parâmetros inválidos", 400

@app.route("/webhook", methods=["POST"])
def receive_webhook():
    """
    Endpoint para receber mensagens do WhatsApp.
    O WhatsApp envia uma solicitação POST com os dados da mensagem.
    """
    try:
        # Obter dados JSON do corpo da solicitação
        data = request.json
        logger.info(f"Webhook recebido: {json.dumps(data, indent=2)}")
        
        # Verificar se é um evento do WhatsApp
        if data.get("object") == "whatsapp_business_account":
            # Processar cada entrada
            for entry in data.get("entry", []):
                # Processar cada alteração
                for change in entry.get("changes", []):
                    # Verificar se é uma mensagem do WhatsApp
                    if change.get("field") == "messages":
                        value = change.get("value", {})
                        
                        # Processar mensagens
                        for message in value.get("messages", []):
                            process_message(message, value.get("contacts", []))
            
            return "EVENT_RECEIVED", 200
        else:
            logger.warning(f"Objeto desconhecido recebido: {data.get('object')}")
            return "Objeto não reconhecido", 404
            
    except Exception as e:
        logger.error(f"Erro ao processar webhook: {str(e)}")
        return "Erro interno", 500

def process_message(message, contacts):
    """
    Processa uma mensagem recebida do WhatsApp.
    
    Args:
        message: Dados da mensagem
        contacts: Informações de contato do remetente
    """

    try:
        # Extrair informações da mensagem
        message_id = message.get("id")
        message_type = message.get("type")
        timestamp = message.get("timestamp")
        
        # Obter informações do contato
        contact = contacts[0] if contacts else {}
        wa_id = contact.get("wa_id", "desconhecido")
        profile_name = contact.get("profile", {}).get("name", "desconhecido")
        normalized_wa_id = normalize_brazilian_phone(wa_id)
        logger.info(f"Mensagem recebida de {profile_name} ({wa_id})")
        
        # Processar diferentes tipos de mensagens
        if message_type == "text":
            text = message.get("text", {}).get("body", "")
            logger.info(f"Mensagem de texto: {text}")
            whatsapp_client.send_text_message(
                to=normalized_wa_id,
                message="Ok, mensagem de texto recebida e processada"
            )
            #examples.run()
                
        elif message_type == "audio":
            logger.info("Áudio recebido")
            whatsapp_client.process_audio_message(message, normalized_wa_id)
            # Processar áudio
        
        #elif message_type == "image":
            # logger.info("Imagem recebida")
            # Processar imagem
            
        #elif message_type == "document":
            # logger.info("Documento recebido")
            # Processar documento
            
        else:
            logger.info(f"Tipo de mensagem não processado: {message_type}")
            
    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)