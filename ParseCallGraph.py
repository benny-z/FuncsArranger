from pprint import pprint
import re
from collections import namedtuple

CallGraphNode = namedtuple("CallGraphNode", "func_name callers callees")
Call = namedtuple("Call", "func_name num_of_calls")

class ParseCallGraph:
    def __init__(self, graph_txt):
        self.graph_txt = graph_txt
        self.idx_func_map = {}
        self.out_graph    = {}

    num_of_calls = 'num_of_calls'
    f_name = 'f_name'

    starts_with_index_pattern = re.compile('^(\[\d+\])')
    func_starts_with_index_pattern = re.compile('(\[\d+\])(\w+)')
    call_pattern = re.compile('.*(?P<%s>[\d+/\d+|\d+])\s+(?P<%s>\w+).*' % (num_of_calls, f_name))

    def parse(self):
        self.strip_header()
        self.map_func_index_to_name()
        self.parse_call_table()
        pprint(self.out_graph)

    def strip_header(self):
        self.graph_txt = re.split('index .* name', self.graph_txt)[-1]

    def map_func_index_to_name(self):
        # stripping the graph txt from the "index by function name" section
        self.graph_txt, index_str = self.graph_txt.split('Index by function name')
        index_str = filter(lambda x: not re.match(r'^\s*$', x), index_str)
        for index, func_name in re.findall(self.func_starts_with_index_pattern, index_str):
            self.idx_func_map.update({index : func_name})

    def parse_call_table(self):
        for entry in re.split('[---]+', self.graph_txt):
            self.parse_entry(entry)

    def parse_entry(self, entry):
        is_caller = True
        index   = ''
        callers = []
        callees = []
        entry = [line for line in entry.split('\n') if line]
        for line in entry:
            if not line.strip():
                continue
            elif re.match(self.starts_with_index_pattern, line):
                index = re.search(self.starts_with_index_pattern, line).group()
                is_caller = False # all the following entries are functions called by the current one
            else: # either a caller or a callee function
                call = self.parse_call(line)
                if is_caller: # caller
                    callers.append(call)
                else: # callee
                    callees.append(call)
        if index:
            func_name = self.idx_func_map[index]
            self.out_graph.update({func_name : CallGraphNode(func_name, callers, callees)})

    def parse_call(self, call_str):
        m = re.match(self.call_pattern, call_str)
        num_of_calls = m.group(self.num_of_calls)
        func_name = m.group(self.f_name)
        return Call(func_name, num_of_calls)
        

f = open('/media/bennyz/Data/Google Drive/assignments/2014/labC/ex3/anl.txt', 'r')
graph_txt = f.read()
f.close()

pcg = ParseCallGraph(graph_txt)
pcg.parse()
