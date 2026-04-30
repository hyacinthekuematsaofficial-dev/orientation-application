from flask import Flask

app = Flask(name)

@app.route('/')
def hello():
    return "Mon application fonctionne !"

if name == 'main':
    app.run(host='0.0.0.0', port=10000)
