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
        # abrindo conexao com banco
        id_produto = 0
        id_anota = 0
        for name in nome_produtos:
            nome = name.text
            name_product = [{'nome: ': nome}]
            print(name_product)
            for i in range(len(name_product)):
                id_produto += i + 1
                print('id do produto: ', id_produto)  # verificando o id
        for price in preco_produtos:
            preco = price.text
            price_product = [{'preco: ': preco}]
            print(price_product)
            for j in range(len(price_product)):
                id_anota += j + 1
                print('id anotação: ', id_anota)  # verificando o id
        # FUNCIONANDO ATE AQUI!!!

        database_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../banco/banco.db')
        with sqlite3.connect(database_path) as con:
            cur = sqlite3.connect('../banco/banco.db')
            # pegando data do dia q rodar
            data_crawler = dt.now().strftime('%Y-%m-%d-%H-%M-%S')
            # gerando os id da tabela produtos


            # se tiver no banco
            res = cur.execute('SELECT id_produto FROM produto WHERE nome=\'{0}\''.format(nome)).fetchone()
            if res is None:  # se nao tiver nada no banco:
                # insere id, nome, preco e desconto
                cur.execute(
                        'INSERT INTO produto(id_produto, nome) VALUES ({0}, \'{1}\')'.format(id_produto, nome))
                con.commit()
                cur.execute(
                    'INSERT INTO anota(id_anota, dia_crawler, preco) VALUES ({0}, \'{1}\', \'{2}\')'.format(
                        id_anota, data_crawler, preco))
                con.commit()

                # inserindo na tabela de intersecção PRODUTO_e_ANOTA
                cur.execute(
                    'INSERT INTO produto_e_anota(id_produto, id_anota) VALUES ({0}, {1})'.format(id_produto, id_anota))

                con.commit()


if __name__ == '__main__':
    main()
