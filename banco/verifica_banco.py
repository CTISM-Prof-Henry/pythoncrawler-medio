import sqlite3
con = sqlite3.connect('banco.db')
cur = con.cursor()


anota = cur.execute('select * from ANOTA').fetchall()
print('anotações:', anota)

con.close()