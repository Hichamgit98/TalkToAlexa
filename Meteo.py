import datetime as dt
import requests

Base_url = 'http://api.openweathermap.org/data/2.5/weather?'
Api_key = 'd428ca471a580e3c08b4d64445b57b70'
City = 'Greenwich'


def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9 / 5) + 32
    return celsius, fahrenheit


url = Base_url + 'appid=' + Api_key + '&q=' + City

response = requests.get(url).json()


temp_kelvin = response['main']['temp']
temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
feels_like_kelvin = response['main']['feels_like']
feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)
city = response['name']
sunrise = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
sunset = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])
# print(sunrise)
wind_speed = response['wind']['speed']
description = response['weather'][0]['description']
humidity = response['main']['humidity']

print(f"Temperature in {city}: {temp_celsius:.2f} °C or {temp_fahrenheit:.2f}°F")
print(f"Temperature in {city} feels like: {feels_like_celsius:.2f} °C or {feels_like_fahrenheit:.2f}°F")
print(f"Humidity in {city}: {humidity}\t % ")
print(f"Wind speed in {city}: {wind_speed}\t km/h ")
print(f"General weather in {city}: {description} ")
print(f"The sun rises in {city} at: {sunrise} Local time ")
print(f"The sun sets in {city} at: {sunset} Local time ")
