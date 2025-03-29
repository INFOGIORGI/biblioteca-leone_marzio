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
        ritorno=2 #torna 2 se l'ISBN non esiste e bisogna creare un nuovo libro

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




def getLibriPerKey(mysql, parolaChiave, genere):
    cursor = mysql.connection.cursor()
    if genere:
        query = "SELECT * FROM Libri WHERE (Titolo LIKE %s OR ISBN LIKE %s) AND Categoria = %s"
        parolaChiave = "%" + parolaChiave + "%"
        cursor.execute(query, (parolaChiave, parolaChiave, genere))
    elif parolaChiave:
        query = "SELECT * FROM Libri WHERE Titolo LIKE %s OR ISBN LIKE %s"
        parolaChiave = "%" + parolaChiave + "%"
        cursor.execute(query, (parolaChiave, parolaChiave))
    else:
        query = "SELECT * FROM Libri"
        cursor.execute(query)
    
    titoli = cursor.fetchall()
    
    libri_con_autori = []
    for titolo in titoli:
        libri_con_autori.append({
            'ISBN': titolo[0],
            'Titolo': titolo[1],
            'Categoria': titolo[2],
            'NumCopie': titolo[3],
            'Autori': titolo[4],
            'Riassunto': titolo[5]
        })
    
    cursor.close()
    return libri_con_autori



def ordinaLibri(libri, tipo):
    
    if tipo:
        return sorted(libri, key=lambda x: x['Titolo'])
    return sorted(libri, key=lambda x: x['Autori'])



def getStatisticheGenere(mysql, genere):
    if genere:
        query = "SELECT Categoria FROM Libri WHERE Categoria = %s"
        cursor = mysql.connection.cursor()
        cursor.execute(query, (genere, ))
        generi = cursor.fetchall()

        return len(generi)
    return None

def registraUtente(mysql, nome, cognome, CF, email, telefono, username, password):
    query="SELECT * FROM Utenti WHERE CF = %s"
    cursor=mysql.connection.cursor()
    cursor.execute(query, (CF, ))
    if cursor.fetchall():
        return False
    query="INSERT INTO Utenti (CF, Nome, Cognome, Email, Telefono) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (CF, nome, cognome, email, telefono))
    query="INSERT INTO Tessera (CF, Nprestiti, DataScadenza, username, Pwd, IsAdmin) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (CF, 0, datetime.now()+relativedelta(months=2), username, password, 0))
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
    
def isAdmin(mysql, username):
    query="SELECT IsAdmin FROM Tessera WHERE Username= %s"
    cursor=mysql.connection.cursor()
    cursor.execute(query, (username, ))
    if cursor.fetchall()[0][0]:
        return True
    return False

def rinnovaTessera(mysql, username):
    query="SELECT * FROM Tessera WHERE Username=%s"
    cursor=mysql.connection.cursor()
    cursor.execute(query, (username,))
    if cursor.fetchall():
        query="UPDATE Tessera SET DataScadenza=%s WHERE Username=%s"
        cursor.execute(query, (datetime.now().date(), username))
        mysql.connection.commit()
        return True #ritorno True se è andato a buon fine

    return False #ritorno False se non esiste l'username
    

def aggiungiprestito(mysql, CF, dataInizio, dataScadenza , IDL):
    query="SELECT * FROM Utenti WHERE CF=%s"
    cursor=mysql.connection.cursor()
    cursor.execute(query, (CF,))
    if cursor.fetchall():
        query="INSERT INTO Prestiti (DataInizio, DataRestituzione, DataScadenza, CF, IDL) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (dataInizio, None, dataScadenza, CF, IDL))
        query="UPDATE Inventario SET isAvailable = 0 WHERE IDL = %s"
        cursor.execute(query, (IDL,))
        mysql.connection.commit()
        return True #ritorno True se è andato a buon fine

    return False #ritorno False se non esiste il CF

def getIDL(mysql, x, y, z):
    query="SELECT IDL, isAvailable FROM Inventario WHERE x=%s AND y=%s AND z=%s"
    cursor=mysql.connection.cursor()
    cursor.execute(query, (x,y,z))
    risultato=cursor.fetchall()
    if risultato:
        if risultato[0][1]:
            return risultato[0][0]
        return "non disponibile"
    return "non esistente"

