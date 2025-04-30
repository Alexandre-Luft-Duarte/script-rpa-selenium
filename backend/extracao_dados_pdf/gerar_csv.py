import csv
from dados import extrair_codigo

def arquivo_csv(dicionario, nome_arquivo):
    with open(nome_arquivo, mode='w', newline='') as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow(['Código Imóvel', 'Linha Digitável', 'Valor a Pagar'])  # Cabeçalho

        for imovel, info in dicionario.items():
            nome_limpo = imovel.replace('iptu_', '').replace('.pdf', '')
            valor = info['valor']
            for codigo in info['codigos']:
                writer.writerow([nome_limpo, f"'{codigo}", valor])

dados = extrair_codigo()
arquivo_csv(dados, 'iptus.csv')

