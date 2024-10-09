from flask import Flask

app = Flask(__name__)

@app.route("/")
def homepage():
    return "homepage"

if __name__ == "__main__":
    app.run()