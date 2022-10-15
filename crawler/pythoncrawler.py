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

        for name in nome_produtos:
            nome = name.text
            print(nome)
        for price in preco_produtos:
            preco = price.text
            print(preco)
        # FUNCIONANDO ATE AQUI!!!

        database_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../banco/banco.db')
        with sqlite3.connect(database_path) as con:
            cur = sqlite3.connect('../banco/banco.db')
            # pegando data do dia q rodar
            data_crawler = dt.now().strftime('%Y-%m-%d-%H-%M-%S')
            print(data_crawler)
            # gerando os id da tabela produtos
            try:
                ultimo_produto_id = int(cur.execute('SELECT MAX(id_produto) from produto').fetchone()[0]) + 1
                print(ultimo_produto_id)
            except:
                ultimo_produto_id = 0
                print(ultimo_produto_id)
            # gerando os id da tabela anota
            try:
                ultimo_anota_id = int(cur.execute('SELECT MAX(id_anota) from anota').fetchone()[0]) + 1
                print(ultimo_anota_id)
            except:
                ultimo_anota_id = 0
                print(ultimo_anota_id)

                # se tiver no banco
                res = cur.execute('SELECT id_produto FROM produto WHERE nome=\'{0}\''.format(nome)).fetchone()
                if res is None:  # se nao tiver nada no banco:
                    # insere id, nome, preco e desconto
                    cur.execute(
                        'INSERT INTO produto(id_produto, nome) VALUES ({0}, \'{1}\')'.format(ultimo_produto_id, nome))
                    con.commit()
                    # definindo id_produto
                    id_produto = ultimo_produto_id
                    ultimo_produto_id += 1
                else:
                    id_produto = res[0]   # atribui o id recuperado a variável id_produto
                # inserindo na tabela ANOTA
                cur.execute(
                    'INSERT INTO anota(id_anota, dia_crawler, preco) VALUES ({0}, \'{1}\', \'{2}\')'.format(ultimo_anota_id, data_crawler, preco))
                con.commit()

                # inserindo na tabela de intersecção PRODUTO_e_ANOTA
                cur.execute(
                    'INSERT INTO produto_e_anota(id_produto, id_anota) VALUES ({0}, {1})'.format(id_produto, ultimo_anota_id))
                con.commit()
                ultimo_anota_id += 1
                con.commit()


if __name__ == '__main__':
    main()

