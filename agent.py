import vertexai
from vertexai.generative_models import SafetySetting, Tool, FunctionDeclaration
from whatsapp_client import WhatsAppClient, create_client_from_env
import os

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types  # Para criar conteúdos (Content e Part)

instrucoes = """
TELEFONE DO CONTATO: {}

------------------------------------------------------------------------------------
PAPEL:
Você é uma atendente do WhatsApp, altamente especializada, que atua em nome da Clínica Essenza, prestando um serviço de excelência. Sua missão é atender aos pacientes de maneira ágil e eficiente, respondendo dúvidas sobre a clínica, os procedimento realizados e auxiliando os pacientes com agendamentos.

PERSONALIDADE E TOM DE VOZ:
- Simpática, prestativa e humana
- Tom de voz sempre simpatico, acolhedor e respeitoso

OBJETIVO:
1. Fornecer atendimento diferenciado e cuidadoso aos pacientes.
2. Responder dúvidas sobre a clínica (procedimentos, horários, localização, formas de pagamento).
3. Agendar, remarcar e cancelar consultas de forma simples e eficaz.
4. Agir passo a passo para garantir rapidez e precisão em cada atendimento.

CONTEXTO:
- Você otimiza o fluxo interno da clínica, provendo informações e reduzindo a carga administrativa dos profissionais de saúde.
- Seu desempenho impacta diretamente a satisfação do paciente e a eficiência das operações médicas.

------------------------------------------------------------------------------------
FLUXOS:

1. Início do atendimento:
   - Envie a mensagem de boas vindas com a função 'send_message' com o parâmetro type='WELCOME'

2. Agendamentos
    - Para agendamentos envie o link da nossa agenda pública, utilizando a função 'send_message' com o parâmetro type='CALENDARIO'

3. Procedimentos:
    - Se a pessoa quer conher mais sobre os procedimentos ofertados, envie a lista de procedimento com a função 'send_message' com o parâmetro type= 'PROCEDIMENTO'
    - Se a pessoa quer mais informações sobre um procedimento em específico, envie uma descrição e imagem (se disponível):
        = Se você tiver o link de imagem do procedimento utilize a função 'send_message' com o parâmetro type= 'image', mensagem=descrição do procedimento e url_image=url da imagem
        = Se você não tiver o link de imagem do procedimento utilize a função 'send_message' com o parâmetro type= 'text', mensagem=descrição do procedimento
       
4. Endereço:
    - Envie a mensagem de endereço com a função 'send_message' com o parâmetro type=  'ENDERECO'

5. Assuntos fora do escopo da clínica (Fallback):
    - Envie a mensagem de fallback com a função 'send_message' com o parâmetro type=  'FALLBACK'

6. Encerramento
    - Envie a mensagem de encerramento com a função 'send_message' com o parâmetro type=  'ENCERRAMENTO'

7. Outros assunto
    - Reponsa com uma mensagem de texto utilizando a função 'send_message' com o parâmetro type= 'text', mensagem=texto gerado pelo gemini

------------------------------------------------------------------------------------
INSTRUÇÕES GERAIS:

1. Respostas claras, objetivas e úteis:
   - Forneça informações sobre especialidades, horários, endereço, valores e convênios.

2. Nunca fornecer informações erradas:
   - Evite erros sobre horários, contatos ou serviços.

3. Utilize uma linguagem informal e acolhedora, com emojis:
   - Mantenha a fluidez do atendimento.

------------------------------------------------------------------------------------
INFORMAÇÕES DA CLÍNICA

Nome da clínica: Clínica Essenza
Endereço: Rua das Rosas, 123 - Centro, Florianópolis - SC
Telefone/WhatsApp: (48) 91234-5678
Email: contato@essenzaclinica.com.br
Horário de atendimento: Segunda a sábado, das 9h às 19h
Link Google Maps: https://maps.app.goo.gl/pJibejW5CF3GPM3JA

Profissional Responsável
Nome: Dra. Camila Ribeiro
Especialização: Biomédica Esteta - CRBM 000000

FORMAS DE PAGAMENTO:
- Formas de pagamento: PIX, dinheiro, cartão de débito ou crédito

PROCEDIMENTOS:

Limpeza de pele profunda	
Higienização, esfoliação, extração e máscara calmante.
180,00
https://www.daniellesales.com.br/wp-content/uploads/2023/07/limpeza-de-pele-profunda-voce-conhece-todos-os-seus-beneficios-danielle-sales.jpg

Peeling de diamante
Esfoliação mecânica para renovação celular e melhora da textura da pele.
200,00
https://24698e6a.delivery.rocketcdn.me/wp-content/uploads/2022/11/1-39-960x540.jpg

Microagulhamento facial
Estimula colágeno e trata cicatrizes de acne, linhas finas e manchas.
350,00

Aplicação de enzimas
Redução localizada de gordura com enzimas injetáveis.
280,00

Revitalização facial
Máscaras, vitaminas e hidratação intensa para viço e elasticidade.
220,00

Botox (área glabelar)
Aplicação para suavizar rugas entre as sobrancelhas.
600,00

Preenchimento labial
Harmonização dos lábios com ácido hialurônico.
950,00

------------------------------------------------------------------------------------

OBSERVAÇÕES FINAIS:

- Nunca forneça diagnósticos ou opiniões médicas.
- Qualquer assunto fora do escopo da clínica deve ser direcionado à ferramenta "FALLBACK".
- Mantenha o tom profissional, claro e respeitoso o tempo todo, utilize emojis para uma conversa mais fluida.
- Link da agenda para agendamento online: https://calendar.app.google/k43eFCyMvQts1ZSs9
- Sempre agendar datas futuras, nunca passadas.
- Se o Paciente estou insatisfeito com vocês, escale imediatamente para humano.

----------------------------------------------------------------------------------------
"""

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 0,
    "top_p": 0.95,
    "seed": 0,
}

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
    ),
]

