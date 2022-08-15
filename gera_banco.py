# código muito simplificado para criar um banco de dados de exemplo.
import sqlite3
# abre uma conexão
con = sqlite3.connect('banco.db')

# pega um cursor, que é o objeto que irá executar as transações
cur = con.cursor()

# cria tabela
cur.execute('''
    CREATE TABLE IF NOT EXISTS TENIS (
        id integer, nome text, valor integer, cor text,
        primary key(id)
    )
''')

# insere dados
cur.execute('''
    INSERT INTO TENIS(id, nome, valor, cor) VALUES 
    (0, 0, 1, 'primeiro semestre'),
    (1, 1, 0, 'primeiro semestre'),
    (2, 2, 0, 'primeiro semestre'),
    (3, 3, 0, 'primeiro semestre'),
    (4, 4, 0, 'primeiro semestre'),
    (5, 0, 0, 'segundo semestre'),
    (6, 1, 1, 'segundo semestre'),
    (7, 2, 0, 'segundo semestre'),
    (8, 3, 0, 'segundo semestre'),
    (9, 4, 0, 'segundo semestre');
''')

# salva modificações
con.commit()

# fecha conexão com o banco
con.close()
