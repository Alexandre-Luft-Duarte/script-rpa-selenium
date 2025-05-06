import csv
from extract import get_data  # Importa a função que extrai os dados dos PDFs

def file_csv(dados, nome_arquivo):
    # Detecta o maior número de linhas digitáveis entre os itens
    max_linhas = 0
    for item in dados:
        qtd = sum(1 for k in item if k.startswith("linha_digitavel_"))
        max_linhas = max(max_linhas, qtd)

    # Cabeçalho dinâmico
    cabecalho = ['arquivo']
    cabecalho += [f'linha_digitavel_{i}' for i in range(1, max_linhas + 1)]
    cabecalho += ['valor', 'nosso_numero', 'nome']

    # Abre o CSV para escrita (sem aspas forçadas)
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow(cabecalho)

        for item in dados:
            linha = [item.get('arquivo', '')]

            # Adiciona todas as linhas digitáveis (ou vazio se não houver)
            for i in range(1, max_linhas + 1):
                linha.append(item.get(f'linha_digitavel_{i}', ''))

            # Adiciona campos finais
            linha += [
                item.get('valor', ''),
                f"'{item.get('nosso_numero', '')}",
                item.get('nome', '')
            ]


            writer.writerow(linha)

# Executa a extração e gera o CSV
if __name__ == '__main__':
    data = get_data()
    file_csv(data, 'iptus.csv')
