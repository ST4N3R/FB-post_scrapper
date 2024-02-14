from flask import Flask, render_template, url_for, request
from modules.data_handler import DataHandler
import pandas as pd
import numpy as np


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    dataHandler = DataHandler()

    if request.method == 'POST':
        url = request.form['url_text']

        if dataHandler.addData(url):
            return url
        else:
            return "Coś poszło nie tak"
    else:
        return render_template('index.html')


@app.route('/visualization', methods=['POST', 'GET'])
def visualization():
    dataHandler = DataHandler()
    data = dataHandler.readData()

    if request.method == 'POST':
        startDate = request.form['startDate']
        endDate = request.form['endDate']
        return render_template(template_name_or_list='visualization.html',
                            labels=[*range(1, 8)],
                            data=dataHandler.dayOfWeek_by_reactionNum(startDate=startDate, endDate=endDate).to_list())
    else:
        return render_template(template_name_or_list='visualization.html',
                            labels=[*range(1, 8)],
                                data=dataHandler.dayOfWeek_by_reactionNum().to_list())


if __name__ == '__main__':
    app.run(debug=True)