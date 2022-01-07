# coding: utf-8
import sys
import time


class Lru:
    def __init__(self, max_size, max_count=0, ttl=0, remover=None):
        self.struct = {
            'max_size': max_size,  # 单位: 字节 / byte
            'max_count': max_count,  # 单位: 字节 / byte
            'used_size': 0,  # 单位: 字节 /byte
            'current_count': 0,  # 单位: 字节 /byte
            'list': [],  # 存 [key] / storage key
            'dict': {},  # 存 {key: val} / storage {key: val}
            'ttl': int(ttl),
            'on_remove': remover,
        }

    def check_size(self):
        """
        python的dict释放不了内存, 有内存泄露的问题
        """
        while 0 < self.struct['max_size'] < self.struct['used_size']:
            self.lru_remove_one()
            self.update_memory_usage()

            # dict键值对的内存释放不了
            break

        while 0 < self.struct['max_count'] < self.struct['current_count']:
            self.lru_remove_one()

    def lru_remove_one(self):
        if len(self.struct['list']) == 0:
            return False

        key = self.struct['list'].pop(-1)
        self.struct['dict'].pop(key)

        if self.struct['on_remove']:
            (self.struct['on_remove'])(key)

        return True

    def lru_set(self, key, val):
        if key in self.struct['dict']:
            self.move_2_head(key)
        else:
            self.struct['list'].insert(0, key)

        self.struct['dict'][key] = {
            'val': val,
            'exp': int(time.time()) + self.struct['ttl'] if self.struct['ttl'] > 0 else 0,
        }

        self.update_memory_usage()

        self.check_size()

        return True

    def lru_get(self, key):
        if key not in self.struct['dict']:
            return ''

        d = self.struct['dict'][key]

        if 'exp' in d:
            if 0 < d['exp'] < time.time():
                self.expire(key)
                self.update_memory_usage()
                return ''

        self.move_2_head(key)

        return d['val']

    def expire(self, key):
        if len(self.struct['list']) == 0:
            return False

        self.struct['list'].remove(key)
        self.struct['dict'].pop(key)

        return True

    def update_memory_usage(self):
        self.struct['used_size'] = int(sys.getsizeof(self.struct['list'])) + int(sys.getsizeof(self.struct['dict']))
        print('memory_usage: ' + str(self.struct['used_size']))

    def update_current_count(self):
        self.struct['current_count'] = int(sys.getsizeof(self.struct['list'])) + int(sys.getsizeof(self.struct['dict']))

    def move_2_head(self, key):
        self.struct['list'].pop(self.struct['list'].index(key))
        self.struct['list'].insert(0, key)

    def on_remove(self, key):
        pass


if __name__ == '__main__':
    pass
