from mpmath.functions.elliptic import nome
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

        # abre uma conexão
        con = sqlite3.connect('banco.db')

        # pega um cursor, que é o objeto que irá executar as transações
        cur = con.cursor()

        # imprimindo na tela o valor do produto
        for produto in zip(nome_produtos, preco_produtos, desconto_produto):  # zipando para poder manipular

            nome = produto[0]  # nome vai na posição 1
            preco = produto[1]  # preço vai na posição 2
            desconto = produto[2]  # desconto vai na posição 3

            if not desconto:  # definindo que se nao houver desconto, mostra na tela:
                print('Nome: %s \nPreço: %s\nDesconto: --' % (nome.text, preco.text))
            else:  # se houver:
                print('Nome: %s \nPreço: %s\nDesconto:  %s' % (nome.text, preco.text, desconto.text))

            cur.execute('''INSERT INTO PRODUTOS() VALUES ({0}, '{1}')'''.format(id, nome))

        time.sleep(2)  # botando p dormir por 2 segundos

        # salva modificações
        con.commit()

        # fecha conexão com o banco
        con.close()

def getnome():
    return nome
def get


if __name__ == '__main__':
    main()
