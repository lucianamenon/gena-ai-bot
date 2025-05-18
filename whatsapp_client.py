import requests
import json
import os
import logging
from typing import List, Dict, Any, Optional, Union
import tempfile
import subprocess

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("whatsapp_client")

class WhatsAppClient:
    """Cliente para integração com a API do WhatsApp Business."""
    
    def __init__(self, phone_number_id: str, access_token: str, version: str = "v22.0"):
        """
        Inicializa o cliente WhatsApp.
        
        Args:
            phone_number_id: ID do número de telefone do WhatsApp Business
            access_token: Token de acesso à API do WhatsApp
            version: Versão da API do WhatsApp (padrão: 22.0)
        """
        self.phone_number_id = phone_number_id
        self.access_token = access_token
        self.version = version
        self.base_url = f"https://graph.facebook.com/{version}/{phone_number_id}"
        self.api_url = f"https://graph.facebook.com/{version}/{phone_number_id}/messages"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
    
    def _send_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Envia uma requisição para a API do WhatsApp.
        
        Args:
            payload: Dados a serem enviados para a API
            
        Returns:
            Resposta da API em formato de dicionário
        """
        # Verificar informações da conta        
        self._check_account_info()
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                data=json.dumps(payload)
            )

            print(f"Status code: {response.status_code}")
            print(f"Resposta: {response.text}")

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao enviar mensagem: {str(e)}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Resposta de erro: {e.response.text}")
            raise
    
    def _check_account_info(self) -> Dict[str, Any]:
        """
        Checa whatsapp account info.
                    
        Returns:
            Resposta da API
        """        
        try:
            response = requests.get(
                self.base_url,
                headers=self.headers
            )
            
            print(f"Status code: {response.status_code}")
            print(f"Resposta: {response.text}")
        
        except Exception as e:
            print(f"Erro: {str(e)}")
            
    def send_text_message(self, to: str, message: str) -> Dict[str, Any]:
        """
        Envia uma mensagem de texto simples.
        
        Args:
            to: Número de telefone do destinatário no formato internacional sem o + (ex: 5511999999999)
            message: Texto da mensagem
            
        Returns:
            Resposta da API
        """
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "text",
            "text": {
                "body": message
            }
        }
        
        logger.info(f"Enviando mensagem de texto para {to}")
        return self._send_request(payload)
    
    def send_button_message(self, to: str, message: str, buttons: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Envia uma mensagem com botões interativos.
        
        Args:
            to: Número de telefone do destinatário
            message: Texto da mensagem
            buttons: Lista de botões no formato [{"id": "btn_id", "title": "Texto do Botão"}]
            
        Returns:
            Resposta da API
        """
        # Converter botões para o formato da API
        formatted_buttons = []
        for button in buttons:
            formatted_buttons.append({
                "type": "reply",
                "reply": {
                    "id": button["id"],
                    "title": button["title"]
                }
            })
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": message
                },
                "action": {
                    "buttons": formatted_buttons
                }
            }
        }
        
        logger.info(f"Enviando mensagem com botões para {to}")
        return self._send_request(payload)
    
    def send_list_message(self, to: str, message: str, button_text: str, sections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Envia uma mensagem com lista de opções.
        
        Args:
            to: Número de telefone do destinatário
            message: Texto da mensagem
            button_text: Texto do botão que abre a lista
            sections: Lista de seções com opções
            
        Returns:
            Resposta da API
        """
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": message
                },
                "action": {
                    "button": button_text,
                    "sections": sections
                }
            }
        }
        
        logger.info(f"Enviando mensagem com lista para {to}")
        return self._send_request(payload)
    
    def send_template_message(self, to: str, template_name: str, language: str = "pt_BR", 
                             components: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Envia uma mensagem de template (para mensagens proativas).
        
        Args:
            to: Número de telefone do destinatário
            template_name: Nome do template aprovado no WhatsApp Business
            language: Código do idioma do template
            components: Componentes do template (parâmetros, botões, etc.)
            
        Returns:
            Resposta da API
        """
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language
                }
            }
        }
        
        if components:
            payload["template"]["components"] = components
        
        logger.info(f"Enviando mensagem de template '{template_name}' para {to}")
        return self._send_request(payload)
    
    def send_product_message(self, to: str, catalog_id: str, product_retailer_id: str) -> Dict[str, Any]:
        """
        Envia um card de produto.
        
        Args:
            to: Número de telefone do destinatário
            catalog_id: ID do catálogo de produtos
            product_retailer_id: ID do produto no catálogo
            
        Returns:
            Resposta da API
        """
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "product",
                "body": {
                    "text": "Confira este produto:"
                },
                "action": {
                    "catalog_id": catalog_id,
                    "product_retailer_id": product_retailer_id
                }
            }
        }
        
        logger.info(f"Enviando card de produto para {to}")
        return self._send_request(payload)
    
    def send_product_list(self, to: str, catalog_id: str, section_title: str, 
                         product_items: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Envia uma lista de produtos.
        
        Args:
            to: Número de telefone do destinatário
            catalog_id: ID do catálogo de produtos
            section_title: Título da seção de produtos
            product_items: Lista de produtos no formato [{"product_retailer_id": "ID_DO_PRODUTO"}]
            
        Returns:
            Resposta da API
        """
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "product_list",
                "header": {
                    "type": "text",
                    "text": "Catálogo de Produtos"
                },
                "body": {
                    "text": "Confira nossos produtos disponíveis:"
                },
                "action": {
                    "catalog_id": catalog_id,
                    "sections": [
                        {
                            "title": section_title,
                            "product_items": product_items
                        }
                    ]
                }
            }
        }
        
        logger.info(f"Enviando lista de produtos para {to}")
        return self._send_request(payload)
    
    def send_location(self, to: str, latitude: float, longitude: float, 
                     name: Optional[str] = None, address: Optional[str] = None) -> Dict[str, Any]:
        """
        Envia uma localização.
        
        Args:
            to: Número de telefone do destinatário
            latitude: Latitude da localização
            longitude: Longitude da localização
            name: Nome do local (opcional)
            address: Endereço do local (opcional)
            
        Returns:
            Resposta da API
        """
        location_data = {
            "latitude": latitude,
            "longitude": longitude
        }
        
        if name:
            location_data["name"] = name
        
        if address:
            location_data["address"] = address
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "location",
            "location": location_data
        }
        
        logger.info(f"Enviando localização para {to}")
        return self._send_request(payload)
    
    def send_image(self, to: str, image_url: str, caption: Optional[str] = None) -> Dict[str, Any]:
        """
        Envia uma imagem.
        
        Args:
            to: Número de telefone do destinatário
            image_url: URL da imagem
            caption: Legenda da imagem (opcional)
            
        Returns:
            Resposta da API
        """
        image_data = {
            "link": image_url
        }
        
        if caption:
            image_data["caption"] = caption
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "image",
            "image": image_data
        }
        
        logger.info(f"Enviando imagem para {to}")
        return self._send_request(payload)
    
    # ... outros métodos de envio de mensagens ...
    
    # ===== MÉTODOS PARA LIDAR COM MÍDIA =====
    
    def get_media_url(self, media_id: str) -> Optional[str]:
        """
        Obtém a URL de download de uma mídia do WhatsApp.
        
        Args:
            media_id: ID da mídia
            
        Returns:
            URL da mídia ou None em caso de erro
        """
        try:
            url = f"https://graph.facebook.com/{self.version}/{media_id}"
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
            
            logger.info(f"Obtendo URL da mídia: {media_id}")
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            media_data = response.json()
            media_url = media_data.get("url")
            
            if not media_url:
                logger.error(f"URL de mídia não encontrada na resposta: {media_data}")
                return None
            
            logger.info(f"URL da mídia obtida com sucesso")
            return media_url
            
        except Exception as e:
            logger.error(f"Erro ao obter URL da mídia: {str(e)}")
            return None
    
    def download_media(self, media_id: str, output_path: Optional[str] = None) -> Optional[str]:
        """
        Baixa uma mídia do WhatsApp.
        
        Args:
            media_id: ID da mídia
            output_path: Caminho onde o arquivo será salvo (opcional)
            
        Returns:
            Caminho do arquivo baixado ou None em caso de erro
        """
        try:
            # Obter a URL da mídia
            media_url = self.get_media_url(media_id)
            if not media_url:
                return None
            
            # Definir o caminho de saída se não for fornecido
            if not output_path:
                # Determinar a extensão com base no tipo MIME
                extension = ".bin"  # Padrão
                
                # Fazer uma requisição HEAD para obter o tipo MIME
                head_response = requests.head(
                    media_url, 
                    headers={"Authorization": f"Bearer {self.access_token}"}
                )
                
                content_type = head_response.headers.get("Content-Type", "")
                if "audio/ogg" in content_type:
                    extension = ".ogg"
                elif "audio/mpeg" in content_type:
                    extension = ".mp3"
                elif "image/jpeg" in content_type:
                    extension = ".jpg"
                elif "image/png" in content_type:
                    extension = ".png"
                elif "video/mp4" in content_type:
                    extension = ".mp4"
                
                # Criar um arquivo temporário com a extensão correta
                output_path = os.path.join(tempfile.gettempdir(), f"{media_id}{extension}")
            
            # Fazer download da mídia
            logger.info(f"Baixando mídia para: {output_path}")
            download_response = requests.get(
                media_url,
                headers={"Authorization": f"Bearer {self.access_token}"}
            )
            download_response.raise_for_status()
            
            # Garantir que o diretório existe
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            
            # Salvar o arquivo
            with open(output_path, "wb") as f:
                f.write(download_response.content)
            
            logger.info(f"Mídia baixada com sucesso: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Erro ao baixar mídia: {str(e)}")
            return None
    
    # ===== MÉTODOS DE TRANSCRIÇÃO DE ÁUDIO =====e
    
    def _convert_audio_format(self, input_path: str, target_format: str = "flac") -> Optional[str]:
        """
        Converte um arquivo de áudio para o formato desejado.
        
        Args:
            input_path: Caminho do arquivo de entrada
            target_format: Formato desejado (flac, wav, mp3)
            
        Returns:
            Caminho do arquivo convertido ou None em caso de erro
        """
        try:
            # Verificar se o arquivo já está no formato correto
            if input_path.lower().endswith(f".{target_format}"):
                return input_path
            
            # Criar um arquivo temporário para a saída
            output_path = tempfile.mktemp(suffix=f".{target_format}")
            
            # Usar FFmpeg para converter o áudio
            logger.info(f"Convertendo áudio para {target_format}: {input_path} -> {output_path}")
            
            # Comando FFmpeg para conversão
            cmd = [
                "ffmpeg",
                "-i", input_path,
                "-y",  # Sobrescrever arquivo de saída se existir
                "-loglevel", "error"
            ]
            
            # Adicionar parâmetros específicos para cada formato
            if target_format == "flac":
                cmd.extend(["-acodec", "flac", "-ar", "16000"])
            elif target_format == "wav":
                cmd.extend(["-acodec", "pcm_s16le", "-ar", "16000"])
            elif target_format == "mp3":
                cmd.extend(["-acodec", "libmp3lame", "-q:a", "2"])
            
            # Adicionar o caminho de saída
            cmd.append(output_path)
            
            # Executar o comando
            subprocess.run(cmd, check=True)
            
            logger.info(f"Conversão concluída: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Erro ao converter áudio: {str(e)}")
            return None
    
    def transcribe_audio_with_gemini(self, audio_path: str) -> Optional[str]:
        """
        Transcreve um arquivo de áudio usando o Gemini.
        
        Args:
            audio_path: Caminho para o arquivo de áudio
            
        Returns:
            Texto transcrito ou None em caso de erro
        """
        try:
            # Importar a biblioteca do Gemini
            try:
                import google.generativeai as genai
            except ImportError:
                logger.error("Biblioteca google.generativeai não instalada. Instale com: pip install google-generativeai")
                return None
            
            # Configurar a API do Gemini
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                logger.error("GEMINI_API_KEY não configurada")
                return None
                
            genai.configure(api_key=api_key)
            
            # Converter para MP3 (formato mais compatível)
            converted_path = self._convert_audio_format(audio_path, "mp3")
            if not converted_path:
                logger.error("Falha ao converter o áudio para MP3")
                return None
            
            # Carregar o modelo Gemini Pro Vision (que pode processar áudio)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Ler o arquivo de áudio
            with open(converted_path, "rb") as f:
                audio_data = f.read()
            
            # Criar a solicitação para o Gemini
            logger.info(f"Enviando áudio para transcrição com Gemini")
            response = model.generate_content([
                "Por favor, transcreva o seguinte áudio em texto. O áudio está em português do Brasil.",
                {"mime_type": "audio/mpeg", "data": audio_data}
            ])
            
            # Limpar arquivos temporários
            if converted_path != audio_path and os.path.exists(converted_path):
                os.unlink(converted_path)
            
            logger.info(f"Transcrição concluída com Gemini: {response.text}")
            return response.text
            
        except Exception as e:
            logger.error(f"Erro ao transcrever com Gemini: {str(e)}")
            return None
    
    def transcribe_audio(self, audio_id: str, service: str = "gemini", language_code: str = "pt-BR") -> Optional[str]:
        """
        Baixa e transcreve um áudio do WhatsApp.
        
        Args:
            audio_id: ID do áudio no WhatsApp
            service: Serviço de transcrição a ser usado ('google' ou 'gemini')
            language_code: Código do idioma (usado apenas com Google Speech-to-Text)
            
        Returns:
            Texto transcrito ou None em caso de erro
        """
        try:
            # Baixar o áudio
            audio_path = self.download_media(audio_id)
            if not audio_path:
                logger.error(f"Não foi possível baixar o áudio: {audio_id}")
                return None
            
            # Transcrever o áudio com o serviço escolhido
            #if service.lower() == "google":
            #    transcription = self.transcribe_audio_with_google(audio_path, language_code)
            if service.lower() == "gemini":
                transcription = self.transcribe_audio_with_gemini(audio_path)
            else:
                logger.error(f"Serviço de transcrição não suportado: {service}")
                return None
            
            # Limpar o arquivo de áudio baixado
            if os.path.exists(audio_path):
                os.unlink(audio_path)
            
            return transcription
            
        except Exception as e:
            logger.error(f"Erro ao transcrever áudio: {str(e)}")
            return None
    
    def process_audio_message(self, message: Dict[str, Any], wa_id: str, service: str = "gemini") -> None:
        """
        Processa uma mensagem de áudio, transcreve e envia a transcrição de volta.
        
        Args:
            message: Dados da mensagem recebida
            wa_id: ID do WhatsApp do remetente
            service: Serviço de transcrição a ser usado ('google' ou 'gemini')
        """
        try:
            # Obter o ID do áudio
            audio_id = message.get("audio", {}).get("id")
            if not audio_id:
                logger.error("ID do áudio não encontrado na mensagem")
                self.send_text_message(
                    to=wa_id,
                    message="Não foi possível processar o áudio. Por favor, tente novamente."
                )
                return
            
            # Informar ao usuário que a transcrição está em andamento
            self.send_text_message(
                to=wa_id,
                message="Recebido! Estou transcrevendo seu áudio, isso pode levar alguns instantes..."
            )
            
            # Transcrever o áudio
            transcription = self.transcribe_audio(audio_id, service)
            
            # Enviar a transcrição de volta para o usuário
            if transcription:
                self.send_text_message(
                    to=wa_id,
                    message=f"📝 *Transcrição do áudio:*\n\n{transcription}"
                )
            else:
                self.send_text_message(
                    to=wa_id,
                    message="Não foi possível transcrever o áudio. Por favor, verifique se o áudio contém fala clara e tente novamente."
                )
                
        except Exception as e:
            logger.error(f"Erro ao processar mensagem de áudio: {str(e)}")
            self.send_text_message(
                to=wa_id,
                message="Ocorreu um erro ao processar o áudio. Por favor, tente novamente mais tarde."
            )

# Função auxiliar para criar o cliente a partir de variáveis de ambiente
def create_client_from_env() -> WhatsAppClient:
    """
    Cria um cliente WhatsApp a partir de variáveis de ambiente.
    
    Variáveis necessárias:
    - WHATSAPP_PHONE_NUMBER_ID: ID do número de telefone do WhatsApp Business
    - WHATSAPP_ACCESS_TOKEN: Token de acesso à API do WhatsApp
    
    Returns:
        Cliente WhatsApp configurado
    """
    phone_number_id = os.environ.get("WHATSAPP_PHONE_NUMBER_ID")
    access_token = os.environ.get("WHATSAPP_ACCESS_TOKEN")
    
    if not phone_number_id or not access_token:
        raise ValueError(
            "As variáveis de ambiente WHATSAPP_PHONE_NUMBER_ID e WHATSAPP_ACCESS_TOKEN são obrigatórias"
        )
    
    return WhatsAppClient(phone_number_id, access_token)

print("Módulo de integração com WhatsApp Business API criado com sucesso!")