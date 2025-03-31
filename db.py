from datetime import datetime
from dateutil.relativedelta import relativedelta

nLibri=20
nFile=6
nScaffali=16
nScaffaliPerCat=2





def addLibro(mysql,ISBN,titolo, categoria,autori, riassunto):
    cursor = mysql.connection.cursor()
    query = '''SELECT * FROM Libri WHERE ISBN=%s'''
    cursor.execute(query,(ISBN,))
    dati = cursor.fetchall()

    if len(dati)!=0:
        return False
    
    query = '''INSERT INTO Libri(ISBN, Titolo, Categoria, NumCopie, Autori, Riassunto) value(%s,%s,%s,0,%s,%s)'''
    cursor.execute(query,(ISBN,titolo, categoria, autori, riassunto))
    mysql.connection.commit()
    return  True


def posizionaLibro(mysql, ISBN, x, y, z):
    query='''SELECT * FROM Inventario WHERE x = %s AND y = %s AND z=%s'''
    cursor = mysql.connection.cursor()
    cursor.execute(query,( x, y, z))
    dati = cursor.fetchall()

    if len(dati)!=0:
        return 0

    query='''SELECT * FROM Libri WHERE ISBN =%s'''
    cursor.execute(query,(ISBN, ))
    dati = cursor.fetchall()

    if len(dati)==0:
        return 2

    query='''INSERT INTO Inventario(ISBN,x,y,z) value(%s,%s,%s,%s)'''
    cursor.execute(query,(ISBN, x, y, z))
    query='''UPDATE Libri SET NumCopie = NumCopie+1 WHERE ISBN = %s'''
    cursor.execute(query,(ISBN,))
    mysql.connection.commit()
    cursor.close()
    return 1

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
        # Ordina per Titolo
        return sorted(libri, key=lambda x: x['Titolo'])
    else:
        # Ordina per tutti gli autori (alfabeticamente)
        libri_ordinati=[]
        for libro in libri:
            libro['Autori']=libro['Autori'].split(', ')
            libro['Autori'].sort()
            libro['Autori'] = ', '.join(libro['Autori'])
            libri_ordinati.append(libro)
        
        return sorted(libri_ordinati, key=lambda x: sorted(x['Autori']))





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
    if cursor.fetchall():    
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
    return 0
    
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
        cursor.execute(query, (datetime.now()+relativedelta(months=2), username))
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
        query='''SELECT ISBN FROM Inventario WHERE IDL = %s'''
        cursor.execute(query, (IDL,))
        ISBN=cursor.fetchall()
        if ISBN:
            query='''UPDATE Libri SET NumCopie = NumCopie-1 WHERE ISBN = %s'''
            cursor.execute(query, (ISBN[0][0],))
            mysql.connection.commit()
        
        return True #ritorno True se è andato a buon fine

    return False #ritorno False se non esiste il CF

def ritornaPrestito(mysql, IDL):
    query="SELECT * FROM Prestiti WHERE IDL=%s"
    cursor=mysql.connection.cursor()
    cursor.execute(query, (IDL,))
    risultato = cursor.fetchall()
    ritorno=1
    if risultato:
        if risultato[0][2]>datetime.now().date():
            ritorno=2
        query="DELETE FROM Prestiti WHERE IDL=%s"
        cursor.execute(query, IDL)
        query="UPDATE Prestiti SET dataRestituzione = %s WHERE IDL=%s"
        return ritorno
    return 0

def get_prestiti(mysql):
    cursor = mysql.connection.cursor()
    query = """
        SELECT DataInizio, DataScadenza, CF, IDL, DataRestituzione
        FROM Prestiti
        ORDER BY DataInizio
    """
    cursor.execute(query)
    risultati = cursor.fetchall()
    cursor.close()
    
    # Mappiamo i risultati in una lista di dizionari
    prestiti = []
    for row in risultati:
        prestito = {
            'DataInizio': row[0],
            'DataScadenza': row[1],
            'CF': row[2],
            'IDL': row[3],
            'DataRestituzione': row[4]  # Può essere None se non ancora restituito
        }
        prestiti.append(prestito)
    return prestiti

def restituisci_prestito(mysql, data_inizio, cf, idl):
    cursor = mysql.connection.cursor()
    query = """
        UPDATE Prestiti
        SET DataRestituzione = NOW()
        WHERE DataInizio = %s AND CF = %s AND IDL = %s
    """
    cursor.execute(query, (data_inizio, cf, idl))
    mysql.connection.commit()
    cursor.close()
        


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

