import sqlite3
from werkzeug.security import generate_password_hash
from config import Config

class User:
    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username
        self.password = password
        self.email = email

    @classmethod
    def get(cls, username=None, email=None):
        koneksi = sqlite3.connect(Config.DATABASE)
        interaksi = koneksi.cursor()
        if username and email:
            interaksi.execute("SELECT * FROM users WHERE username=? AND email=?", (username, email))
        elif username:
            interaksi.execute("SELECT * FROM users WHERE username=?", (username,))
        elif email:
            interaksi.execute("SELECT * FROM users WHERE email=?", (email,))
        else:
            return None
        row = interaksi.fetchone()
        if row:
            return cls(*row)
        return None
    

    @classmethod
    def create(cls, username, password, email):
        koneksi = sqlite3.connect(Config.DATABASE)
        interaksi = koneksi.cursor()
        hashed_password = generate_password_hash(password)
        interaksi.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, hashed_password, email))
        koneksi.commit()
        koneksi.close()

class Admin:
    def __init__(self, id, username, password, email,):
        self.id = id
        self.username = username
        self.password = password
        self.email = email


    @classmethod
    def getadmin(cls, username=None, email=None):
        koneksi = sqlite3.connect(Config.DATABASE)
        interaksi = koneksi.cursor()
        if username and email:
            interaksi.execute("SELECT * FROM admin WHERE username=? AND email=?", (username, email))
        elif username:
            interaksi.execute("SELECT * FROM admin WHERE username=?", (username,))
        elif email:
            interaksi.execute("SELECT * FROM admin WHERE email=?", (email,))
        else:
            return None
        row = interaksi.fetchone()
        if row:
            return cls(*row)
        return None
    

    @classmethod
    def create(cls, username, password, email):
        koneksi = sqlite3.connect(Config.DATABASE)
        interaksi = koneksi.cursor()
        hashed_password = generate_password_hash(password)
        interaksi.execute("INSERT INTO admin (username, password, email) VALUES (?, ?, ?)", (username, hashed_password, email))
        koneksi.commit()
        koneksi.close()

def create_tables():
    koneksi = sqlite3.connect(Config.DATABASE)
    interaksi = koneksi.cursor()
    interaksi.execute("""CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT,
                email TEXT
                )""")
    koneksi.commit()
    koneksi.close()

def create_tables():
    koneksi = sqlite3.connect(Config.DATABASE)
    interaksi = koneksi.cursor()
    interaksi.execute("""CREATE TABLE IF NOT EXISTS admin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT,
                email TEXT
                )""")
    koneksi.commit()
    koneksi.close()