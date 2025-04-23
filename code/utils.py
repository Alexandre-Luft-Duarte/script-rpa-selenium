import pandas as pd
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os, subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By



# Função para ler o arquivo com os códigos do imóveis
def ler_codigos_csv(caminho_csv="arquivo/iptu_96_25032025.csv"):
    df = pd.read_csv(caminho_csv, delimiter=";")
    codigos_imoveis = df['imovel_prefeitura'].tolist() # Converte as colunas dos códigos em uma lista
    return codigos_imoveis


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


def iniciar_navegacao_iptu(driver):
    # Maximiza a janela
    driver.maximize_window()

    # Acessa o site da prefeitura
    driver.get("https://www.saomiguel.sc.gov.br/")
    time.sleep(3)

    # Pesquisa "IPTU" na barra de busca
    botao_servicos = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "form-control"))
    )
    botao_servicos.send_keys("IPTU")

    # Clica no botão de pesquisa
    safe_click(driver, By.CLASS_NAME, "icon-smo-search")
    time.sleep(3)

    # Clica no link de IPTU
    safe_click(driver, By.XPATH, "/html/body/main/div/div[2]/div/a[1]")
    time.sleep(10)

    # Muda para a nova aba aberta
    abas = driver.window_handles
    driver.switch_to.window(abas[1])

    # Acessa o sistema Betha
    driver.get('https://e-gov.betha.com.br/cdweb/03114-473/contribuinte/rel_guiaiptu.faces')
    time.sleep(3)


# Função que tenta encontrar e clicar em um elemento de forma segura
def safe_click(driver, by, value, timeout=10, tentativas=2):
    for tentativa in range(tentativas):
        try:
            el = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))

            if el.is_displayed():
                try:
                    el.click()
                    print(f"Clique normal bem-sucedido em {value}")
                except ElementClickInterceptedException:
                    print(f"Elemento interceptado, tentando via JS: {value}")
                    driver.execute_script("arguments[0].click();", el)
                return True
            else:
                print(f"Elemento {value} está oculto.")
                return False

        except (StaleElementReferenceException, TimeoutException) as e:
            print(f"Tentativa {tentativa + 1}/{tentativas} falhou ao clicar em {value}: {e}")
            time.sleep(1)

    print(f"Não foi possível clicar no elemento {value} após {tentativas} tentativas.")
    return False



def baixar_pdf_iptu(driver, codigo, pasta_download="pdfs_iptu"):
    aba_principal = driver.current_window_handle
    abas_antes = driver.window_handles

    print("Aguardando nova aba ou fallback para aba atual...")
    try:
        WebDriverWait(driver, 5).until(lambda d: len(d.window_handles) > len(abas_antes))
        nova_aba = [aba for aba in driver.window_handles if aba not in abas_antes][0]
        driver.switch_to.window(nova_aba)
        print("Nova aba detectada.")
        nova_aba_aberta = True
    except TimeoutException:
        print("Nenhuma nova aba foi aberta. Usando aba atual.")
        nova_aba_aberta = False

    # Espera a URL mudar e o PDF carregar
    time.sleep(2)
    pdf_url = driver.current_url
    print(f"URL do PDF: {pdf_url}")

    # Baixa o PDF com wget
    nome_arquivo = os.path.join(pasta_download, f"iptu_{codigo}.pdf")
    subprocess.run(["wget", "-O", nome_arquivo, pdf_url])
    print(f"PDF baixado como: {nome_arquivo}")

    # Fecha aba nova se foi aberta e volta para principal
    if nova_aba_aberta:
        driver.close()
        driver.switch_to.window(aba_principal)







