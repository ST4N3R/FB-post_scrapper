from flask import Flask, render_templates, url_for


app = Flask(__name__)


@app.route('/')
def index():
    return render_templates('index.html')


if __name__ == '__main__':
    app.run(debug=True)