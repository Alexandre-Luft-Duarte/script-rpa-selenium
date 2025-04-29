import pdfplumber, os, re, logging, csv

# Oculta os avisos do pdfminer
logging.getLogger("pdfminer").setLevel(logging.ERROR)

# Caminho absoluto da pasta pdfs_teste
pasta = os.path.join(os.path.dirname(__file__), "/home/flexpro/Documentos/RPA_Projetos/iptu_selenium/backend/emissao_pdfs/pdfs_iptu")
arquivos = os.listdir(pasta)

def extrair_codigo():
    codigos_validos = {}
    for nome_pdf in arquivos:
        if nome_pdf.lower().endswith(".pdf"):
            caminho_pdf = os.path.join(pasta, nome_pdf)
            with pdfplumber.open(caminho_pdf) as pdf:
                for pagina in pdf.pages:
                    texto = pagina.extract_text()
                    if texto:
                        linhas = texto.split("\n")
                        for linha in linhas:
                            candidatos = re.findall(r'[\d\.\s\-]{30,}', linha)  # pega trechos longos com números e pontuação
                            for candidato in candidatos:
                                somente_digitos = re.sub(r'\D', '', candidato)
                                if len(somente_digitos) == 47:
                                     codigos_validos.setdefault(nome_pdf, []).append(somente_digitos)
                                    
    return codigos_validos

                                    
                                