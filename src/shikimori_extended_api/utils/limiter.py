import asyncio
import collections
import functools
from datetime import timedelta, datetime

TD0 = timedelta(0)


class Limiter:
    def __init__(self, max_queries: int, period: float, *, name: str):
        self.name = name

        self.period = timedelta(seconds=period)
        self.history = collections.deque([datetime.min, ] * 5, maxlen=max_queries)

        self._alock = asyncio.Lock()

    @property
    def _timespan(self):
        return datetime.now() - self.history[1]

    def __call__(self, f):
        @functools.wraps(f)
        async def wrapped(*args, **kwargs):
            async with self:
                return await f(*args, **kwargs)

        return wrapped

    async def __aenter__(self):
        async with self._alock:
            sleep_time = self.period - self._timespan
            if sleep_time > TD0:
                seconds = ts if (ts := sleep_time.total_seconds()) > 0.1 else 0.1
                await asyncio.sleep(seconds)  # total_seconds

            self.history.append(datetime.now())

            return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
