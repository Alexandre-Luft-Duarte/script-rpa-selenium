import pandas as pd
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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


def iniciar_driver(download_dir="pdfs_iptu"):
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    import os

    os.makedirs(download_dir, exist_ok=True)
    path = os.path.abspath(download_dir)

    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True  # ESSENCIAL
    }
    chrome_options.add_experimental_option("prefs", prefs)

    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


