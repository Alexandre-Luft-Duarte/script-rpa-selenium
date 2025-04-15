from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from utils import ler_codigos_csv, safe_click
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException

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

        #botao_emissao = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "mainForm:emitirUnificada")))
        #botao_emissao.click()

        # Verifica se a mensagem de sem iptu existe
        try:
            mensagem_sem_iptu = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "mainForm:master:messageSection:warn"))).text.strip()
            if mensagem_sem_iptu:
                print(f"Código {codigo} não possui IPTU.")
                continue
        except TimeoutException:
            pass
        
        # Chama a função que procura e clica em um elemento. Tenta clicar no botão de débitos em aberto
        safe_click(driver, By.ID, "P0")
        time.sleep(2)

        try:
            marcar_qtd_parcelas = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "mainForm:P:0:F:0:resumo:4:selectedUnica")))
            print("Selecionando quantidade de parcelas...")
            driver.execute_script("arguments[0].click();", marcar_qtd_parcelas)
            time.sleep(2)
        except TimeoutException:
            print("Seletor de parcelas não encontrado — seguindo normalmente.")
        except Exception as e:
            print(f"Erro ao tentar clicar em quantidade de parcelas: {e}")

        time.sleep(2)

        # Chama a função que procura e clica em um elemento. Tenta clicar no botão de marcar todas
        safe_click(driver, By.ID, "selectAll")

        time.sleep(2)

        if safe_click(driver, By.ID, "mainForm:emitirUnificada"):
            print("Clicou em emissão")
        else: 
            print("Não clicou")

print("Deu boa")
time.sleep(5)
