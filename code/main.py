from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from utils import ler_codigos_csv, safe_click, aguardar_download_pdf
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os
from selenium.common.exceptions import TimeoutException




# Caminho absoluto da pasta pdfs_iptu
pasta_download = os.path.join(os.path.expanduser("~"), "Área de Trabalho", "pdfs_iptu")
os.makedirs(pasta_download, exist_ok=True)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": pasta_download,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True  # Faz com que o Chrome baixe o PDF em vez de abrir
})


# Inicializa o Chrome
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.maximize_window()

# Abre e navega no site da prefeitura
driver.get("https://www.saomiguel.sc.gov.br/")

time.sleep(3)

# Clica na barra de pesquisa
botao_servicos = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CLASS_NAME, "form-control")))
botao_servicos.click()

# Pesquisa iptu
botao_servicos.send_keys('IPTU')

# Clica no botão de pesquisar
botao_pesquisar_iptu = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CLASS_NAME, 'icon-smo-search')))
botao_pesquisar_iptu.click()

time.sleep(3)

# Clica em iptu
botao_iptu = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "/html/body/main/div/div[2]/div/a[1]")))
botao_iptu.click()

time.sleep(3)

# Seleciona uma aba diferente
abas = driver.window_handles
driver.switch_to.window(abas[1])

# Abre e Começa a navegar no site do betha
driver.get('https://e-gov.betha.com.br/cdweb/03114-473/contribuinte/rel_guiaiptu.faces')

time.sleep(3)

# Inserindo os códigos dos imóveis
for cont, codigo in enumerate(ler_codigos_csv(), 1):
    print(f"\nPesquisando o código do imóvel {codigo}")

    if cont == 1:
        # Primeiro acesso: clica no botão que revela o campo de pesquisa
        botao_codigo_imovel = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div/div/form/div[1]/div[1]/div[2]/div/div[1]/div[3]/div/div/div/a"))
        )
        botao_codigo_imovel.click()
    else:
        # Clica no botão de nova consulta
        botao_nova_consulta = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div/div/form/div[1]/div[1]/div[3]/span/input"))
        )
        botao_nova_consulta.click()
        time.sleep(1)

    # Campo para digitar o código
    campo_input_imovel = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.ID, "mainForm:iImoveis"))
    )
    campo_input_imovel.clear()
    campo_input_imovel.send_keys(str(codigo))

    # Clica no botão para pesquisar
    botao_continuar_pesquisar_imovel = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.ID, "mainForm:btIImoveis"))
    )
    botao_continuar_pesquisar_imovel.click()
    time.sleep(1)

    # Verifica se apareceu a mensagem de "sem IPTU"
    try:
        mensagem_sem_iptu = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, "mainForm:master:messageSection:warn"))
        ).text.strip()
        if mensagem_sem_iptu:
            print(f"Código {codigo} não possui IPTU.")
            continue
    except TimeoutException:
        pass

    # Clique em débitos em aberto
    safe_click(driver, By.ID, "P0")
    time.sleep(2)

    # Verifica se existe seletor de quantidade de parcelas
    try:
        marcar_qtd_parcelas = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(@id, 'selectedUnica')]"))
        )
        print("Selecionando quantidade de parcelas...")
        driver.execute_script("arguments[0].click();", marcar_qtd_parcelas)
        time.sleep(2)
    except TimeoutException:
        print("Seletor de parcelas não encontrado — seguindo normalmente.")
    except Exception as e:
        print(f"Erro ao tentar clicar em quantidade de parcelas: {e}")

    # Clica em marcar todas as parcelas
    if safe_click(driver, By.ID, "selectAll"):
        print("Parcelas marcadas com sucesso.")
    else:
        print("Falha ao marcar parcelas.")

    time.sleep(3)

    # Clica em emitir guia (se disponível)
    if safe_click(driver, By.ID, "mainForm:emitirUnificada"):
        print("Clicou em emissão.")
    try:
        caminho_pdf = aguardar_download_pdf(pasta_download, nome_parcial=str(codigo))
        print(f"[{codigo}] PDF salvo em: {caminho_pdf}")
    except TimeoutError as e:
        print(f"[{codigo}] Erro ao baixar o PDF: {e}")
    else:
        print("Botão de emissão não encontrado ou não clicável.")

print("Deu boa")
time.sleep(5)
