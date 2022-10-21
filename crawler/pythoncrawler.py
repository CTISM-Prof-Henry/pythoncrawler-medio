from selenium import webdriver
import os
import time
import sqlite3
from datetime import datetime as dt


def main():
    if os.name == 'nt':
        path = './geckodriver.exe'
    else:
        path = './geckodriver'

    with webdriver.Firefox(executable_path=path) as driver:
        # abre uma instância do firefox na página dada
        driver.get(
            'https://www.netshoes.com.br/busca?nsCat=Natural&q=asics')  # link do produto

        # adicionando a tag onde esta o preço
        nome_produtos = driver.find_elements_by_tag_name("div.item-card__description__product-name")
        preco_produtos = driver.find_elements_by_tag_name("span.haveInstallments")
        time.sleep(4)

        database_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../banco/banco.db')
        with sqlite3.connect(database_path) as con:
            # pegando data do dia q rodar
            data_crawler = dt.now().strftime('%Y-%m-%d-%H-%M-%S')
            # gerando os id da tabela produtos

            cur = con.cursor()  # cria cursor
            id_produto = 0
            for name in nome_produtos:
                nome = name.text
                name_product = {'na': nome}  # inserindo em um dicionario
                print(name_product)
                # gerando id dos produtos
                for i in range(len(name_product)):  # contando itens do dicionario para gerar id
                    id_produto += i + 1  # acrescentando 1 a cada id
                    print('id do produto: ', id_produto)  # verificando o id

                try:
                    ultimo_produto = int(cur.execute('SELECT MAX(id_produto) from produto').fetchone()[0]) + 1
                except:
                    ultimo_produto = 0

            id_anota = 0
            # criando laço para inserir preço e id anota
            for price in preco_produtos:
                preco = price.text  # definindo preco como text
                price_product = [{'preco: ': preco}]  # inserindo em um diciionario
                print(price_product)
                # gerando id das anotações
                for j in range(len(price_product)):  # contando itens do dicionario para gerar id
                    id_anota += j + 1  # acrescentando 1 a cada id
                    print('id anotação: ', id_anota)  # verificando o id
                    try:
                        ultimo_anota = int(cur.execute('SELECT MAX(id_anota) from anota').fetchone()[0]) + 1
                    except:
                        ultimo_anota = 0
                    res = cur.execute('SELECT id_produto FROM produto WHERE nome=\'{0}\''.format(nome)).fetchone()
                    if res is None:  # não achou nada no banco; o produto não existe lá ainda
                        # insere no banco o produto
                        cur.execute(
                            'INSERT INTO anota(id_anota, dia_crawler, preco) VALUES ({0}, \'{1}\', \'{2}\')'.format(ultimo_anota, data_crawler, preco)
                        )
                        id_ant = ultimo_anota
                        ultimo_anota += 1
                    else:
                        # atribui o id recuperado a variável id_produto
                        id_ant = res[0]
                    cur.execute(
                        'INSERT INTO anota(id_anota, dia_crawler, preco) VALUES ({0}, \'{1}\', \'{2}\')'.format(
                            ultimo_anota, data_crawler, preco)
                    )
          


if __name__ == '__main__':
    main()