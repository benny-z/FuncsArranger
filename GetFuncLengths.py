from pprint import pprint
from os import chdir, walk
from os.path import dirname, join, basename
import subprocess
import fnmatch
import re

FUNC_SIZE_NAME_PATTERN = '([\w\d]+)\s\w\s[\d|a-fA-F]+\s([\d|a-fA-F]+)'
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
			o_content = str(subprocess.check_output(['nm' ,'-S', '-f', 'posix', o_f_name]))
			o_content = o_content.replace('\\n', '\n')
			obj_file_basename = basename(o_f_name)
			func_name_to_size += [match.groups() for match in re.finditer(FUNC_SIZE_NAME_PATTERN, o_content)]
		return { k:int(v,16) for k,v in dict(func_name_to_size).items()} 
			
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