import pdfplumber, os, re, logging

logging.getLogger("pdfminer").setLevel(logging.ERROR)

folder = "/home/flexpro/Documentos/RPA_Projetos/iptu_selenium/backend/emission_pdfs_iptu/pdfs_iptu"
files = os.listdir(folder)

def get_data():
    extracted_data = []

    for pdf_name in files:
        if not pdf_name.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(folder, pdf_name)
        row_data = {"arquivo": pdf_name}  # dicionário final da linha
        amount_to_pay = None
        our_number = None
        sacado_name = None

        with pdfplumber.open(pdf_path) as pdf:
            for idx, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                lines = text.split("\n")

                linha_digitavel = None
                for line in lines:
                    for cand in re.findall(r'[\d\. ]{40,}', line):
                        digitos = re.sub(r'\D', '', cand)
                        if len(digitos) == 47:
                            linha_digitavel = cand.strip()
                            break
                    if linha_digitavel:
                        break

                # Adiciona a linha digitável de cada página SEM interromper o loop
                row_data[f"linha_digitavel_{idx + 1}"] = linha_digitavel or "N/A"

                # Os outros campos só precisam ser preenchidos uma vez
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

                if our_number is None:
                    m = re.search(r'\b(\d{18})\b', text)
                    if m:
                        our_number = m.group(1)

                if sacado_name is None:
                    m = re.search(r'-(?:\s*([A-ZÀ-Ÿ\/\. ]+?)\s*)-', text)
                    if m:
                        sacado_name = m.group(1)

        # Depois do loop:
        row_data["valor"] = amount_to_pay or "N/A"
        row_data["nosso_numero"] = our_number or "N/A"
        row_data["nome"] = sacado_name or "N/A"

        extracted_data.append(row_data)

    return extracted_data

