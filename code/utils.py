import pandas as pd
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os, shutil

# Função para ler o arquivo com os códigos do imóveis
def ler_codigos_csv(caminho_csv="arquivo/iptu_96_25032025.csv"):
    df = pd.read_csv(caminho_csv, delimiter=";")
    codigos_imoveis = df['imovel_prefeitura'].tolist() # Converte as colunas dos códigos em uma lista
    return codigos_imoveis


# Função que tenta encontrar e clicar em um elemento de forma segura
def safe_click(driver, by, value, timeout=10, tentativas=2):
    for tentativa in range(tentativas):
        try:
            el = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
            driver.execute_script("arguments[0].click();", el)
            return True
        except (StaleElementReferenceException, TimeoutException) as e:
            print(f"Tentativa {tentativa + 1}/{tentativas} falhou: {e}")
            time.sleep(1)
    print(f"Não foi possível clicar no elemento {value} após {tentativas} tentativas.")
    return False


def mover_pdf_baixado(pasta_origem, pasta_destino, timeout=30):
    """
    Espera o download de um PDF terminar na pasta_origem
    e move o arquivo para pasta_destino.
    """
    os.makedirs(pasta_destino, exist_ok=True)

    tempo_inicial = time.time()
    pdf_encontrado = None

    while time.time() - tempo_inicial < timeout:
        arquivos = os.listdir(pasta_origem)
        arquivos_pdf = [f for f in arquivos if f.endswith(".pdf")]
        arquivos_temp = [f for f in arquivos if f.endswith(".crdownload")]

        if arquivos_pdf and not arquivos_temp:
            pdf_encontrado = arquivos_pdf[0]  # pega o primeiro que achar
            break

        time.sleep(1)

    if not pdf_encontrado:
        print("Nenhum PDF baixado foi detectado a tempo.")
        return False

    origem = os.path.join(pasta_origem, pdf_encontrado)
    destino = os.path.join(pasta_destino, pdf_encontrado)

    shutil.move(origem, destino)
    print(f"PDF movido para: {destino}")
    return True



