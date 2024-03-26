import asyncio
import pathlib

import environ

from shikimoriextendedapi import Client as ShikimoriClient, api_endpoint

# Для начала создай приложение по адресу https://shikimori.one/oauth/applications
# Затем найди `client_id` и `client_secret` по адресу https://shikimori.one/oauth
# Их нужно указать при инициализации клиента, например, через переменные окружения

# Подгружаем переменные окружения любым удобным способом, например, через
# библиотеку django-environ
BASE_DIR = pathlib.Path(__file__).resolve().parent
env = environ.Env()
# Не забудь создать файл .env и записать туда `client_id` и `client_secret`,
# а также название приложения (важно! это требование api shikimori)
environ.Env.read_env(BASE_DIR / '.env')


async def main():
    shiki_client = ShikimoriClient(
        application_name=env('APPLICATION_NAME'),  # обязателен всегда
        client_id=env('CLIENT_ID'),                # для получения токена
        client_secret=env('CLIENT_SECRET')         # для получения токена
    )

    # Запрос кода авторизации
    code = input(f"Авторизуйтесь на Shikimori -> {shiki_client.auth_url} -> введите авторизационный код:")
    print("-" * 80)

    # Получение токена через код авторизации, полученный выше
    token = await shiki_client.get_access_token(code)
    print("Получен токен:", token)
    print("-" * 80)

    # Токен лучше сохранить для дальнейшего использования, например, в базу данных

    # С токеном можно получить доступ к защищенным эндпоинтам, например:
    # GET /api/users/whoami - Информация о пользователе, который авторизовал приложение

    # Здесь ничего не будет выведено, т.к. токен не указан
    print("Запрос к защищенному эндпоинту без токена:")
    print(await shiki_client.get(api_endpoint.users.whoami))
    print("-" * 80)

    # А здесь информация будет получена успешно
    print("Запрос к защищенному эндпоинту с токеном:")
    print(await shiki_client.get(api_endpoint.users.whoami, token=token))
    print("-" * 80)

    # Без токена можно получить доступ к незащищенным эндопоинтам
    # Полный список всех эндпоинтов смотри в официальной документации


if __name__ == '__main__':
    asyncio.run(main())
