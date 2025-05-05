import csv
from extract import get_data  # Importa a função que extrai os dados dos PDFs

def file_csv(dicionario, nome_arquivo):
    # Abre (ou cria) o arquivo CSV no modo escrita
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo)
        # Cabeçalho
        writer.writerow(['Código Imóvel', 'Linha Digitável', 'Valor a Pagar', 'Nosso número', 'Sacado'])

        # Para cada PDF (imóvel) no dicionário...
        for imovel, info in dicionario.items():
            # Extrai o "código do imóvel" do nome do arquivo
            name = imovel.replace('iptu_', '').replace('.pdf', '')
            linha_digitavel = info.get('codigo_barras', 'N/A')
            valor = info.get('valor', 'N/A')
            nosso_numero = info.get('nosso_numero', 'N/A')
            nome = info.get('nome')

            # Escreve uma única linha por imóvel
            writer.writerow([name, f"'{linha_digitavel}", valor, f"'{nosso_numero}", nome])

# Executa a extração e gera o CSV
if __name__ == '__main__':
    data = get_data()
    file_csv(data, 'iptus.csv')
