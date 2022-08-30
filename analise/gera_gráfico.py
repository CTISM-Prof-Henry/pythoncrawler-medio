# para ver uma galeria com exemplos de gráficos no matplotlib, acesse 
# este link: https://matplotlib.org/stable/gallery/index.html

from matplotlib import pyplot as plt
import numpy as np
import sqlite3

def acessa_banco():
    con = sqlite3.connect('banco.db')
    cur = con.cursor()


    dados1 = cur.execute('''
        select x, y
        from exemplo 
        where semestre='primeiro semestre'
    ''').fetchall()
    dados2 = cur.execute('''
        select x, y
        from exemplo 
        where semestre='segundo semestre'
    ''').fetchall()

    # zip(*dados1) transforma uma lista de tuplas em duas tuplas:
    # dados1 = [(0, 1), (0, 0), (0, 0), (0, 0), (0, 0)]
    # zip(*dados1) vira x = (0, 0, 0, 0, 0) e y1 = (1, 0, 0, 0, 0)
    x, y1 = zip(*dados1)
    x, y2 = zip(*dados2)

    return list(x), list(y1), list(y2)


def desenha(x, y1, y2):
    fig, ax = plt.subplots()

    ax.bar(x, y1, label='primeiro semestre', color='#b434eb')
    ax.bar(x, y2, label='segundo semestre', color='#86d96c')

    ax.set_xticks(x)
    ax.set_xticklabels(['segunda', 'terça', 'quarta', 'quinta', 'sexta'])

    ax.set_xlabel('dias da semana')
    ax.set_ylabel('RAPAAAAAZ')

    ax.set_title('nível de alegria nesta escola')

    plt.legend(loc='upper right')

    plt.savefig('gráfico.png', format='png')
    plt.show()

def main():
    x, y1, y2 = acessa_banco()
    desenha(x, y1, y2)


if __name__ == '__main__':
    main()
