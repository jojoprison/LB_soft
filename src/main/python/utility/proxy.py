import time
from pathlib import Path
from datetime import datetime
from utility.paths import get_source_code_path

import requests
from bs4 import BeautifulSoup
import random

FREE_FILENAME = 'free_proxy_list.txt'
WORKING_FILENAME = 'working_proxy_list.txt'


class Proxy:
    ip = None
    port = None
    protocol = None
    country = None
    date_founded = None

    def __init__(self, ip, port, protocol, country, date_founded):
        self.ip = ip
        self.port = port
        self.protocol = protocol
        self.country = country
        self.date_founded = date_founded

    def proxy_signature(self):
        return self.ip + ':' + self.port

    def __str__(self):
        return self.protocol + '://' + self.ip + ':' + self.port + ' - ' \
               + self.country + ', ' + str(self.date_founded)

    def __repr__(self):
        return self.protocol + '://' + self.ip + ':' + self.port + ' - ' \
               + self.country + ', ' + str(self.date_founded)


def parse(proxy_str):
    protocol, proxy_str = proxy_str.split('://')
    # ставим доп параметр сплиту, т.к. нам нужны разделить только первым двоеточием которое отделяет порт
    ip, proxy_str = proxy_str.split(':', 1)
    port, proxy_str = proxy_str.split(' - ')
    country, date_founded = proxy_str.split(', ')

    return Proxy(ip, port, protocol, country, date_founded)


def free_proxy_list():
    req = requests.get('https://scrapingant.com/free-proxies/')

    soup = BeautifulSoup(req.text, 'html.parser')
    proxy_list = soup.find('table', class_='proxies-table').find_all('tr')

    # удаляем заголовки самой таблицы
    del proxy_list[0]

    result_proxy_list = []

    for proxy_tr in proxy_list:
        proxy_data = proxy_tr.find_all('td')

        if proxy_data[3].text.endswith('Unknown'):
            country = proxy_data[3].text.split(' ')[-1]
        else:
            country = ' '.join(proxy_data[3].text.split(' ')[1:])

        proxy = Proxy(
            # ip
            proxy_data[0].text,
            # port
            proxy_data[1].text,
            # protocol
            proxy_data[2].text,
            country,
            # date founded
            datetime.now()
        )

        # передаю именно строковое значение чтобы потом записать в файл writelines list[str]
        result_proxy_list.append(proxy)

    return result_proxy_list


# TODO пробнуть хранить в json
# запускать периодически чтоб обновлять лист проксей
def save_to_file():
    filename = f'{get_source_code_path()}/utility/{FREE_FILENAME}'
    proxy_file_path = Path(filename)
    # проверяет наличие файла, если его нет - создает
    proxy_file_path.touch(exist_ok=True)

    # забираем все прокси из файла в формате стринги
    with open(proxy_file_path) as file:
        file_proxy_list_str = file.readlines()

    # преобразуем в объекты кастомного класса Proxy и до вида ip:port
    file_proxy_ip_list = []
    for proxy_str in file_proxy_list_str:
        file_proxy_ip_list.append(parse(proxy_str).proxy_signature())

    # забираем свежие фришные прокси с сайта
    fresh_proxy_list = free_proxy_list()

    # преобразуем их до вида ip:port
    fresh_proxy_ip_list = []
    for proxy in fresh_proxy_list:
        fresh_proxy_ip_list.append(proxy.proxy_signature())

    # убираем прокси из списка, если они уже есть в файле
    new_proxy_ip_list = list(set(fresh_proxy_ip_list) - set(file_proxy_ip_list))

    print('new proxy: ', new_proxy_ip_list)

    # записываем новые прокси в файл
    with open(proxy_file_path, 'a') as file:
        for new_proxy_ip in new_proxy_ip_list:
            for fresh_proxy in fresh_proxy_list:
                if fresh_proxy.proxy_signature() == new_proxy_ip:
                    file.write(str(fresh_proxy) + '\n')


# возвращает список проксей из файла, если есть
def read_from_file():
    filename = f'{get_source_code_path()}/utility/{FREE_FILENAME}'
    proxy_file_path = Path(filename)

    # проверяем наличие файла с проксями
    if proxy_file_path.exists():

        with open(filename) as file:
            file_proxy_list_str = file.readlines()

        # преобразуем в объекты кастомного класса Proxy и до вида ip:port
        # file_proxy_ip_list = []
        # for proxy_str in file_proxy_list_str:
        #     file_proxy_ip_list.append(parse(proxy_str).proxy_signature())

        # return file_proxy_ip_list
        return file_proxy_list_str
    else:
        return []


def random_proxy():
    file_proxy_ip_list = read_from_file()

    rand_proxy = random.choice(file_proxy_ip_list)

    return rand_proxy


def add_to_working_file(proxy):
    working_filename = f'{get_source_code_path()}/utility/{WORKING_FILENAME}'
    working_proxy_file_path = Path(working_filename)
    # проверяет наличие файла, если его нет - создает
    working_proxy_file_path.touch(exist_ok=True)

    # забираем все прокси из файла в формате стринги
    with open(working_proxy_file_path) as file:
        working_file_proxy_list_str = file.readlines()

    # преобразуем в объекты кастомного класса Proxy и до вида ip:port
    working_file_proxy_ip_list = []
    for proxy_str in working_file_proxy_list_str:
        working_file_proxy_ip_list.append(parse(proxy_str).proxy_signature())

    # если прокси еще нет в файле
    if proxy.proxy_signature() not in working_file_proxy_ip_list:
        # записываем рабочую проксю в файл
        with open(working_proxy_file_path, 'a') as file:
            file.write(str(proxy) + '\n')

        print(f'proxy added in working: {proxy}')
        return True
    else:
        return False


if __name__ == '__main__':
    while True:
        save_to_file()
        print('wait 600 sec...')
        time.sleep(600)

    # file = read_from_file()
    # r_proxy = random_proxy()
    # print(r_proxy)
    # prox = parse(r_proxy)
    # add_to_working_file(prox)
