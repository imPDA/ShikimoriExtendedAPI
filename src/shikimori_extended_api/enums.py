from enum import Enum


class AnimeStatus(Enum):
    PLANNED = 'planned'
    WATCHING = 'watching'
    REWATCHING = 'rewatching'
    COMPLETED = 'completed'
    ON_HOLD = 'on_hold'
    DROPPED = 'dropped'
