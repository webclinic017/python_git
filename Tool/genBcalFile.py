from tool_function import gen_pathList
from tool_function import gen_bcal_file
from natsort import natsorted
import os

bcal_name_final = "BoardCal_forJason_final.csv"
relative_path = os.getcwd()
try:
    os.remove(relative_path + "\\ori_bcal\\" + bcal_name_final)
except OSError as e:
    print(e)
else:
    print("File is deleted successfully")
    
path_list = gen_pathList(relative_path + "\\gen_bcal","csv")
golden_number = 1
print(path_list)
for file in natsorted(path_list):
    print(file)
    gen_bcal_file(file, golden_number)
    golden_number = golden_number + 1
# dataDictionary(path_list_csv,10)
