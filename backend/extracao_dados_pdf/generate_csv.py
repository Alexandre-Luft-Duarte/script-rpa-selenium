import csv
from extract import get_data  # Importa a função que extrai os dados dos PDFs

# Função para gerar um arquivo CSV com os dados extraídos
def file_csv(dicionario, nome_arquivo):
    # Abre (ou cria) o arquivo CSV no modo escrita
    with open(nome_arquivo, mode='w', newline='') as arquivo:
        writer = csv.writer(arquivo)  # Cria um escritor CSV
        # Escreve o cabeçalho das colunas no arquivo
        writer.writerow(['Código Imóvel', 'Linha Digitável', 'Valor a Pagar'])

        # Percorre o dicionário retornado pela função get_data()
        for imovel, info in dicionario.items():
            # Remove prefixos e sufixos do nome do arquivo para extrair o "código do imóvel"
            nome_limpo = imovel.replace('iptu_', '').replace('.pdf', '')
            valor = info['valor']  # Valor a pagar associado a esse imóvel

            # Para cada código de barras associado ao imóvel
            for codigo in info['codigos']:
                # Escreve uma linha no CSV com: código do imóvel, linha digitável (com aspas), e valor
                writer.writerow([nome_limpo, f"'{codigo}", valor])

# Executa a extração dos dados dos PDFs
data = get_data()

# Gera o arquivo CSV com os dados extraídos
file_csv(data, 'iptus.csv')
