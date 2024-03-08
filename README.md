## Shikimori Extended API
Оболочка для API сайта [shikimori.one](https://shikimori.one) на языке Python.

>_RTFM! Ссылка на [официальную документацию](https://shikimori.one/api/doc) по работе с API сайта.
Внимательно ознакомьтесь с ней!_

### Особенности библиотеки

- встроенные лимитеры на 5rps и 90rpm, согласно документации ([тык](https://shikimori.one/api/doc/2.0#:~:text=Restrictions,5rps%20and%2090rpm)), чтобы не попасть на бан за игнор таймаутов;
- автоповтор запроса если запрос всё-таки попал на таймаут;
- библиотека полностью асинхронна (на httpx);
- интересная фича с билдером url (замена ручного вбивания строк в запросы).

### Инструкции см. в [папке с примерами](./examples)
- [Как правильно использовать встроенный билдер url](./examples/1_urls.py)
- [Пример базового использования](./examples/2_basic_usage.py)

[//]: # (- Доступ к незащищенным эндпоинтам, где не требуется создания приложения - скоро)

### Установка (poetry)
```shell
poetry add git+https://github.com/imPDA/shikimoriextendedapi.git
```

### ⚠️ В разработке
По любым вопросам быстрее всего отвечу в Discord.
<br><img src="https://assets-global.website-files.com/6257adef93867e50d84d30e2/636e0a6a49cf127bf92de1e2_icon_clyde_blurple_RGB.png" width=15/><b> imPDA</b>
