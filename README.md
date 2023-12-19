## Shikimori Extended API
Оболочка для API сайта [shikimori.me](https://shikimori.me) на языке Python.
<br>_Ссылка на [официальную документацию](https://shikimori.me/api/doc) по работе с API сайта._

### Особенности библиотеки

- встроенные лимитеры на 5rps и 90rpm, согласно документации API
- библиотека полностью асинхронна (httpx)

### Простые use-case добавлены в папку с примерами

- Как получить токены доступа и доступ к защищенным эндпоинтам - [здесь](./examples/app_example.py)

[//]: # (- Доступ к незащищенным эндпоинтам, где не требуется создания приложения - скоро)

### Установка
```shell
pip install git+https://github.com/imPDA/shikimoriextendedapi.git@latest
```
<br>Не забудь добавить переменные в окружение!

## ⚠️ In-development state
- Everything can change during development
- I`m using it for my own Discord bots, so I prioritize my own needs

☕ Please do not hesitate to contact me if you interested in cooperation, have any ideas, need help<br>
☕ Discord: impda
