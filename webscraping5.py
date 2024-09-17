import requests
from datetime import datetime, timedelta

def buscar_municipios():
    url_municipios = "https://api-dados-abertos.tce.ce.gov.br/municipios"
    response = requests.get(url_municipios)
    if response.status_code == 200:
        data = response.json()
        municipios = {municipio['nome_municipio'].upper(): municipio['codigo_municipio'] for municipio in data['data']}
        return municipios
    else:
        print(f"Erro ao acessar a API de municípios: {response.status_code}")
        return {}

def gerar_datas_intervalo(data_inicial, data_final):
    data_inicial = datetime.strptime(data_inicial, '%Y%m')
    data_final = datetime.strptime(data_final, '%Y%m')
    datas = []

    while data_inicial <= data_final:
        datas.append(data_inicial.strftime('%Y%m'))
        data_inicial += timedelta(days=30)  # Incrementa aproximadamente um mês

    return datas

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
    for item in dados:
        if isinstance(item, dict):
            codigo_orgao = item.get('codigo_orgao', '')
            item['nome_orgao'] = orgaos.get(codigo_orgao, 'Desconhecido')

            codigo_unidade = item.get('codigo_unidade', '').strip()
            item['nome_unidade'] = unidades.get((codigo_orgao, codigo_unidade), 'Desconhecida')

    return dados

def get_data(url, orgaos, unidades, tipo_dado):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            if isinstance(data['data'], dict) and 'data' in data['data']:
                # Acessa a camada correta de dados para despesas
                return substituir_codigos_por_nomes(data['data']['data'], orgaos, unidades)
            else:
                # Para outras estruturas, como receitas
                return substituir_codigos_por_nomes(data['data'], orgaos, unidades)
        else:
            print(f"Estrutura inesperada na resposta da API para {tipo_dado}: {data}")
            return []
    else:
        print(f"Erro ao acessar a API: {response.status_code}")
        return []

municipios = buscar_municipios()
if not municipios:
    exit()

nome_municipio = input("Digite o nome do município: ").strip().upper()

if nome_municipio in municipios:
    codigo_municipio = municipios[nome_municipio]
    exercicio_orcamento = input("Digite o exercício orçamentário (ex: 202400): ")
    
    # Solicita as datas de referência inicial e final
    data_referencia_inicial = input("Digite a data de referência inicial (ex: 202305): ")
    data_referencia_final = input("Digite a data de referência final (ex: 202404): ")

    # Gera todas as datas do intervalo
    datas_referencia = gerar_datas_intervalo(data_referencia_inicial, data_referencia_final)

    url_orgaos = f"https://api-dados-abertos.tce.ce.gov.br/orgaos?codigo_municipio={codigo_municipio}&exercicio_orcamento={exercicio_orcamento}"
    url_unidades = f"https://api-dados-abertos.tce.ce.gov.br/unidades_orcamentarias?codigo_municipio={codigo_municipio}&exercicio_orcamento={exercicio_orcamento}&quantidade=100&deslocamento=0"
    
    orgaos = buscar_orgaos(url_orgaos)
    unidades = buscar_unidades(url_unidades)

    opcao = input("Escolha uma opção: 1 - Receitas, 2 - Despesas, 3 - Ambos: ")

    json_resultados = {'receitas': [], 'despesas': []}

    for data_referencia in datas_referencia:
        url_receitas = f"https://api-dados-abertos.tce.ce.gov.br/balancete_receita_orcamentaria?codigo_municipio={codigo_municipio}&exercicio_orcamento={exercicio_orcamento}&data_referencia={data_referencia}"
        url_despesas = f"https://api-dados-abertos.tce.ce.gov.br/balancete_despesa_orcamentaria?codigo_municipio={codigo_municipio}&exercicio_orcamento={exercicio_orcamento}&data_referencia={data_referencia}&quantidade=100&deslocamento=0"
        
        if opcao == '1':
            json_resultados['receitas'].extend(get_data(url_receitas, orgaos, unidades, "receitas"))
        elif opcao == '2':
            json_resultados['despesas'].extend(get_data(url_despesas, orgaos, unidades, "despesas"))
        elif opcao == '3':
            json_resultados['receitas'].extend(get_data(url_receitas, orgaos, unidades, "receitas"))
            json_resultados['despesas'].extend(get_data(url_despesas, orgaos, unidades, "despesas"))
        else:
            print("Opção inválida. Por favor, escolha 1, 2 ou 3.")
            break

    print("Resultados:", json_resultados)

else:
    print("Município não encontrado. Por favor, verifique o nome e tente novamente.")
