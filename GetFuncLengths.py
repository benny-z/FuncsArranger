from pprint import pprint
from os import chdir, walk
from os.path import dirname, join, basename
import subprocess
import fnmatch
import re

FUNC_SIZE_NAME_PATTERN = re.compile('([\w\d]+)\s\w\s[\d|a-fA-F]+\s([\d|a-fA-F]+)')

def parse_file(file_content):
	func_to_size_map = {}
	for func_name, func_size in re.findall(FUNC_SIZE_NAME_PATTERN, file_content):
		func_to_size_map.update({func_name : int(func_size,16) })
	return func_to_size_map

def get_all_funcs(obj_files_lst):
	filename_to_funcs_size = {}
	for o_f_name in obj_files_lst:
		o_file_content = subprocess.check_output(['nm' ,'-S', '-f', 'posix', o_f_name])
		func_name_to_size_map = parse_file(o_file_content)
		filename_to_funcs_size.update({basename(o_f_name) : func_name_to_size_map})
	return filename_to_funcs_size
		

def get_obj_files_lst(base_dir):
	matches = []
	for root, dirnames, filenames in walk(base_dir):
		for filename in fnmatch.filter(filenames, '*.o'):
			matches.append(join(root, filename))
	return matches

if '__main__' == __name__:
	cur_dir = dirname(__file__) or '.'
	chdir(cur_dir)

    gprof_file_system = sys.argv[1]

	obj_files_lst = get_obj_files_lst(cur_dir)
	pprint(get_all_funcs(obj_files_lst))