# tool para acionar function calling
tools = Tool(
	function_declarations=[
		FunctionDeclaration(
			name="send_message",
			description="Envia mensagens para o cliente.",
			parameters={
				"type": "object",
				"properties": {
					"to": {
						"type": "string",
						"description": "Número do telefone do cliente"
					},
					"type": {
						"type": "string",
						"description": "Tipo da mensagem a ser enviada (text, image, welcome, fallback, procedimentos endereco, encerramento)"
					},
                    "message": {
						"type": "string",
						"description": "Mensagem (texto) a ser enviado ao cliente."
					},
                    "image_url": {
						"type": "string",
						"description": "URL da imagem a ser enviada ao cliente."
					},
                    "required": ["to", "type"]
				}
			}
            
		)
	]
)

# Função auxiliar que envia uma mensagem para um agente via Runner e retorna a resposta final
def call_agent(agent: Agent, message_text: str) -> str:
    # Cria um serviço de sessão em memória
    session_service = InMemorySessionService()
    # Cria uma nova sessão (você pode personalizar os IDs conforme necessário)
    session = session_service.create_session(app_name=agent.name, user_id="user1", session_id="session1")
    # Cria um Runner para o agente
    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
    # Cria o conteúdo da mensagem de entrada
    content = types.Content(role="user", parts=[types.Part(text=message_text)])

    final_response = ""
    # Itera assincronamente pelos eventos retornados durante a execução do agente
    for event in runner.run(user_id="user1", session_id="session1", new_message=content):
        if event.is_final_response():
          for part in event.content.parts:
            if part.text is not None:
              final_response += part.text
              final_response += "\n"
    return final_response

def process_user_input(message, phone_number):

    buscador = Agent(
        name="Secretária Virtual",
        model="gemini-2.0-flash",
        instruction=instrucoes.format(phone_number),
        description="Você é uma atendente do WhatsApp, altamente especializada, que atua em nome da Clínica Essenza, prestando um serviço de excelência. Sua missão é atender aos pacientes de maneira ágil e eficiente, respondendo dúvidas sobre a clínica, os procedimento realizados e auxiliando os pacientes com agendamentos.",
        tools=[tools]
    )

    lancamentos = call_agent(buscador, message)
    return lancamentos

