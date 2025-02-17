
import json
import datetime

def addLibro(mysql,ISBN,titolo, categoria, x, y, z):
    cursor = mysql.connection.cursor()
    query = '''SELECT * FROM Libri WHERE ISBN=%s'''
    cursor.execute(query,(ISBN,))
    dati = cursor.fetchall() #torna il risultato della query
    if len(dati)==0:
        query = '''INSERT INTO Libri(ISBN, Titolo, Categoria, NumCopie) value(%s,%s,%s,%s)'''
        cursor.execute(query,(ISBN,titolo, categoria, numCopie))
        query='''INSERT INTO Inventario(ISBN,x,y,z) value(%s,%s,%s)'''
        cursor.execute(query,(ISBN,titolo, categoria, numCopie))
        mysql.connection.commit()
        cursor.close()
        return False #torna False se l'ISBN non esiste e bisogna creare un nuovo libro

    query = '''INSERT INTO Libri(ISBN, Titolo, Categoria, NumCopie) value(%s,%s,%s,%s)'''
    cursor.execute(query,(ISBN,titolo, categoria, numCopie))
    mysql.connection.commit()
    cursor.close()




        def getUtenti():
            query="SELECT * FROM UTENTI"
            cursor=mysql.connection.cursor()
            cursor.execute(query)
            return cursor.fetchall()