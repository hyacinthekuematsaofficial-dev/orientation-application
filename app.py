@app.route('/resultat')
def resultat():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    orientation = session.get('orientation_result')
    if not orientation:
        conn = sqlite3.connect('orientation.db')
        c = conn.cursor()
        c.execute("""SELECT moyenne_scientifique, moyenne_litteraire, orientation
                     FROM orientations WHERE user_id=? ORDER BY id DESC LIMIT 1""",
                  (session['user_id'],))
        result = c.fetchone()
        conn.close()
        if result:
            orientation = {
                'type': result[2],
                'moyenne_sci': result[0],
                'moyenne_lit': result[1]
            }
        else:
            flash('Remplissez d\'abord le formulaire')
            return redirect(url_for('formulaire_notes'))
    return render_template('resultat.html',
                          orientation=orientation,
                          theme=session.get('theme', 'light'))

@app.route('/admin/dashboard')
@role_required('admin')
def admin_dashboard():
    conn = sqlite3.connect('orientation.db')
    c = conn.cursor()
    c.execute("SELECT id, nom, matricule, age FROM users WHERE role='eleve'")
    eleves = c.fetchall()
    conn.close()
    return render_template('admin_dashboard.html',
                          eleves=eleves,
                          theme=session.get('theme', 'light'))

@app.route('/admin/delete/<int:user_id>')
@role_required('admin')
def delete_user(user_id):
    conn = sqlite3.connect('orientation.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id=?", (user_id,))
    c.execute("DELETE FROM notes WHERE user_id=?", (user_id,))
    c.execute("DELETE FROM orientations WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()
    flash('Utilisateur supprimé')
    return redirect(url_for('admin_dashboard'))

@app.route('/conseiller/dashboard')
@role_required('conseiller')
def conseiller_dashboard():
    conn = sqlite3.connect('orientation.db')
    c = conn.cursor()
    c.execute("""SELECT u.nom, u.matricule, u.age, o.orientation
                 FROM users u
                 LEFT JOIN orientations o ON u.id = o.user_id
                 WHERE u.role='eleve'""")
    eleves = c.fetchall()
    conn.close()
    return render_template('conseiller_dashboard.html',
                          eleves=eleves,
                          theme=session.get('theme', 'light'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Déconnecté')
    return redirect(url_for('index'))

if name == 'main':
    app.run(debug=True)
