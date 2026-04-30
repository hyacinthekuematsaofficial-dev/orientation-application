@app.route('/resultat')
@role_required('eleve')
def resultat():
    conn = sqlite3.connect('orientation.db')
    c = conn.cursor()
    
    # Récupérer la dernière orientation
    c.execute('''SELECT moyenne_scientifique, moyenne_litteraire, orientation, date_orientation 
                 FROM orientations WHERE user_id = ? ORDER BY date_orientation DESC LIMIT 1''', 
              (session['user_id'],))
    orientation = c.fetchone()
    
    # Récupérer les notes
    c.execute('''SELECT mathematiques, anglais, francais, physique_chimie, svt, 
                        histoire, education_civique, geographie 
                 FROM notes WHERE user_id = ? ORDER BY id DESC LIMIT 1''', 
              (session['user_id'],))
    notes = c.fetchone()
    
    conn.close()
    
    if not orientation or not notes:
        flash('Vous devez d\'abord remplir le formulaire de notes.')
        return redirect(url_for('formulaire_notes'))
    
    matieres = ['Mathématiques', 'Anglais', 'Français', 'Physique-Chimie', 
                'SVT', 'Histoire', 'Éducation civique', 'Géographie']
    
    return render_template('resultat.html', 
                         orientation=orientation, 
                         notes=notes,
                         matieres=matieres)

@app.route('/admin/dashboard')
@role_required('admin')
def admin_dashboard():
    conn = sqlite3.connect('orientation.db')
    c = conn.cursor()
    
    # Récupérer tous les élèves avec leurs orientations
    c.execute('''SELECT u.id, u.nom, u.matricule, u.age, o.orientation, o.date_orientation
                 FROM users u
                 LEFT JOIN orientations o ON u.id = o.user_id
                 WHERE u.role = 'eleve' ''')
    eleves = c.fetchall()
    
    # Statistiques
    c.execute("SELECT COUNT(*) FROM users WHERE role = 'eleve'")
    total_eleves = c.fetchone()[0]
    
    c.execute("SELECT orientation, COUNT(*) FROM orientations GROUP BY orientation")
    stats_orientation = c.fetchall()
    
    conn.close()
    
    return render_template('admin_dashboard.html', 
                         eleves=eleves,
                         total_eleves=total_eleves,
                         stats_orientation=stats_orientation)

@app.route('/admin/delete_user/<int:user_id>')
@role_required('admin')
def delete_user(user_id):
    conn = sqlite3.connect('orientation.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
    c.execute("DELETE FROM notes WHERE user_id = ?", (user_id,))
    c.execute("DELETE FROM orientations WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    
    flash('Utilisateur supprimé avec succès.')
    return redirect(url_for('admin_dashboard'))

@app.route('/conseiller/dashboard')
@role_required('conseiller')
def conseiller_dashboard():
    conn = sqlite3.connect('orientation.db')
    c = conn.cursor()
    
    # Récupérer tous les élèves avec leurs orientations pour consultation
    c.execute('''SELECT u.id, u.nom, u.matricule, u.age, o.orientation, o.moyenne_scientifique, 
                        o.moyenne_litteraire, o.date_orientation
                 FROM users u
                 LEFT JOIN orientations o ON u.id = o.user_id
                 WHERE u.role = 'eleve' ''')
    eleves = c.fetchall()
    
    conn.close()
    
    return render_template('conseiller_dashboard.html', eleves=eleves)

@app.route('/logout')
def logout():
    session.clear()
    flash('Déconnexion réussie.')
    return redirect(url_for('index'))

if name == 'main':
    init_db()
    app.run(debug=True)
