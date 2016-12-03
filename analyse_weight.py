# encoding=utf-8

# 提取权重核心函数
# Wang Yulu, 18810656098@163.com

import sys

import jieba.analyse

from file_operations import read_file_to_array, write_file_from_array_of_tuples

# 函数 analyse_weight

def analyse_weight(input_filename, output_filename=""):

	# 打开文本文件,按行读入
	input_lines = read_file_to_array(input_filename)

	# 分析
	result = jieba.analyse.textrank(", ".join(input_lines), topK=500, withWeight=True)

	# 输出

	# 屏幕输出
	print(result)

	# 文件输出
	if (output_filename != ""):
		write_file_from_array_of_tuples(result, output_filename)
		print("\n*\tThe analysed result has been written into file " + output_filename + ".\n")

# 命令行运行入口函数
# 支持通过命令行下形如 python analyse_weight input_filename output_filename 直接调用本函数
if __name__ == "__main__":
	analyse_weight(*sys.argv[1:])
