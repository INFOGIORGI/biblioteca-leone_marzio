from flask import Flask,render_template
from flask_mysqldb import MySQL
import db



app = Flask(__name__)
app.config['MYSQL_HOST']="138.41.20.102"
app.config['MYSQL_PORT']=53306
app.config['MYSQL_USER']="5di"
app.config['MYSQL_PASSWORD']="colazzo"
app.config['MYSQL_DB']="leone_marzio"
mysql= MySQL(app)

@app.route("/")
def hello():
    return render_template("index.html", message='Ciao mondo!!')


# with app.app_context():
#     print(db.getLibri(mysql, "888"))

# dati=((1,), (3,), (2,))
# print(max(dati)[0])

# with app.app_context():
#     db.addLibro(mysql,"0123456789111", "mambita", "soreta", 2,3,6)
#     db.addLibro(mysql,"0123456789111", "mambita", "soreta", 9,0,1)
#     db.addLibro(mysql,"0123456789111", "mambita", "soreta", 5,1,1)

with app.app_context():
    print(db.getLibri(mysql, " "))
    print(db.ordinaLibri(mysql, True))


app.run(debug=True)
