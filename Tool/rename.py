from tool_function import gen_pathList
from tool_function import gen_fileList
import os
import shutil
import re

pattern_copy = r'\w*copy\w*'
relative_path = os.getcwd()
# file_list = gen_pathList("C:\\Users\\Brian.tsai\\Desktop\\Python\\Tool\\rename_file","stdf")
# for file in file_list:
#     shutil.copyfile(file, file.replace(".stdf", "_copy.stdf"))

path_list = gen_pathList(relative_path + "\\rename_file","csv")
gold_start = int(input("輸入起始gold的編號: "))
for path in path_list:
    # if re.search(pattern_copy, path) != None:  
    os.rename(path, relative_path + "\\rename_file\\gold" + str(gold_start) + ".csv")
    gold_start = gold_start + 1