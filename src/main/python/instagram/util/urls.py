def generate_user_url(username):
    return f'https://www.instagram.com/{username}/'


def parse_username(url):
    return url.split('/')[-2]


if __name__ == '__main__':
    print(parse_username('https://www.instagram.com/rameshe._/'))
