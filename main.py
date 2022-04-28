import requests
import PySimpleGUI as sg
from io import BytesIO
from PIL import Image


def get_img(token):
    response = requests.get(
        url='https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=10000',
        stream=True
    ).json()
    for item in response['data']['cryptoCurrencyList']:
        if item.get('symbol').lower() == token.lower() or item.get('name').lower() == token.lower():
            r = requests.get(url=f'https://s2.coinmarketcap.com/static/img/coins/64x64/{item.get("id")}.png')
            pil_image = Image.open(BytesIO(r.content))
            pil_image.thumbnail((60, 60))
            png_bio = BytesIO()
            pil_image.save(png_bio, format="PNG")

            return png_bio.getvalue()


def get_info(token):
    response = requests.get(url='https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=10000').json()
    for item in response['data']['cryptoCurrencyList']:
        if item.get('symbol').lower() == token.lower() or item.get('name').lower() == token.lower():
            name = item['name']
            symbol = item['symbol']
            total_supply = item['totalSupply']
            market_cap = item['quotes'][0]['marketCap']
            price = item['quotes'][0]['price']
            volume = item['quotes'][0]['volume24h']

            print(f'Токен - {name} ({symbol})\n'
                  f'Цена - {round(price, 2)} $USD\n'
                  f'Количество монет - {round(total_supply, 2)} {symbol.upper()}\n'
                  f'Рыночная капитализация - {round(market_cap, 2)} $USD\n'
                  f'Объем рынка (24ч) - {round(volume, 2)} $USD\n')

            return


sg.theme('Reddit')
layout = [
    [sg.Text('Enter coin'), sg.InputText(do_not_clear=False)],
    [sg.Button('Ok'), sg.Button('Exit')],
    [sg.Output(size=(50, 7)), sg.Image(key="-IMAGE-", size=(60, 60))]
]
window = sg.Window('Crypto', layout)


if __name__ == '__main__':
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event:
            get_info(values[0])
            window["-IMAGE-"].update(get_img(values[0]))

