from flask import Flask, render_template, url_for, request
import functions_framework


app = Flask(__name__)


# todo: Połączenie z bazą danych GCP

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        url = request.form['url_text']
        return url
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)