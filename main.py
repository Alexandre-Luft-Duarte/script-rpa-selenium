from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from utils import ler_codigos_csv

# Inicializa o Chrome
driver = webdriver.Chrome()
driver.maximize_window()

# Abre e navega no site da prefeitura
driver.get("https://www.saomiguel.sc.gov.br/")

time.sleep(3)

# Clica na barra de pesquisa
botao_servicos = driver.find_element(By.CLASS_NAME, "form-control")
botao_servicos.click()

# Pesquisa iptu
botao_servicos.send_keys('IPTU')

# Clica no botão de pesquisar
botao_pesquisar_iptu = driver.find_element(By.CLASS_NAME, 'icon-smo-search').click()

time.sleep(1)

# Clica em iptu
botao_iptu = driver.find_element(By.XPATH, "/html/body/main/div/div[2]/div/a[1]").click()

time.sleep(3)

# Seleciona uma aba diferente
abas = driver.window_handles
driver.switch_to.window(abas[1])

# Abre e Começa a navegar no site do betha
driver.get('https://e-gov.betha.com.br/cdweb/03114-473/contribuinte/rel_guiaiptu.faces')

time.sleep(2)

# Inserindo os códigos dos imóveis
for posicao, codigo in enumerate(ler_codigos_csv()):
    print(f"Pesquisando o código do imóvel {codigo}")

    # Clica onde após o clique aparece o campo para colocar o código
    botao_codigo_imovel = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/div/form/div[1]/div[1]/div[2]/div/div[1]/div[3]/div/div/div/a")
    botao_codigo_imovel.click()

    # Clica no campo para escrever e escreve o código
    campo_input_imovel = driver.find_element(By.ID, "mainForm:iImoveis")
    campo_input_imovel.click()
    campo_input_imovel.clear()
    campo_input_imovel.send_keys(str(codigo))
    
    time.sleep(1)

    # Fazendo a pesquisa
    botao_continuar_pesquisar_imóvel = driver.find_element(By.ID, "mainForm:btIImoveis")
    botao_continuar_pesquisar_imóvel.click()

    time.sleep(1)

    if posicao > 0:
        # Após fazer a consulta do iptu, clica em fazer nova consulta
        botao_nova_consulta = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/div/form/div[1]/div[1]/div[3]/span/input")
        botao_nova_consulta.click()

        # Limpa o campo para colocar o código seguinte
        campo_input_imovel.click()
        campo_input_imovel.clear()
        campo_input_imovel.send_keys(str(codigo))
    campo_input_imovel.clear()


time.sleep(5)
