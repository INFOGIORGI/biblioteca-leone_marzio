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
);

-- Tabella Autori
INSERT INTO Autori (ISNI, Nome, Cognome, DataNascita, DataMorte)
VALUES 
('0000000121464392', 'Alessandro', 'Manzoni', '1785-03-07', '1873-05-22'),
('0000000121456321', 'Giovanni', 'Verga', '1840-09-02', '1922-01-27'),
('0000000121459383', 'Italo', 'Calvino', '1923-10-15', '1985-09-19'),
('0000000121452790', 'Umberto', 'Eco', '1932-01-05', '2016-02-19'),
('0000000121467210', 'Gabriele', "D'Annunzio", '1863-03-12', '1938-03-01');

-- Tabella Libri
INSERT INTO Libri (ISBN, Titolo, Categoria, NumCopie)
VALUES 
('9788804498122', 'I Promessi Sposi', 'Romanzo Storico', 10),
('9788804536571', 'Il Nome della Rosa', 'Romanzo Storico', 8),
('9788804671531', 'Il Barone Rampante', 'Narrativa', 5),
('9788804725525', 'Mastro-don Gesualdo', 'Romanzo', 6),
('9788804778472', 'Il Piacere', 'Narrativa', 4);

-- Tabella Autorato
INSERT INTO Autorato (ISNI, ISBN)
VALUES 
('0000000121464392', '9788804498122'),
('0000000121456321', '9788804725525'),
('0000000121459383', '9788804671531'),
('0000000121452790', '9788804536571'),
('0000000121467210', '9788804778472');

-- Tabella Utenti
INSERT INTO Utenti (CF, Nome, Cognome, Email, Telefono)
VALUES 
('RSSMRA85M01H501Z', 'Mario', 'Rossi', 'mario.rossi@example.com', '3281234567'),
('VRDLGI84C10H501L', 'Luigi', 'Verdi', 'luigi.verdi@example.com', '3279876543'),
('BNCLRA80A01H501X', 'Lara', 'Bianchi', 'lara.bianchi@example.com', '3291239876'),
('MNTGPP85L20H501W', 'Giuseppe', 'Monti', 'giuseppe.monti@example.com', '3204567890'),
('CLDMLA88E10H501K', 'Michela', 'Colombo', 'michela.colombo@example.com', '3216549870');

-- Tabella Inventario
INSERT INTO Inventario (ISBN, X, Y, Z)
VALUES 
('9788804498122', 1, 1, 1),
('9788804536571', 1, 1, 2),
('9788804671531', 1, 2, 1),
('9788804725525', 2, 1, 1),
('9788804778472', 2, 2, 1);

-- Tabella Prestiti
INSERT INTO Prestiti (DataInizio, DataRestituzione, DataScadenza, CF, IDL)
VALUES 
('2025-01-10', '2025-01-20', '2025-01-31', 'RSSMRA85M01H501Z', 1),
('2025-02-01', NULL, '2025-02-28', 'VRDLGI84C10H501L', 2),
('2025-02-05', '2025-02-15', '2025-02-28', 'BNCLRA80A01H501X', 3),
('2025-03-01', NULL, '2025-03-31', 'MNTGPP85L20H501W', 4),
('2025-03-10', '2025-03-20', '2025-03-31', 'CLDMLA88E10H501K', 5);

-- Tabella Tessera
INSERT INTO Tessera (CF, Nprestiti, DataScadenza, username, Pwd, IsAdmin)
VALUES 
('RSSMRA85M01H501Z', 5, '2026-12-31', 'mrossi', 'password1', 0),
('VRDLGI84C10H501L', 3, '2026-12-31', 'lverdi', 'password2', 0),
('BNCLRA80A01H501X', 4, '2026-12-31', 'lbianchi', 'password3', 0),
('MNTGPP85L20H501W', 2, '2026-12-31', 'gmonti', 'password4', 0),
('CLDMLA88E10H501K', 6, '2026-12-31', 'mcolombo', 'password5', 1);
