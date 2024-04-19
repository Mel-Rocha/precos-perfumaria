import requests
from bs4 import BeautifulSoup
import re

def scrape_product_price(url):
    # Realiza o request para a URL
    response = requests.get(url)

    # Verifica se a requisição foi bem-sucedida
    if response.status_code != 200:
        raise Exception("URL inválida ou não encontrada")

    # Parseia o conteúdo HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Inicializa uma variável para armazenar o preço extraído usando a expressão regular
    price_from_regex = None

    # Encontra todos os elementos que contêm a chave "Value" usando expressão regular
    pattern = r'"Value"\s*:\s*([\d.]+)'
    matches = re.findall(pattern, response.text)

    # Se houver correspondências, extrai o valor encontrado
    if matches:
        price_from_regex = matches[0]
    else:
        price_from_regex = "Nenhum valor correspondente encontrado."

    # Retorna apenas o preço extraído usando a expressão regular
    return price_from_regex

# Teste da função
url = "https://www.ikesaki.com.br/coloracao-igora-royal-8-77-louro-claro-cobre-extra-60g-76-37/p"
price_from_regex = scrape_product_price(url)
print("Preço extraído usando regex:", price_from_regex)

def scrape_product_info(url):
    # Realiza o request para a URL
    response = requests.get(url)
    # Verifica se a requisição foi bem-sucedida
    if response.status_code != 200:
        raise Exception("URL inválida ou não encontrada")

    # Parseia o conteúdo HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontra o título do produto
    product_element = soup.find('h1')
    product = product_element.text.strip() if product_element else None


    # Retorna um dicionário com as chaves "product" e "price"
    return {"product": product}

url = 'https://www.ikesaki.com.br/coloracao-igora-royal-8-77-louro-claro-cobre-extra-60g-76-37/p'
product_info = scrape_product_info(url)
print(product_info)
