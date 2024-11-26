from app import app

@app.route('/')
@app.route('/index')

def inde():
    return "Hello World!"