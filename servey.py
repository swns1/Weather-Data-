import requests
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect
from datetime import datetime as dt
import os
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ENDPOINT_URL = "https://api.openweathermap.org/data/2.5/forecast"
API_KEY = os.getenv("WEATHER_API_KEY") 

class Weather:
    def __init__(self, city_name):
        params = {
            "q": city_name,
            "appid": API_KEY,
            "cnt": 9
        }
        self.response = requests.get(ENDPOINT_URL, params=params)
        self.data = self.response.json()["list"]
        self.city = self.response.json()["city"]["name"]
        self.country = self.response.json()["city"]["country"]
        self.list_weathers = []
        self.weathers()

    def weathers(self):
        for num in range(9):
            data = self.data[num]
            x = data["weather"][0]["icon"]
            w_list = {
                "temp": f"{round(data['main']['temp'] - 273.15, 2)} °C",
                "speed": f"{round(data['wind']['speed'] * 3.6, 2)} km/h",
                "gust": f"{round(data['wind']['gust'] * 3.6, 2)} km/h",
                "descrip": data["weather"][0]["description"].capitalize(),
                "icon": f"https://openweathermap.org/img/wn/{x}@2x.png",
                "humidity": f"{data['main']['humidity']}%"
            }
            self.list_weathers.append(w_list)

class Form(FlaskForm):
    city = StringField("City Name", validators=[DataRequired()])
    submit = SubmitField("Search")


@app.route("/", methods=["GET", "POST"])
def home():
    form = Form()
    city_name = None
    data = None
    weather = None
    year = dt.now().year

    if request.method == "POST":
        city_name = request.form.get("city")
        weather = Weather(city_name)
        data = weather.list_weathers

    return render_template("index.html", form=form, weather=data, city=weather, year=year)

if __name__ == "__main__":
    app.run(debug=True, port=5003)