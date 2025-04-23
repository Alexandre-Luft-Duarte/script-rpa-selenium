
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils import ler_codigos_csv, safe_click, iniciar_navegacao_iptu, iniciar_driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException


driver = iniciar_driver("pdfs_iptu")
iniciar_navegacao_iptu(driver)

# Inserindo os códigos dos imóveis
for cont, codigo in enumerate(ler_codigos_csv(), 1):
    print(f"\nPesquisando o código do imóvel {codigo}")

    if cont == 1:
        # Primeiro acesso: clica no botão que revela o campo de pesquisa
        safe_click(driver, By.XPATH, "/html/body/div[1]/div[2]/div/div/div/form/div[1]/div[1]/div[2]/div/div[1]/div[3]/div/div/div/a")
    else:
        # Clica no botão de nova consulta
        safe_click(driver, By.XPATH, "/html/body/div[1]/div[2]/div/div/div/form/div[1]/div[1]/div[3]/span/input")
        time.sleep(1)

    # Campo para digitar o código
    campo_input_imovel = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.ID, "mainForm:iImoveis"))
    )
    campo_input_imovel.clear()
    campo_input_imovel.send_keys(str(codigo))

    # Clica no botão para pesquisar
    safe_click(driver, By.ID, "mainForm:btIImoveis")
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
        EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'selectedUnica')]"))
        )
        if not marcar_qtd_parcelas.is_selected:
            driver.execute_script("arguments[0].click();", marcar_qtd_parcelas)
            print("Selecionando quantidade de parcelas...")
            time.sleep(2)
        else:
            print("Parcela já selecionada")
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
    #if safe_click(driver, By.ID, "mainForm:emitirUnificada"):
     #   print("Clicou em emissão.")
    #else:
     #   print("Botão de emissão não encontrado ou não clicável.")
    

print("Deu boa")
time.sleep(5)