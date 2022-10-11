from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import datetime

import sqlite3

from selenium.webdriver.remote.webelement import WebElement


def main():
    if os.name == 'nt':
        path = './geckodriver.exe'
    else:
        path = './geckodriver'

    with webdriver.Firefox(executable_path=path) as driver:
        # abre uma instância do firefox na página dada
        driver.get(
            'https://www.netshoes.com.br/busca?nsCat=Natural&q=handebol+asics&genero=feminino')  # link do produto

        # adicionando a tag onde esta o preço
        nome_produtos = driver.find_elements_by_tag_name("div.item-card__description__product-name")
        preco_produtos = driver.find_elements_by_tag_name("span.haveInstallments")
        desconto_produto = driver.find_elements_by_tag_name("li.discount.text")

        # data e hora:
        data_crawler = datetime.datetime.now()  # pegando data de acesso
        print("Dia de acesso: ", data_crawler.date())
        print("Horario de acesso: ", data_crawler.time())
        # imprimindo na tela o valor do produto
        for produto in zip(nome_produtos, preco_produtos, desconto_produto):  # zipando para poder manipular

            nome = produto[0]  # nome vai na posição 1
            preco = produto[1]  # preço vai na posição 2
            desconto = produto[2]  # desconto vai na posição 3

            con = sqlite3.connect('../banco/banco.db')
            # pega um cursor, que é o objeto que irá executar as transações
            cur = con.cursor()

            # pega o ultimo id da tabela produtos
            try:
                last_id = int(cur.execute('SELECT MAX(id_produto) from produtos').fetchone()[0]) + 1
            except:
                last_id = 0

            for element in produto:
                cur.execute(
                    'INSERT INTO produtos(id_produto, nome, desconto) VALUES ({0}, \'{1}\', \'{2}\')'.format(last_id, element.text, desconto)
                )
                last_id += 1

                con.commit()
                # fecha conexão com o banco
                con.close()


if __name__ == '__main__':
    main()
