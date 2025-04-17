from utils import (
    iniciar_driver,
    ler_codigos_csv,
    acessar_portal_prefeitura,
    processar_codigo_imovel,
    preparar_emissao_guia,
    emitir_e_baixar
)
import time

def main():
    driver = iniciar_driver("pdfs_iptu")
    driver.maximize_window()

    acessar_portal_prefeitura(driver)

    for cont, codigo in enumerate(ler_codigos_csv(), 1):
        primeira_vez = cont == 1
        if not processar_codigo_imovel(driver, codigo, primeira_vez):
            continue

        preparar_emissao_guia(driver)
        emitir_e_baixar(driver, codigo)

    print("Processo finalizado com sucesso.")
    time.sleep(3)

if __name__ == "__main__":
    main()
