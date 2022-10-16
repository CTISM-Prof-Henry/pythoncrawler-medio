import sqlite3
con = sqlite3.connect('banco.db')
cur = con.cursor()

produto = cur.execute('select * from produto').fetchall()
anota = cur.execute('select * from anota').fetchall()
anota_produto = cur.execute('select * from produto_e_anota').fetchall()

print('produto:', produto)
print('anotações:', anota)
print('os dois', anota_produto)


con.close()