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
                
                numero_documento = None
                our_number = None
                for line in lines:
                    for cand in re.findall(r'\b(\d{18})\b', line):
                        digitos = re.sub(r'\D', '', cand)
                        if len(digitos) == 18:
                            our_number = cand.strip()
                            numero_documento = digitos[-8:-1]
                            break
                    if our_number:
                        break

                vencimento = None
                for line in lines:
                    # Procura por linhas que contenham a palavra "VENCIMENTO"
                    if 'VENCIMENTO' in line.upper():
                        # Procura por datas no formato DD/MM/AAAA
                        match = re.search(r'\b(\d{2}/\d{2}/\d{4})\b', line)
                        if match:
                            vencimento = match.group(1)
                            break  # Interrompe o loop ao encontrar a data


                row_data[f"linha_digitavel_{idx + 1}"] = linha_digitavel or "N/A"
                row_data[f"nosso_numero_{idx + 1}"] = our_number or "N/A"
                row_data[f"data_vencimento_{idx + 1}"] = vencimento or "N/A"
                row_data[f"numero_documento_{idx + 1}"] = numero_documento or "N/A"

                # Os outros campos só precisam ser preenchidos uma vez
                amount_to_pay = None
                sacado_name = None
                lote = None
                quadra = None

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

                if sacado_name is None:
                    m = re.search(r'-(?:\s*([A-ZÀ-Ÿ\/\. ]+?)\s*)-', text)
                    if m:
                        sacado_name = m.group(1)
                    
                if lote is None:  # Captura apenas o primeiro "Lote" encontrado
                    for line in lines:
                        if 'Lote:' in line:
                            match = re.search(r'Lote:\s*(.+)', line)
                            if match:
                                lote = match.group(1).strip()  # Captura qualquer coisa após "Lote:" e remove espaços extras
                                break  # Interrompe o loop após encontrar o primeiro "Lote"

                if quadra is None:  # Captura apenas o primeiro "Quadra" encontrado
                    for line in lines:
                        if 'Quadra:' in line:
                            match = re.search(r'Quadra:\s*(\d+)', line)
                            if match:
                                quadra = match.group(1).strip()  # Captura qualquer coisa após "Quadra:" e remove espaços extras
                                break  # Interrompe o loop após encontrar o primeiro "Quadra"
                        

        # Depois do loop:
        row_data["valor"] = amount_to_pay or "N/A"
        row_data["nome"] = sacado_name or "N/A"
        row_data["lote"] = lote or "N/A"
        row_data["quadra"] = quadra or "N/A"

        extracted_data.append(row_data)

    return extracted_data

