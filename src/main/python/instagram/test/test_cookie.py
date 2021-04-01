import requests
from instagram.config import USERNAME, PASSWORD

with requests.Session() as session:
    # Ваш URL с формами логина
    url = "https://www.instagram.com"

    # Получаем страницу с формой логина
    session.get(url)

    # Данные в виде словаря, которые будут отправляться в POST
    dann = dict(username=USERNAME, password=PASSWORD)
    # Отправляем данные в POST, в session записываются наши куки
    session.post(url, dann)

    # Ваш второй URL - тот с которого вам нужно спарсить данные
    url2 = "https://www.instagram.com/p/B7GZRfiCR6D/"

    # Все! Вы получили Response. Поскольку в session записались куки авторизации - при вызове метода get()
    # с этой сессии в Request отправляются ваши куки.
    r = session.get(url2)

# Дальше делайте с вашими данными все что захотите
print(r.text)
