# encoding=utf-8

# 分析地址函数
# Wang Yulu, 18810656098@163.com

import sys, pprint

import address_dict

from file_operations import read_file_to_array, write_file_from_array



# 分析地址函数

def parse_address(input_filename, output_filename=""):

	result = []
	working_index = -1

	# 打开文本文件,按行读入
	input_lines = read_file_to_array(input_filename)

	# 处理
	for working_line in input_lines:

		# 跳过空行
		if working_line == "":
			continue

		working_index += 1
		result.append(address_dict.parsed_format) # 增加一项地址分析结果空结构

		# 1. 分析城市
		for city in address_dict.cities:
			# 在原文开头查找城市模式
			if working_line[:len(city)] == city: # 找到城市
				working_line = working_line[len(city):] # 分离并去掉城市信息
				if working_line[:1] == '市':
					working_line = working_line[1:] # 去除额外的"市"字

		# 2. 分析行政区划
		# 加载区划列表
		for district in address_dict.districts:

			# 在原文的靠前部分查找区划模式
			if working_line.find(district,0,6) != -1: # 找到区划
				result[working_index]['区'] = district # Parse区划
				working_line = working_line[len(district):] # 分离区划

				for deprecated_district in address_dict.deprecated_districts: # 查找旧区划名称
					if result[working_index]['区'] == deprecated_district[0]: # 找到旧区划
						result[working_index]['区'] = deprecated_district[1]  # 转换为新区划
						working_line = working_line[len(deprecated_district[1]):] # 分离区划

				if working_line[:1] == '区':
					working_line = working_line[1:] # 去除额外的"区"字

				break

		print(input_lines[working_index][:],
			  '\n[区]', result[working_index]['区'],
			  '\n[剩余工作]', working_line,
			  '\n'
			  )

	# 屏幕输出
	# pprint.pprint(result, indent=4)

	# 文件输出
	if (output_filename != ""):
		with open(output_filename,'w') as output_file:
			pprint.pprint(result, stream=output_file, indent=4)
			print("*** Parsed results have been written into file " + output_filename + ". ***\n")

# 命令行运行入口函数
# 支持通过命令行下形如 python parse_address input_filename output_filename 直接调用本函数
if __name__ == "__main__":
	parse_address(*sys.argv[1:])
