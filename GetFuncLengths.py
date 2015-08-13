from pprint import pprint
from os import chdir, walk
from os.path import dirname, join, basename
import subprocess
import fnmatch
import re

FUNC_SIZE_NAME_PATTERN = re.compile('([\w\d]+)\s\w\s[\d|a-fA-F]+\s([\d|a-fA-F]+)')
SEPARATOR = "###"

class FuncsLengthsParser:
	def __init__(self, base_dir):
		self.base_dir = base_dir

	def parse(self):
		obj_files_lst = self.get_obj_files_lst()
		return self.get_all_funcs(obj_files_lst)

	def get_all_funcs(self, obj_files_lst):
		chdir(self.base_dir)
		func_name_to_size = []
		for o_f_name in obj_files_lst:
			o_content = subprocess.check_output(['nm' ,'-S', '-f', 'posix', o_f_name])
			obj_file_basename = basename(o_f_name)
			func_name_to_size += self.parse_file(o_content, obj_file_basename)
		return dict(func_name_to_size)
			
	def parse_file(self, f_content, obj_file_name):
		func_to_size_map = []
		for func_name, func_size in re.findall(FUNC_SIZE_NAME_PATTERN, f_content):
			func_to_size_map.append(\
				#('%s%s%s' % (obj_file_name, SEPARATOR, func_name), int(func_size,16)))
				(func_name, int(func_size,16)))
		return func_to_size_map

	def get_obj_files_lst(self):
		matches = []
		for root, dirnames, filenames in walk(self.base_dir):
			for filename in fnmatch.filter(filenames, '*.o'):
				matches.append(join(root, filename))
		return matches

if '__main__' == __name__:
	import sys
	base_dir = sys.argv[1]
	flp = FuncsLengthsParser(base_dir)
	pprint(flp.parse())