from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'ma_cle_secrete_123456'

# ==================== BASE DE DONNÉES ====================

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
            password TEXT,
            theme TEXT DEFAULT 'light'
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

# ==================== MÉTIERS (AVEC PHOTOS) ====================

METIERS_SCIENTIFIQUE = [
    {"nom": "Médecin", "salaire": "3 000 - 8 000 €", "description": "Diagnostique et traite les maladies. Études: 9-12 ans.", "image": "https://cdn.pixabay.com/photo/2020/10/15/14/32/doctor-5657994_640.jpg"},
    {"nom": "Ingénieur Informatique", "salaire": "2 800 - 6 000 €", "description": "Conçoit des logiciels et systèmes informatiques.", "image": "https://cdn.pixabay.com/photo/2016/11/19/14/00/code-1839406_640.jpg"},
    {"nom": "Architecte", "salaire": "2 500 - 7 000 €", "description": "Conçoit des bâtiments et supervise les travaux.", "image": "https://cdn.pixabay.com/photo/2016/11/18/17/46/architect-1836070_640.jpg"},
    {"nom": "Pharmacien", "salaire": "2 500 - 6 000 €", "description": "Prépare et délivre des médicaments.", "image": "https://cdn.pixabay.com/photo/2016/11/29/06/58/pharmacist-1868190_640.jpg"},
    {"nom": "Vétérinaire", "salaire": "2 200 - 5 000 €", "description": "Soigne les animaux.", "image": "https://cdn.pixabay.com/photo/2018/10/01/17/25/veterinarian-3716775_640.jpg"},
    {"nom": "Chercheur", "salaire": "2 200 - 5 000 €", "description": "Mène des expériences scientifiques.", "image": "https://cdn.pixabay.com/photo/2016/02/19/11/19/laboratory-1210472_640.jpg"}
]

METIERS_LITTERAIRE = [
    {"nom": "Avocat", "salaire": "3 000 - 10 000 €", "description": "Défend des clients devant la justice.", "image": "https://cdn.pixabay.com/photo/2017/09/01/20/23/lawyer-2704888_640.jpg"},
    {"nom": "Journaliste", "salaire": "1 800 - 4 500 €", "description": "Recherche et rédige des articles d'actualité.", "image": "https://cdn.pixabay.com/photo/2015/11/19/21/10/glasses-1052010_640.jpg"},
    {"nom": "Enseignant", "salaire": "2 000 - 3 500 €", "description": "Transmet des connaissances aux élèves.", "image": "https://cdn.pixabay.com/photo/2015/01/20/13/13/teacher-605689_640.jpg"},
    {"nom": "Psychologue", "salaire": "2 200 - 5 000 €", "description": "Aide les personnes en difficulté psychologique.", "image": "https://cdn.pixabay.com/photo/2016/11/22/19/08/human-1850195_640.jpg"},
    {"nom": "Écrivain", "salaire": "Variable", "description": "Écrit des livres, romans ou scénarios.", "image": "https://cdn.pixabay.com/photo/2016/03/23/04/01/antique-1274056_640.jpg"},
    {"nom": "Traducteur", "salaire": "2 000 - 4 500 €", "description": "Traduit des textes d'une langue à une autre.", "image": "https://cdn.pixabay.com/photo/2014/09/17/20/26/language-449383_640.jpg"}
]

def calcul_orientation(maths, physique, svt, anglais, francais, histoire, education, geo):
    moy_sci = (maths * 3 + physique * 3 + svt * 2) / 8
    moy_lit = (anglais * 2 + francais * 2 + histoire * 2 + education * 2 + geo * 2) / 10
    if moy_sci >= moy_lit:
        return moy_sci, moy_lit, "Scientifique", METIERS_SCIENTIFIQUE
    else:
        return moy_sci, moy_lit, "Litteraire", METIERS_LITTERAIRE

init_db()

