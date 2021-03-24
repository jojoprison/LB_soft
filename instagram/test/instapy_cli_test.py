import time
from instapy_cli import client
from instagram.utility.paths import *
import random

with open(f'{get_module_path()}/accounts.txt') as file:
    account_list = file.readlines()

    account_data = random.choice(account_list)

if account_data:
    # так как формат хранения в файле login:pass, phone
    account_data_split = account_data.split(':')
    username = account_data_split[0]

    account_data_split = account_data_split[1].split(',')
    password = account_data_split[0]
    phone_number = account_data_split[1].replace(' ', '')

    image_files = [f'{get_user_content_dir_path(username)}\\sport.jpg']

    with client(username, password) as cli:

        for i in range(0, len(image_files)):
            print('image: ', image_files[i])

            res = cli.upload(image_files[i], story=True)

            print('IG: >> ', res)

            time.sleep(5)
else:
    print('нет акка')