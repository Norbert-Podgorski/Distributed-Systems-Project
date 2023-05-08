from flask import Flask, render_template
from main import main

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")


@app.route('/run_main')
def run_main():
    main()
    print("It's working")


if __name__ == '__main__':
    app.run(debug=True, port=5001)
