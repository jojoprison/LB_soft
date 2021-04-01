import os

from utility.paths import get_module_path


# путь к модулю с инстой
def get_instagram_module_path():
    return get_module_path('instagram')


def get_user_directory_path(username):
    directory_path = f'{get_instagram_module_path()}\\users\\{username}'

    # создаём папку с именем пользователя для чистоты проекта
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)

    return directory_path


def get_user_content_dir_path(username):
    content_dir_path = f'{get_user_directory_path(username)}\\content'

    # создаём папку с именем пользователя для чистоты проекта
    if not os.path.exists(content_dir_path):
        os.mkdir(content_dir_path)

    return content_dir_path


def get_user_posts_file_path(username):
    return f'{get_user_directory_path(username)}\\{username}_posts.txt'


if __name__ == '__main__':
    print(get_instagram_module_path())
    # print(get_user_directory_path('squalordf'))
