from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
import bcrypt
import db
import os

app = Flask(__name__)
app.config['MYSQL_HOST'] = "138.41.20.102"
app.config['MYSQL_PORT'] = 53306
app.config['MYSQL_USER'] = "5di"
app.config['MYSQL_PASSWORD'] = "colazzo"
app.config['MYSQL_DB'] = "leone_marzio"
mysql = MySQL(app)

# Genera una secret key casuale (consigliato):
app.config['SECRET_KEY'] = os.urandom(24)

app.permanent_session_lifetime = timedelta(days=30) # Session Life Time
app.config['SESSION_TYPE'] = "filesystem"  # Session Storage Type

@app.route('/')
def home():
    libri = db.getLibriPerKey(mysql, "", "")
    return render_template('index.html', libri=libri)

@app.route('/librarian', methods=['GET', 'POST'])
def librarian():
    if request.method == 'POST':
        form_type=request.form['form_type']
        if form_type == 'aggiunzione_libro':
            ISBN = request.form['ISBN']
            titolo = request.form['titolo']
            categoria = request.form['categoria']
            autori = request.form['autori']
            riassunto = request.form['riassunto']

            if db.addLibro(mysql, ISBN, titolo, categoria,autori, riassunto):
                flash("Il libro è stato memorizzato con successo")
                return redirect(url_for('librarian'))
            
            flash("Esiste già un libro con questo ISBN")
            return redirect(url_for('librarian'))
        
        elif form_type == 'posizionamento_libro':
            ISBN = request.form['ISBN']
            x = request.form['x']
            y = request.form['y']
            z = request.form['z']
            if db.posizionaLibro(mysql, ISBN, x, y, z) == 1:
                flash("Libro posizionato con successo")
            elif db.posizionaLibro(mysql, ISBN, x, y, z) == 0:
                flash("Esiste già un libro in questa posizione")
            else:
                flash("ISBN inesistente")
            return redirect(url_for('librarian'))

        elif form_type == 'rinnovamento_tessera':
            username=request.form['username']
            if not db.rinnovaTessera(mysql, username):
                flash("Username inesistente")
            else:
                flash("Tessera aggiornata con successo")
            return redirect(url_for('librarian'))
        elif form_type == 'aggiunzione_prestito':
            x= request.form['x']
            y=request.form['y']
            z=request.form['z']
            idl=db.getIDL(mysql, x,y,z)

            if idl == "non disponibile":
                flash("Libro già in prestito")
            elif idl== "non esistente":
                flash(f"Non esiste nessun libro in posizione {x}, {y}, {z}")
            else:
                cf= request.form['CF']
                dataInizio= request.form['dataInizio']
                dataScadenza= request.args.get('dataScadenza', datetime.now()+relativedelta(months=1))
                if db.aggiungiprestito(mysql, cf, dataInizio, dataScadenza, idl):
                    flash("Prestito aggiunto con successo")
                else:
                    flash("Codice fiscale inesistente")
            return redirect(url_for('librarian'))
        elif form_type == 'rimozione_prestito':
            IDL=request.form['IDL']
            risultato=db.ritornaPrestito(mysql, IDL)
            if risultato==2:
                flash("Applicare sanzione per la tarda restituzione")
            elif risultato==1:
                flash("Libro restituito con successo")
            elif risultato==0:
                flash("IDL non in prestito")
            return redirect(url_for('librarian'))
            
    
    return render_template('librarian.html')

    
@app.route('/prestiti')
def prestiti():
    # Ottiene la lista dei prestiti ordinati per DataInizio
    lista_prestiti = db.get_prestiti(mysql)
    return render_template('prestiti.html', prestiti=lista_prestiti)

@app.route('/restituisci', methods=['POST'])
def restituisci():
    # Legge i dati inviati dal form della modale
    data_inizio = request.form.get('DataInizio')
    cf = request.form.get('CF')
    idl = request.form.get('IDL')
    
    # Aggiorna il prestito nel database: setta DataRestituzione a NOW()
    if not db.restituisci_prestito(mysql, data_inizio, cf, idl):
        flash("Sanzione da applicare per la tarda consegna del libro")
    return redirect(url_for('prestiti'))

@app.route('/users')
def users():
    key = request.args.get('key', '')
    genere = request.args.get('genere', '')
    ordina = request.args.get('ordina', '')  # "titolo" o "autore"

    # Recupera libri in base al genere e titolo o all'ISBN
    libri = db.getLibriPerKey(mysql, key, genere)
    numero_libri = db.getStatisticheGenere(mysql, genere)



    # Ordina i libri se richiesto (titolo o autore)
    if ordina == "titolo":
        libri = db.ordinaLibri(libri, tipo=True)  # Ordinamento per titolo
    elif ordina == "autore":
        libri = db.ordinaLibri(libri, tipo=False)  # Ordinamento per autore

    return render_template('users.html', libri=libri, numero_libri=numero_libri, genere_selezionato=genere, key_selezionata =key, ordina=ordina)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        cf=request.form['CF']
        if db.registraUtente(mysql, request.form['nome'], request.form['cognome'], cf, request.form['email'], request.form['telefono'], username, bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())):
            session['user'] = username
            flash(f"Successfully registered username - {session['user']}.")
            session['isAdmin'] = False
        else:
            flash(f"L'utente con codice fiscale: {cf} è già registrato.")
            return redirect(url_for("register"))
        return redirect(url_for("home"))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def logIn():
    if request.method=="POST":
        username=request.form['username']
        risultato=db.getHashedPw(mysql, username)
        if risultato==0: flash(f"L'username {username} non esiste")
        elif risultato==2: 
            flash(f"La tessera è scaduta, rivolgersi al bibliotecario per rinnovarla")
        else:
            if bcrypt.checkpw(request.form['password'].encode('utf-8'), risultato.encode('utf-8')):
                session['user']=username
                flash(f"Log in avvenuto con successo, bentornato {username}")
                if db.isAdmin(mysql, username):
                    session['isAdmin']=True
                else:
                    session['isAdmin']=False
                return redirect(url_for("home"))
            else:
                flash(f"password errata")
                return redirect(url_for("logIn"))

    return render_template('login.html')

@app.route('/logout')
def logOut():
    session.clear()  # Rimuove tutte le chiavi dalla sessione
    flash("Log out effettuato con successo")
    response = redirect(url_for('home'))
    response.set_cookie('session', '', expires=0)  # Invalida il cookie di sessione
    return response


if __name__ == '__main__':
    app.run(debug=True, port=6969)
