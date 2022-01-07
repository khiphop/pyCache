# coding:utf-8

import socket
from zlib import crc32
from app.util.con_hash import ConHash

if __name__ == "__main__":
    Ch = ConHash(5)
    Ch.add_nodes(['192.168.2.69:8001', '192.168.2.69:8002', '192.168.2.69:3', '192.168.2.69:4', '192.168.2.69:5'])
    print(Ch.hash_ring)
    print(Ch.hash_ring_map)

    for i in range(10):
        print(Ch.choose_node('kevin' + str(i)))

    Ch.remove_nodes(['192.168.2.69:8001'])
    print('---------------')

    for i in range(10):
        print(Ch.choose_node('kevin' + str(i)))
    # print(Ch.choose_node('allen'))

