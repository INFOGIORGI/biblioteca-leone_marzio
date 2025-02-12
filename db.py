from flask import Flask,render_template
from flask_mysqldb import MySQL
class DB:

    def __init__(self): #costruttore della classe DB
        query='''
        CREATE TABLE IF NOT EXISTS Autori(
        ISNI CHAR(16) PRIMARY KEY,
        Nome VARCHAR(32) NOT NULL,
        Cognome VARCHAR(32) NOT NULL,
        DataNascita DATE NOT NULL,
        DataMorte DATE
    );

    CREATE TABLE IF NOT EXISTS  Libri(
        ISBN CHAR(13) PRIMARY KEY,
        Titolo VARCHAR(32) NOT NULL,
        Categoria VARCHAR(32) NOT NULL,
        NumCopie INT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS  Autorato(
        ISNI CHAR(16) NOT NULL,
        ISBN CHAR(13) NOT NULL,

        PRIMARY KEY(ISNI, ISBN),
        FOREIGN KEY (ISNI) REFERENCES Autori(ISNI),
        FOREIGN KEY (ISBN) REFERENCES Libri(ISBN)
    );

    CREATE TABLE IF NOT EXISTS  Utenti(
        CF CHAR(16) PRIMARY KEY,
        Nome VARCHAR(32) NOT NULL,
        Cognome VARCHAR(32) NOT NULL,
        Email VARCHAR(32) NOT NULL,
        Telefono VARCHAR(16) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS  Inventario(
        IDL INT NOT NULL AUTO_INCREMENT,
        ISBN CHAR(13) NOT NULL,
        X INT NOT NULL,
        Y INT NOT NULL,
        Z INT NOT NULL,

        PRIMARY KEY (IDL),
        FOREIGN KEY (ISBN) REFERENCES Libri(ISBN)
    );

    CREATE TABLE IF NOT EXISTS  Prestiti(
        DataInizio DATE NOT NULL,
        DataRestituzione DATE,
        DataScadenza DATE NOT NULL,
        CF CHAR(16) NOT NULL,
        IDL INT NOT NULL,

        PRIMARY KEY (DataInizio, CF, IDL),
        FOREIGN KEY (CF) REFERENCES Utenti (CF),
        FOREIGN KEY (IDL) REFERENCES Inventario(IDL)
    );

    CREATE TABLE IF NOT EXISTS  Tessera(
        CF CHAR(16) PRIMARY KEY,
        Nprestiti INT NOT NULL,
        DataScadenza DATE NOT NULL,
        username VARCHAR(32) NOT NULL,
        Pwd VARCHAR(32) NOT NULL,
        IsAdmin TINYINT(1) NOT NULL,

        FOREIGN KEY (CF) REFERENCES Utenti(CF)
    );'''
        cursor=mysql.connection.cursor()
        cursor.execute(query)

        app = Flask(__name__)
        app.config['MYSQL_HOST']="138.41.20.102"
        app.config['MYSQL_PORT']=53306
        app.config['MYSQL_USER']="ospite"
        app.config['MYSQL_PASSWORD']="ospite"
        app.config['MYSQL_DB']="leone_marzio"
        mysql= MySQL(app)


        def getUtenti():
            query="SELECT * FROM UTENTI"
            cursor=mysql.connection.cursor()
            cursor.execute(query)
            return cursor.fetchall()