from flask import Flask, render_template, url_for, request


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        url = request.form['url_text']
        return 'Hello'
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)