
import json
import datetime
from flask import flash

nLibri=20
nFile=6
nScaffali=16
nScaffaliPerCat=2

def addLibro(mysql,ISBN,titolo, categoria, x, y, z):
    cursor = mysql.connection.cursor()
    query = '''SELECT * FROM Libri WHERE ISBN=%s'''
    cursor.execute(query,(ISBN,))
    dati = cursor.fetchall()
    ritorno=True
    if len(dati)==0:
        query = '''INSERT INTO Libri(ISBN, Titolo, Categoria) value(%s,%s,%s)'''
        cursor.execute(query,(ISBN,titolo, categoria))
        mysql.connection.commit()
        ritorno=False #torna False se l'ISBN non esiste e bisogna creare un nuovo libro

    query='''SELECT * FROM Inventario WHERE x = %s AND y = %s AND z=%s'''
    cursor.execute(query,( x, y, z))
    dati = cursor.fetchall()

    if len(dati)!=0:
        # flash("esiste già un libro in questa posizione")
        # print("esiste già")
        return False


    query='''INSERT INTO Inventario(ISBN,x,y,z) value(%s,%s,%s,%s)'''
    cursor.execute(query,(ISBN, x, y, z))
    query='''UPDATE Libri SET NumCopie = NumCopie+1 WHERE ISBN = %s'''
    cursor.execute(query,(ISBN,))
    mysql.connection.commit()
    cursor.close()
    return ritorno




def getLibri(mysql, parolaChiave):
    query="SELECT * FROM Libri WHERE Titolo LIKE %s OR ISBN LIKE %s OR Categoria LIKE %s"
    cursor=mysql.connection.cursor()
    parolaChiave="%"+parolaChiave+"%"
    cursor.execute(query,(parolaChiave,parolaChiave,parolaChiave))
    titoli=cursor.fetchall()

    return titoli

def ordinaLibri(mysql, tipo):
    query="SELECT * FROM Libri"
    cursor=mysql.connection.cursor()
    cursor.execute(query)
    libri=cursor.fetchall()
    query="SELECT * FROM Autorato"
    cursor=mysql.connection.cursor()
    cursor.execute(query)
    autorato=cursor.fetchall()
    if(tipo):
        return sorted(libri, key=lambda x: x[1])
    autoriOrdinati=[]
    for libro in libri:
        autori=list(getAutoriPerISBN(mysql, libro[0]))
        autori=sorted(autori)
        for autore in autori:
            autoriOrdinati.libro.append
    
    return 


def getAutoriPerISBN(mysql, ISBN):
    query="""
        SELECT Autori.Nome, Autori.Cognome
        FROM Autorato
        JOIN Autori ON Autorato.ISNI=Autori.ISNI
        WHERE ISBN = %s
        """
    cursor=mysql.connection.cursor()
    cursor.execute(query)
    autori=cursor.fetchall()
    return tuple(f"{autore[0]} {autore[1]}" for autore in autori)