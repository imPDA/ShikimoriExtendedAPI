import asyncio
import os

from dotenv import load_dotenv
from shikimori_extended_api import Client as ShikimoriClient
from shikimori_extended_api.client import api_endpoint

load_dotenv()

APPLICATION_NAME = os.environ['APPLICATION_NAME']
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')


async def main():
    client = ShikimoriClient(
        application_name=APPLICATION_NAME,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )

    # 1) Аналог примеру из библиотеки pyshiki (заброшена)
    # https://github.com/OlegWock/PyShiki
    # GET  http://shikimori.org/api/animes/search?q=Lucky+Star
    print(await client.get(api_endpoint.animes.search(q='Lucky Star')))
    print("-" * 80)

    # 2) Подсчёт суммарной длительности, проведённой за просмотром аниме
    # Встроенная функция, которая проходится по всем просмотренным аниме и суммирует их длительность
    # Есть точный подсчёт и примерный, примерный - быстрее в несколько раз
    print(await client.fetch_total_watch_time(272747))
    print("-" * 80)

    # Точный - делает запрос по всем аниме, лимитирован допустимым количеством запросов в минуту и секунду -> дольше
    # print(await client.fetch_total_watch_time(272747, accurate=True))
    # print("-" * 80)

    # Неточный всегда будет занижать. По моей статистике:
    # - на сайте указано `67 дней аниме`
    # - неточный подсчёт даёт 92460 мин ~= 64.21 дня (занижено на ~4%)
    # - точный запрос даёт 97577 мин ~= 67.76 дня (хорошо совпадает со значением, указанном на сайте)

    # 3) Показать инфу по конкретному пользователю (по id)
    # Есть три эквивалентных способа задать url: .id(), .paste(), []
    # method_1 = api_endpoint.users.id(272747)()
    # method_2 = api_endpoint.users.paste(272747)()
    # method_3 = api_endpoint.users[272747]()
    print(await client.get(api_endpoint.users[272747]()))
    print("-" * 80)


if __name__ == '__main__':
    asyncio.run(main())
