# coding:utf-8

from app.util.con_hash import ConHash

if __name__ == "__main__":
    Ch = ConHash(5)
    Ch.add_nodes(['192.168.2.69:1111', '192.168.2.69:2222', '192.168.2.69:3333', '192.168.2.69:4444'])
    print(Ch.hash_ring)
    print(Ch.hash_ring_map)

    for i in range(10):
        node = Ch.choose_node('kevin' + str(i))
        print('kevin' + str(i) + ' : ' + node)

    Ch.remove_nodes(['192.168.2.69:1111'])
    print('---------------')

    for i in range(10):
        node = Ch.choose_node('kevin' + str(i))
        print('kevin' + str(i) + ' : ' + node)

    Ch.add_nodes(['192.168.2.69:5555'])
    print('---------------')

    for i in range(10):
        node = Ch.choose_node('kevin' + str(i))
        print('kevin' + str(i) + ' : ' + node)

    # print(Ch.choose_node('allen'))
