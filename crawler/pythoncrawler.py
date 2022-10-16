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
            'https://www.netshoes.com.br/busca?nsCat=Natural&q=handebol+asics&genero=feminino')  # link do produto

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
                name_product = [{nome}]  # inserindo em um dicionario
                print(name_product)
                # gerando id dos produtos
                for i in range(len(name_product)):  # contando itens do dicionario para gerar id
                    id_produto += i + 1  # acrescentando 1 a cada id
                    print('id do produto: ', id_produto)  # verificando o id
                    cur.execute('INSERT OR REPLACE INTO produto(nome, id_produto) VALUES ({0}, \'{1}\' )'.format(name_product, id_produto))
                    con.commit()

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
                    cur.execute('INSERT INTO anota(preco, dia_crawler, id_anota) VALUES ({0}, \'{1}\', {2})'.format(price_product, data_crawler, id_anota))
                    con.commit()
            con.commit()


if __name__ == '__main__':
    main()
