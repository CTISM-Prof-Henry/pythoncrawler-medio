import sqlite3
con = sqlite3.connect('banco.db')
cur = con.cursor()

produto = cur.execute('select * from PRODUTO').fetchall()
anota = cur.execute('select * from ANOTA').fetchall()
anota_produto = cur.execute('select * from PRODUTO_e_ANOTA').fetchall()

print('produto:', produto)
print('anotações:', anota)
print('os dois', anota_produto)


con.close()