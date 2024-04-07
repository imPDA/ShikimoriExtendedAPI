from typing import Self


class URL:
    def __init__(self, url: str) -> None:
        self.url = url

    def _add(self, path: str) -> Self:
        return URL(self.url + f'/{path}')

    def __getattr__(self, item: str) -> Self:
        # add a new section to url
        return self._add(item)

    def __getitem__(self, arg) -> Self:
        """Alternative to id() and paste()"""
        return self._add(arg)

    def __str__(self) -> str:
        return self.url
    
    def id(self, id_: int) -> Self:
        return self._add(str(id_))
    
    def paste(self, arg: str) -> Self:
        return self._add(arg)
