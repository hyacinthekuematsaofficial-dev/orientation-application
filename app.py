from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'ma_cle_secrete_123456'

def init_db():
    conn = sqlite3.connect('orientation.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            matricule TEXT UNIQUE,
            age INTEGER,
            role TEXT,
            password TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS orientations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            moyenne_sci REAL,
            moyenne_lit REAL,
            orientation TEXT,
            date_orientation TEXT
        )
    ''')
    conn.commit()
    conn.close()

def calcul_orientation(maths, physique, svt, anglais, francais, histoire, education, geo):
    moy_sci = (maths * 3 + physique * 3 + svt * 2) / 8
    moy_lit = (anglais * 2 + francais * 2 + histoire * 2 + education * 2 + geo * 2) / 10
    if moy_sci >= moy_lit:
        return moy_sci, moy_lit, "Scientifique"
    else:
        return moy_sci, moy_lit, "Litteraire"

init_db()

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Orientation Scolaire</title>
        <style>
            body { font-family: Arial; background: linear-gradient(135deg, #667eea, #764ba2); text-align: center; padding: 50px; color: white; }
            .btn { background: white; color: #764ba2; padding: 10px 20px; margin: 10px; border-radius: 5px; text-decoration: none; display: inline-block; }
        </style>
    </head>
    <body>
        <h1>🎓 Orientation Scolaire</h1>
        <p>Aide les eleves de 3eme a choisir leur voie</p>
        <a href="/inscription" class="btn">📝 S'inscrire</a>
        <a href="/login" class="btn">🔐 Se connecter</a>
    </body>
    </html>
    '''

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
            c.execute("INSERT INTO users (nom, matricule, age, role, password) VALUES (?,?,?,?,?)",
                     (nom, matricule, age, role, password))
            conn.commit()
            return '<h2>✅ Inscription reussie !</h2><a href="/login">Se connecter</a>'
        except:
            return '<h2>❌ Ce matricule existe deja</h2><a href="/inscription">Reessayer</a>'
        finally:
            conn.close()
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Inscription</title>
        <style>
            body { font-family: Arial; background: linear-gradient(135deg, #667eea, #764ba2); padding: 50px; }
            .card { max-width: 400px; margin: auto; background: white; padding: 30px; border-radius: 10px; }
            input, select { width: 100%; padding: 8px; margin: 5px 0 15px 0; border-radius: 5px; border: 1px solid #ddd; }
            .btn { background: #764ba2; color: white; padding: 10px; border: none; border-radius: 5px; width: 100%; cursor: pointer; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>📝 Inscription</h2>
            <form method="POST">
                <label>Nom :</label>
                <input type="text" name="nom" required>
                <label>Matricule :</label>
                <input type="text" name="matricule" required>
                <label>Age :</label>
                <input type="number" name="age" required>
                 <label>Role :</label>
                <select name="role">
                    <option value="eleve">Eleve</option>
                    <option value="conseiller">Conseiller</option>
                    <option value="admin">Administrateur</option>
                </select>
                <label>Mot de passe :</label>
                <input type="password" name="password" required>
                <button type="submit" class="btn">S'inscrire</button>
            </form>
            <p><a href="/login">Deja inscrit ? Se connecter</a></p>
        </div>
    </body>
    </html>
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
            return redirect('/dashboard')
        else:
            return '<h2>❌ Matricule ou mot de passe incorrect</h2><a href="/login">Reessayer</a>'
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Connexion</title>
        <style>
            body { font-family: Arial; background: linear-gradient(135deg, #667eea, #764ba2); padding: 50px; }
            .card { max-width: 400px; margin: auto; background: white; padding: 30px; border-radius: 10px; }
            input { width: 100%; padding: 8px; margin: 5px 0 15px 0; border-radius: 5px; border: 1px solid #ddd; }
            .btn { background: #764ba2; color: white; padding: 10px; border: none; border-radius: 5px; width: 100%; cursor: pointer; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>🔐 Connexion</h2>
            <form method="POST">
                <label>Matricule :</label>
                <input type="text" name="matricule" required>
                <label>Mot de passe :</label>
                <input type="password" name="password" required>
                <button type="submit" class="btn">Se connecter</button>
            </form>
            <p><a href="/inscription">Pas de compte ? S'inscrire</a></p>
        </div>
    </body>
    </html>
    '''

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    
    nom = session['nom']
    role = session['role']
    
    if role == 'eleve':
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Tableau de bord</title>
            <style>
                body {{ font-family: Arial; background: linear-gradient(135deg, #667eea, #764ba2); text-align: center; padding: 50px; color: white; }}
                .btn {{ background: white; color: #764ba2; padding: 15px 30px; margin: 10px; border-radius: 5px; text-decoration: none; display: inline-block; }}
            </style>
        </head>
        <body>
            <h1>📊 Bonjour {nom} !</h1>
            <p>Bienvenue sur votre espace eleve</p>
            <a href="/formulaire" class="btn">📝 Remplir mes notes</a>
            <a href="/resultat" class="btn">🎉 Voir mon resultat</a>
            <a href="/logout" class="btn">🚪 Deconnexion</a>
        </body>
        </html>
        '''
    else:
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Tableau de bord</title>
            <style>
                body {{ font-family: Arial; background: linear-gradient(135deg, #667eea, #764ba2); text-align: center; padding: 50px; color: white;  }}
                .btn {{ background: white; color: #764ba2; padding: 15px 30px; margin: 10px; border-radius: 5px; text-decoration: none; display: inline-block; }}
            </style>
        </head>
        <body>
            <h1>👑 Bonjour {nom} ({role})</h1>
            <a href="/logout" class="btn">Deconnexion</a>
        </body>
        </html>
        '''

@app.route('/formulaire', methods=['GET', 'POST'])
def formulaire():
    if 'user_id' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        maths = float(request.form['maths'])
        physique = float(request.form['physique'])
        svt = float(request.form['svt'])
        anglais = float(request.form['anglais'])
        francais = float(request.form['francais'])
        histoire = float(request.form['histoire'])
        education = float(request.form['education'])
        geo = float(request.form['geo'])
        
        moy_sci, moy_lit, orientation = calcul_orientation(maths, physique, svt, anglais, francais, histoire, education, geo)
        
        conn = sqlite3.connect('orientation.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO orientations (user_id, moyenne_sci, moyenne_lit, orientation, date_orientation)
            VALUES (?,?,?,?,?)
        ''', (session['user_id'], moy_sci, moy_lit, orientation, str(datetime.now())))
        conn.commit()
        conn.close()
        
        session['moy_sci'] = moy_sci
        session['moy_lit'] = moy_lit
        session['orientation'] = orientation
        
        return redirect('/resultat')
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Formulaire de notes</title>
        <style>
            body { font-family: Arial; background: linear-gradient(135deg, #667eea, #764ba2); padding: 20px; }
            .card { max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 10px; }
            input { width: 100%; padding: 8px; margin: 5px 0 15px 0; border-radius: 5px; border: 1px solid #ddd; }
            .btn { background: #764ba2; color: white; padding: 10px; border: none; border-radius: 5px; width: 100%; cursor: pointer; }
            .row { display: flex; gap: 20px; }
            .col { flex: 1; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>📝 Entrez vos notes (sur 20)</h2>
            <form method="POST">
                <div class="row">
                    <div class="col">
                        <h3>🔬 Matieres scientifiques</h3>
                        <label>Mathematiques (x3) :</label>
                        <input type="number" step="0.5" name="maths" required>
                        <label>Physique-Chimie (x3) :</label>
                        <input type="number" step="0.5" name="physique" required>
                        <label>SVT (x2) :</label>
                        <input type="number" step="0.5" name="svt" required>
                    </div>
                    <div class="col">
                        <h3>📚 Matieres litteraires</h3>
                        <label>Anglais (x2) :</label>
                        <input type="number" step="0.5" name="anglais" required>
                        <label>Francais (x2) :</label>
                        <input type="number" step="0.5" name="francais" required>
                        <label>Histoire (x2) :</label>
                        <input type="number" step="0.5" name="histoire" required>
                        <label>Education civique (x2) :</label>
                        <input type="number" step="0.5" name="education" required>
                        <label>Geographie (x2) :</label>
                        <input type="number" step="0.5" name="geo" required>
                    </div>
                </div>
                <button type="submit" class="btn">🎯 Calculer mon orientation</button>
            </form>
        </div>
    </body>
    </html>
    '''
@app.route('/resultat')
def resultat():
    if 'user_id' not in session:
        return redirect('/login')
    
    if 'orientation' in session:
        moy_sci = session['moy_sci']
        moy_lit = session['moy_lit']
        orientation = session['orientation']
        
        if orientation == "Scientifique":
            couleur = "#667eea"
            emoji = "🔬"
        else:
            couleur = "#f093fb"
            emoji = "📚"
        
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Resultat</title>
            <style>
                body {{ font-family: Arial; background: linear-gradient(135deg, #667eea, #764ba2); text-align: center; padding: 50px; color: white; }}
                .card {{ max-width: 500px; margin: auto; background: white; padding: 30px; border-radius: 20px; color: #333; }}
                .result {{ background: {couleur}; color: white; padding: 30px; border-radius: 15px; margin-bottom: 20px; }}
                .btn {{ background: #764ba2; color: white; padding: 10px 20px; border-radius: 5px; text-decoration: none; display: inline-block; margin-top: 20px; }}
            </style>
            <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1"></script>
        </head>
        <body>
            <div class="card">
                <div class="result">
                    <h1 style="font-size: 48px;">{emoji}</h1>
                    <h1>Serie {orientation}</h1>
                    <p>Felicitations !</p>
                </div>
                <div style="display: flex; gap: 20px;">
                    <div style="flex:1; background: #f0f0f0; padding: 10px; border-radius: 10px;">
                        <h3>📊 Moyenne Scientifique</h3>
                        <p style="font-size: 24px; color: #667eea;">{moy_sci:.2f}/20</p>
                    </div>
                    <div style="flex:1; background: #f0f0f0; padding: 10px; border-radius: 10px;">
                        <h3>📚 Moyenne Litteraire</h3>
                        <p style="font-size: 24px; color: #667eea;">{moy_lit:.2f}/20</p>
                    </div>
                </div>
                <a href="/dashboard" class="btn">← Retour</a>
            </div>
            <script>
                canvasConfetti({{ particleCount: 200, spread: 70, origin: {{ y: 0.6 }} }});
                setTimeout(() => canvasConfetti({{ particleCount: 150, spread: 100 }}), 500);
            </script>
        </body>
        </html>
        '''
    else:
        return redirect('/formulaire')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
