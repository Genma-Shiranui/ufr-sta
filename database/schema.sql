CREATE TABLE IF NOT EXISTS departement (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    description TEXT,
    responsable TEXT,
    contact TEXT
);

CREATE TABLE IF NOT EXISTS formation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    niveau TEXT,
    duree TEXT,
    conditions TEXT,
    debouches TEXT,
    departement_id INTEGER,
    FOREIGN KEY (departement_id) REFERENCES departement(id)
);

CREATE TABLE IF NOT EXISTS actualite (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    date TEXT NOT NULL,
    description TEXT,
    photo TEXT
);

CREATE TABLE IF NOT EXISTS activite (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    date TEXT NOT NULL,
    lieu TEXT,
    organisateur TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS album (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    description TEXT,
    date TEXT
);

CREATE TABLE IF NOT EXISTS photo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fichier TEXT NOT NULL,
    album_id INTEGER,
    activite_id INTEGER,
    FOREIGN KEY (album_id) REFERENCES album(id),
    FOREIGN KEY (activite_id) REFERENCES activite(id)
);

CREATE TABLE IF NOT EXISTS enseignant (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    grade TEXT,
    departement_id INTEGER,
    email TEXT,
    recherche TEXT,
    photo TEXT,
    FOREIGN KEY (departement_id) REFERENCES departement(id)
);

CREATE TABLE IF NOT EXISTS contact_message (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    email TEXT NOT NULL,
    sujet TEXT,
    message TEXT,
    date_envoi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

INSERT OR IGNORE INTO admin (id, username, password) VALUES (1, 'admin', 'ufr2026');
