import asyncio
import os

from dotenv import load_dotenv
from shikimori_extended_api import Client as ShikimoriClient
from shikimori_extended_api.client import api_endpoint

# 1) Создай приложение -> https://shikimori.me/oauth/applications

# 2) Найди `client_id` и `client_secret` -> https://shikimori.me/oauth

# 3) Внеси необходимые переменные в локальное окружение, например через .env файл и библиотеку `dotenv`:
#    3.1 заполни `.env` файл в этой же директории
#    3.2 установи библиотеку -> pip install python-dotenv
#    3.2 load_dotenv() всё сделает за тебя!

load_dotenv()

APPLICATION_NAME = os.environ['APPLICATION_NAME']
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')


async def main():
    shiki_client = ShikimoriClient(
        application_name=APPLICATION_NAME,  # обязателен всегда
        client_id=CLIENT_ID,                # обязателен для получения токена
        client_secret=CLIENT_SECRET         # обязателен для получения токена
    )

    # 4) Запроси у пользователя код авторизации.
    #    Он может быть получен, например, после подтверждения авторизации по ссылке `auth_url`

    code = input(f"Авторизайтесь на Shikimori по [ссылке]({shiki_client.auth_url}) и введите авторизационный код:\n")
    print("-" * 80)

    # 5) Код затем преобразуется в токен доступа через `get_access_token` метод

    token = await shiki_client.get_access_token(code)
    print("Получен токен:", token)
    print("-" * 80)

    # 6) Рекомендую создать базу данных и сохранить токен - он потребуется для дальнейшего взаимодействия с ресурсом
    #    ... сохранение токена в базу ...

    # 7) С этим токенон можно получить доступ к защищенным эндпоинтам, например:
    # GET /api/users/whoami - Информация о пользователе, который авторизовал приложение
    # Запрос складывается следующим образом:
    # - shiki_client.get(...) - запрос через метод GET (также можно использовать .post())
    # - api_endpoint - эндпоинт для api, эквивалент https://shikimori.one/api
    # - .users.whoami - эквивалент /users/whoami
    # - в конце нужно сделать вызов, чтобы получить адрес целиком. Итого: shiki_client.get(api_endpoint.users.whoami(), ...)
    # - далее передаётся токен (при наличии) и нужные параметры (headers, ...)

    # Здесь ничего не будет выведено, т.к. это защищенный эндпоинт и нужен токен, но токен не указан
    print("Запрос к защищенному эндпоинту без токена:")
    print(await shiki_client.get(api_endpoint.users.whoami()))
    print("-" * 80)

    # А здесь информация будет получена успешно
    print("Запрос к защищенному эндпоинту с токеном:")
    print(await shiki_client.get(api_endpoint.users.whoami(), token=token))
    print("-" * 80)

    # 8) Без токена можно получить доступ к незащищенным эндопоинтам, т.е. нужно будет указать `application_name` и
    #    затем сразу переходить к 8му пункту.

    # Полный список всех эндпоинтов смотри в официальной документации.


if __name__ == '__main__':
    asyncio.run(main())
