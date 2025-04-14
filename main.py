from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from utils import ler_codigos_csv, safe_click, show
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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
    print(f"Pesquisando o código do imóvel {codigo}")

    if cont == 1:
        # Clica onde após o clique aparece o campo para colocar o código
        botao_codigo_imovel = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div/div/form/div[1]/div[1]/div[2]/div/div[1]/div[3]/div/div/div/a")))
        botao_codigo_imovel.click()

        # Clica no campo para escrever e escreve o código
        campo_input_imovel = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "mainForm:iImoveis")))
        campo_input_imovel.clear()
        campo_input_imovel.send_keys(str(codigo))
        
        # Fazendo a pesquisa
        botao_continuar_pesquisar_imóvel = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "mainForm:btIImoveis")))
        botao_continuar_pesquisar_imóvel.click()

        # Chama a função que procura e clica em um elemento. Tenta clicar no botão de débitos em aberto
        safe_click(driver, By.ID, "P0")

        # Chama a função que procura e clica em um elemento. Tenta clicar no botão de marcar todas as parcelas
        safe_click(driver, By.ID, "selectAll")
    else:
        # Após fazer a consulta do primeiro iptu, clica em fazer nova consulta
        botao_nova_consulta = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div/div/form/div[1]/div[1]/div[3]/span/input")))
        botao_nova_consulta.click()

        time.sleep(1)

        campo_input_imovel = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "mainForm:iImoveis")))
        # Limpa o campo para colocar o código seguinte
        campo_input_imovel.clear()
        campo_input_imovel.send_keys(str(codigo))

        # Faz a pesquisa novamente
        botao_continuar_pesquisar_imóvel = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "mainForm:btIImoveis")))
        botao_continuar_pesquisar_imóvel.click()


        if not show(driver, By.ID, "mainForm:master:messageSection:warn"):
            safe_click(driver, By.ID, "P0") # Chama a função que procura e clica em um elemento. Tenta clicar no botão de débitos em aberto
            safe_click(driver, By.ID, "selectAll") # Chama a função que procura e clica em um elemento. Tenta clicar no botão de débitos em aberto
        #else:
         #   print("Mensagem de sem iptu encontrada. Pulando cliques.")

print("Deu boa")
time.sleep(5)
