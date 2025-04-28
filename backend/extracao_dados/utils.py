import pdfplumber, os, re, logging

# Oculta os avisos do pdfminer para evitar excesso de mensagens no terminal
logging.getLogger("pdfminer").setLevel(logging.ERROR)

# Define o caminho absoluto para a pasta onde estão os PDFs
pasta = os.path.join(os.path.dirname(__file__), "/home/flexpro/Área de Trabalho/RPA/iptu_selenium/emissao_pdfs/pdfs_iptu")

# Lista todos os arquivos existentes na pasta
arquivos = os.listdir(pasta)


def extrair_codigo():
    for nome_pdf in arquivos: # Percorre todos os arquivos da pasta
        if nome_pdf.lower().endswith(".pdf"): # Verifica se o arquivo é um PDF (ignora se não for)
            caminho_pdf = os.path.join(pasta, nome_pdf) # Monta o caminho completo do PDF
            with pdfplumber.open(caminho_pdf) as pdf:  # Abre o PDF usando pdfplumber
                for pagina in pdf.pages:  # Percorre todas as páginas do PDF
                    texto = pagina.extract_text() # Extrai o texto da página
                    if texto:
                        linhas = texto.split("\n")  # Se o texto foi extraído, divide-o em linhas
                        codigos_validos = []  # Lista para armazenar códigos válidos encontrados
                        for linha in linhas:   # Percorre cada linha de texto
                            candidatos = re.findall(r'[\d\.\s\-]{30,}', linha) # (busca trechos com números, pontos, espaços e hífens com no mínimo 30  caracteres)
                            for candidato in candidatos:
                                somente_digitos = re.sub(r'\D', '', candidato) # Remove tudo que não for dígito do candidato
                                if len(somente_digitos) == 47:
                                    codigos_validos.append(somente_digitos) # Adiciona à lista de códigos válidos
                        if codigos_validos: # Após processar todas as linhas da página
                            print(f"\nCódigos de 47 dígitos encontrados no PDF {nome_pdf}:")
                            for cod in codigos_validos:
                                print(f"{cod}")
                        else:
                            print("Nenhum código válido encontrado nesta página.")
