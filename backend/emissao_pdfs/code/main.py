from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from backend.extracao_dados_pdf.utils import (
    ler_codigos_csv,
    safe_click,
    iniciar_navegacao_iptu,
    iniciar_driver,
    aguardar_download_renomear,
    selecionar_parcela_unica,
)


# Função que processa cada código de imóvel, fazendo a pesquisa e emitindo a guia
def processar_codigo(driver, codigo, primeira_consulta=False):
    print(f"\nPesquisando o código do imóvel {codigo}")

    # Verifica se é a primeira consulta. Caso seja, exibe o campo de pesquisa, caso contrário, começa uma nova consulta.
    if primeira_consulta:
        # Clica no botão que revela o campo de pesquisa (só faz isso na primeira consulta)
        safe_click(driver, By.XPATH, "/html/body/div[1]/div[2]/div/div/div/form/div[1]/div[1]/div[2]/div/div[1]/div[3]/div/div/div/a")
    else:
        # Clica no botão de nova consulta para os demais códigos
        safe_click(driver, By.XPATH, "/html/body/div[1]/div[2]/div/div/div/form/div[1]/div[1]/div[3]/span/input")
        time.sleep(1)

    # Localiza o campo de input para o código do imóvel e insere o código
    campo_input = safe_click(driver, By.ID, "mainForm:iImoveis")
    campo_input.clear()  # Limpa o campo de entrada antes de digitar o código
    campo_input.send_keys(str(codigo))

    # Clica no botão de pesquisa para buscar o imóvel
    safe_click(driver, By.ID, "mainForm:btIImoveis")
    time.sleep(1)

    # Verifica se aparece a mensagem de "sem IPTU" e se aparecer, pula o imóvel
    try:
        mensagem = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, "mainForm:master:messageSection:warn"))
        ).text.strip()  # Acessa a mensagem e remove os espaços em branco
        if mensagem:
            print(f"Código {codigo} não possui IPTU.")  # Informa que o imóvel não tem IPTU
            return  # Sai da função, pois não há IPTU para esse código
    except TimeoutException:
        pass  # Caso a mensagem de erro não apareça, continua a execução

    # Clica no botão para visualizar os débitos em aberto
    safe_click(driver, By.ID, "P0")
    time.sleep(2) 

    # Seleciona a parcela única, se necessário
    selecionar_parcela_unica(driver)

    # Tenta marcar todas as parcelas e fornece feedback sobre o sucesso ou falha da operação
    if safe_click(driver, By.ID, "selectAll"):
        print("Parcelas marcadas com sucesso.")
    else:
        print("Falha ao marcar parcelas.")

    time.sleep(3)

    # Clica no botão de emissão de guia e aguarda o download do arquivo
    if safe_click(driver, By.ID, "mainForm:emitirUnificada"):
        print("Clicou em emissão.")
        aguardar_download_renomear(driver, "pdfs_iptu", f"iptu_{codigo}.pdf")
    else:
        print("Botão de emissão não encontrado ou não clicável.")  # Caso o botão não esteja disponível


# Função principal que inicializa o driver e chama a função de processamento para cada código
def main():
    driver = iniciar_driver("pdfs_iptu")  # Inicia o driver do navegador e define o diretório de downloads
    iniciar_navegacao_iptu(driver)  # Acessa o site e navega até a página do IPTU

    codigos = ler_codigos_csv()  # Lê os códigos dos imóveis do arquivo CSV
    for i, codigo in enumerate(codigos):
        # Processa o código atual, passando True para a primeira consulta e False para as demais
        processar_codigo(driver, codigo, primeira_consulta=(i == 0))

    print("Processo finalizado.")  # Exibe mensagem de finalização
    time.sleep(5)  # Aguarda 5 segundos antes de fechar o navegador


# Chama a função principal quando o script é executado diretamente
if __name__ == "__main__":
    main()
