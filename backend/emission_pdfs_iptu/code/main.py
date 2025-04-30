from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from utils import (
    read_codes_csv,
    safe_click,
    start_navegation,
    start_driver,
    wait_download,
    select_single_installment,
)


# Função que processa cada código de imóvel, fazendo a pesquisa e emitindo a guia
def process_code(driver, code, first_consultation=False):
    print(f"\nPesquisando o código do imóvel {code}")

    # Verifica se é a primeira consulta. Caso seja, exibe o campo de pesquisa, caso contrário, começa uma nova consulta.
    if first_consultation:
        # Clica no botão que revela o campo de pesquisa (só faz isso na primeira consulta)
        safe_click(driver, By.XPATH, "/html/body/div[1]/div[2]/div/div/div/form/div[1]/div[1]/div[2]/div/div[1]/div[3]/div/div/div/a")
    else:
        # Clica no botão de nova consulta para os demais códigos
        safe_click(driver, By.XPATH, "/html/body/div[1]/div[2]/div/div/div/form/div[1]/div[1]/div[3]/span/input")
        time.sleep(1)

    # Localiza o campo de input para o código do imóvel e insere o código
    input_field = safe_click(driver, By.ID, "mainForm:iImoveis")
    input_field.clear()  # Limpa o campo de entrada antes de digitar o código
    input_field.send_keys(str(code))

    # Clica no botão de pesquisa para buscar o imóvel
    safe_click(driver, By.ID, "mainForm:btIImoveis")
    time.sleep(1)

    # Verifica se aparece a mensagem de "sem IPTU" e se aparecer, pula o imóvel
    try:
        message = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, "mainForm:master:messageSection:warn"))
        ).text.strip()  # Acessa a mensagem e remove os espaços em branco
        if message:
            print(f"Código {code} não possui IPTU.")  # Informa que o imóvel não tem IPTU
            return  # Sai da função, pois não há IPTU para esse código
    except TimeoutException:
        pass  # Caso a mensagem de erro não apareça, continua a execução

    # Clica no botão para visualizar os débitos em aberto
    safe_click(driver, By.ID, "P0")
    time.sleep(2) 

    # Seleciona a parcela única, se necessário
    select_single_installment(driver)

    # Tenta marcar todas as parcelas e fornece feedback sobre o sucesso ou falha da operação
    if safe_click(driver, By.ID, "selectAll"):
        print("Parcelas marcadas com sucesso.")
    else:
        print("Falha ao marcar parcelas.")

    time.sleep(3)

    # Clica no botão de emissão de guia e aguarda o download do arquivo
    if safe_click(driver, By.ID, "mainForm:emitirUnificada"):
        print("Clicou em emissão.")
        wait_download(driver, "pdfs_iptu", f"iptu_{code}.pdf")
    else:
        print("Botão de emissão não encontrado ou não clicável.")  # Caso o botão não esteja disponível


# Função principal que inicializa o driver e chama a função de processamento para cada código
def main():
    driver = start_driver("pdfs_iptu")  # Inicia o driver do navegador e define o diretório de downloads
    start_navegation(driver)  # Acessa o site e navega até a página do IPTU

    codigos = read_codes_csv()  # Lê os códigos dos imóveis do arquivo CSV
    for i, codigo in enumerate(codigos):
        # Processa o código atual, passando True para a primeira consulta e False para as demais
        process_code(driver, codigo, primeira_consulta=(i == 0))

    print("Processo finalizado.")  # Exibe mensagem de finalização
    time.sleep(5)  # Aguarda 5 segundos antes de fechar o navegador


# Chama a função principal quando o script é executado diretamente
if __name__ == "__main__":
    main()
