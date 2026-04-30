from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime

app = Flask(name)
app.secret_key = 'votre_cle'

def init_db():
    conn = sqlite3.connect('orientation.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, nom TEXT, matricule TEXT, age INTEGER, role TEXT, password TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS orientations (id INTEGER PRIMARY KEY, user_id INTEGER, moyenne_sci REAL, moyenne_lit REAL, orientation TEXT, date TEXT)')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return '<h1>Bienvenue sur Orientation Scolaire</h1><a href="/inscription">Inscription</a> <a href="/login">Connexion</a>'

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        nom = request.form['nom']
        matricule = request.form['matricule']
        age = request.form['age']
        role = request.form['role']
        password = request.form['password']
        conn = sqlite3.connect('orientation.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (nom, matricule, age, role, password) VALUES (?,?,?,?,?)", (nom, matricule, age, role, password))
            conn.commit()
            return '<h2>Inscription reussie !</h2><a href="/login">Connexion</a>'
        except:
            return '<h2>Erreur</h2><a href="/inscription">Reessayer</a>'
        finally:
            conn.close()
    return '''
    <form method="POST">
        Nom: <input type="text" name="nom" required><br>
        Matricule: <input type="text" name="matricule" required><br>
        Age: <input type="number" name="age" required><br>
        Role: <select name="role"><option value="eleve">Eleve</option><option value="admin">Admin</option></select><br>
        Mot de passe: <input type="password" name="password" required><br>
        <button type="submit">S'inscrire</button>
    </form>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        matricule = request.form['matricule']
        password = request.form['password']
        conn = sqlite3.connect('orientation.db')
        c = conn.cursor()
        c.execute("SELECT id, nom, role FROM users WHERE matricule=? AND password=?", (matricule, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['user_id'] = user[0]
            session['nom'] = user[1]
            session['role'] = user[2]
            return f'<h2>Bienvenue {user[1]} !</h2><a href="/dashboard">Dashboard</a>'
        else:
            return '<h2>Erreur</h2><a href="/login">Reessayer</a>'
    return '<form method="POST">Matricule: <input type="text" name="matricule"><br>Mot de passe: <input type="password" name="password"><br><button type="submit">Connexion</button></form>'

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    return f'<h1>Bonjour {session["nom"]}</h1><a href="/logout">Deconnexion</a>'

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if name == 'main':
    app.run(host='0.0.0.0', port=10000)
