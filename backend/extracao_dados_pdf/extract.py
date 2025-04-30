import pdfplumber, os, re, logging

# Oculta os avisos do pdfminer
logging.getLogger("pdfminer").setLevel(logging.ERROR)

# Caminho absoluto da pasta pdfs_teste
folder = os.path.join(os.path.dirname(__file__), "/home/flexpro/Documentos/RPA_Projetos/iptu_selenium/backend/emission_pdfs_iptu/pdfs_iptu")
files = os.listdir(folder)


def get_data():
    extracted_data = {}

    for pdf_name in files:
        if pdf_name.lower().endswith(".pdf"):
            pdf_path = os.path.join(folder, pdf_name)
            with pdfplumber.open(pdf_path) as pdf:
                csv_data = []
                amount_to_pay = None

                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        lines = text.split("\n")

                        # Captura códigos de barras
                        for line in lines:
                            digitable_line = re.findall('[\d\.\s\-]{30,}', line)
                            for candidate in digitable_line:
                                digits_only = re.sub('\D', '', candidate)
                                if len(digits_only) == 47:
                                    csv_data.append(digits_only)

                        # Procura valor a pagar com base em palavras-chave
                        for line in lines:
                            if 'VALOR À PAGAR' in line or 'IMPOSTO PREDIAL' in line:
                                values = re.findall('\d+,\d{2}', line)
                                if values:
                                    amount_to_pay = values[-1]  # Último valor na linha
                                    break

                        # Se não achou com contexto, tenta pegar o último valor geral
                        if not amount_to_pay:
                            all_values = re.findall('\d+,\d{2}', text)
                            if all_values:
                                amount_to_pay = all_values[-1]

                if csv_data:
                    unique_codes = list(set(csv_data))  # elimina duplicados
                    extracted_data[pdf_name] = {
                        "codigos": unique_codes,
                        "valor": amount_to_pay or "N/A"
                    }


    return extracted_data

