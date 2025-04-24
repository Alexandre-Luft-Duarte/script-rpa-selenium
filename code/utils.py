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


def selecionar_parcela_unica(driver):
    try:
        input_parcela = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'selectedUnica')]"))
        )
        if not input_parcela.is_selected():
            print("Parcela única não selecionada. Clicando...")
            driver.execute_script("arguments[0].click();", input_parcela)
            time.sleep(1)
        else:
            print("Parcela única já está selecionada. Pulando clique.")
    except Exception as e:
        print(f"Erro ao selecionar parcela única: {e}")


def aguardar_download_renomear(driver, download_dir, nome_destino, timeout=15):
    # Captura a aba atual no momento da chamada
    janela_original = driver.current_window_handle

    # Aguarda nova aba ser aberta (com no máximo 5 tentativas)
    for _ in range(5):
        novas_janelas = [h for h in driver.window_handles if h != janela_original]
        if novas_janelas:
            break
        time.sleep(1)
    else:
        print("⚠️ Nenhuma nova aba foi detectada.")
        return

    nova_janela = novas_janelas[0]
    driver.switch_to.window(nova_janela)

    # Aguarda download e renomeia
    inicio = time.time()
    while time.time() - inicio < timeout:
        arquivos = [f for f in os.listdir(download_dir) if f.endswith(".pdf")]
        if arquivos:
            arquivo_baixado = sorted(
                arquivos, key=lambda x: os.path.getctime(os.path.join(download_dir, x)), reverse=True)[0]
            caminho_origem = os.path.join(download_dir, arquivo_baixado)
            caminho_destino = os.path.join(download_dir, nome_destino)
            os.rename(caminho_origem, caminho_destino)
            print(f"✅ Renomeado para: {caminho_destino}")

            driver.close()
            driver.switch_to.window(janela_original)
            return

        time.sleep(1)

    print("⚠️ Tempo de espera para o download excedido.")
    # Garante retorno mesmo em falha
    if len(driver.window_handles) > 1:
        driver.close()
    driver.switch_to.window(janela_original)







