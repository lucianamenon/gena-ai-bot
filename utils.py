import re
from typing import Optional

def normalize_brazilian_phone(phone_number: str) -> str:
    """
    Normaliza um número de telefone brasileiro para o formato internacional completo.
    
    Regras:
    1. Se o número já começa com 55 e tem comprimento correto, verifica se precisa adicionar o 9
    2. Se o número não começa com 55, assume que é brasileiro e adiciona o prefixo
    3. Lida com formatos como: 42984285525, 984285525, 5542984285525, etc.
    
    Args:
        phone_number: Número de telefone em qualquer formato
        
    Returns:
        Número normalizado no formato internacional (ex: 5542984285525)
    """
    if not phone_number:
        return phone_number
    
    # Remover caracteres não numéricos
    clean_number = re.sub(r'\D', '', phone_number)
    
    # Se o número já está no formato internacional completo (13 dígitos para BR)
    if clean_number.startswith('55') and len(clean_number) == 13:
        return clean_number
    
    # Se o número está no formato internacional sem o 9 (12 dígitos para BR)
    if clean_number.startswith('55') and len(clean_number) == 12:
        area_code = clean_number[2:4]
        subscriber = clean_number[4:]
        return f"55{area_code}9{subscriber}"
    
    # Se o número tem apenas o código de área + número (10 dígitos)
    if len(clean_number) == 10:
        area_code = clean_number[:2]
        subscriber = clean_number[2:]
        return f"55{area_code}9{subscriber}"
    
    # Se o número tem código de área + 9 + número (11 dígitos)
    if len(clean_number) == 11 and clean_number[2] == '9':
        area_code = clean_number[:2]
        subscriber = clean_number[2:]
        return f"55{area_code}{subscriber}"
    
    # Se o número tem apenas o 9 + número (9 dígitos)
    if len(clean_number) == 9 and clean_number[0] == '9':
        # Não temos o código de área, então não podemos normalizar completamente
        return clean_number
    
    # Se o número tem apenas o número sem o 9 (8 dígitos)
    if len(clean_number) == 8:
        # Não temos o código de área, então não podemos normalizar completamente
        return f"9{clean_number}"
    
    # Se não conseguimos identificar o formato, retornamos o número original limpo
    return clean_number

def is_brazilian_number(phone_number: str) -> bool:
    """
    Verifica se um número de telefone é brasileiro.
    
    Args:
        phone_number: Número de telefone
        
    Returns:
        True se for um número brasileiro, False caso contrário
    """
    clean_number = re.sub(r'\D', '', phone_number)
    
    # Números brasileiros começam com 55 ou têm 10/11 dígitos
    return (clean_number.startswith('55') or 
            len(clean_number) == 10 or 
            len(clean_number) == 11)

def extract_area_code(phone_number: str) -> Optional[str]:
    """
    Extrai o código de área de um número brasileiro.
    
    Args:
        phone_number: Número de telefone
        
    Returns:
        Código de área ou None se não for possível extrair
    """
    clean_number = re.sub(r'\D', '', phone_number)
    
    if clean_number.startswith('55'):
        return clean_number[2:4]
    elif len(clean_number) >= 10:
        return clean_number[:2]
    
    return None