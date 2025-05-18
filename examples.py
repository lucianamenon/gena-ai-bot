from whatsapp_client import WhatsAppClient, create_client_from_env
import os

def run():

    client = create_client_from_env()
    
    # Número de telefone do destinatário (formato internacional sem o +)
    to = os.environ.get("TEST_NUMBER")  # Substitua pelo número real
    
    # Exemplo 1: Enviar mensagem de texto simples
    response = client.send_text_message(
        to=to,
        message="Olá! Esta é uma mensagem de teste da API do WhatsApp."
    )
    print(f"Resposta da mensagem de texto: {response}")
    
    # Exemplo 2: Enviar mensagem com botões
    response = client.send_button_message(
        to=to,
        message="Por favor, escolha uma opção:",
        buttons=[
            {"id": "btn_sim", "title": "Sim"},
            {"id": "btn_nao", "title": "Não"},
            {"id": "btn_talvez", "title": "Talvez"}
        ]
    )
    print(f"Resposta da mensagem com botões: {response}")
    
    # Exemplo 3: Enviar mensagem com lista de opções
    sections = [
        {
            "title": "Categorias",
            "rows": [
                {
                    "id": "cat_eletronicos",
                    "title": "Eletrônicos",
                    "description": "Smartphones, TVs, etc."
                },
                {
                    "id": "cat_moda",
                    "title": "Moda",
                    "description": "Roupas, calçados, etc."
                }
            ]
        },
        {
            "title": "Promoções",
            "rows": [
                {
                    "id": "promo_dia",
                    "title": "Promoção do Dia",
                    "description": "Ofertas especiais"
                }
            ]
        }
    ]
    
    response = client.send_list_message(
        to=to,
        message="Escolha uma categoria:",
        button_text="Ver opções",
        sections=sections
    )
    print(f"Resposta da mensagem com lista: {response}")
    
    # Exemplo 4: Enviar mensagem de template (mensagem ativa/proativa)
    # Nota: O template deve estar aprovado no WhatsApp Business
    components = [
        {
            "type": "body",
            "parameters": [
                {
                    "type": "text",
                    "text": "João"
                },
                {
                    "type": "text",
                    "text": "50%"
                }
            ]
        }
    ]
    
    response = client.send_template_message(
        to=to,
        template_name="promocao_especial",  # Nome do seu template aprovado
        language="pt_BR",
        components=components
    )
    print(f"Resposta da mensagem de template: {response}")
    
    # Exemplo 5: Enviar card de produto
    # Nota: Você precisa ter um catálogo de produtos configurado
    response = client.send_product_message(
        to=to,
        catalog_id="123456789",  # ID do seu catálogo
        product_retailer_id="SKU123"  # ID do produto
    )
    print(f"Resposta do card de produto: {response}")
    
    # Exemplo 6: Enviar lista de produtos
    product_items = [
        {"product_retailer_id": "SKU123"},
        {"product_retailer_id": "SKU456"},
        {"product_retailer_id": "SKU789"}
    ]
    
    response = client.send_product_list(
        to=to,
        catalog_id="123456789",  # ID do seu catálogo
        section_title="Produtos em Destaque",
        product_items=product_items
    )
    print(f"Resposta da lista de produtos: {response}")
    
    # Exemplo 7: Enviar localização
    response = client.send_location(
        to=to,
        latitude=-23.5505,
        longitude=-46.6333,
        name="Escritório Central",
        address="Av. Paulista, 1000, São Paulo - SP"
    )
    print(f"Resposta da localização: {response}")
    
    # Exemplo 8: Enviar imagem
    response = client.send_image(
        to=to,
        image_url="https://example.com/imagem.jpg",
        caption="Confira nossa nova loja!"
    )
    print(f"Resposta da imagem: {response}")