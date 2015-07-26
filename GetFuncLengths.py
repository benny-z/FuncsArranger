from os import chdir, walk
from os.path import dirname, join
import subprocess
import fnmatch

def get_all_funcs(obj_files_lst):
	for o_f_name in obj_files_lst:
		result = subprocess.check_output(['nm' ,'-S', '-f', 'posix', o_f_name])
		print(result)

def get_obj_files_lst(base_dir):
	matches = []
	for root, dirnames, filenames in walk(base_dir):
		for filename in fnmatch.filter(filenames, '*.o'):
			matches.append(join(root, filename))
	return matches

if '__main__' == __name__:
	cur_dir = dirname(__file__)
	chdir(cur_dir)

	obj_files_lst = get_obj_files_lst(cur_dir)
	get_all_funcs(obj_files_lst)