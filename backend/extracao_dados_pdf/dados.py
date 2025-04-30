import pdfplumber, os, re, logging

# Oculta os avisos do pdfminer
logging.getLogger("pdfminer").setLevel(logging.ERROR)

# Caminho absoluto da pasta pdfs_teste
pasta = os.path.join(os.path.dirname(__file__), "/home/flexpro/Documentos/RPA_Projetos/iptu_selenium/backend/emissao_pdfs_iptu/pdfs_iptu")
arquivos = os.listdir(pasta)

import pdfplumber, os, re, logging

# Oculta os avisos do pdfminer
logging.getLogger("pdfminer").setLevel(logging.ERROR)

# Caminho absoluto da pasta pdfs_teste
pasta = "/home/flexpro/Documentos/RPA_Projetos/iptu_selenium/backend/emissao_pdfs_iptu/pdfs_iptu"
arquivos = os.listdir(pasta)

def extrair_codigo():
    dados_extraidos = {}

    for nome_pdf in arquivos:
        if nome_pdf.lower().endswith(".pdf"):
            caminho_pdf = os.path.join(pasta, nome_pdf)
            with pdfplumber.open(caminho_pdf) as pdf:
                codigos_validos = []
                valor_a_pagar = None

                for pagina in pdf.pages:
                    texto = pagina.extract_text()
                    if texto:
                        linhas = texto.split("\n")

                        # Captura códigos de barras
                        for linha in linhas:
                            linha_digitavel = re.findall('[\d\.\s\-]{30,}', linha)
                            for candidato in linha_digitavel:
                                somente_digitos = re.sub('\D', '', candidato)
                                if len(somente_digitos) == 47:
                                    codigos_validos.append(somente_digitos)

                        # Procura valor a pagar com base em palavras-chave
                        for linha in linhas:
                            if 'VALOR À PAGAR' in linha or 'IMPOSTO PREDIAL' in linha:
                                valores = re.findall('\d+,\d{2}', linha)
                                if valores:
                                    valor_a_pagar = valores[-1]  # Último valor na linha
                                    break

                        # Se não achou com contexto, tenta pegar o último valor geral
                        if not valor_a_pagar:
                            todos_valores = re.findall('\d+,\d{2}', texto)
                            if todos_valores:
                                valor_a_pagar = todos_valores[-1]

                if codigos_validos:
                    codigos_unicos = list(set(codigos_validos))  # elimina duplicados
                    dados_extraidos[nome_pdf] = {
                        "codigos": codigos_unicos,
                        "valor": valor_a_pagar or "N/A"
                    }


    return dados_extraidos

