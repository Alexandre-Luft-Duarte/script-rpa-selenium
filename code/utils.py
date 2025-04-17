import os, wget, time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def ler_codigos_csv(caminho_csv="arquivo/iptu_96_25032025.csv"):
    df = pd.read_csv(caminho_csv, delimiter=";")
    codigos_imoveis = df['imovel_prefeitura'].tolist()  # Converte as colunas dos códigos em uma lista
    return codigos_imoveis

def safe_click(driver, by, selector, timeout=10):
    try:
        el = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, selector))
        )
        el.click()
        return True
    except:
        return False

def iniciar_driver(download_dir="pdfs_iptu"):
    os.makedirs(download_dir, exist_ok=True)
    caminho_absoluto = os.path.abspath(download_dir)

    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": caminho_absoluto,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def acessar_portal_prefeitura(driver):
    driver.get("https://www.saomiguel.sc.gov.br/")
    time.sleep(3)
    if safe_click(driver, By.CLASS_NAME, "form-control"):
        barra = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "form-control")))
        barra.send_keys("IPTU")
    safe_click(driver, By.CLASS_NAME, "icon-smo-search")
    time.sleep(3)
    safe_click(driver, By.XPATH, "/html/body/main/div/div[2]/div/a[1]")
    time.sleep(10)
    abas = driver.window_handles
    driver.switch_to.window(abas[1])
    driver.get('https://e-gov.betha.com.br/cdweb/03114-473/contribuinte/rel_guiaiptu.faces')
    time.sleep(3)

def processar_codigo_imovel(driver, codigo, primeira_vez):
    print(f"\nPesquisando o código do imóvel {codigo}")
    if primeira_vez:
        safe_click(driver, By.XPATH, "/html/body/div[1]/div[2]/div/div/div/form/div[1]/div[1]/div[2]/div/div[1]/div[3]/div/div/div/a")
    else:
        safe_click(driver, By.XPATH, "/html/body/div[1]/div[2]/div/div/div/form/div[1]/div[1]/div[3]/span/input")
        time.sleep(1)

    try:
        campo_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "mainForm:iImoveis"))
        )
        campo_input.clear()
        campo_input.send_keys(str(codigo))
    except:
        print("❌ Campo de código do imóvel não encontrado.")
        return False

    if not safe_click(driver, By.ID, "mainForm:btIImoveis"):
        return False
    time.sleep(1)

    try:
        mensagem = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, "mainForm:master:messageSection:warn"))
        ).text.strip()
        if mensagem:
            print(f"Código {codigo} não possui IPTU.")
            return False
    except:
        pass
    return True

def preparar_emissao_guia(driver):
    if not safe_click(driver, By.ID, "P0"):
        print("❌ Falha ao clicar em débitos em aberto.")
        return
    time.sleep(2)

    try:
        marcar_parcela = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(@id, 'selectedUnica')]"))
        )
        print("Selecionando quantidade de parcelas...")
        driver.execute_script("arguments[0].click();", marcar_parcela)
        time.sleep(2)
    except:
        print("Seletor de parcelas não encontrado — seguindo normalmente.")

    if safe_click(driver, By.ID, "selectAll"):
        print("Parcelas marcadas com sucesso.")
    else:
        print("Falha ao marcar parcelas.")

def emitir_e_baixar(driver, codigo):
    if not safe_click(driver, By.ID, "mainForm:emitirUnificada"):
        print("Botão de emissão não encontrado ou não clicável.")
        return False

    print("Clicou em emissão.")
    time.sleep(10)
    url_pdf = driver.current_url
    try:
        wget.download(url_pdf, out=f"pdfs_iptu/{codigo}.pdf")
    except Exception as e:
        print(f"Erro ao baixar o PDF do código {codigo}: {e}")
        return False

    driver.close()
    driver.switch_to.window(driver.window_handles[1])
    return True
