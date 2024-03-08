from shikimoriextendedapi import api_endpoint

""" 
URL начинается с базового api_endpoint, к которому добавляется путь через точку, 
в конце ставятся скобки: `api_endpoint.some.path.here()`.

Получим URL для эндпоинта /api/users/whoami:
url = api_endpoint.users.whoami()

Если необходимо вставить id, это делается с помощью id(some_id_here). Например,
получим конкретного пользователя по id, эндпоинт выглядит как /api/users/:id:
url = api_endpoint.users.id(272747)()  # imPDA

Больше примеров ниже и в документации:
- API v2: https://shikimori.one/api/doc/2.0
- API v1: https://shikimori.one/api/doc/1.0
"""


if __name__ == '__main__':
    # GET /api/users/whoami	Show current user's brief info
    print(f"{api_endpoint.users.whoami() = }")

    # GET /api/users/:id    Show an user
    print(f"{api_endpoint.users.id(272747)() = }")

    # GET /api/animes	List animes
    print(f"{api_endpoint.animes() = }")

    # GET /api/animes/:id	Show an anime
    print(f"{api_endpoint.animes.id(31240)() = }")
