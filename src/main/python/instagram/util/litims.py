import datetime
import locale


def get_limits(reg_date):
    locale.setlocale(locale.LC_ALL, '')
    # print(locale.getlocale())
    # datee = '7 сентября 2017 г. 23:08'
    reg_date_formatted = datetime.datetime.strptime(reg_date, '%d %B %Y')
    print(reg_date_formatted)

def format_reg_date(reg_date):
    
