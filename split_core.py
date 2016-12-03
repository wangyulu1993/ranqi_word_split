# encoding=utf-8

# 地址分词核心函数
# Wang Yulu, 18810656098@163.com

import sys

import jieba

from file_operations import read_file_to_array, write_file_from_array

# 函数 split_core
#	作用：将输入文件的每一行都按照指定的分词符号分词
#	输入参数：
#		input_filename - 字符串,输入文件名
#		spearator - 字符串,分词符号，如逗号
#		output_filename - 可选,字符串,输出文件名
#	返回：屏幕打印分词结果
def split_core(input_filename, separator, output_filename=""):

	# 打开文本文件,按行读入
	input_lines = read_file_to_array(input_filename)

	# 分词
	
	split_lines = []

	# 载入自定义词典
	jieba.load_userdict("./test_dicts/dict1.txt")
	
	for input_line in input_lines:
		if input_line != "":
			split_lines.append(separator.join(jieba.cut(input_line)))

	# 输出

	# 屏幕输出
	for split_line in split_lines:
		print(split_line)

	# 文件输出
	if (output_filename != ""):
		write_file_from_array(split_lines, output_filename)
		print("\n*\tThe split lines has been written into file " + output_filename + ".\n")

# 命令行运行入口函数
# 支持通过命令行下形如 python split_core input_filename separator output_filename 直接调用本函数
if __name__ == "__main__":
	split_core(*sys.argv[1:])
