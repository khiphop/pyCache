# coding: utf-8
from zlib import crc32
import threading


def str_2_hash(key):
    return abs(crc32(bytes(key, encoding="utf8")))


def handle_node(node):
    return node.split('-')[0]


def pkg_v_node_name(node, no):
    return str(node) + '-vn' + str(no)


class ConHash:
    def __init__(self, v_node_c):
        self.mutex = threading.Lock()

        self.hash_ring_map = {}
        self.hash_ring = []
        self.v_node_c = int(v_node_c)

    def add_nodes(self, nodes=None):
        if nodes is None:
            return False

        for i in range(len(nodes)):
            # add a real node
            self.do_add(nodes[i])
            for v in range(self.v_node_c):
                # add a virtual node
                self.do_add(pkg_v_node_name(nodes[i], v))

        self.hash_ring.sort()

        return self.hash_ring_map

    def do_add(self, node):
        self.mutex.acquire()

        node = str(node)
        nodeHash = str_2_hash(node)

        if nodeHash in self.hash_ring:
            pass
        else:
            self.hash_ring_map[nodeHash] = node
            self.hash_ring.append(nodeHash)

        self.mutex.release()

    def remove_nodes(self, nodes=None):
        if nodes is None:
            return False

        for node in nodes:
            self.do_remove(node)

            for v in range(self.v_node_c):
                self.do_remove(pkg_v_node_name(node, v))

        return self.hash_ring_map

    def do_remove(self, node):
        self.mutex.acquire()

        node = str(node)
        nodeHash = str_2_hash(node)

        self.hash_ring.remove(nodeHash)
        del self.hash_ring_map[nodeHash]

        self.mutex.release()

    def choose_node(self, key):
        self.mutex.acquire()

        keyHash = str_2_hash(key)
        node = self.hash_ring_map[self.hash_ring[0]]

        for nodeHash in self.hash_ring:
            if keyHash < nodeHash:
                node = self.hash_ring_map[nodeHash]
                break
            else:
                continue

        self.mutex.release()

        return handle_node(node)


if __name__ == '__main__':
    pass
