from flask import Flask, render_template, url_for, request
from modules.data_handler import DataHandler
import pandas as pd


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    # dataHandler = DataHandler()

    if request.method == 'POST':
        url = request.form['url_text']

        # if dataHandler.addData(url):
        #     return url
        # else:
        #     return "Coś poszło nie tak"
    else:
        return render_template('index.html')


@app.route('/day_of_week', methods=['POST', 'GET'])
def day_of_week():
    # dataHandler = DataHandler()
    # data = dataHandler.readData()

    if request.method == 'POST':
        startDate = request.form['startDate']
        endDate = request.form['endDate']
        # return render_template(template_name_or_list='day_of_week.html',
        #                     labels=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        #                     data=dataHandler.dayOfWeek_by_reactionNum(startDate=startDate, endDate=endDate).to_list())
    else:
        # return render_template(template_name_or_list='day_of_week.html',
        #                     labels=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        #                         data=dataHandler.dayOfWeek_by_reactionNum().to_list())
        return render_template(template_name_or_list='day_of_week.html',
                            labels=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                                data=[4, 7, 2, 8, 3, 4, 1])


if __name__ == '__main__':
    app.run(debug=True)