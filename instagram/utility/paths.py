import pathlib
import os

PROJECT_NAME = 'LB_soft'


# путь к проекту
def get_project_root_path():
    current_path = pathlib.Path().cwd()
    project_path = ''

    for parent_path in current_path.parents:
        parent_path_parts = parent_path.parts
        if parent_path_parts[len(parent_path_parts) - 1] == PROJECT_NAME:
            project_path = parent_path
            break

    return project_path


# путь к модулю проекта с определенным приложением (inst, db, vk)
def get_module_path():
    current_path = pathlib.Path().cwd()

    while True:
        current_path_parts = current_path.parts
        if current_path_parts[len(current_path_parts) - 2] == PROJECT_NAME:
            module_path = current_path
            break
        else:
            current_path = current_path.parent

    return module_path


def get_user_page_url(username):
    return f'https://www.instagram.com/{username}/'


def get_user_directory_path(username):
    directory_path = f'{get_module_path()}\\users\\{username}'

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
