from pprint import pprint
import utils
import sys
import GetFuncLengths
import ParseCallGraph
import gen_alg

def run():
	base_dir = sys.argv[1]
	gprof_file_system = sys.argv[2]

	flp = GetFuncLengths.FuncsLengthsParser(base_dir)
	funcs_to_length_map = flp.parse()

	graph_txt = None
	with open(gprof_file_system, 'r') as f:
		graph_txt = f.read()
	if graph_txt is None:
		raise(utils.ERROR_MESSAGE)

	pcg = ParseCallGraph.ParseCallGraph(graph_txt)
	parsed_call_graph, index_to_func_map, func_to_index_map = pcg.parse()

	if parsed_call_graph is None:
		raise(utils.ERROR_MESSAGE)

	if len(funcs_to_length_map) > len(func_to_index_map) + 1:
		# if a function is not called, e.g. "int main()", 
		# it wouldn't appear in the gprof's output in the 
		# section that maps indices to function names.
		# There should be at most 1 such function
		raise(utils.ERROR_MESSAGE)

	index_to_length_map = \
		{func_to_index_map[func_name] : length \
		for func_name, length in funcs_to_length_map.items() if func_name in func_to_index_map.keys()}
	ga = gen_alg.GenAlg(parsed_call_graph, index_to_length_map)
	best_gene = ga.run()
	best_gene = [index_to_func_map[index] for index in best_gene]
	pprint(best_gene)
	# return [index_to_func_map[func.getattr('id')] for func in ordering]

if '__main__' == __name__:
	run()