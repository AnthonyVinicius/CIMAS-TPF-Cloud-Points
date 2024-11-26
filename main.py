from flask import Flask

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'temp'
app.secret_key = 'your_secret_key'

# Rota para o formulário de upload
from routes import *

if __name__ == "__main__":
    app.run(debug=True)