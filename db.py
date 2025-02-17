
import json
import datetime

def addLibro(mysql,ISBN,titolo, categoria, x, y, z):
    cursor = mysql.connection.cursor()
    query = '''SELECT * FROM Libri WHERE ISBN=%s'''
    cursor.execute(query,(ISBN,))
    dati = cursor.fetchall() #torna il risultato della query
    if len(dati)==0:
        query = '''INSERT INTO Libri(ISBN, Titolo, Categoria) value(%s,%s,%s)'''
        cursor.execute(query,(ISBN,titolo, categoria))
        query='''INSERT INTO Inventario(ISBN,x,y,z) value(%s,%s,%s)'''
        cursor.execute(query,(ISBN, x, y, z))
        query='''UPDATE Libri SET NumCopie = NumCopie+1 WHERE ISBN = %s'''
        cursor.execute(query,(ISBN,))
        mysql.connection.commit()
        cursor.close()
        return False #torna False se l'ISBN non esiste e bisogna creare un nuovo libro

    query='''INSERT INTO Inventario(ISBN,x,y,z) value(%s,%s,%s)'''
    cursor.execute(query,(ISBN, x, y, z))
    query='''UPDATE Libri SET NumCopie = NumCopie+1 WHERE ISBN = %s'''
    cursor.execute(query,(ISBN,))
    mysql.connection.commit()
    cursor.close()
    return True




def getLibri(mysql, parolaChiave):
    query="SELECT Titolo FROM Libri"
    cursor=mysql.connection.cursor()
    cursor.execute(query)
    titoli=cursor.fetchall()
    titoliCorretti=[]
    for titolo in titoli:
        if parolaChiave in titolo[0].lower():
            titoliCorretti.append(titolo)
     
    return titoliCorretti
