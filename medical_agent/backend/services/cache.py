import time
from dataclasses import dataclass
from typing import Dict, Generic, Optional, TypeVar

K = TypeVar("K")
V = TypeVar("V")


@dataclass
class _CacheEntry(Generic[V]):
    value: V
    expires_at: float


class TTLCache(Generic[K, V]):
    def __init__(self, ttl_seconds: int):
        self._ttl_seconds = ttl_seconds
        self._data: Dict[K, _CacheEntry[V]] = {}

    def get(self, key: K) -> Optional[V]:
        entry = self._data.get(key)
        if not entry:
            return None
        if entry.expires_at < time.time():
            self._data.pop(key, None)
            return None
        return entry.value

    def set(self, key: K, value: V) -> None:
        self._data[key] = _CacheEntry(value=value, expires_at=time.time() + self._ttl_seconds)

    def clear(self) -> None:
        self._data.clear()
