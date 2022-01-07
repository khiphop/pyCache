# coding: utf-8
import threading


def handle_set_val(val):
    return bytes(str(val), encoding='utf8')


def handle_get_val(byte_val):
    if not byte_val:
        return ''

    return byte_val.decode()


class Cac:
    def __init__(self, lru):
        self.struct = {
            'mutex': threading.Lock(),
            'lru': lru,
        }

    def get_cache(self, key):
        key = str(key)
        self.struct['mutex'].acquire()

        r = self.struct['lru'].lru_get(key)
        self.struct['mutex'].release()

        return handle_get_val(r)

    def set_cache(self, key, val):
        self.struct['mutex'].acquire()

        r = self.struct['lru'].lru_set(key, handle_set_val(val))

        self.struct['mutex'].release()

        return r


if __name__ == '__main__':
    pass
