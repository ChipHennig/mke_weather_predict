# mke_weather_predict
A [SARIMA](https://machinelearningmastery.com/sarima-for-time-series-forecasting-in-python/) model trained on the [GHCN-Daily historical weather dataset](https://www.ncdc.noaa.gov/ghcn-daily-description).

Notes:
1. A pretrained model is located at src/sarima_model.pkl
2. src/file_io.py and src/train_sarima.py are useful for training your own model
3. data/mke_weather.db saves time if you want to do more with Milwaukee historical weather data

## Technologies:
- pandas
- SQLite
- pmdarima
