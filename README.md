# mke_weather_predict
A [SARIMA](https://machinelearningmastery.com/sarima-for-time-series-forecasting-in-python/) model trained on the [GHCN-Daily historical weather dataset](https://data.nodc.noaa.gov/cgi-bin/iso?id=gov.noaa.ncdc:C00861).

Notes:
1. A pretrained model is located at src/sarima_model.pkl
2. src/file_io.py and src/train_sarima.py are useful for training your own model
3. data/mke_weather.db saves time if you want to do more with Milwaukee historical weather data

## Technologies:
- pandas
- SQLite
- pmdarima

## [Website](http://hi.mke-weather-sarima.com/)
- is a Flask app on AWS Elastic Beanstalk
- uses [OpenWeather](https://openweathermap.org/api) API for current weather data
- might include other trained models in the future!
