"""
train_sarima.py provides

1) functions to import and query
data from the sqlite database: /data/mke_weather.db

2) functions to train a SARIMA statsmodel from pmdarima:
http://alkaline-ml.com/pmdarima/

A pretrained model exists at: sarima_model.pkl
"""
import pandas as pd
import pmdarima as pm
import src.file_io as io
import _sqlite3
import joblib
from datetime import date


def create_table(sql_conn, table_name, df):
    df.to_sql(table_name, sql_conn, if_exists='replace', index=False)


def get_table_df(sql_conn, table_name):
    df = pd.read_sql_query("SELECT * FROM " + table_name, sql_conn)
    return df


def make_avg_temp(sql_conn):
    avg_df = pd.read_sql_query("""
        SELECT DATE, (TMAX + TMIN) / 2 AS AVG_TEMP
        FROM   TEMPERATURES
        """, sql_conn)
    avg_df = avg_df.astype({"AVG_TEMP": 'float16'})
    return avg_df


def sarima_train(data):
    model = pm.arima.auto_arima(data, seasonal=True, m=4)
    print(model.summary())
    joblib.dump(model, 'sarima_model.pkl', compress=True)


def sarima_pred(predict_date):
    # The most recent date from my training data
    # Find this with: last_date = datetime.strptime(avg.iloc[-1].DATE, "%Y-%m-%d %H:%M:%S").date()
    last_date = date(2020, 5, 27)
    days_after = predict_date - last_date
    model = joblib.load('sarima_model.pkl')
    prediction = model.predict(days_after.days)[-1]
    print("SARIMA prediction in Celsius: " + str(prediction))


def run(init_run=True):
    conn = _sqlite3.connect('..\\data\\mke_weather.db')

    if init_run:
        # Initial import to database
        stations_df = io.read_stations('..\\data\\ghcnd-stations.txt')
        create_table(conn, "STATIONS", stations_df)

        stations = get_table_df(conn, "STATIONS")
        stations = stations[stations["NAME"].str.contains("MILWAUKEE")]
        station_list = list(stations.STATION_ID)
        temperatures_url = 'https://www.ncei.noaa.gov/data/global-historical-climatology-network-daily/access/'

        temperatures_df = io.read_temperatures(temperatures_url, station_list)
        create_table(conn, "TEMPERATURES", temperatures_df)

        print(get_table_df(conn, "TEMPERATURES"))

    avg = make_avg_temp(conn)
    print(avg)

    # time_series_avg = avg.set_index('DATE')
    # sarima_train(time_series_avg)
    sarima_pred(date(2020, 6, 1))


run(init_run=False)
