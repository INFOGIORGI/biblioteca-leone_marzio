from flask import Flask, request, render_template, redirect, url_for, session
from flask_mysqldb import MySQL
import db

app = Flask(__name__)
app.config['MYSQL_HOST'] = "138.41.20.102"
app.config['MYSQL_PORT'] = 53306
app.config['MYSQL_USER'] = "5di"
app.config['MYSQL_PASSWORD'] = "colazzo"
app.config['MYSQL_DB'] = "leone_marzio"
mysql = MySQL(app)

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
        x = request.form['x']
        y = request.form['y']
        z = request.form['z']
        db.addLibro(mysql, ISBN, titolo, categoria, x, y, z)
        return redirect(url_for('home'))
    
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
        libri = db.ordinaLibri(mysql, tipo=True)  # Ordinamento per titolo
    elif ordina == "autore":
        libri = db.ordinaLibri(mysql, tipo=False)  # Ordinamento per autore

    return render_template('users.html', libri=libri, numero_libri=numero_libri, genere_selezionato=genere, ordina=ordina)


@app.route('/register')
def register():
    session['message'] = "Enter your username to continue."
    if request.method == 'POST':
        username = request.form['username']
        session['user'] = username
        session['greet'] = f"Successfully registered username - {session['user']}."
        return redirect(url_for("home"))
 
    return render_template('register.html')

@app.route('/login')
def logIn():

    return render_template('login.html')

@app.route('/logout')
def logOut():

    return render_template('logout.html')

if __name__ == '__main__':
    app.run(debug=True)
