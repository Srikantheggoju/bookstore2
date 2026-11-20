from flask import Flask, render_template

app = Flask(__name__)

books = [
    {"name": "DevOps Handbook", "price": "$25"},
    {"name": "Kubernetes Up & Running", "price": "$30"},
    {"name": "Docker Deep Dive", "price": "$20"}
]

@app.route("/")
def home():
    return render_template("index.html", books=books)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

