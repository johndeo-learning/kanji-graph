#
#
import csv
import sys
import pdb
#pdb.set_trace()
import pprint
import time


class Graph(object):
    """A set of connected nodes. Each node represents a kanji character or primitive."""

    def __init__(self, name, fname):
        self.name = name
        with open(fname, newline='') as f:
            reader = csv.reader(f)
            self.nodes = self.init_nodes(reader)
        self.graph = self.init_graph()
        self.fill_graph(fname)
        self.inverse_fill_primitives()
        self.inverse_fill_mnemonics()
    def init_nodes(self, reader):
        primitiveSet = set([])
        characterSet = set([])
        for row in reader:
            if row[1] == 'character':
                characterSet.add(row[0])
            elif row[1] == 'primitive':
                primitiveSet.add(row[0])
        nodeList = list(characterSet) + list(primitiveSet)
        self.characters = list(characterSet)
        self.primitives = list(primitiveSet)
        return nodeList
    def init_graph(self):
        c_dict = {
            'node_type': 'character',
            'primitives': [],
            'primitive for': [],
            'mnemonics':[],
            'mnemonic for': [],
            'looks like':[],
            'topic':[]
            }
        p_dict = {
            'node_type': 'primitive',
            'primitives': [],
            'primitive for': [],
            'mnemonics':[],
            'mnemonic for': [],
            'looks like':[],
            'topic':[]
            }
        graph = dict.fromkeys(self.characters)
        for key in self.characters:
            graph[key] = {}
            graph[key]['node_type'] = 'character'
            graph[key]['primitives'] = []
            graph[key]['mnemonics'] = []
        p_graph = dict.fromkeys(self.primitives)
        for key in self.primitives:
            graph[key] = {}
            graph[key]['node_type'] = 'primitive'
            graph[key]['primitives'] = []
            graph[key]['mnemonics'] = []
        return graph
    def fill_graph(self, fname):
        graph = self.graph
        with open(fname, newline='') as f:
            reader = csv.reader(f)
            self.file_list = []
            for row in reader:
                self.file_list.append(row)
        for row in self.file_list:
            key = row[0]
            print('key: '+key+' -- node_type: '+graph[key]['node_type'])
            prim_list = []
            mnemonic_list = []
            if (row[2] != '') and (row[2] == 'primitives'):
                for i in range(3,len(row)):
                    if row[i] != '':
                        prim_list.append(row[i])
            elif (row[2] != '') and (row[2] == 'mnemonics'):
                for i in range(3,len(row)):
                    if row[i] != '':
                        mnemonic_list.append(row[i])
            graph[key]['mnemonics'] = mnemonic_list
            print('mnemonics:')
            pprint.pprint(graph[key]['mnemonics'])
            graph[key]['primitives'] = prim_list
            print('primitives:')
            pprint.pprint(graph[key]['primitives'])
        self.graph = graph
        return
    def inverse_fill_primitives(self):
        for primitive in self.primitives:
            characters = []
            for key in self.graph:
                if primitive in self.graph[key]['primitives']:
                    characters.append(key)
            self.graph[primitive]['primitive for'] = characters
        return True
    def inverse_fill_mnemonics(self):
        for mnemonic in self.nodes:
            nodes = []
            for key in self.graph:
                if mnemonic in self.graph[key]['mnemonics']:
                    nodes.append(key)
            self.graph[mnemonic]['mnemonic for'] = nodes
        return True

if __name__ == "__main__":
    command = sys.argv[1]
    graph_file = sys.argv[2]
    if command == '-i':
        try:
            graph = Graph("kanji",graph_file)
            pdb.set_trace()
        except FileNotFoundError:
            print('File not found')
