import csv
from extract import get_data  # Importa a função que extrai os dados dos PDFs

def file_csv(dados, nome_arquivo):
    # Detecta o maior número de linhas digitáveis e de nossos números
    max_linhas = 0
    max_linhas_2 = 0
    max_linhas_3 = 0

    for item in dados:
        qtd = sum(1 for k in item if k.startswith("linha_digitavel_"))
        max_linhas = max(max_linhas, qtd)

        qtd_2 = sum(1 for k in item if k.startswith("nosso_numero_"))
        max_linhas_2 = max(max_linhas_2, qtd_2)

        qtd_2 = sum(1 for k in item if k.startswith("data_vencimento_"))

    # Cabeçalho dinâmico
    cabecalho = ['arquivo']
    cabecalho += [f'linha_digitavel_{i}' for i in range(1, max_linhas + 1)]
    cabecalho += [f'nosso_numero_{i}' for i in range(1, max_linhas_2 + 1)] 
    cabecalho += [f'data_vencimento_{i}' for i in range(1, max_linhas_3 + 1)]
    cabecalho += ['valor', 'nome']


    # Abre o CSV para escrita
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow(cabecalho)


        for item in dados:
            linha = [item.get('arquivo', '')]

            # Adiciona todas as linhas digitáveis
            for i in range(1, max_linhas + 1):
                linha.append(item.get(f'linha_digitavel_{i}', ''))

            # Adiciona todos os nossos números
            for i in range(1, max_linhas_2 + 1):
                numero = item.get(f'nosso_numero_{i}', '')
                linha.append(item.get(f"'{numero}" if numero else ''))

            # Adiciona todas as datas de vencimento da parcela
            for i in range(1, max_linhas_3 + 1):
                data = (item.get(f'data_vencimento_{i}', ''))
                linha.append(item.get(f"'{data}" if data else ''))

            # Adiciona campos finais
            linha += [
                item.get('valor', ''),
                item.get('nome', '')
            ]

            writer.writerow(linha)

# Executa a extração e gera o CSV
if __name__ == '__main__':
    data = get_data()
    file_csv(data, 'iptus.csv')
