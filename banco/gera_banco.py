# código muito simplificado para criar um banco de dados de exemplo.
import sqlite3
import os


def main():
    # abre uma conexão
    database_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../banco/banco.db')

    if os.path.exists(database_path):
        os.remove(database_path)

    # abre uma conexão com o banco e fecha automaticamente no fim do bloco with
    with sqlite3.connect(database_path) as con:
        # pega um cursor, que é o objeto que irá executar as transações
        # pega um cursor, que é o objeto que irá executar as transações
        cur = con.cursor()

        # cria tabela
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS produto (
                        id_produto integer,
                        nome text, 
                        primary key (id_produto)
                    )
        ''')

        cur.execute('''
                   CREATE TABLE IF NOT EXISTS anota (
                       id_anota integer, 
                       dia_crawler text, 
                       preco text,
                       primary key(id_anota)
                   )
               ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS produto_e_anota (
                id_anota integer not null, id_produto integer not null,
                primary key(id_anota, id_produto),
                foreign key (id_produto) references produto(id_produto)
                foreign key (id_anota) references anota(id_anota)
        
            )
        ''')

        # salva modificações
        con.commit()

        # fecha conexão com o banco


if __name__ == '__main__':
    main()
