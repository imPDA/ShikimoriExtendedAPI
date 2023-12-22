from typing import Any, Self
from urllib.parse import urlencode


class URL:
    def __init__(self, url: str):
        self.url = url

    def _add(self, path: str) -> Self:
        return URL(self.url + f'/{path}')

    def __getattr__(self, item: str) -> Self:
        if item.lower() in ['id', 'paste']:
            # if `id` or `paste` -> do nothing, make a call after it to paste smth into url via `__call__`
            return self

        # in all other cases just add a new section to url
        return self._add(item)

    def __call__(self, arg: Any = None, /, **kwargs) -> Self | str:
        # if a positional arg provided, add to the url path
        if arg:
            return self._add(arg)

        return f"{self.url}{'?' if kwargs else ''}{urlencode(kwargs)}"

    def __str__(self) -> str:
        return self.url
