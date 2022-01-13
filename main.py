# coding: utf-8
import datetime
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from app.util.cac import Cac
from app.util.con_hash import ConHash
from app.util.group import Group
from flask import Flask, request
from app.util.nod import Nod
from common.readconfig import ReadConfig

app = Flask(__name__)


# remover defined by you
def on_remove(key):
    print('on_remove')
    log_file = './onRemove.txt'
    file_handle = open(log_file, mode='a')
    file_handle.write((datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S') + ' | ' + key + '\n')


def resp(code=0, msg='success', data=None):
    para = {
        'error_code': code,
        'msg': msg,
        'data': data
    }

    return json.dumps(para, ensure_ascii=False, indent=4)


@app.route('/inner/<group>/<key>', methods=['GET'])
def get_cache(group, key):
    if not group or not key:
        return resp(4000, 'fail')

    val = Nd.get_dispatch(group, key, True)

    return resp(0, 'success', val)


@app.route('/cache/<group>/<key>', methods=['GET'])
def inner_get(group, key):
    if not group or not key:
        return resp(4000, 'fail')

    val = Nd.get_dispatch(group, key)

    return resp(0, 'success', val)


@app.route('/cache', methods=['POST'])
def set_cache():
    if request.args is None:
        return resp(4000, 'fail')

    # args = json.loads(request.get_data().decode('utf-8'))
    # rs = Nd.set_dispatch(str(args['group']), str(args['key']), str(args['val']))

    group = request.form['group']
    key = request.form['key']
    val = request.form['val']

    Nd.set_dispatch(str(group), str(key), str(val))

    return resp(0, 'success', True)


@app.route('/inner', methods=['POST'])
def inner_set():
    if request.args is None:
        return resp(4000, 'fail')

    # args = json.loads(request.get_data().decode('utf-8'))
    group = request.form['group']
    key = request.form['key']
    val = request.form['val']

    rs = Nd.set_dispatch(str(group), str(key), str(val), True)

    return resp(0, 'success', rs)


@app.route('/node/<ip>/<port>', methods=['POST'])
def add_node(ip, port):
    if not ip or not port:
        return resp(4000, 'fail')

    return resp(0, 'success', ConHa.add_nodes([str(ip) + ':' + str(port)]))


@app.route('/node/<ip>/<port>', methods=['DELETE'])
def remove_node(ip, port):
    if not ip or not port:
        return resp(4000, 'fail')

    return resp(0, 'success', ConHa.remove_nodes([str(ip) + ':' + str(port)]))


@app.route('/data', methods=['PUT'])
def data_persistence():
    Nd.data_persistence()

    return resp(0, 'success')


def get_rule():
    return [
        {
            'name': 'room',
            'size': 1 << 9,
            'ttl': 172800,
            'back_source': {
                'url': 'http://192.168.2.69:8001',
                'field': 'data.title',
            },
        },
        {
            'name': 'user',
            'size': 1 << 20,
            'ttl': 172800,
            'back_source': {
                'url': 'http://192.168.2.69:8001',
                'field': 'data.version',
            },
        },
    ]


if __name__ == "__main__":
    try:
        Conf = ReadConfig()
        self_ip = Conf.get_config('http', 'ip')
        self_port = Conf.get_config('http', 'port')

        ConHa = ConHash(Conf.get_config('con_hash', 'v_node_c'))
        ConHa.add_nodes([str(self_ip) + ':' + str(self_port)])

        groups = []
        rules = get_rule()

        for i in range(len(rules)):
            g = rules[i]
            groups.append({
                'name': g['name'],
                'operator': Cac(g['size'], g['ttl'], 0, on_remove),
                'back_source': g['back_source'],
            })

        Nd = Nod(ConHa, Group(groups), self_ip, self_port)

        app.run(host='0.0.0.0', port=self_port, threaded=True, debug=False)
    except BaseException as err:
        print('__main__ exception: ')
        print(err)
    finally:
        pass
