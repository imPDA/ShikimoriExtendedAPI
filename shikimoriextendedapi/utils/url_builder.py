from typing import Self
from urllib.parse import urlencode


def skip_none(kwargs: dict) -> dict:
    return {k: v for k, v in kwargs.items() if v is not None}

class BaseURL:   
    def __init__(self, url: str) -> None:
        self.url = url

    def __call__(self, **kwargs) -> str:
        return f"{self.url}{'?' if kwargs else ''}{urlencode(skip_none(kwargs))}"

    def __str__(self) -> str:
        return self.url


class URL(BaseURL):
    def _add(self, path: str) -> Self:
        self.url += f'/{path}'
        return self
    
    def __getattr__(self, item: str) -> Self:
        # add a new section to url
        return self._add(item)

    def __getitem__(self, arg) -> Self:
        """Alternative to id() and paste()"""
        return self._add(arg)

    def id_(self, id_: int) -> Self:
        return self._add(str(id_))
    
    def paste(self, arg: str) -> Self:
        return self._add(arg)

class EndpointURL(BaseURL):
    def _add(self, path: str) -> URL:
        return URL(self.url + f'/{path}')
        
    def __getattr__(self, item: str) -> URL:
        # add a new section to url
        return self._add(item)

    def __getitem__(self, arg) -> URL:
        """Alternative to id() and paste()"""
        return self._add(arg)

    def id_(self, id_: int) -> URL:
        return self._add(str(id_))
    
    def paste(self, arg: str) -> URL:
        return self._add(arg)