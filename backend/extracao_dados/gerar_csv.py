import csv
from utils import extrair_codigo

def arquivo_csv(dicionario, nome_arquivo):
    with open(nome_arquivo, mode='w', newline='') as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow(['Código Imóvel', 'Linha Digitável'])  # Cabeçalho

        for imovel, codigos_de_barra in dicionario.items():
            nome_limpo = imovel.replace('iptu_', '').replace('.pdf', '')
            for codigo in codigos_de_barra:
                writer.writerow([nome_limpo, f"{codigo}"])

dados = extrair_codigo()
print(dados) 
arquivo_csv(dados, 'iptus.csv')

