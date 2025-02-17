from flask import Flask,render_template
from flask_mysqldb import MySQL
from db import DB #importo la classe DB

app = Flask(__name__)
db = DB() #creo un oggetto della classe DB con il costruttore che crea le tabelle se già non esistono


    app = Flask(__name__)
    app.config['MYSQL_HOST']="138.41.20.102"
    app.config['MYSQL_PORT']=53306
    app.config['MYSQL_USER']="ospite"
    app.config['MYSQL_PASSWORD']="ospite"
    app.config['MYSQL_DB']="leone_marzio"
    mysql= MySQL(app)

@app.route("/")
def hello():
    db = DB() #creo un oggetto della classe db con il costruttore che crea le tabelle se già non esistono
    return render_template("index.html", message='Ciao mondo!!')




app.run(debug=True)
