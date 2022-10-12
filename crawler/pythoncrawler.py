from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
from datetime import datetime as dt

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
        nome = driver.find_elements_by_tag_name("div.item-card__description__product-name")
        preco = driver.find_elements_by_tag_name("span.haveInstallments")
        desconto = driver.find_elements_by_tag_name("li.discount.text")
        time.sleep(4)
        # abrindo conexao com banco
        database_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'banco.db')
        with sqlite3.connect(database_path) as con:
            cur = sqlite3.connect('../banco/banco.db')
            # pegando data do dia q rodar
            data_crawler = dt.now().strftime('%Y-%m-%d-%H-%M-%S')
            # gerando os id da tabela produtos
            try:
                ultimo_produto_id = int(cur.execute('SELECT MAX(id_produto) from produtos').fetchone()[0]) + 1
            except:
                ultimo_produto_id = 0
            # gerando os id da tabela anota
            try:
                ultimo_anota_id = int(cur.execute('SELECT MAX(id_anotacao) from anotacoes').fetchone()[0]) + 1
            except:
                ultimo_anota_id = 0

                # se tiver no banco
                res = cur.execute('SELECT id_produto FROM PRODUTO WHERE nome=\'{0}\''.format(nome)).fetchone()
                if res is None:  # se nao tiver nada no banco:
                    # insere id, nome, preco e desconto
                    cur.execute(
                        'INSERT OR REPLACE INTO PRODUTO(id_produto, nome, desconto) VALUES ({0}, \'{1}\', \'{2}\')'.format
                        (ultimo_produto_id, nome.text, preco.text, desconto.text)
                    )
                    # definindo id_produto
                    id_produto = ultimo_produto_id
                    ultimo_produto_id += 1
                else:
                    id_produto = res[0]   # atribui o id recuperado a variável id_produto

                # inserindo na tabela ANOTA
                cur.execute(
                    'INSERT OR REPLACE INTO ANOTA(id_anota, data_crawler, preco) VALUES ({0}, \'{1}\', \'{2}\')'.format(
                        ultimo_anota_id, data_crawler, preco.text)
                )

                # inserindo na tabela de intersecção PRODUTO_e_ANOTA
                cur.execute(
                    'INSERT OR REPLACE INTO PRODUTO_e_ANOTA(id_produto, id_anota) VALUES ({0}, {1})'.format(
                        id_produto, ultimo_anota_id
                    )
                )
                ultimo_anota_id += 1
                con.commit()
                # fechando conexão com o banco
                con.close()


if __name__ == '__main__':
    main()
