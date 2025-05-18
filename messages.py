from whatsapp_client import WhatsAppClient, create_client_from_env
import os


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
            image_url=image_url
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
