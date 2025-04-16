import pandas as pd
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os, requests


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



# Função para jogar o pdf em uma pasta específica
import time
import os

def aguardar_download_pdf(pasta_destino, nome_parcial=None, timeout=30):
    """
    Aguarda até que um PDF seja baixado para a pasta destino.
    Se nome_parcial for passado, verifica se o nome contém essa substring.
    """
    tempo_inicial = time.time()
    while time.time() - tempo_inicial < timeout:
        for arquivo in os.listdir(pasta_destino):
            if arquivo.endswith(".pdf") and (nome_parcial in arquivo if nome_parcial else True):
                caminho_arquivo = os.path.join(pasta_destino, arquivo)
                if not arquivo.endswith(".crdownload"):  # Garante que o download terminou
                    return caminho_arquivo
        time.sleep(1)
    raise TimeoutError("PDF não foi baixado dentro do tempo limite.")


