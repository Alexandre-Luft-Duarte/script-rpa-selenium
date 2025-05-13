import csv
from extract import get_data  # Importa a função que extrai os dados dos PDFs

def file_csv(dados, nome_arquivo):
    # Detecta o maior número de linhas digitáveis e de outros campos
    max_linhas = 0
    max_linhas_2 = 0
    max_linhas_3 = 0
    max_linhas_4 = 0

    # Calcula os valores máximos com base nos dados
    for item in dados:
        max_linhas = max(max_linhas, sum(1 for k in item if k.startswith("linha_digitavel_")))
        max_linhas_2 = max(max_linhas_2, sum(1 for k in item if k.startswith("nosso_numero_")))
        max_linhas_3 = max(max_linhas_3, sum(1 for k in item if k.startswith("data_vencimento_")))
        max_linhas_4 = max(max_linhas_4, sum(1 for k in item if k.startswith("numero_documento_")))

    # Cabeçalho dinâmico intercalado
    cabecalho = ['arquivo']

    # Determina o número máximo de colunas baseado no maior valor entre as categorias
    max_colunas = max(max_linhas, max_linhas_2, max_linhas_3, max_linhas_4)

    # Gera o cabeçalho intercalado
    for i in range(1, max_colunas + 1):
        if i <= max_linhas:
            cabecalho.append(f'linha_digitavel_{i}')
        if i <= max_linhas_2:
            cabecalho.append(f'nosso_numero_{i}')
        if i <= max_linhas_3:
            cabecalho.append(f'data_vencimento_{i}')
        if i <= max_linhas_4:
            cabecalho.append(f'numero_documento_{i}')

    # Adiciona os campos fixos ao final
    cabecalho += ['valor', 'nome', 'lote', 'quadra']

    # Abre o CSV para escrita
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow(cabecalho)

        for item in dados:
            linha = [item.get('arquivo', '')]

            # Adiciona os valores intercalados
            for i in range(1, max_colunas + 1):
                if i <= max_linhas:
                    linha.append(item.get(f'linha_digitavel_{i}', ''))
                if i <= max_linhas_2:
                    linha.append(item.get(f'nosso_numero_{i}', ''))
                if i <= max_linhas_3:
                    linha.append(item.get(f'data_vencimento_{i}', ''))
                if i <= max_linhas_4:
                    linha.append(item.get(f'numero_documento_{i}', ''))

            # Adiciona os campos fixos
            linha += [
                item.get('valor', ''),
                item.get('nome', ''),
                item.get('lote', ''),
                item.get('quadra', '')
            ]

            writer.writerow(linha)

# Executa a extração e gera o CSV
if __name__ == '__main__':
    data = get_data()
    file_csv(data, 'iptus.csv')