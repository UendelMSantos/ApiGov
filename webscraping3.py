import requests

codigo_municipio = input("Digite o código do município: ")
exercicio_orcamento = input("Digite o exercício orçamentário (ex: 202400): ")
data_referencia = input("Digite a data de referência (ex: 202405): ")

url_orgaos = f"https://api-dados-abertos.tce.ce.gov.br/orgaos?codigo_municipio={codigo_municipio}&exercicio_orcamento={exercicio_orcamento}"
url_unidades = f"https://api-dados-abertos.tce.ce.gov.br/unidades_orcamentarias?codigo_municipio={codigo_municipio}&exercicio_orcamento={exercicio_orcamento}&quantidade=100&deslocamento=0"
url_receitas = f"https://api-dados-abertos.tce.ce.gov.br/balancete_receita_orcamentaria?codigo_municipio={codigo_municipio}&exercicio_orcamento={exercicio_orcamento}&data_referencia={data_referencia}"
url_despesas = f"https://api-dados-abertos.tce.ce.gov.br/balancete_despesa_orcamentaria?codigo_municipio={codigo_municipio}&exercicio_orcamento={exercicio_orcamento}&data_referencia={data_referencia}&quantidade=100&deslocamento=0"

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

def substituir_codigos_por_nomes(dados, orgaos, unidades):
    """ Substitui códigos pelos nomes dos órgãos e unidades. """
    for item in dados:
        if isinstance(item, dict):  # Verifica se item é um dicionário
            codigo_orgao = item.get('codigo_orgao', '')
            item['nome_orgao'] = orgaos.get(codigo_orgao, 'Desconhecido')

            codigo_unidade = item.get('codigo_unidade', '').strip()
            item['nome_unidade'] = unidades.get((codigo_orgao, codigo_unidade), 'Desconhecida')

    return dados


def get_data_receitas(url, orgaos, unidades):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        receitas = substituir_codigos_por_nomes(data.get('data', []), orgaos, unidades)
        return {"data": receitas}
    else:
        print(f"Erro ao acessar a API de receitas: {response.status_code}")
        return {}

def get_data_despesas(url, orgaos, unidades):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        despesas = substituir_codigos_por_nomes(data.get('data', []), orgaos, unidades)
        return {"data": despesas}
    else:
        print(f"Erro ao acessar a API de despesas: {response.status_code}")
        return {}

orgaos = buscar_orgaos(url_orgaos)
unidades = buscar_unidades(url_unidades)

opcao = input("Escolha uma opção: 1 - Receitas, 2 - Despesas, 3 - Ambos: ")

if opcao == '1':
    json_receitas = get_data_receitas(url_receitas, orgaos, unidades)
    print(json_receitas)
elif opcao == '2':
    json_despesas = get_data_despesas(url_despesas, orgaos, unidades)
    print(json_despesas)
elif opcao == '3':
    json_receitas = get_data_receitas(url_receitas, orgaos, unidades)
    json_despesas = get_data_despesas(url_despesas, orgaos, unidades)
    print("Receitas:", json_receitas)
    print("Despesas:", json_despesas)
else:
    print("Opção inválida. Por favor, escolha 1, 2 ou 3.")
