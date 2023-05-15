from flask import Flask, render_template, request
from main import main
from heatmap import generate_heatmap

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")


@app.route('/run_main')
def run_main():
    main()


@app.route('/run_heatmap')
def run_heatmap():
    generate_heatmap()


if __name__ == '__main__':
    app.run(debug=True, port=5001)
