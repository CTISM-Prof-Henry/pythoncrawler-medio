# para ver uma galeria com exemplos de gráficos no matplotlib, acesse 
# este link: https://matplotlib.org/stable/gallery/index.html

from matplotlib import pyplot as plt
import numpy as np
import sqlite3
from datetime import datetime as dt


def acessa_banco():
    con = sqlite3.connect('../banco/banco.db')
    cur = con.cursor()

    dados1 = cur.execute('''
                select A.id_produto, A.nome, B.preco, B.dia_crawler
                from produto as A
                inner join produto_e_anota as C on A.id_produto = C.id_produto
                inner join anota as B on C.id_anota = B.id_anota
            ''').fetchall()  # type: list

    processados = dict()

    # linha é uma tupla de 4 posições nessa ordem: id_produto, nome, preco, date_annotation
    # pois essas foram as colunas selecionadas na cláusula select
    for linha in dados1:
        # o formato deve ser o mesmo que foi usado para armazenar a string
        data = dt.strptime(linha[3], '%Y-%m-%d-%H-%M-%S')

        if linha[1] in processados:
            # adiciona à lista
            processados[linha[1]] += [{'preço': linha[2], 'data': data}]
        else:
            # cria lista
            processados[linha[1]] = [{'preço': linha[2], 'data': data}]

    return processados


def desenha(produto):
    fig, ax = plt.subplots()

    for nome, dados in produto.items():
        datas = []
        precos = []
        for linha in dados:
            datas += [linha['data']]
            precos += [linha['preço']]

        processados = list(sorted(zip(datas, precos), key=lambda x: x[0]))
        datas, precos = zip(*processados)
        datas = [x.timestamp() for x in datas]
        ax.plot(datas, precos, label=nome)

    ax.set_title('preços dos produtos coletados pelo crawler')

    plt.legend(loc='upper right')

    plt.savefig('gráfico.png', format='png')
    plt.show()


def main():
    produto = acessa_banco()
    desenha(produto)


if __name__ == '__main__':
    main()
