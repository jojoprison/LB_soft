from instagram.config import users_settings_dict

if __name__ == '__main__':
    second_user_dict = list(users_settings_dict.values())[1]
    USERNAME = second_user_dict['login']
    PASSWORD = second_user_dict['password']
    print(USERNAME)
    print(PASSWORD)
