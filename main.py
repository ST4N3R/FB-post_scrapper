from flask import Flask, render_template, url_for, request
from modules.data_handler import DataHandler
import pandas as pd


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


@app.route('/day_of_week', methods=['POST', 'GET'])
def day_of_week():
    dataHandler = DataHandler()
    dataHandler.readData()

    if request.method == 'POST':
        startDate = request.form['startDate']
        endDate = request.form['endDate']
        return render_template(template_name_or_list='day_of_week.html',
                               labels=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                               data=dataHandler.dayOfWeek_by_reactionNum(startDate=startDate, endDate=endDate).to_list())
    else:
        return render_template(template_name_or_list='day_of_week.html',
                               labels=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                               data=dataHandler.dayOfWeek_by_reactionNum().to_list(),)


@app.route('/months', methods=['POST', 'GET'])
def months():
    dataHandler = DataHandler()
    dataHandler.readData()

    if request.method == 'POST':
        startDate = request.form['startDate']
        endDate = request.form['endDate']
        return render_template(template_name_or_list='months.html',
                               labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Nov', 'Oct', 'Dec'],
                               data=dataHandler.month_by_reactionNum(startDate=startDate, endDate=endDate).to_list())
    else:
        return render_template(template_name_or_list='months.html',
                               labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Nov', 'Oct', 'Dec'],
                               data=dataHandler.month_by_reactionNum().to_list())


@app.route('/hole_year', methods=['POST', 'GET'])
def hole_year():
    dataHandler = DataHandler()
    dataHandler.readData()

    if request.method == 'POST':
        startDate = request.form['startDate']
        endDate = request.form['endDate']

        dates, nums = dataHandler.hole_year(startDate=startDate, endDate=endDate)
        return render_template(template_name_or_list='hole_year.html',
                               labels=dates,
                               data=nums)
    else:
        dates, nums = dataHandler.hole_year()
        return render_template(template_name_or_list='hole_year.html',
                               labels=dates,
                               data=nums)

if __name__ == '__main__':
    app.run(debug=True)