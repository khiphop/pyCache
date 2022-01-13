# coding: utf-8
import requests
import json
import sys


def inner_get(node, group, key):
    """
    此处阻塞请求, 需要优化 / need perf: it's a block request
    """
    print('Inner_get')
    try:
        url = 'http://' + str(node) + '/inner/' + str(group) + '/' + str(key)
        r = requests.get(url=url, timeout=0.2)
        d = json.loads(r.content)
        val = d['data']
    except BaseException as err:
        val = ''

    return val


def inner_set(node, group, key, val):
    """
    此处阻塞请求, 需要优化 / need perf: it's a block request
    """
    print('Inner_set')
    try:
        url = 'http://' + str(node) + '/inner'
        data = {
            "group": group,
            "key": key,
            "val": val
        }

        r = requests.post(url=url, data=data, timeout=0.2)
        d = json.loads(r.content)
        val = d['data']
    except BaseException as err:
        val = False

    return val


class Nod:
    def __init__(self, con_hash, group_cache, http_ip, http_port):
        self.con_hash = con_hash
        self.group_cache = group_cache
        self.http_ip = http_ip
        self.http_port = http_port

        self.cmd()

    def cmd(self):
        if len(sys.argv) == 0:
            return False

        for no in range(len(sys.argv)):
            # Data restore
            if sys.argv[no] == '-dr':
                f = open("data.txt")
                line = f.readline()
                while line:
                    # print(line, end='')

                    args = json.loads(line)
                    self.set_dispatch(str(args['g']), str(args['k']), str(args['v']['val']))

                    line = f.readline()

                f.close()

        with open("data.txt", 'w') as f1:
            f1.seek(0)
            f1.truncate()

        return True

    def get_dispatch(self, group, key, inner=False):
        node = self.con_hash.choose_node(key)
        print('Node: ' + node)

        if inner:
            print("It's a inner call")

        if node == str(self.http_ip) + ':' + str(self.http_port) or inner:
            return self.group_cache.gp_get(group, key)
        else:
            return inner_get(node, group, key)
            pass

    def set_dispatch(self, group, key, val, inner=False):
        node = self.con_hash.choose_node(key)
        print('Node: ' + node)

        if inner:
            print("Trigger a inner call")

        if node == str(self.http_ip) + ':' + str(self.http_port) or inner:
            return self.group_cache.gp_set(group, key, val)
        else:
            return inner_set(node, group, key, val)

    def data_persistence(self):
        list_file = './data.txt'
        list_file_handle = open(list_file, mode='w')

        ll, dt = self.group_cache.copy_data()
        for one in ll:
            group_name = one['g']

            for key in one['d']:
                print(key)

                dt[group_name][key]['val'] = dt[group_name][key]['val'].decode()

                list_file_handle.write(json.dumps({'g': group_name, 'k': key, 'v': dt[group_name][key]}) + '\n')

        del ll, dt


if __name__ == '__main__':
    pass