def send_message(to, type, message="Olá! Esta é uma mensagem de teste da API do WhatsApp.", image_url="https://example.com/imagem.jpg"): 

    client = create_client_from_env()

    if type == 'text':
        response = client.send_text_message(
            to=to,
            message=message
        )
        print(f"Resposta da mensagem de texto: {response}")

    if type == 'image':
        response = client.send_text_message(
            to=to,
            image_url=image_url,
            message=message
        )
        print(f"Resposta da mensagem de texto: {response}")
    
    elif type == 'welcome':
        # Exemplo 2: Enviar mensagem com botões
        response = client.send_button_message(
            to=to,
            message=f"""Olá! 👋 Seja bem-vinda(o) à Clínica Essenza.
    Sou a assistente virtual da Dra. Camila Ribeiro e estou aqui para te ajudar com agendamentos, informações sobre nossos procedimentos estéticos ou qualquer outra dúvida.
    Como posso te ajudar hoje?""",
            buttons=[
                {"id": "btn_endereco", "title": "Endereço"},
                {"id": "btn_agendamento", "title": "Agendamentos"},
                {"id": "btn_procedimentos", "title": "Procedimentos"}
            ]
        )
        print(f"Resposta da mensagem com botões: {response}")
    
    elif type == 'fallback':
        # Exemplo 2: Enviar mensagem com botões
        response = client.send_button_message(
            to=to,
            message=f"""Hmm... não entendi muito bem o que você quis dizer 😕
Você pode reformular a pergunta ou escolher uma das opções abaixo:""",
            buttons=[
                {"id": "btn_endereco", "title": "Endereço"},
                {"id": "btn_agendamento", "title": "Agendamentos"},
                {"id": "btn_procedimentos", "title": "Procedimentos"}
            ]
        )
        print(f"Resposta da mensagem com botões: {response}")

    elif type == 'procedimentos':
        # Exemplo 3: Enviar mensagem com lista de opções
        sections = [
            {
                "title": "Procedimentos",
                "rows": [
                    {
                        "id": "limpeza_pele",
                        "title": "Limpeza de Pele Profunda",
                        "description": "Procedimento que remove impurezas, cravos e células mortas, promovendo a renovação celular e melhorando a textura da pele. Valor: R$ 180,00"
                    },
                    {
                        "id": "peeling_diamante",
                        "title": "Peeling de Diamante",
                        "description": "Esfoliação mecânica para renovação celular e melhora da textura da pele. Valor: R$ 200,00"
                    },
                    {
                        "id": "microagulhamento_facial",
                        "title": "Microagulhamento Facial",
                        "description": "Estimula a produção de colágeno e trata cicatrizes de acne, rugas finas e manchas. Valor: R$ 350,00"
                    },
                    {
                        "id": "aplicacao_enzimas",
                        "title": "Aplicação de Enzimas",
                        "description": "Injeções subcutâneas que auxiliam na quebra de gordura localizada. Valor: R$ 280,00"
                    },
                    {
                        "id": "revitalizacao_facial",
                        "title": "Revitalização Facial",
                        "description": "Combinação de hidratação profunda e vitaminas para melhorar o viço e a elasticidade da pele. Valor: R$ 220,00"
                    },
                    {
                        "id": "botox_glabela",
                        "title": "Botox (Área Glabelar)",
                        "description": "Aplicação de toxina botulínica na região entre as sobrancelhas para suavizar linhas de expressão. Valor: R$ 600,00"
                    },
                    {
                        "id": "preenchimento_labial",
                        "title": "Preenchimento Labial",
                        "description": "Harmonização dos lábios com ácido hialurônico para volume e contorno. Valor: R$ 950,00"
                    }
                ]
            }
        ]
    
        response = client.send_list_message(
            to=to,
            message="Gostaria de mais informações sobre qual dos procedimentos:",
            button_text="Ver opções",
            sections=sections
        )
        print(f"Resposta da mensagem com lista: {response}")

    elif type == 'endereco':
        # Exemplo 7: Enviar localização
        response = client.send_location(
            to=to,
            latitude=-27.6041405,
            longitude=-48.5621391,
            name="Clínica Essenza",
            address="Rua das Rosas, 123 – Centro, Florianópolis – SC"
        )
        print(f"Resposta da localização: {response}")

    elif type == 'encerramento':
        response = client.send_text_message(
            to=to,
            text=f"""Foi um prazer te atender! 💖
Se tiver mais alguma dúvida ou quiser reagendar seu atendimento, é só me chamar aqui.
A Clínica Essenza agradece sua confiança. Até logo! ✨')"""
        )
        print(f"Resposta da mensagem de texto: {response}")
