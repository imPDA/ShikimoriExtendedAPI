from typing import Self
from urllib.parse import urlencode


def skip_none(kwargs: dict) -> dict:
    return {k: v for k, v in kwargs.items() if v is not None}


class URL:
    def __init__(self, url: str) -> None:
        self.url = url

    @classmethod
    def _add(cls, prev_url: str, path: str) -> Self:
        return cls(prev_url + f'/{path}')

    def __getattr__(self, item: str) -> Self:
        # add a new section to url
        return self._add(self.url, item)

    def __getitem__(self, arg) -> Self:
        """Alternative to id() and paste()"""
        return self._add(self.url, arg)

    def __call__(self, **kwargs) -> str:
        return f"{self.url}{'?' if kwargs else ''}{urlencode(skip_none(kwargs))}"

    def __str__(self) -> str:
        return self.url
    
    def id(self, id_:int) -> Self:
        return self._add(self.url, str(id_))
    
    def paste(self, arg: str) -> Self:
        return self._add(self.url, arg)
