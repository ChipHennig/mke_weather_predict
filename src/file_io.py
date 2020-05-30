import os
import pandas as pd
from calendar import monthrange
import requests


def read_stations(stations_path):
    """

    :param stations_path:
    :return:
    """
    with open(stations_path, 'r', encoding="utf-8") as file:
        cols_dict = {
            "STATION_ID": [],
            "LAT": [],
            "LON": [],
            "ELEVATION": [],
            "STATE": [],
            "NAME": []
        }
        for line in file:
            if line.startswith('US'):
                cols = line.split()
                cols_dict["STATION_ID"].append(cols[0])
                cols_dict["LAT"].append(float(cols[1]))
                cols_dict["LON"].append(float(cols[2]))
                cols_dict["ELEVATION"].append(float(cols[3]))
                cols_dict["STATE"].append(cols[4])
                cols_dict["NAME"].append(cols[5])
    df = pd.DataFrame(data=cols_dict)
    return df


def read_temperatures(temperatures_url, station_list, init_parse=True):
    """
    If init_parse=True, downloads data from the ghcn_daily dataset temperatures_url
    Reads the csv files downloaded and append them into a single dataframe

    :param temperatures_url:
    :param station_list:
    :param init_parse
    :return:
    """
    all_temps = pd.DataFrame(columns=["STATION", "DATE", "TMAX", "TMIN"])
    for station_id in station_list:
        if init_parse:
            # Initial scraping and writing csvs
            page = requests.get(temperatures_url + station_id + '.csv')
            decoded_content = page.content.decode('utf-8')
            station_write = open('..\\data\\station_csv\\' + station_id + '.csv', 'w')
            station_write.write(decoded_content)
            station_write.close()
        stations_temps = pd.read_csv('..\\data\\station_csv\\' + station_id + '.csv')
        if 'TMIN' in stations_temps.columns and 'TMAX' in stations_temps.columns:
            stations_temps = stations_temps[["STATION", "DATE", "TMAX", "TMIN"]]
            all_temps = all_temps.append(stations_temps)
    all_temps = all_temps.dropna()
    all_temps.TMIN = all_temps.TMIN.divide(10)
    all_temps.TMAX = all_temps.TMAX.divide(10)
    all_temps = all_temps.astype({"DATE": 'datetime64', "TMAX": 'float16', "TMIN": 'float16'})
    all_temps = all_temps.drop_duplicates("DATE")
    all_temps = all_temps.sort_values("DATE")
    return all_temps


def read_temperatures_dly(temperatures_path):
    """
    Reads files of .dly type (not completely functional)
    Not used for data currently in database

    :param temperatures_path:
    :return:
    """
    temperature_files = [f for f in os.listdir(temperatures_path)]
    all_temps = pd.DataFrame(columns=["STATION_ID", "DATE", "TEMP_MAX", "TEMP_MIN"])
    all_temps = all_temps.astype({"DATE": 'datetime64', "TEMP_MIN": 'float16', "TEMP_MAX": 'float16'})
    for temp_file in temperature_files:
        cols_dict = {
            "STATION_ID": [],
            "DATE": [],
            "TEMP_MIN": [],
            "TEMP_MAX": []
        }
        with open(temperatures_path + temp_file, 'r', encoding="utf-8") as file:
            for line in file:
                id = line[:11]
                year = line[11:15]
                month = line[15:17]
                element = line[17:21]
                if element == 'TMIN' or element == 'TMAX':
                    col = 21
                    day = 1
                    while not day > monthrange(int(year), int(month))[1]:
                        day_str = day
                        if day_str < 10:
                            day_str = '0' + str(day)
                        else:
                            day_str = str(day)
                        date = year + '-' + month + '-' + day_str
                        if date not in cols_dict["DATE"]:
                            cols_dict["STATION_ID"].append(id)
                            cols_dict["DATE"].append(date)
                        val = float(line[col:col + 5]) / 10
                        index = cols_dict["STATION_ID"].index(id)
                        if element == 'TMIN':
                            cols_dict["TEMP_MIN"].insert(index, val)
                        elif element == 'TMAX':
                            cols_dict["TEMP_MAX"].insert(index, val)
                        day += 1
                        col += 8
        df = pd.DataFrame(data=cols_dict)
        df = df.astype({"DATE": 'datetime64', "TEMP_MIN": 'float16', "TEMP_MAX": 'float16'})
        all_temps = all_temps.append(df)
        # Remove rows with missing values
        all_temps = all_temps[(all_temps.TEMP_MIN != -1000) & (all_temps.TEMP_MAX != -1000)]
    return all_temps
