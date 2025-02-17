from flask import Flask,render_template
from flask_mysqldb import MySQL
import db

libriPerFila=20
filePerScaffale=6
nScaffali=10

app = Flask(__name__)
app.config['MYSQL_HOST']="138.41.20.102"
app.config['MYSQL_PORT']=53306
app.config['MYSQL_USER']="ospite"
app.config['MYSQL_PASSWORD']="ospite"
app.config['MYSQL_DB']="leone_marzio"
mysql= MySQL(app)

@app.route("/")
def hello():
    return render_template("index.html", message='Ciao mondo!!')


with app.app_context():
    print(db.getLibri(mysql, "il"))



app.run(debug=True)
