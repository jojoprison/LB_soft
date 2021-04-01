import pathlib

PROJECT_NAME = 'LB_soft'


# путь к проекту
def get_project_root_path():
    current_path = pathlib.Path().cwd()

    project_path = None

    if current_path.name == PROJECT_NAME:
        project_path = current_path
    else:
        for parent_path in current_path.parents:
            parent_path_parts = parent_path.parts
            if parent_path_parts[len(parent_path_parts) - 1] == PROJECT_NAME:
                project_path = parent_path
                break

    return project_path


# путь до диры с кодом (такой стал из за fbs обертки)
def get_source_code_path():
    return get_project_root_path().joinpath('src/main/python/')


# путь до диры с ресурсами для упаковки в экзешник (сюда засуну драйвера для браузеров)
def get_resources_path():
    return get_project_root_path().joinpath('src\\main\\resources\\')


# путь к модулю блока с определенным приложением (inst, tiktok, vk)
def get_module_path(module_name):
    return get_source_code_path().joinpath(module_name)


# путь к модулю проекта с определенным приложением (inst, db, vk)
def get_old_module_path(module_name):
    # берет путь к файлу, который ЗАПУСКАЕТСЯ, а не просто откуда вызвался метод
    current_path = pathlib.Path().cwd()

    while True:
        # берем части пути
        current_path_parts = current_path.parts
        # ищем до python, сорсы лежал тут, папка такая из за пакетера fbs
        if current_path_parts[len(current_path_parts) - 1] == 'python':
            module_path = current_path.joinpath(module_name)
            break
        else:
            # идем выше по дереву директорий
            current_path = current_path.parent

    return module_path


if __name__ == '__main__':
    # print(type(get_module_path('instagram')))
    get_project_root_path()
