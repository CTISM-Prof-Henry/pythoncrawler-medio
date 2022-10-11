# código muito simplificado para criar um banco de dados de exemplo.
import sqlite3
# abre uma conexão
con = sqlite3.connect('banco.db')

# pega um cursor, que é o objeto que irá executar as transações
cur = con.cursor()

# cria tabela
cur.execute('''
    CREATE TABLE IF NOT EXISTS PRODUTO (
        id_produto integer, nome text, desconto text,
        primary key(id_produto)
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS ANOTA (
        id_anota integer, preco text, data_crawler text,
        primary key(id_anota)
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS INTERSECTA (
        id_anota integer not null, id_produto integer not null,
        primary key(id_anota, id_produto),
        foreign key (id_produto) references PRODUTO(id_produto)
        foreign key (id_anota) references ANOTA(id_anota)
        
    )
''')


# salva modificações
con.commit()

# fecha conexão com o banco
con.close()
