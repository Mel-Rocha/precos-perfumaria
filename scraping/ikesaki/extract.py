import requests
from bs4 import BeautifulSoup

def scrape_whole_page(url):
    # Realiza o request para a URL
    response = requests.get(url)
    # Verifica se a requisição foi bem-sucedida
    if response.status_code != 200:
        raise Exception("URL inválida ou não encontrada")

    # Parseia o conteúdo HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Formata o HTML usando o método prettify()
    html_prettified = soup.prettify()

    return html_prettified

url = 'https://www.ikesaki.com.br/coloracao-igora-royal-8-77-louro-claro-cobre-extra-60g-76-37/p'

html_content = scrape_whole_page(url)
print(html_content)

