import time
import random
import os
from stem import Signal
from stem.control import Controller
import requests


def check_old_ip():
    with requests.get('https://ipinfo.io') as response:
        response_json = response.json()
        ip = response_json['ip']
        color_S = random.choice(list(COLORS.keys()))
        print(colorText(f'[[{color_S}]]'))
        print(f'\n-----Tor New Identity-----\nold ip: {ip}')


def check_new_ip():
    with requests.get('https://ipinfo.io') as response:
        response_json = response.json()
        ip = response_json['ip']
        city = response_json['city']
        timezone = response_json['timezone']
        country = response_json['country']
        print(f'New ip: {ip}\ncity: {city}\ntime zone: {timezone}\ncountry: {country}\n----------\n')


def tor_identity(Time):
    while True:
        time.sleep(Time)
        check_old_ip()
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
            check_new_ip()


def colorText(text):
    for color in COLORS:
        text = text.replace("[[" + color + "]]", COLORS[color])
    return text


COLORS = {
    "red": "\u001b[31;1m",
    "green": "\u001b[32m",
    "yellow": "\u001b[33;1m",
    "blue": "\u001b[34;1m",
    "magenta": "\u001b[35m",
    "cyan": "\u001b[36m",
}

os.system('clear')

file = open('logo.txt')
text = ''.join(file.readlines())
print(colorText(colorText(text)))


def loop():
    try:
        question = input(
            colorText('[[green]]are you want to set time to tor new identity [Y,n] if No[n] tor time default is 10 '
                      'sec new '
                      'identity:[[magenta]]'))

        if question == 'n' or question == 'N':
            print(colorText("[[magenta]]also you can stop program with [CTRL+C]"))
            tor_identity(10)

        elif question == 'y' or question == 'n':
            input_time = int(input(colorText('[[cyan]]pls set Your Tyime:')))
            print(colorText("[[magenta]]also you can stop program with [CTRL+C]"))
            tor_identity(input_time)

        else:
            print(colorText('[[magenta]]pls enter true value'))
            loop()

    finally:

        input_keep = input('\n'+colorText('[[red]]are you sure to exit : [Y,n] [[magenta]]'))

        if input_keep == 'N' or input_keep == 'n':
            loop()

        else:
            exit()


loop()


