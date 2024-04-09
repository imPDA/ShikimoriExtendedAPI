from time import perf_counter


class Catchtime:
    def __init__(self):
        self.start = None
        self.time = None

    def __enter__(self):
        self.start = perf_counter()
        return self

    def __exit__(self, type_, value, traceback):
        self.time = perf_counter() - self.start
