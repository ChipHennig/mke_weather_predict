from flask import Flask
from flask import request
from datetime import datetime
from datetime import date
import joblib

app = Flask(__name__)


@app.route('/src/page_request', methods = ['GET'])
def temp_predict():
    celsius = sarima_pred()
    fahrenheit = (celsius * 9 / 5) + 32
    return str(round(fahrenheit, 2))


def sarima_pred():
    last_date = date(2020, 5, 27)
    predict_date = datetime.today().date()
    days_after = predict_date - last_date
    model = joblib.load('sarima_model.pkl')
    return model.predict(days_after.days)[-1]