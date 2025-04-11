from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from utils import ler_codigos_csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

# Inicializa o Chrome
driver = webdriver.Chrome()
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

        # Marcando a opção de débitos em aberto
        botao_debitos_em_aberto = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "P0")))
        botao_debitos_em_aberto.click()

        # Marcando a opção de marcar todas as parcelas
        botato_marcar_todas_parcelas = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "selectAll")))
        botato_marcar_todas_parcelas.click()
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
    for tentaivas in range(2):
        try:
            # Marcando a opção de débitos em aberto
            botao_debitos_em_aberto2 = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "P0")))
            botao_debitos_em_aberto2.click()
        except StaleElementReferenceException:
            print('erro')
            time.sleep(1)


print("Deu boa")
time.sleep(5)
