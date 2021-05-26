from instagram.instagram_bot import *
from multiprocessing import Pool
import time
import locale
import datetime


def create():
    account_auth_data = get_accounts_auth_data(1)[0]
    print(account_auth_data)

    bot = InstagramBot(account_auth_data[0], account_auth_data[1])

    return bot


def run(username, password):
    botto = InstagramBot(username, password)

    botto.login()
    # bot.like_post('https://www.instagram.com/p/CMptl3oLVuv/')
    # bot.comment_post('https://www.instagram.com/p/CMptl3oLVuv/', 'голос сутулиц')
    botto.like_comment_post('https://www.instagram.com/p/CMptl3oLVuv/', 'DWARPHOLOMEO LMAO')

    botto.close_driver()


def run_single():
    account_auth_data = get_accounts_auth_data(1)[0]
    print(account_auth_data)
    run(account_auth_data[0], account_auth_data[1])


def run_multiprocessing():
    # для нескольких окон
    process_count = int(input('Enter the number of browsers: '))
    accounts_auth_data = get_accounts_auth_data(process_count)
    print(accounts_auth_data)
    # будет открыто максимум 2 процесса, остальные будут открыты после завершения предыдущих
    with Pool(processes=process_count) as pool:
        pool.starmap(run, accounts_auth_data)


def switch_month(month):

    switcher = {
        'января': 'январь',
        'февраля': 'февраль',
        'марта': 'март',
        'апреля': 'апрель',
        'мая': 'май',
        'июня': 'июнь',
        'июля': 'июль',
        'августа': 'август',
        'сентября': 'сентябрь',
        'октября': 'октябрь',
        'ноября': 'ноябрь',
        'декабря': 'декабрь'
    }

    return switcher.get(month, 'Неправильно введен месяц')


if __name__ == '__main__':
    # bot = create()
    # bot.login()
    #
    # bot.get_account_info()
    #
    # bot.wait_and_close_driver()



    switch_month
