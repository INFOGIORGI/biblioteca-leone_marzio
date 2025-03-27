from datetime import datetime
from dateutil.relativedelta import relativedelta

nLibri=20
nFile=6
nScaffali=16
nScaffaliPerCat=2





def addLibro(mysql,ISBN,titolo, categoria,autori, x, y, z):
    cursor = mysql.connection.cursor()
    query = '''SELECT * FROM Libri WHERE ISBN=%s'''
    cursor.execute(query,(ISBN,))
    dati = cursor.fetchall()
    ritorno=1
    if len(dati)==0:
        query = '''INSERT INTO Libri(ISBN, Titolo, Categoria, NumCopie, Autori) value(%s,%s,%s,0,%s)'''
        cursor.execute(query,(ISBN,titolo, categoria, autori))
        mysql.connection.commit()
        ritorno=2 #torna False se l'ISBN non esiste e bisogna creare un nuovo libro

    query='''SELECT * FROM Inventario WHERE x = %s AND y = %s AND z=%s'''
    cursor.execute(query,( x, y, z))
    dati = cursor.fetchall()

    if len(dati)!=0:
        return 0


    query='''INSERT INTO Inventario(ISBN,x,y,z) value(%s,%s,%s,%s)'''
    cursor.execute(query,(ISBN, x, y, z))
    query='''UPDATE Libri SET NumCopie = NumCopie+1 WHERE ISBN = %s'''
    cursor.execute(query,(ISBN,))
    mysql.connection.commit()
    cursor.close()
    return ritorno




def getLibri(mysql, parolaChiave):
    query = "SELECT * FROM Libri WHERE Titolo LIKE %s OR ISBN LIKE %s OR Categoria LIKE %s"
    cursor = mysql.connection.cursor()
    parolaChiave = "%" + parolaChiave + "%"
    cursor.execute(query, (parolaChiave, parolaChiave, parolaChiave))
    titoli = cursor.fetchall()
    
    libri_con_autori = []
    for titolo in titoli:
        libri_con_autori.append({
            'ISBN': titolo[0],
            'Titolo': titolo[1],
            'Categoria': titolo[2],
            'NumCopie': titolo[3],
            'Autori': titolo[4]
        })
    
    cursor.close()
    return libri_con_autori



def ordinaLibri(libri, tipo):
    
    if tipo:
        return sorted(libri, key=lambda x: x['Titolo'])
    return sorted(libri, key=lambda x: x['Autori'])


def getLibriPerGenere(mysql, genere):

    query = "SELECT * FROM Libri WHERE Categoria = %s"
    cursor = mysql.connection.cursor()
    cursor.execute(query, (genere,))
    libri = cursor.fetchall()
    cursor.close()
    
    libri_con_autori = []
    for libro in libri:
        libri_con_autori.append({
            'ISBN': libro[0],
            'Titolo': libro[1],
            'Categoria': libro[2],
            'NumCopie': libro[3],
            'Autori': libro[4]
        })
    
    return libri_con_autori


def getStatisticheGenere(mysql, genere):
    query = "SELECT Categoria FROM Libri WHERE Categoria = %s"
    cursor = mysql.connection.cursor()
    cursor.execute(query, (genere, ))
    generi = cursor.fetchall()

    return len(generi)

def registraUtente(mysql, nome, cognome, CF, email, telefono, username, password):
    query="SELECT * FROM Utenti WHERE CF = %s"
    cursor=mysql.connection.cursor()
    cursor.execute(query, (CF, ))
    if cursor.fetchall():
        return False
    query="INSERT INTO Utenti (CF, Nome, Cognome, Email, Telefono) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (CF, nome, cognome, email, telefono))
    query="INSERT INTO Tessera (CF, Nprestiti, DataScadenza, username, Pwd, IsAdmin) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (CF, 0, datetime.now()+relativedelta(months=1), username, password, 0))
    mysql.connection.commit()
    return True

def getHashedPw(mysql, username):
    query="SELECT * FROM Tessera WHERE Username = %s"
    cursor=mysql.connection.cursor()
    cursor.execute(query, (username, ))
    if cursor.fetchall()=="":
        return 0
    query="SELECT DataScadenza from Tessera WHERE Username=%s"
    cursor=mysql.connection.cursor()
    cursor.execute(query, (username, ))
    utente= cursor.fetchall()
    if utente[0][0]<datetime.now().date():
        return 2
    query="SELECT Pwd from Tessera WHERE Username=%s"
    cursor=mysql.connection.cursor()
    cursor.execute(query, (username, ))
    return cursor.fetchall()[0][0]
    




        
