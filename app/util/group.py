# coding: utf-8
import threading
import time
import hashlib
import requests
import json
import copy


def do_http(url):
    """
    此处阻塞请求, 需要优化 / need perf: it's a block request
    """
    try:
        r = requests.post(url=url, timeout=0.2)
        d = json.loads(r.content)
    except BaseException as err:
        d = ''

    return d


def get_back_source_gk(group, key):
    return hashlib.md5(group.encode(encoding='UTF-8')).hexdigest() \
                     + '-' + hashlib.md5(key.encode(encoding='UTF-8')).hexdigest()


class Group:
    def __init__(self, groups):
        self.back_source = {}
        self.back_source_gk = {}
        self.back_source_cd = 5

        self.struct = {
            'mutex': threading.Lock(),
            'map': {}
        }

        for i in range(len(groups)):
            g = groups[i]
            group_name = g['name']
            self.struct['map'][group_name] = g['operator']
            self.back_source[group_name] = g['back_source']

    def gp_get(self, group, key):
        group = str(group)
        if group not in self.struct['map']:
            return ''

        val = self.struct['map'][group].get_cache(key)

        # 触发回源 / trigger back-source
        if not val:
            print('trigger back-source')
            self.struct['mutex'].acquire()

            val = self.on_back_source(group, key)
            if val:
                self.struct['map'][group].set_cache(key, val)

            self.struct['mutex'].release()

        return val

    def gp_set(self, group, key, val):
        group = str(group)
        if group not in self.struct['map']:
            return False

        r = self.struct['map'][group].set_cache(key, val)

        return r

    def on_back_source(self, group, key):
        # 复检数据是否存在 / recheck if val exists
        val = self.struct['map'][group].get_cache(key)
        if val:
            print('recheck if val exists')

            return val

        # 回源cd / back-source cool down
        gk_key = get_back_source_gk(group, key)
        if gk_key in self.back_source_gk and int(self.back_source_gk[gk_key]) > int(time.time()):
            print('back-source cd')

            return ''

        # 回源开始 / indeed start back source
        print('indeed start back source')

        fetch_field = self.back_source[group]['field']

        # async http request
        url = self.back_source[group]['url']
        url = url + '?group=' + str(group) + '&key=' + key
        resp = do_http(url)

        # update back-source cool down
        self.back_source_gk[gk_key] = int(time.time()) + self.back_source_cd

        if not resp:
            return ''

        fields = fetch_field.split('.')
        r = ''

        try:
            for i in range(len(fields)):
                if i == 0:
                    r = resp[fields[i]]
                else:
                    r = r[fields[i]]
        except BaseException as err:
            pass

        return r

    def copy_data(self):
        self.struct['mutex'].acquire()

        ll = []
        dt = {}
        for g in self.struct['map']:
            if len(self.struct['map'][g].struct['lru'].struct['list']) == 0:
                continue

            ll.append(copy.deepcopy({'g': g, 'd': self.struct['map'][g].struct['lru'].struct['list']}))
            # dt.append(copy.deepcopy({'g': g, 'd': self.struct['map'][g].struct['lru'].struct['dict']}))
            dt[g] = copy.deepcopy(self.struct['map'][g].struct['lru'].struct['dict'])

        self.struct['mutex'].release()

        return ll, dt


if __name__ == '__main__':
    pass
