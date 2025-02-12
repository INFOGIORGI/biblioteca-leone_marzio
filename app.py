from flask import Flask,render_template
from db import DB #importo la classe DB

app = Flask(__name__)
db = DB() #creo un oggetto della classe DB con il costruttore che crea le tabelle se già non esistono



@app.route("/")
def hello():
    db = DB() #creo un oggetto della classe db con il costruttore che crea le tabelle se già non esistono
    return render_template("index.html", message='Ciao mondo!!')




app.run(debug=True)
