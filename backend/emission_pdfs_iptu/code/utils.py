import os, time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
)

# Lê o arquivo CSV contendo os códigos dos imóveis e retorna uma lista com esses códigos.
def read_codes_csv(caminho_csv="file_csv/iptu_96_25032025.csv"):
    # Usa o pandas para ler o arquivo CSV e separa os dados com o delimitador ';'.
    df = pd.read_csv(caminho_csv, delimiter=";")
    # Retorna a coluna 'imovel_prefeitura' como uma lista de códigos de imóveis.
    return df['imovel_prefeitura'].tolist()


# Inicia o driver do Chrome com configurações personalizadas para os downloads.
def start_driver(download_dir="pdfs_iptu"):
    os.makedirs(download_dir, exist_ok=True) # Cria o diretório para os downloads, caso não exista.
    absolute_path = os.path.abspath(download_dir)

    # Configurações do Chrome para definir o diretório de download e desabilitar a solicitação de confirmação.
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": absolute_path,  # Define o diretório de downloads.
        "download.prompt_for_download": False,  # Desabilita o prompt de confirmação de download.
        "download.directory_upgrade": True,  # Permite atualizar o diretório de download.
        "plugins.always_open_pdf_externally": True,  # Força a abertura de arquivos PDF no navegador, sem exibir o visualizador.
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Inicializa o WebDriver com o ChromeDriverManager, que gerencia a instalação do driver necessário.
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


# Navega até a página de consulta do IPTU no site de São Miguel.
def start_navegation(driver):
    driver.maximize_window()
    driver.get("https://www.saomiguel.sc.gov.br/") # Acessa a página principal do site da Prefeitura.
    time.sleep(3)

    # Espera até que a barra de busca esteja visível e, em seguida, realiza a pesquisa por "IPTU".
    search = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "form-control"))
    )
    search.send_keys("IPTU")

    # Clica no ícone de busca para realizar a pesquisa.
    safe_click(driver, By.CLASS_NAME, "icon-smo-search")
    time.sleep(3)

    # Clica no link que leva à página do IPTU.
    safe_click(driver, By.XPATH, "/html/body/main/div/div[2]/div/a[1]")
    time.sleep(10)

    # Troca para a nova aba que é aberta (betha).
    tabs = driver.window_handles
    driver.switch_to.window(tabs[1])

    # Acessa a URL do sistema de consulta do IPTU.
    driver.get("https://e-gov.betha.com.br/cdweb/03114-473/contribuinte/rel_guiaiptu.faces")
    time.sleep(3)


# Tenta clicar em um elemento com segurança, realizando várias tentativas e fallback via JavaScript.
def safe_click(driver, by, value, timeout=10, attempts=2):
    for attempt in range(attempts):
        try:
            # Aguarda até que o elemento esteja visível.
            el = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            if el.is_displayed():
                try:
                    # Tenta clicar no elemento.
                    el.click()
                except ElementClickInterceptedException:
                    # Se houver um erro no clique, tenta clicar via JavaScript.
                    driver.execute_script("arguments[0].click();", el)
                return el
        except (TimeoutException, StaleElementReferenceException):
            # Se não conseguir clicar, aguarda 1 segundo e tenta novamente.
            time.sleep(1)
    return None


# Seleciona a opção de parcela única se estiver disponível no sistema.
def select_single_installment(driver):
    try:
        # Aguarda até que o input da parcela única esteja visível na página.
        input_installment = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'selectedUnica')]"))
        )
        # Se a parcela não estiver selecionada, clica nela para selecioná-la.
        if not input_installment.is_selected():
            driver.execute_script("arguments[0].click();", input_installment)
            time.sleep(1)
    except Exception as e:
        # Caso ocorra algum erro ao tentar selecionar a parcela, exibe a mensagem de erro.
        print(f"Erro ao selecionar parcela única: {e}")


# Aguarda o download do PDF e renomeia o arquivo para o nome desejado.
def wait_download(driver, download_dir, nome_destino, timeout=15):
    janela_original = driver.current_window_handle
    for _ in range(5):
        # Verifica se novas janelas foram abertas após o clique de emissão.
        new_windows = [h for h in driver.window_handles if h != janela_original]
        if new_windows:
            break
        time.sleep(1)
    else:
        # Se não houver novas janelas, retorna sem realizar o processo.
        return

    new_window = new_windows[0]
    driver.switch_to.window(new_window)

    inicio = time.time()
    while time.time() - inicio < timeout:
        # Verifica se algum arquivo PDF foi baixado no diretório especificado.
        files = [f for f in os.listdir(download_dir) if f.endswith(".pdf")]
        if files:
            # Se o arquivo foi baixado, seleciona o mais recente e renomeia.
            downloaded_files = sorted(files, key=lambda x: os.path.getctime(os.path.join(download_dir, x)))[-1]
            os.rename(os.path.join(download_dir, downloaded_files), os.path.join(download_dir, nome_destino))
            driver.close()   # Fecha a janela de download e retorna para a janela original.
            driver.switch_to.window(janela_original)
            return
        time.sleep(1)

    # Caso o download não tenha ocorrido dentro do tempo limite, fecha a nova janela.
    if len(driver.window_handles) > 1:
        driver.close()
    driver.switch_to.window(janela_original)

