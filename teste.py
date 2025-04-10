import pandas as pd
from selenium import webdriver
import time

# Caminho para o CSV
#CSV_PATH = "arquivo/iptu_96_25032025.csv"

# Lê os códigos do CSV
#df = pd.read_csv(CSV_PATH, delimiter=";")
#codigos = df["imovel_prefeitura"].tolist()

# Inicializa o Chrome
driver = webdriver.Chrome()
driver.maximize_window()

# Abre o site da prefeitura
driver.get("https://www.saomiguel.sc.gov.br/")

time.sleep(3)

# Clica na barra de pesquisa
botao_servicos = driver.find_element('class name', "form-control")
botao_servicos.click()

# Pesquisa iptu
botao_servicos.send_keys('IPTU')

# Clica no botão de pesquisar
botao_pesquisar = driver.find_element('class name', 'icon-smo-search')
botao_pesquisar.click()

# Clica em iptu
botao_iptu = driver.find_element('class name', 'link-item-title')
botao_iptu.click()
time.sleep(5)

