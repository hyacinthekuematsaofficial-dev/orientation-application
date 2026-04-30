@app.route('/resultat')
def resultat():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if 'resultat' in session:
        moy_sci, moy_lit, orientation = session['resultat']
        
        if orientation == "Scientifique":
            style = "background: linear-gradient(135deg, #667eea, #764ba2);"
            emoji = "🔬"
        else:
            style = "background: linear-gradient(135deg, #f093fb, #f5576c);"
            emoji = "📚"
        
        return f'''
        <!DOCTYPE html>
        <html>
        <head><title>Resultat</title>
        <style>
            body {{ font-family: Arial; background: linear-gradient(135deg, #667eea, #764ba2); text-align: center; padding: 50px; color: white; }}
            .card {{ max-width: 500px; margin: auto; background: white; padding: 30px; border-radius: 20px; color: #333; }}
            .result {{ {style} color: white; padding: 30px; border-radius: 15px; margin-bottom: 20px; }}
            .btn {{ display: inline-block; background: #764ba2; color: white; padding: 10px 20px; margin-top: 20px; border-radius: 5px; text-decoration: none; }}
        </style>
        </head>
        <body>
            <div class="card">
                <div class="result">
                    <h1 style="font-size: 48px;">{emoji}</h1>
                    <h1>Serie {orientation}</h1>
                    <p>Felicitations !</p>
                </div>
                <div style="display: flex; gap: 20px; margin: 20px 0;">
                    <div style="flex:1; background: #f0f0f0; padding: 10px; border-radius: 10px;">
                        <h3>Moyenne Scientifique</h3>
                        <p style="font-size: 24px; color: #667eea;">{moy_sci:.2f}/20</p>
                    </div>
                    <div style="flex:1; background: #f0f0f0; padding: 10px; border-radius: 10px;">
                        <h3>Moyenne Litteraire</h3>
                        <p style="font-size: 24px; color: #667eea;">{moy_lit:.2f}/20</p>
                    </div>
                </div>
                <a href="/dashboard" class="btn">Retour</a>
            </div>
            <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1"></script>
            <script>
                canvasConfetti({{ particleCount: 200, spread: 70, origin: {{ y: 0.6 }} }});
                setTimeout(() => canvasConfetti({{ particleCount: 150, spread: 100 }}), 500);
            </script>
        </body>
        </html>
        '''
    else:
        return redirect(url_for('formulaire'))

@app.route('/logout')
def logout():
    session.clear()
    return '<h2>Deconnecte</h2><a href="/">Accueil</a>'

if name == 'main':
    app.run(host='0.0.0.0', port=10000, debug=False)
