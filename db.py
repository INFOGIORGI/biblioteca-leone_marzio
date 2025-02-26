
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
    query = "SELECT ISBN, Titolo, Categoria, NumCopie FROM Libri WHERE Titolo LIKE %s OR ISBN LIKE %s OR Categoria LIKE %s"
    cursor = mysql.connection.cursor()
    parolaChiave = "%" + parolaChiave + "%"
    cursor.execute(query, (parolaChiave, parolaChiave, parolaChiave))
    titoli = cursor.fetchall()
    
    libri_con_autori = []
    for titolo in titoli:
        ISBN = titolo[0]
        autori = getAutoriPerISBN(mysql, ISBN)
        libri_con_autori.append({
            'ISBN': ISBN,
            'Titolo': titolo[1],
            'Categoria': titolo[2],
            'NumCopie': titolo[3],
            'Autori': autori
        })
    
    cursor.close()
    return libri_con_autori



def ordinaLibri(mysql, tipo):
    query = "SELECT ISBN, Titolo, Categoria, NumCopie FROM Libri"
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    libri = cursor.fetchall()

    libri_con_autori = []
    for libro in libri:
        ISBN = libro[0]
        autori = getAutoriPerISBN(mysql, ISBN)
        libri_con_autori.append({
            'ISBN': ISBN,
            'Titolo': libro[1],
            'Categoria': libro[2],
            'NumCopie': libro[3],
            'Autori': autori
        })
    
    cursor.close()
    
    if tipo:
        return sorted(libri_con_autori, key=lambda x: x['Titolo'])
    return sorted(libri_con_autori, key=lambda x: x['Autori'])



def getAutoriPerISBN(mysql, ISBN):
    query="""
        SELECT Autori.Nome, Autori.Cognome
        FROM Autorato
        JOIN Autori ON Autorato.ISNI=Autori.ISNI
        WHERE ISBN = %s
        """
    cursor=mysql.connection.cursor()
    cursor.execute(query, (ISBN,))
    autori=cursor.fetchall()
    return tuple(f"{autore[0]} {autore[1]}" for autore in autori)


def getLibriPerGenere(mysql, genere):

    query = "SELECT ISBN, Titolo, Categoria, NumCopie FROM Libri WHERE Categoria = %s"
    cursor = mysql.connection.cursor()
    cursor.execute(query, (genere,))
    libri = cursor.fetchall()
    cursor.close()
    
    libri_con_autori = []
    for libro in libri:
        ISBN = libro[0]
        autori = getAutoriPerISBN(mysql, ISBN)
        libri_con_autori.append({
            'ISBN': ISBN,
            'Titolo': libro[1],
            'Categoria': libro[2],
            'NumCopie': libro[3],
            'Autori': ', '.join(autori)
        })
    
    return libri_con_autori


def getStatisticheGenere(mysql, genere):
    query = "SELECT Categoria FROM Libri WHERE Categoria = %s"
    cursor = mysql.connection.cursor()
    cursor.execute(query, (genere, ))
    generi = cursor.fetchall()

    return len(generi)






        
