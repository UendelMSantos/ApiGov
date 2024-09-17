import requests

codigo_municipio = input("Digite o código do município: ")
exercicio_orcamento = input("Digite o exercício orçamentário (ex: 202400): ")
data_referencia = input("Digite a data de referência (ex: 202405): ")

url_despesas = f"https://api-dados-abertos.tce.ce.gov.br/balancete_despesa_orcamentaria?codigo_municipio={codigo_municipio}&exercicio_orcamento={exercicio_orcamento}&data_referencia={data_referencia}&quantidade=100&deslocamento=0"
url_receitas = f"https://api-dados-abertos.tce.ce.gov.br/balancete_receita_orcamentaria?codigo_municipio={codigo_municipio}&exercicio_orcamento={exercicio_orcamento}&data_referencia={data_referencia}"

def get_data(url, tipo):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if tipo == 'despesas':
            despesas = data['data']['data']
            total_despesas = sum(
                float(item.get('valor_empenhado_ate_mes', 0)) + 
                float(item.get('valor_pago_ate_mes', 0)) + 
                float(item.get('valor_supl_ate_mes', 0))
                for item in despesas
            )
            print(f"O montante total das despesas é: R$ {total_despesas:.2f}")
        elif tipo == 'receitas':
            receitas = data['data']
            total_receitas = sum(
                float(item.get('valor_arrecadacao_ate_mes', 0)) 
                for item in receitas
            )
            print(f"O montante total das receitas é: R$ {total_receitas:.2f}")
            
    else:
        print(f"Erro ao acessar a API: {response.status_code}")

get_data(url_despesas, 'despesas')
get_data(url_receitas, 'receitas')

