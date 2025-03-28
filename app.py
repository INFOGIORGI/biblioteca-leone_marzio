from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from datetime import timedelta
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
    libri = db.getLibri(mysql, '')
    return render_template('index.html', libri=libri)

@app.route('/librarian', methods=['GET', 'POST'])
def librarian():
    if request.method == 'POST':
        ISBN = request.form['ISBN']
        titolo = request.form['titolo']
        categoria = request.form['categoria']
        autori = request.form['autori']
        x = request.form['x']
        y = request.form['y']
        z = request.form['z']
        ritorno=db.addLibro(mysql, ISBN, titolo, categoria,autori, x, y, z)
        if ritorno==0:
            flash("Esiste già un libro in questa posizione")
            return redirect(url_for('librarian'))
        elif ritorno==2:
            flash("il libro è stato memorizzato per la prima volta")
        
        return redirect(url_for('librarian'))
    
    return render_template('librarian.html')

@app.route('/users')
def users():
    genere = request.args.get('genere', '')
    ordina = request.args.get('ordina', '')  # "titolo" o "autore"

    # Recupera libri in base al genere
    if genere:
        libri = db.getLibriPerGenere(mysql, genere)
        numero_libri = db.getStatisticheGenere(mysql, genere)
    else:
        libri = db.getLibri(mysql, "")
        numero_libri = None

    # Ordina i libri se richiesto (titolo o autore)
    if ordina == "titolo":
        libri = db.ordinaLibri(libri, tipo=True)  # Ordinamento per titolo
    elif ordina == "autore":
        libri = db.ordinaLibri(libri, tipo=False)  # Ordinamento per autore

    return render_template('users.html', libri=libri, numero_libri=numero_libri, genere_selezionato=genere, ordina=ordina)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        cf=request.form['CF']
        if db.registraUtente(mysql, request.form['nome'], request.form['cognome'], cf, request.form['email'], request.form['telefono'], username, bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())):
            session['user'] = username
            session['message'] = f"Successfully registered username - {session['user']}."
            session['isAdmin'] = False
        else:
            session['message']=f"L'utente con codice fiscale: {cf} è già registrato."
            return redirect(url_for("register"))
        return redirect(url_for("home"))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def logIn():
    if request.method=="POST":
        username=request.form['username']
        risultato=db.getHashedPw(mysql, username)
        if risultato==0: session["message"]=f"L'username {username} non esiste"
        elif risultato==2: 
            session["message"]=f"La tessera è scaduta, rivolgersi al bibliotecario per rinnovarla"
        else:
            if bcrypt.checkpw(request.form['password'].encode('utf-8'), risultato.encode('utf-8')):
                session['user']=username
                session['message']=f"Log in avvenuto con successo, bentornato {username}"
                if db.isAdmin(mysql, username):
                    session['isAdmin']=True
                else:
                    session['isAdmin']=False
                return redirect(url_for("home"))
            else:
                session['message']=f"password errata"
                return redirect(url_for("logIn"))

    return render_template('login.html')

@app.route('/logout')
def logOut():
    if 'user' in session:
        session.pop('user')
        session['message']="Log out effettuato con successo"
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
