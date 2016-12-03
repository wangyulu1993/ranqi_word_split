# encoding=utf-8

# 文件操作函数
# Wang Yulu, 18810656098@163.com

import codecs

def read_file_to_array(input_filename):
	lines = codecs.open(input_filename, encoding="utf-8").readlines()
	try:
		lines.remove("\r\n")
	except ValueError:
		pass
	return lines


def write_file_from_array(array_to_write, output_filename):
	output_file = codecs.open(output_filename, mode="w", encoding="utf-8")
	output_file.writelines(str(array_to_write))
	output_file.close()

def write_file_from_array_of_tuples(array_to_write, output_filename):
	output_file = codecs.open(output_filename, mode="w", encoding="utf-8")
	for line in array_to_write:
		output_file.write(str(line)+"\n")
	output_file.close()
