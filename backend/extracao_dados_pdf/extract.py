import pdfplumber, os, re, logging

logging.getLogger("pdfminer").setLevel(logging.ERROR)

folder = "/home/flexpro/Documentos/RPA_Projetos/iptu_selenium/backend/emission_pdfs_iptu/pdfs_iptu"
files = os.listdir(folder)

def get_data():
    extracted_data = {}

    for pdf_name in files:
        if not pdf_name.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(folder, pdf_name)
        barcode_code = None
        amount_to_pay = None
        our_number = None

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                lines = text.split("\n")

                # captura o código de barras (único)
                if barcode_code is None:
                    for line in lines:
                        for cand in re.findall(r'[\d\.\s\-]{30,}', line):
                            digits = re.sub(r'\D', '', cand)
                            if len(digits) == 47:
                                barcode_code = digits
                                break
                        if barcode_code:
                            break  # já encontrou, sai do loop de linhas

                # encontra o valor a pagar
                if amount_to_pay is None:
                    for line in lines:
                        if 'VALOR À PAGAR' in line or 'IMPOSTO PREDIAL' in line:
                            vals = re.findall(r'\d+,\d{2}', line)
                            if vals:
                                amount_to_pay = vals[-1]
                                break
                    if amount_to_pay is None:
                        all_vals = re.findall(r'\d+,\d{2}', text)
                        if all_vals:
                            amount_to_pay = all_vals[-1]

                # encontra nosso número de 18 dígitos
                if our_number is None:
                    m = re.search(r'\b(\d{18})\b', text)
                    if m:
                        our_number = m.group(1)

                # se já tiver encontrado todos, pode parar
                if barcode_code and amount_to_pay and our_number:
                    break

        extracted_data[pdf_name] = {
            "codigo_barras": barcode_code or "N/A",
            "valor":        amount_to_pay or "N/A",
            "nosso_numero": our_number   or "N/A",
        }

    return extracted_data
