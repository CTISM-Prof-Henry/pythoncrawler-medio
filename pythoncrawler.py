from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

from selenium.webdriver.remote.webelement import WebElement


def main():
    if os.name == 'nt':
        path = './geckodriver.exe'
    else:
        path = './geckodriver'

    with webdriver.Firefox(executable_path=path) as driver:
        # abre uma instância do firefox na página dada
        driver.get('https://www.netshoes.com.br/busca?nsCat=Natural&q=handebol+asics&genero=feminino')  # link do produto
        # adicionando a tag onde esta o preço
        nome_produtos = driver.find_elements_by_tag_name("div.item-card__description__product-name")  # type: list
        preco_produtos = driver.find_elements_by_tag_name("div.pr")  # type: list
        # imprimindo na tela o valor do produto

        for produto in zip(nome_produtos, preco_produtos):
            nome = produto[0]  # type: WebElement
            preco = produto[1]  # type: WebElement
            print('Nome: %s Preço: %s' % (nome.text, preco.text))
        time.sleep(10)


if __name__ == '__main__':
    main()
