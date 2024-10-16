from flask import Flask

app = Flask(__name__)

@app.route("/")  # Mudei de "/http://127.0.0.1:5000" para "/"
def hello_world():
    return "<h1>Hello, World!</h1>" "<p>eu sou um teste do projeto de interface do banco de dados NEVOLI</p>"
    

if __name__ == "__main__":
    app.run(debug=True)
