import pathlib

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
