# coding: utf-8
import threading

from pyCache.app.util.lru import Lru


def handle_set_val(val):
    return bytes(str(val), encoding='utf8')


def handle_get_val(byte_val):
    if not byte_val:
        return ''

    return byte_val.decode()


class Cac:
    def __init__(self, max_size, c=0, ttl=0, remover=None):
        self.mutex = threading.Lock()
        self.lru = Lru(max_size, c, ttl, remover)

    def get_cache(self, key):
        key = str(key)
        self.mutex.acquire()

        r = self.lru.lru_get(key)
        self.mutex.release()

        return handle_get_val(r)

    def set_cache(self, key, val):
        self.mutex.acquire()

        r = self.lru.lru_set(key, handle_set_val(val))

        self.mutex.release()

        return r


if __name__ == '__main__':
    pass
