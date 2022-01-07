"""对一致性hash进行学习，构造没有vnode的hash，增加和删除节点以进行观察，会产生对应的雪崩效应"""
from zlib import crc32


class conhashnorep(object):
    def __init__(self, nodes=None, replicas=5):
        """此处nodes代表需要初始化的node列表，为进行对比先提供虚拟节点副本数,ring是存储hash-node的字典，key是存储所有hash值的列表"""
        self.nodes = nodes
        self.replicas = replicas
        self.ring = {}
        self._sorted_keys = []
        self.add_nodes(nodes)

    def _add_node(self, node):
        for i in range(self.replicas):
            # 虚拟节点只是起到了多布置几个节点的效果, 不保证达到均匀分布
            bnode = "%s_vnode%s" % (node, i)
            bnode = bytes(bnode, encoding="utf8")
            nodehash = abs(crc32(bnode))
            self.ring[nodehash] = node
            self._sorted_keys.append(nodehash)
        self._sorted_keys.sort()

    def add_nodes(self, nodes):
        if nodes:
            for node in nodes:
                self._add_node(node)

    def remove_nodes(self, nodes):
        """对于remove的操作，如果直接操作已经产生的ring字典，会比较麻烦，因为ring是{hashnode：node}的键值对形式，
        直接处理涉及到字典直接查找值ring.values()/ring.keys()，以及通过值来remove(key)的操作，太麻烦"""
        if nodes:
            for node in nodes:
                for i in range(self.replicas):
                    bnode = "%s_vnode%s" % (node, i)
                    bnode = bytes(bnode, encoding="utf8")
                    nodehash = abs(crc32(bnode))
                    del self.ring[nodehash]
                    self._sorted_keys.remove(nodehash)

    def get_node(self, key):
        bkey = bytes(key, encoding="utf8")
        keyhash = abs(crc32(bkey))
        i = 0
        for nodehash in self._sorted_keys:
            i += 1
            if keyhash < nodehash:
                # print("%d Keyhash:%s Nodehash:%s" % (i,keyhash,nodehash))
                return self.ring[nodehash]
            else:
                continue
        if i == len(self._sorted_keys):
            # print("None Keyhash:%s Nodehash:%s" % (keyhash,self._sorted_keys[0]))
            return self.ring[self._sorted_keys[0]]

    def count_server(self, number):
        '''server_list用于存放重复出现的server，server_counnt用于统计出现频数'''
        server_list = []
        server_count = {}
        for i in range(number):
            kei = "key_%s" % i
            server = self.get_node(kei)
            server_list.append(server)
        for m in set(server_list):
            server_count[m] = server_list.count(m)
        '''根据字典的键进行排序，如果需要逆序则添加 reverse=True'''
        server_count = dict(sorted(server_count.items(), key=lambda e: e[1], reverse=True))
        print("ServerCount:", server_count)


ini_servers = [
    '127.0.0.1:1',
    '127.0.0.1:2',
    '127.0.0.1:3',
    '127.0.0.1:4',
    # '127.0.0.1:7005',
]
h = conhashnorep(ini_servers)
print(h.ring)

"""构建一些object来观察会分配到哪一个节点"""
# for i in range(20):
part_servers = ['127.0.0.2:1', '127.0.0.2:2']
h.count_server(200)
h.add_nodes(part_servers)
h.count_server(200)
h.remove_nodes(['127.0.0.1:1', '127.0.0.1:2'])
h.count_server(200)
