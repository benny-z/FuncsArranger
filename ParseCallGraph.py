import numpy as np
import sys
from pprint import pprint
import re
from collections import namedtuple
from os.path import dirname
from os import chdir

CallGraphNode = namedtuple("CallGraphNode", "func_name callers callees")
Call = namedtuple("Call", "func_name num_of_calls")

class ParseCallGraph:
    def __init__(self, graph_txt):
        self.graph_txt = graph_txt
        self.index_to_func = {}
        self.func_to_index = {}
        self.calls_mat     = {}

    num_of_calls = 'num_of_calls'
    f_name = 'f_name'

    starts_with_index_pattern = re.compile('^(\[\d+\])')
    func_starts_with_index_pattern = re.compile('(\[\d+\])(\w+)')
    call_pattern = re.compile('.*(?P<%s>[\d+/\d+|\d+])\s+(?P<%s>\w+).*' % (num_of_calls, f_name))

    def parse(self):
        self.strip_header()
        self.map_func_index_to_name()
        self.func_to_index = {v:k for k,v in self.index_to_func.items()}
        self.init_calls_mat()
        self.parse_call_table()
        return self.calls_mat, self.index_to_func, self.func_to_index

    def init_calls_mat(self):
        x = len(self.index_to_func)
        self.calls_mat = np.zeros((x,x))

    def strip_header(self):
        self.graph_txt = re.split('index .* name', self.graph_txt)[-1]

    def map_func_index_to_name(self):
        # stripping the graph txt from the "index by function name" section
        self.graph_txt, index_str = self.graph_txt.split('Index by function name')
        index_str = filter(lambda x: not re.match(r'^\s*$', x), index_str)
        for index, func_name in re.findall(self.func_starts_with_index_pattern, index_str):
            self.index_to_func.update({int(self.strip_func_index(index)) : func_name})

    def parse_call_table(self):
        for entry in re.split('[---]+', self.graph_txt):
            self.parse_entry(entry)

    def strip_func_index(self, func_index):
        return func_index.replace('[','').replace(']','')

    def parse_entry(self, entry):
        is_caller = True
        func_index = ''
        callers = []
        callees = []
        entry = [line for line in entry.split('\n') if line]
        for line in entry:
            if not line.strip():
                continue
            elif re.match(self.starts_with_index_pattern, line):
                func_index = re.search(self.starts_with_index_pattern, line).group()
                is_caller = False # all the following entries are functions called by the current one
            else: # either a caller or a callee function
                call = self.parse_call(line)
                if is_caller: # caller
                    callers.append(call)
                else: # callee
                    callees.append(call)

        if func_index:
            for callee in callees:
                calle_func_name = callee[0]
                callee_index = self.func_to_index[calle_func_name]
                func_index = int(self.strip_func_index(func_index))
                func_index -= 1
                callee_index -= 1
                self.calls_mat[func_index, callee_index] = callee[1]
                # what should we do with the "caller"?

    def parse_call(self, call_str):
        m = re.match(self.call_pattern, call_str)
        num_of_calls = m.group(self.num_of_calls)
        func_name = m.group(self.f_name)
        return func_name, num_of_calls
        


def main():
    cur_dir = dirname(__file__) or '.'
    chdir(cur_dir)

    gprof_file_system = sys.argv[1]

    graph_txt = None
    with open(gprof_file_system, 'r') as f:
        graph_txt = f.read()
    
    if graph_txt is None:
        raise("WTF?!")

    pcg = ParseCallGraph(graph_txt)
    parsed_call_graph = pcg.parse()
    pprint(parsed_call_graph)

if '__main__' == __name__:
    main()