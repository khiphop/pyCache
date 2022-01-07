import threading
from flask import Flask, request
from app.util.lru import Lru
import datetime
import json


def on_remove(key):
    log_file = './onRemove.txt'
    file_handle = open(log_file, mode='a')
    file_handle.write((datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S') + ' | ' + key + '\n')


app = Flask(__name__)
mutex = threading.Lock()


@app.route('/cache/<key>', methods=['GET'])
def getCache(key):
    if request.args is None:
        return ''

    para = {
        'error_code': 200,
        'msg': 'success',
        'data': Lru.lru_get(key)
    }

    return json.dumps(para, ensure_ascii=False, indent=4)


@app.route('/cache', methods=['POST'])
def setCache():
    if request.args is None:
        return ''

    # request body 获取和记录
    args = json.loads(request.get_data().decode('utf-8'))
    key = args['key']
    val = args['val']

    # for i in range(2):
    #     test1(1)

    para = {
        'error_code': 200,
        'msg': 'success',
        'data': Lru.lru_set(key, val),
    }

    return json.dumps(para, ensure_ascii=False, indent=4)


def test1(no):
    mutex.acquire()
    print('test1:' + str(no))
    print('test1:' + str(no))
    print('test1:' + str(no))
    mutex.release()


def test2(no):
    mutex.acquire()
    print('test2:' + str(no))
    print('test2:' + str(no))
    print('test2:' + str(no))
    mutex.release()


if __name__ == "__main__":
    Lru = Lru(1 << 9, 0, 0, on_remove)

    app.run(host='0.0.0.0', port=7000)

    # threads = []
    # for i in range(20):
    #     t = threading.Thread(target=test1, args=(i,))
    #     threads.append(t)
    #     t = threading.Thread(target=test2, args=(i,))
    #     threads.append(t)
    #
    # for i in range(len(threads)):
    #     threads[i].start()
    #
    # for i in range(len(threads)):
    #     threads[i].join()
