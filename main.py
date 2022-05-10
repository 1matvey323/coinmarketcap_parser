import requests
import PySimpleGUI as Sg
from io import BytesIO
from PIL import Image


class Parser:
    def __init__(self, token, layout):
        self.__layout = layout
        self.__token = token
        self.__window = Sg.Window('Crypto', layout)
        self.__limit = 1000

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, token):
        self.__token = token

    @property
    def window(self):
        return self.__window

    @window.setter
    def window(self, window):
        self.__window = window

    def get_img(self):
        response = requests.get(
            url=f'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit={self.__limit}',
            stream=True
        ).json()
        for item in response['data']['cryptoCurrencyList']:
            if item.get('symbol').lower() == self.__token.lower() or item.get('name').lower() == self.__token.lower():
                r = requests.get(url=f'https://s2.coinmarketcap.com/static/img/coins/64x64/{item.get("id")}.png')
                pil_image = Image.open(BytesIO(r.content))
                pil_image.thumbnail((60, 60))
                png_bio = BytesIO()
                pil_image.save(png_bio, format="PNG")

                return png_bio.getvalue()

    def get_info(self):
        response = requests.get(
            url=f'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit={self.__limit}').json()
        for item in response['data']['cryptoCurrencyList']:
            if item.get('symbol').lower() == self.__token.lower() or item.get('name').lower() == self.__token.lower():
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


def main():
    Sg.theme('Reddit')
    layout = [
        [Sg.Text('Enter coin'), Sg.InputText(do_not_clear=False)],
        [Sg.Button('Ok'), Sg.Button('Exit')],
        [Sg.Output(size=(50, 7)), Sg.Image(key="-IMAGE-", size=(60, 60))]
    ]
    parser = Parser('', layout)

    while True:
        event, values = parser.window.read()
        if event == Sg.WIN_CLOSED or event == 'Exit':
            break
        if event:
            parser.token = values[0]
            parser.get_info()
            parser.window["-IMAGE-"].update(parser.get_img())


if __name__ == '__main__':
    main()
