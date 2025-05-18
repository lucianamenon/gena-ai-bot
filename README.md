# 🤖 GENA - Assistente Virtual WhatsApp

Um assistente virtual inteligente que utiliza a API do WhatsApp Business e o Gemini AI para oferecer atendimento automatizado, responder dúvidas sobre os procedimentos da sua clínica, auxiliar em agendamentos e muito mais.

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Arquitetura](#-arquitetura)
- [Pré-requisitos](#-pré-requisitos)
- [Configuração](#-configuração)
- [Uso](#-uso)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Desenvolvimento](#-desenvolvimento)
- [Troubleshooting](#-troubleshooting)
- [Contribuição](#-contribuição)
- [Licença](#-licença)

## 🌟 Visão Geral

O **Assistente Virtual GENA** é uma solução completa para automatizar o atendimento ao cliente via WhatsApp. Utilizando o poder do Gemini AI para processamento de linguagem natural, o assistente pode entender as intenções dos clientes via áudio e texto, fornecer informações sobre procedimentos, auxiliar em agendamentos e muito mais.

O sistema funciona como um webhook que recebe mensagens do WhatsApp, processa as intenções do usuário com o Gemini AI e executa as operações correspondentes, como enviar informações sobre procedimentos, compartilhar a localização da clínica ou auxiliar em agendamentos.

## ✨ Funcionalidades

### Atendimento ao Cliente
- **Boas-vindas personalizadas** - Recepção amigável com opções de navegação
- **Informações sobre procedimentos** - Detalhes sobre tratamentos estéticos e preços
- **Localização da clínica** - Envio de endereço e coordenadas geográficas
- **Agendamentos** - Auxílio para marcar consultas e procedimentos
- **Respostas a perguntas frequentes** - Informações sobre a clínica e serviços

### Processamento de Linguagem Natural
- Entendimento de linguagem natural com Gemini AI
- Processamento de áudio com transcrição automática
- Detecção de intenções e entidades nas mensagens dos clientes

### Interface WhatsApp
- Mensagens interativas com botões para navegação
- Listas para seleção de procedimentos
- Envio de localização geográfica
- Suporte a mensagens com imagens e texto
- Processamento de mensagens de áudio

## 🏗 Arquitetura

O sistema é composto por quatro componentes principais:

1. **Webhook do WhatsApp** (`app.py`) - Recebe e envia mensagens através da API do WhatsApp Business
2. **Agente Gemini** (`agent.py`) - Processa mensagens usando o Gemini AI para entender intenções
3. **Cliente WhatsApp** (`whatsapp_client.py`) - Gerencia a comunicação com a API do WhatsApp
4. **Utilitários** (`utils.py`) - Funções auxiliares, como normalização de números de telefone

## 📋 Pré-requisitos

- Python 3.11 ou superior
- Docker e Docker Compose (opcional, para containerização)
- Conta no WhatsApp Business API
- Acesso ao Gemini AI (API Key)

## 🔧 Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/lucianamenon/gena-ai-bot.git
cd gena-ai-bot
```

### 2. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```plaintext
# WhatsApp Business API
WHATSAPP_PHONE_NUMBER_ID=seu_phone_number_id
WHATSAPP_ACCESS_TOKEN=seu_access_token
VERIFY_TOKEN=seu_token_de_verificacao

# Gemini AI
GEMINI_API_KEY=sua_chave_api_gemini

# Configurações do servidor
PORT=5000
```

### 3. Instale as dependências (sem Docker)

```shellscript
pip install -r requirements.txt
```

### 4. Ou use Docker Compose

```shellscript
docker-compose up -d
```

## 🚀 Uso

### Iniciar o servidor

```shellscript
# Sem Docker
python app.py

# Com Docker
docker-compose up -d
```

### Configurar o Webhook do WhatsApp

1. Configure um servidor público com HTTPS (use ngrok para testes)
2. Registre a URL do webhook no WhatsApp Business API:
`https://seu-dominio.com/webhook`
3. Use o token de verificação definido em `VERIFY_TOKEN`


### Testar o assistente

Envie uma mensagem para o número do WhatsApp configurado e o assistente responderá de acordo com as instruções programadas.

## 📱 Exemplos de Interação

### Boas-vindas

**Cliente**: "Olá"

**Assistente**:

```plaintext
Olá! 👋 Seja bem-vinda(o) à Clínica Essenza.
Sou a assistente virtual da Dra. Camila Ribeiro e estou aqui para te ajudar com agendamentos, informações sobre nossos procedimentos estéticos ou qualquer outra dúvida.
Como posso te ajudar hoje?

[Endereço] [Agendamentos] [Procedimentos]
```

### Informações sobre procedimentos

**Cliente**: "Quais procedimentos vocês oferecem?"

**Assistente**:

```plaintext
Gostaria de mais informações sobre qual dos procedimentos:

[Ver opções]
- Limpeza de Pele Profunda
- Peeling de Diamante
- Microagulhamento Facial
- Aplicação de Enzimas
- Revitalização Facial
- Botox (Área Glabelar)
- Preenchimento Labial
```

### Localização da clínica

**Cliente**: "Onde fica a clínica?"

**Assistente**: *Envia localização geográfica*

```plaintext
Clínica Essenza
Rua das Rosas, 123 – Centro, Florianópolis – SC
```

## 🧩 Estrutura do Projeto

```plaintext
clinica-essenza-whatsapp/
├── app.py                    # Webhook do WhatsApp
├── agent.py                  # Integração com Gemini AI
├── whatsapp_client.py        # Cliente para API do WhatsApp
├── utils.py                  # Funções utilitárias
├── messages.py               # Funções para enviar mensagens
├── requirements.txt          # Dependências Python
├── Dockerfile                # Configuração do Docker
├── docker-compose.yml        # Configuração do Docker Compose
└── .env                      # Variáveis de ambiente (não versionado)
```

### Descrição dos Componentes

#### app.py

Webhook que recebe e processa mensagens do WhatsApp. Gerencia a verificação do webhook e o encaminhamento de mensagens para o agente.

#### agent.py

Integração com o Gemini AI para processamento de linguagem natural. Define as instruções para o assistente virtual e gerencia a comunicação com a API do Gemini.

#### whatsapp_client.py

Cliente para a API do WhatsApp Business. Implementa métodos para enviar diferentes tipos de mensagens (texto, botões, listas, localização) e processar mensagens de áudio.

#### utils.py

Funções utilitárias, incluindo normalização de números de telefone brasileiros.

#### messages.py

Funções para enviar diferentes tipos de mensagens para os clientes.

## 🛠 Desenvolvimento

### Adicionar novos tipos de mensagens

Para adicionar suporte a novos tipos de mensagens no WhatsApp, estenda a classe `WhatsAppClient` em `whatsapp_client.py`:

```python
def send_new_message_type(self, to, ...):
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        # Configuração específica do tipo de mensagem
    }
    
    return self._send_request(payload)
```

### Melhorar as instruções do assistente

Para melhorar o comportamento do assistente, ajuste as instruções no arquivo `agent.py`:

```python
instrucoes = """
PAPEL:
Você é uma atendente do WhatsApp, altamente especializada...
...
"""
```

## 🔍 Troubleshooting

### Erros comuns

#### ModuleNotFoundError: No module named 'google.adk'

Este erro ocorre quando a biblioteca `google-adk` não está instalada ou há um erro de digitação na importação. Verifique se todas as dependências estão instaladas corretamente:

```shellscript
pip install -r requirements.txt
```

#### ImportError: cannot import name 'safetySetting' from 'vertexai.generative_models'

Este erro ocorre devido a um erro de capitalização. A classe correta é `SafetySetting` (com 'S' maiúsculo):

```python
# Incorreto
from vertexai.generative_models import safetySetting

# Correto
from vertexai.generative_models import SafetySetting
```

#### Erro ao enviar mensagem: 400 Bad Request

Verifique se o número de telefone está no formato correto (com código do país) e se o token de acesso está válido.

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

1. Faça um fork do projeto
2. Crie sua branch de feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request


## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- [WhatsApp Business API](https://developers.facebook.com/docs/whatsapp)
- [Gemini AI](https://ai.google.dev/)
- [Flask](https://flask.palletsprojects.com/)
- [Docker](https://www.docker.com/)
