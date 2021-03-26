from instagram.instagram_bot import *
from multiprocessing import Pool


def run_bot(username, password):
    bot = InstagramBot(username, password)

    bot.login()

    account_info = bot.get_account_info()
    print(account_info)

    bot.like_post('https://www.instagram.com/p/CM1O8xVHoSV/')

    bot.close_driver()


def main():
    process_count = int(input('Enter the number of browsers: '))
    accounts_auth_data = get_accounts_auth_data(process_count)
    print(accounts_auth_data)
    # будет открыто максимум 2 процесса, остальные будут открыты после завершения предыдущих
    with Pool(processes=process_count) as pool:
        pool.starmap(run_bot, accounts_auth_data)


if __name__ == '__main__':
    main()
