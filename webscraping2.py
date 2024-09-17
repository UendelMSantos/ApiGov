import requests

codigo_municipio = input("Digite o código do município: ")
exercicio_orcamento = input("Digite o exercício orçamentário (ex: 202400): ")
data_referencia = input("Digite a data de referência (ex: 202405): ")

url_orgaos = f"https://api-dados-abertos.tce.ce.gov.br/orgaos?codigo_municipio={codigo_municipio}&exercicio_orcamento={exercicio_orcamento}"
url_unidades = f"https://api-dados-abertos.tce.ce.gov.br/unidades_orcamentarias?codigo_municipio={codigo_municipio}&exercicio_orcamento={exercicio_orcamento}&quantidade=100&deslocamento=0"
url_receitas = f"https://api-dados-abertos.tce.ce.gov.br/balancete_receita_orcamentaria?codigo_municipio={codigo_municipio}&exercicio_orcamento={exercicio_orcamento}&data_referencia={data_referencia}"


def buscar_orgaos(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        orgaos = {orgao['codigo_orgao']: orgao['nome_orgao'] for orgao in data['data']}
        return orgaos
    else:
        print(f"Erro ao acessar a API de órgãos: {response.status_code}")
        return {}


def buscar_unidades(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        unidades = {(unidade['codigo_orgao'], unidade['codigo_unidade'].strip()): unidade['nome_unidade'] for unidade in data['data']}
        return unidades
    else:
        print(f"Erro ao acessar a API de unidades: {response.status_code}")
        return {}


def get_data_receitas(url, orgaos, unidades):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        receitas = data['data']
        for receita in receitas:
            codigo_orgao = receita.get('codigo_orgao', '')
            nome_orgao = orgaos.get(codigo_orgao, 'Desconhecido')
            receita['nome_orgao'] = nome_orgao
            
            codigo_unidade = receita.get('codigo_unidade', '').strip()
            nome_unidade = unidades.get((codigo_orgao, codigo_unidade), 'Desconhecida')
            receita['nome_unidade'] = nome_unidade
            
            print(f"Órgão: {nome_orgao}, Unidade: {nome_unidade}, Receita: R$ {receita.get('valor_arrecadacao_ate_mes', 0):.2f}")
    else:
        print(f"Erro ao acessar a API de receitas: {response.status_code}")

orgaos = buscar_orgaos(url_orgaos)
unidades = buscar_unidades(url_unidades)

get_data_receitas(url_receitas, orgaos, unidades)
