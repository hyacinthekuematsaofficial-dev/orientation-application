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

@app.route('/resultat')
def resultat():
    if 'user_id' not in session:
        return '<a href="/connexion">Veuillez vous connecter</a>'
    
    if 'resultat' in session:
        moy_sci, moy_let, orientation = session['resultat']
        
        if orientation == "Scientifique":
            style = "background: linear-gradient(135deg, #667eea, #764ba2);"
            emoji = "🔬"
        else:
            style = "background: linear-gradient(135deg, #f093fb, #f5576c);"
            emoji = "📚"
        
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Résultat</title>
            <style>
                body {{ font-family: Arial; background: linear-gradient(135deg, #667eea, #764ba2); color: white; text-align: center; padding: 50px; }}
                .card {{ background: white; color: #333; max-width: 500px; margin: auto; padding: 30px; border-radius: 20px; }}
                .result {{ {style} color: white; padding: 30px; border-radius: 15px; margin-bottom: 20px; }}
                .btn {{ display: inline-block; background: #764ba2; color: white; padding: 10px 20px; margin-top: 20px; border-radius: 5px; text-decoration: none; }}
            </style>
        </body>
        <body>
            <div class="card">
                <div class="result">
                    <h1 style="font-size: 48px;">{emoji}</h1>
                    <h1>Série {orientation}</h1>
                    <p>Félicitations !</p>
                </div>
                <div class="row" style="display: flex; gap: 20px; margin: 20px 0;">
                    <div class="col" style="flex:1; background: #f0f0f0; padding: 10px; border-radius: 10px;">
                        <h3>📊 Moyenne Scientifique</h3>
                        <p style="font-size: 24px; color: #667eea;">{moy_sci:.2f}/20</p>
                    </div>
                    <div class="col" style="flex:1; background: #f0f0f0; padding: 10px; border-radius: 10px;">
                        <h3>📚 Moyenne Littéraire</h3>
                        <p style="font-size: 24px; color: #667eea;">{moy_let:.2f}/20</p>
                    </div>
                </div>
                <a href="/dashboard" class="btn">Retour au tableau de bord</a>
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
        return '<a href="/notes">Remplissez d\'abord le formulaire de notes</a>'

@app.route('/logout')
def logout():
    session.clear()
    return '<h2>🚪 Déconnecté</h2><a href="/">Retour à l\'accueil</a>'

if name == 'main':
    app.run(host='0.0.0.0', port=10000, debug=False)
