from flask import Flask
app = Flask(name)

@app.route('/')
def home():
    return "Mon application fonctionne"

if name == 'main':
    app.run()
