import time
import locale
import datetime


def convert_reg_date(reg_date):
    reg_date_split = reg_date.split(' ')
    reg_month = reg_date_split[1]

    month_switcher = {
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

    month_converted = month_switcher.get(reg_month, 'Неправильный месяц')

    date_converted = ''

    for idx, reg_date_part in enumerate(reg_date_split):
        # если сейчас находимся на части с месяцем
        if not idx == 1:
            date_converted = date_converted + str(reg_date_part)
        else:
            date_converted = date_converted + month_converted

        if idx != len(reg_date_split) - 1:
            date_converted += ' '

    return date_converted


if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, '')
    # print(locale.getlocale())
    # temp_date = datetime.datetime.strptime('11 сентябрь 2020', '%d %B %Y')
    # print(temp_date)

    datee = '7 сентября 2017 г. 23:08'
    # month = datee.split(' ')[1]
    print(convert_reg_date(datee))
