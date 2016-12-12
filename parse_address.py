# encoding=utf-8

# 分析地址函数
# Wang Yulu, 18810656098@163.com

import sys, re

import address_dict

from file_operations import read_file_to_array


# 删除字符串首的特定字符
def remove_initial_char_if_exist(string, char):
	if string[:1] == char:
		return string[1:]
	return string


# 分析地址函数
def parse_address(input_filename, output_filename=""):

	result = [] # 最终结果数组
	working_index = -1 # 正在处理的行index

	# 打开文本文件,按行读入所有地址到 input_lines 数组
	input_lines = read_file_to_array(input_filename)

	# 打开输出文件
	if output_filename:
		output_file = open(output_filename,'w')

	# 处理主循环

	for input_line in input_lines:

		# working_line 为当前正在处理的地址,可能随处理而增删内容
		working_line = input_line

		# working_index 为当前处理行的行号
		working_index += 1

		# 跳过空行
		if working_line == "":
			continue

		result.append(address_dict.parsed_format) # 增加一项地址分析结果空结构

		# 1. 分析城市
		for city in address_dict.cities:
			# 在原文开头查找城市模式
			if working_line[:len(city)] == city: # 找到城市
				working_line = working_line[len(city):] # 分离并去掉城市信息
				working_line = remove_initial_char_if_exist(working_line, "市") # 去除额外的"市"字

		# 2. 分析行政区划

		# 加载区划列表
		for district in address_dict.districts:

			# 在原文的靠前部分查找区划模式
			if working_line.find(district,0,5) != -1: # 找到区划
				result[working_index]['区'] = district # Parse区划
				working_line = working_line[len(district):] # 分离区划

				# 查找是否计算为旧有区划
				for deprecated_district in address_dict.deprecated_districts: # 查找旧区划名称
					if result[working_index]['区'] == deprecated_district[0]: # 找到旧区划
						result[working_index]['区'] = deprecated_district[1]  # 转换为新区划

				working_line = remove_initial_char_if_exist(working_line, "区") # 去除额外的"区"字

				break # 找到区划即可结束找区循环

		# 3. 分析楼号

		# 加载楼号终止词
		for building_stopword in address_dict.building_stopwords:
			# 楼号正则模式
			building_pattern = re.compile("[0-9A-Za-z]*" + building_stopword)
			building = building_pattern.search(working_line)

			if building: # 匹配到模式
				result[working_index]['楼号'] = building.group(0) # Parse楼号
				working_line = re.sub(building_pattern, "[楼号位置]", working_line, count=1) # 标志楼号位置

				result[working_index]['~街道和小区'] = working_line.split("[楼号位置]")[0] # 分离楼号前部分

				result[working_index]['~单元和门牌'] = working_line.split("[楼号位置]")[1] # 分离楼号后部分

				working_line = working_line.replace("[楼号位置]","") # 去除楼号位置标志
				break

		# 4. 分析街道
		for street_stopword in address_dict.street_stopwords:
			# 街道正则模式
			street_pattern = re.compile(".*" + street_stopword)
			# 此处必须贪婪匹配
			street = street_pattern.search(working_line)

			if street: # 匹配到模式
				result[working_index]['街道'] = street.group(0) # Parse街道
				working_line = re.sub(street_pattern, "", working_line) # 去除街道信息
				break

		# 5. 分析小区
			# 街道和小区部分,去除街道即为小区
		result[working_index]['小区'] = result[working_index]['~街道和小区'].replace(result[working_index]['街道'], "")

		# 6. 分析单元和门牌
		# 去除无意义开头标记
		result[working_index]['~单元和门牌'] = remove_initial_char_if_exist(result[working_index]['~单元和门牌'], "#" )
		result[working_index]['~单元和门牌'] = remove_initial_char_if_exist(result[working_index]['~单元和门牌'], "-" )

		# 如果找到"-"标记,分隔
		if result[working_index]['~单元和门牌'].find("-") != -1:
			result[working_index]['单元'] = result[working_index]['~单元和门牌'].split("-")[0]
			result[working_index]['门牌'] = result[working_index]['~单元和门牌'].split("-")[1]
		# 如果找到"单元"标记,分隔
		if result[working_index]['~单元和门牌'].find("单元") != -1:
			result[working_index]['单元'] = result[working_index]['~单元和门牌'].split("单元")[0]
			result[working_index]['门牌'] = result[working_index]['~单元和门牌'].split("单元")[1]
		# 如果未找到任何标记,全计入门牌
		else:
			result[working_index]['门牌'] = result[working_index]['~单元和门牌']

		# 本行工作结果输出
		line_1 = '\n[原文]\n' + input_lines[working_index]\
				 + '\n[区]' + result[working_index]['区']\
				 + '\n[街道]' + result[working_index]['街道']\
				 + '\n[小区]' + result[working_index]['小区']\
				 + '\n[楼号]' + result[working_index]['楼号']\
			     + '\n[单元]' + result[working_index]['单元']\
			     + '\n[门牌]' + result[working_index]['门牌']

		line_2 =  '\n\n[附加信息]'\
				  + '\n[~街道和小区]' + result[working_index]['~街道和小区']\
				  + '\n[~单元和门牌]' + result[working_index]['~单元和门牌']\
				  + '\n[working_line]' + working_line\
				  + '\n'

		print(line_1, line_2)

		# 本行工作文件输出
		if output_filename:
			output_file.writelines(line_1)
			output_file.writelines(line_2)

	if output_filename:
		print("*** Parsed results have been written into file " + output_filename + ". ***\n")

# 命令行运行入口函数
# 支持通过命令行下形如 python parse_address input_filename output_filename 直接调用本函数
if __name__ == "__main__":
	#parse_address(*sys.argv[1:])
	parse_address("test.txt", "output_test1")