import json
import PySimpleGUI as sg
import pyowm
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

sg.theme('BluePurple')

with open("creds.json") as creds:
    creds = json.load(creds)

owm = OWM(creds["owm_key"])
mgr = owm.weather_manager()


layout = [  [sg.Text('Check the weather in your area!')], [sg.Text('What is your location?'), sg.InputText()], [sg.Button('Go'), sg.Button('Exit')] ]

window = sg.Window('Hazy - GUI', layout)

while True:
    event, values = window.read()
    if event == 'Go': # if user clicks Go
        break
    if event == 'Exit':
        exit(0)

try:
    observation = mgr.weather_at_place(values[0])
except pyowm.commons.exceptions.NotFoundError:
    layout = [ [sg.Text(f'An error has occured!')], [sg.Text(f'The location you have entered is not recognized. The program will now exit.')], [sg.Button('OK')] ]

    window = sg.Window('Hazy - Error', layout)

    while True:
        event, values = window.read()
        if event == 'OK':
            exit(0)
else:
    w = observation.weather
    will_it_rain = mgr.forecast_at_place(values[0], '3h')
    today = timestamps.tomorrow()
    rain_q  = will_it_rain.will_be_rainy_at(today)

    if rain_q:
        but_will_it_rain_tomorrow = "It is likely to rain tomorrow."
    else:
        but_will_it_rain_tomorrow = "It doesn't look like it will rain tomorrow."

    window.close()

    windspeed = (w.wind())

    temp = round(w.temperature("fahrenheit")["temp"])

    realfeel = round(w.temperature("fahrenheit")["feels_like"])

    layout =  [  [sg.Text(f'Current weather for {values[0]}')], [sg.Text(f'{w.status} with winds at {windspeed["speed"]}mph.')], [sg.Text(f'Temperature: {temp}° with a RealFeel of {realfeel}°')], [sg.Text(f'Humidity: {w.humidity}%')], [sg.Button('Exit')] ]

    window = sg.Window('Hazy - GUI', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks Exit
            break