# ==================== PAGES ====================

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Orientation Scolaire</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea, #764ba2); text-align: center; padding: 50px; color: white; min-height: 100vh; }
            .container { max-width: 500px; margin: 0 auto; background: rgba(255,255,255,0.1); border-radius: 20px; padding: 40px; backdrop-filter: blur(10px); }
            h1 { font-size: 2.5em; margin-bottom: 20px; }
            p { margin-bottom: 30px; font-size: 1.2em; }
            .btn { display: inline-block; background: white; color: #764ba2; padding: 12px 30px; margin: 10px; border-radius: 30px; text-decoration: none; font-weight: bold; transition: transform 0.3s; }
            .btn:hover { transform: scale(1.05); }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎓 Orientation Scolaire</h1>
            <p>Aide les élèves de 3ème à choisir leur voie professionnelle</p>
            <a href="/inscription" class="btn">📝 S'inscrire</a>
            <a href="/login" class="btn">🔐 Se connecter</a>
        </div>
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
            return '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Inscription réussie</title>
                <style>
                    body { font-family: Arial; background: linear-gradient(135deg, #667eea, #764ba2); text-align: center; padding: 50px; color: white; }
                    .card { background: white; color: #333; max-width: 400px; margin: auto; padding: 40px; border-radius: 20px; }
                    .btn { background: #764ba2; color: white; padding: 10px 20px; border-radius: 30px; text-decoration: none; display: inline-block; margin-top: 20px; }
                </style>
                <meta http-equiv="refresh" content="2;url=/login">
            </head>
            <body>
                <div class="card">
                    <h2>✅ Inscription réussie !</h2>
                    <p>Redirection automatique vers la page de connexion...</p>
                    <a href="/login" class="btn">Cliquez ici si pas redirigé</a>
                </div>
            </body>
            </html>
            '''
        except:
            return '<h2>❌ Ce matricule existe déjà</h2><a href="/inscription">Réessayer</a>'
        finally:
            conn.close()
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Inscription</title>
        <style>
            body { font-family: Arial; background: linear-gradient(135deg, #667eea, #764ba2); padding: 50px; }
            .card { max-width: 450px; margin: auto; background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
            h2 { text-align: center; color: #764ba2; margin-bottom: 20px; }
            input, select { width: 100%; padding: 12px; margin: 8px 0 20px 0; border-radius: 10px; border: 1px solid #ddd; }
            .btn { background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 12px; border: none; border-radius: 30px; width: 100%; cursor: pointer; font-size: 16px; }
            label { font-weight: bold; color: #555; }
            .link { text-align: center; margin-top: 20px; }
            a { color: #667eea; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>📝 Créer un compte</h2>
            <form method="POST">
                <label>Nom complet :</label>
                <input type="text" name="nom" required>
                <label>Matricule :</label>
                <input type="text" name="matricule" required placeholder="Ex: 2024-001">
                <label>Âge :</label>
                <input type="number" name="age" required>
                <label>Rôle :</label>
                <select name="role">
                    <option value="eleve">📚 Élève</option>
                    <option value="conseiller">🎓 Conseiller</option>
                    <option value="admin">👑 Administrateur</option>
                </select>
                <label>Mot de passe :</label>
                <input type="password" name="password" required>
                <button type="submit" class="btn">S'inscrire</button>
            </form>
            <div class="link"><a href="/login">Déjà inscrit ? Se connecter</a></div>
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
            return '<h2>❌ Matricule ou mot de passe incorrect</h2><a href="/login">Réessayer</a>'
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Connexion</title>
        <style>
            body { font-family: Arial; background: linear-gradient(135deg, #667eea, #764ba2); padding: 50px; }
            .card { max-width: 450px; margin: auto; background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
            h2 { text-align: center; color: #764ba2; margin-bottom: 20px; }
            input { width: 100%; padding: 12px; margin: 8px 0 20px 0; border-radius: 10px; border: 1px solid #ddd; }
            .btn { background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 12px; border: none; border-radius: 30px; width: 100%; cursor: pointer; font-size: 16px; }
            label { font-weight: bold; color: #555; }
            .link { text-align: center; margin-top: 20px; }
            a { color: #667eea; text-decoration: none; }
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
            <div class="link"><a href="/inscription">Pas de compte ? S'inscrire</a></div>
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
                body {{ font-family: Arial; background: linear-gradient(135deg, #667eea, #764ba2); text-align: center; padding: 50px; color: white; min-height: 100vh; }}
                .container {{ max-width: 600px; margin: 0 auto; background: rgba(255,255,255,0.1); border-radius: 20px; padding: 40px; backdrop-filter: blur(10px); }}
                h1 {{ margin-bottom: 10px; }}
                .btn {{ display: inline-block; background: white; color: #764ba2; padding: 15px 35px; margin: 15px; border-radius: 40px; text-decoration: none; font-weight: bold; font-size: 16px; transition: transform 0.3s; }}
                .btn:hover {{ transform: scale(1.05); }}
                .logout {{ background: rgba(255,255,255,0.2); color: white; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Bonjour {nom} !</h1>
                <p>Bienvenue sur votre espace élève</p>
                <a href="/formulaire" class="btn">📝 Remplir mes notes</a>
                <a href="/logout" class="btn logout">🚪 Déconnexion</a>
            </div>
        </body>
        </html>
        '''
    else:
        return f'<h1>Bonjour {nom} (Rôle: {role})</h1><a href="/logout">Déconnexion</a>'

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
        
        moy_sci, moy_lit, orientation, metiers = calcul_orientation(maths, physique, svt, anglais, francais, histoire, education, geo)
        
        conn = sqlite3.connect('orientation.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO orientations (user_id, moyenne_sci, moyenne_lit, orientation, date_orientation)
            VALUES (?,?,?,?,?)
        ''', (session['user_id'], moy_sci, moy_lit, orientation, str(datetime.now())))
        conn.commit()
        conn.close()
        
        # Stocker les résultats en session pour le popup
        session['resultat_popup'] = {
            'moy_sci': moy_sci,
            'moy_lit': moy_lit,
            'orientation': orientation,
            'metiers': metiers
        }
        
        return redirect('/dashboard#popup')
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Formulaire de notes</title>
        <style>
            body { font-family: Arial; background: linear-gradient(135deg, #667eea, #764ba2); padding: 20px; min-height: 100vh; }
            .card { max-width: 900px; margin: 30px auto; background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
            h2 { text-align: center; color: #764ba2; margin-bottom: 20px; }
            input { width: 100%; padding: 10px; margin: 5px 0 15px 0; border-radius: 10px; border: 1px solid #ddd; }
            .btn { background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 12px; border: none; border-radius: 30px; width: 100%; cursor: pointer; font-size: 16px; font-weight: bold; }
            .row { display: flex; gap: 30px; flex-wrap: wrap; }
            .col { flex: 1; min-width: 250px; }
            label { font-weight: bold; color: #555; }
            h3 { color: #667eea; margin-bottom: 15px; border-bottom: 2px solid #667eea; display: inline-block; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>📝 Entrez vos notes (sur 20)</h2>
            <form method="POST">
                <div class="row">
                    <div class="col">
                        <h3>🔬 Matières scientifiques</h3>
                        <label>Mathématiques (x3) :</label>
                        <input type="number" step="0.5" name="maths" required>
                        <label>Physique-Chimie (x3) :</label>
                        <input type="number" step="0.5" name="physique" required>
                        <label>SVT (x2) :</label>
                        <input type="number" step="0.5" name="svt" required>
                    </div>
                    <div class="col">
                        <h3>📚 Matières littéraires</h3>
                        <label>Anglais (x2) :</label>
                        <input type="number" step="0.5" name="anglais" required>
                        <label>Français (x2) :</label>
                        <input type="number" step="0.5" name="francais" required>
                        <label>Histoire (x2) :</label>
                        <input type="number" step="0.5" name="histoire" required>
                        <label>Éducation civique (x2) :</label>
                        <input type="number" step="0.5" name="education" required>
                        <label>Géographie (x2) :</label>
                        <input type="number" step="0.5" name="geo" required>
                    </div>
                </div>
                <button type="submit" class="btn">🎯 Calculer mon orientation</button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/dashboard_with_popup')
def dashboard_with_popup():
    if 'user_id' not in session:
        return redirect('/login')
    
    resultat = session.pop('resultat_popup', None)
    nom = session['nom']
    
    if resultat:
        moy_sci = resultat['moy_sci']
        moy_lit = resultat['moy_lit']
        orientation = resultat['orientation']
        metiers = resultat['metiers']
        
        if orientation == "Scientifique":
            couleur = "#667eea"
            emoji = "🔬"
            titre = "Série Scientifique"
        else:
            couleur = "#f093fb"
            emoji = "📚"
            titre = "Série Littéraire"
        
        # Générer HTML des métiers
        metiers_html = ""
        for m in metiers:
            metiers_html += f'''
            <div style="background: white; border-radius: 15px; padding: 15px; text-align: center; cursor: pointer;" onclick="alert('{m["nom"]}\\n\\n{m["description"]}\\n\\n💰 Salaire: {m["salaire"]}')">
                <img src="{m["image"]}" style="width: 80px; height: 80px; border-radius: 50%; object-fit: cover; margin-bottom: 10px;" onerror="this.src='https://via.placeholder.com/80'">
                <h4 style="margin: 5px 0;">{m["nom"]}</h4>
                <p style="color: #666; font-size: 12px;">💰 {m["salaire"]}</p>
                <p style="color: #999; font-size: 11px;">👆 Cliquez pour détails</p>
            </div>
            '''
        
        popup_html = f'''
        <div id="resultatPopup" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 1000; display: flex; align-items: center; justify-content: center;">
            <div style="background: white; max-width: 600px; width: 90%; max-height: 85%; overflow-y: auto; border-radius: 20px; padding: 25px; text-align: center; position: relative; animation: fadeIn 0.5s;">
                <button onclick="closePopup()" style="position: absolute; top: 15px; right: 20px; background: none; border: none; font-size: 28px; cursor: pointer;">&times;</button>
                <div style="background: {couleur}; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
                    <h1 style="font-size: 48px; margin: 0;">{emoji}</h1>
                    <h2 style="color: white; margin: 10px 0;">{titre}</h2>
                    <p style="color: white;">Félicitations {nom} !</p>
                </div>
                <div style="display: flex; gap: 20px; margin-bottom: 20px;">
                    <div style="flex:1; background: #f0f0f0; padding: 10px; border-radius: 10px;">
                        <h4>📊 Moyenne Scientifique</h4>
                        <p style="font-size: 24px; color: #667eea;">{moy_sci:.2f}/20</p>
                    </div>
                    <div style="flex:1; background: #f0f0f0; padding: 10px; border-radius: 10px;">
                        <h4>📚 Moyenne Littéraire</h4>
                        <p style="font-size: 24px; color: #667eea;">{moy_lit:.2f}/20</p>
                    </div>
                </div>
                <h3 style="color: #764ba2;">💼 Métiers possibles</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 15px; margin-top: 15px;">
                    {metiers_html}
                </div>
                <button onclick="closePopup()" style="background: #764ba2; color: white; padding: 10px 25px; border: none; border-radius: 30px; margin-top: 20px; cursor: pointer;">Fermer</button>
            </div>
        </div>
        <style>
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: scale(0.9); }}
                to {{ opacity: 1; transform: scale(1); }}
            }}
        </style>
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1"></script>
        <script>
            function closePopup() {{
                document.getElementById('resultatPopup').style.display = 'none';
                window.location.hash = '';
            }}
            canvasConfetti({{ particleCount: 200, spread: 70, origin: {{ y: 0.6 }} }});
            setTimeout(() => canvasConfetti({{ particleCount: 150, spread: 100 }}), 500);
            setTimeout(() => canvasConfetti({{ particleCount: 300, spread: 120, origin: {{ y: 0.5 }} }}), 1000);
            window.onclick = function(event) {{
                if (event.target == document.getElementById('resultatPopup')) {{
                    closePopup();
                }}
            }}
        </script>
        '''
        
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Résultat</title>
            <meta http-equiv="refresh" content="0;url=/dashboard">
        </head>
        <body>
            {popup_html}
        </body>
        </html>
        '''
    
    return redirect('/dashboard')

# Rediriger /dashboard vers la version avec popup si résultat présent
@app.route('/dashboard_redirect')
def dashboard_redirect():
    if 'resultat_popup' in session:
        return redirect('/dashboard_with_popup')
    return redirect('/dashboard')

# Remplacer la route dashboard par une redirection conditionnelle
# Note: Pour que le popup fonctionne, après soumission du formulaire on va directement vers /dashboard_with_popup

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
