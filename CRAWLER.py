from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os


def main():
    if os.name == 'nt':
        path = './geckodriver.exe'
    else:
        path = './geckodriver'

    with webdriver.Firefox(executable_path=path) as driver:
        # abre uma instância do firefox na página dada
        driver.get(
            'https://www.netshoes.com.br/tenis-asics-gelrebound-feminino-preto+verde-2FV-8422-871')  # link do produto
        # adicionando a tag onde esta o preço
        nome_produto1 = driver.find_elements_by_tag_name("h1")

        # imprimindo na tela o valor do produto
        for some in nome_produto1:
            print(some.text)
        preco_produto = driver.find_elements_by_tag_name("div.default-price")
        for some in preco_produto:
            print(some.text)
        time.sleep(10)


if __name__ == '__main__':
    main()
