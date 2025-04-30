import pdfplumber, os, re, logging

# Oculta os avisos do pdfminer, que o pdfplumber usa internamente
logging.getLogger("pdfminer").setLevel(logging.ERROR)

# Caminho absoluto para a pasta onde estão os PDFs
folder = os.path.join(os.path.dirname(__file__), "/home/flexpro/Documentos/RPA_Projetos/iptu_selenium/backend/emission_pdfs_iptu/pdfs_iptu")

# Lista todos os arquivos da pasta
files = os.listdir(folder)

# Função principal que extrai os dados dos PDFs
def get_data():
    extracted_data = {}  # Dicionário final onde os dados serão armazenados

    for pdf_name in files:
        # Processa apenas arquivos com extensão .pdf
        if pdf_name.lower().endswith(".pdf"):
            pdf_path = os.path.join(folder, pdf_name)  # Caminho completo do PDF

            with pdfplumber.open(pdf_path) as pdf:
                csv_data = []        # Lista para armazenar códigos de barras encontrados
                amount_to_pay = None # Variável para armazenar o valor a pagar

                for page in pdf.pages:
                    text = page.extract_text()  # Extrai o texto da página
                    if text:
                        lines = text.split("\n")  # Divide o texto em linhas

                        # Loop para encontrar códigos de barras nas linhas
                        for line in lines:
                            # Busca sequências longas de números, espaços, pontos ou traços
                            digitable_line = re.findall('[\d\.\s\-]{30,}', line)
                            for candidate in digitable_line:
                                # Remove tudo que não for dígito
                                digits_only = re.sub('\D', '', candidate)
                                # Valida se tem exatamente 47 dígitos (formato padrão do código de barras)
                                if len(digits_only) == 47:
                                    csv_data.append(digits_only)

                        # Tenta encontrar o valor a pagar com base em palavras-chave
                        for line in lines:
                            if 'VALOR À PAGAR' in line or 'IMPOSTO PREDIAL' in line:
                                values = re.findall('\d+,\d{2}', line)  # Busca valores no formato 999,99
                                if values:
                                    amount_to_pay = values[-1]  # Pega o último valor encontrado na linha
                                    break

                        # Se não encontrou com palavras-chave, tenta pegar o último valor do texto completo
                        if not amount_to_pay:
                            all_values = re.findall('\d+,\d{2}', text)
                            if all_values:
                                amount_to_pay = all_values[-1]

                if csv_data:
                    # Remove códigos de barras duplicados
                    unique_codes = list(set(csv_data))

                    # Armazena os dados extraídos para o PDF atual
                    extracted_data[pdf_name] = {
                        "codigos": unique_codes,
                        "valor": amount_to_pay or "N/A"  # Se não encontrou valor, preenche com "N/A"
                    }

    return extracted_data  # Retorna o dicionário com os dados de todos os PDFs
