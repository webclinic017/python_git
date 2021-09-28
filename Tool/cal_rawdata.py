from tool_function import gen_pathList
from tool_function import cal_rawdata
# fileList = gen_fileList("C:\\Users\\Brian.tsai\\Desktop\\Python\\Tool\\chk_boardcal","csv")
path_list = gen_pathList("C:\\Users\\Brian.tsai\\Desktop\\Python\\Tool\\cal_rawdata","csv")
for file in path_list:
    print(file)
    cal_rawdata(file)