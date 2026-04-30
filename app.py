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
        
        return redirect(url_for('resultat'))
    
    return render_template('formulaire.html')

@app.route('/resultat')
def resultat():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if 'orientation' in session:
        return render_template('resultat.html', 
                              orientation=session['orientation'],
                              moy_sci=session['moy_sci'],
                              moy_lit=session['moy_lit'])
    else:
        return redirect(url_for('formulaire'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if name == 'main':
    app.run(host='0.0.0.0', port=10000, debug=False)
