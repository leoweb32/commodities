import requests
from bs4 import BeautifulSoup
import json

# URLs das páginas que queremos acessar
urls = {
    'Boi Gordo': 'https://www.noticiasagricolas.com.br/cotacoes/boi-gordo',
    'Soja': 'https://www.noticiasagricolas.com.br/cotacoes/soja',
    'Milho': 'https://www.noticiasagricolas.com.br/cotacoes/milho',
    'Ovo': 'https://www.noticiasagricolas.com.br/cotacoes/ovos',
    'Leite': 'https://www.noticiasagricolas.com.br/cotacoes/leite'
}

# Função para extrair os dados da tabela
def extrair_dados(url, commodity_name):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontrar a tabela de interesse
        table = soup.find('table', class_='cot-fisicas')
        if not table:
            print(f"Erro: Não foi possível encontrar a tabela para {commodity_name}")
            return []
        
        # Extrair os dados da tabela
        data = []
        for row in table.find('tbody').find_all('tr'):
            cols = row.find_all('td')
            if len(cols) >= 3:  # Verificar se há pelo menos 3 colunas
                data.append({
                    'Commodity': commodity_name,
                    'Data': cols[0].text.strip(),
                    'à vista R$': cols[1].text.strip(),
                    'Variação (%)': cols[2].text.strip(),
                })
        return data
    else:
        print(f"Erro ao acessar a página {commodity_name}: {response.status_code}")
        return []

# Lista para armazenar os dados de todas as commodities
dados_totais = []

# Percorrer todas as URLs e extrair os dados
for commodity, url in urls.items():
    dados = extrair_dados(url, commodity)
    dados_totais.extend(dados)

# Imprimir os dados extraídos
for item in dados_totais:
    print(f"Commodity: {item['Commodity']}, Data: {item['Data']}, à vista R$: {item['à vista R$']}, Variação (%): {item['Variação (%)']}")

# Salvar os dados em um arquivo JSON
with open('dados_commodities.json', 'w') as f:
    json.dump(dados_totais, f, indent=4)

print("Dados salvos em 'dados_commodities.json'")