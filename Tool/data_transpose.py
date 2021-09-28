from tool_function import gen_pathList
from tool_function import dataDictionary
from natsort import natsorted
import csv
import os
import re

try:
    os.remove("C:\\Users\\Brian.tsai\\Desktop\\Python\\Tool\\data_transpose\\correlation.csv")
except OSError as e:
    print(e)
else:
    print("File is deleted successfully")

pattern_Parameter = r'\w*Parameter\w*'
pattern_Tests = r'\w*Tests\W*\w*'
pattern_Patterns = r'\w*Patterns\w*'
pattern_Unit = r'\w*Unit\w*'
pattern_HighL = r'\w*HighL\w*'
pattern_LowL = r'\w*LowL\w*'
row_Parameter = []
row_Tests = []
row_Patterns = []
row_Unit = []
row_HighL = []
row_LowL = []
path_list = gen_pathList("C:\\Users\\Brian.tsai\\Desktop\\Python\\Tool\\data_transpose","csv")
print(path_list)
with open(path_list[0], newline='') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        # print(row) 
        try:
            if re.search(pattern_Parameter, row[0]) != None:
                row_Parameter = row
            if re.search(pattern_Tests, row[0]) != None:
                row_Tests = row
            if re.search(pattern_Patterns, row[0]) != None:
                row_Patterns = row
            if re.search(pattern_Unit, row[0]) != None:
                row_Unit = row
            if re.search(pattern_HighL, row[0]) != None:
                row_HighL = row    
            if re.search(pattern_LowL, row[0]) != None:
                row_LowL = row                
        except IndexError:
            continue        
    # print(row_Tests)
try:
    os.remove("C:\\Users\\Brian.tsai\\Desktop\\Python\\Tool\\data_analysis\\data.csv")
except OSError as e:
    print(e)
else:
    print("File is deleted successfully")

path_list_1 = gen_pathList("C:\\Users\\Brian.tsai\\Desktop\\Python\\Tool\\data_analysis","csv")
print(path_list_1)
row_final = [] 
num = 0
for file in path_list_1:
    # file.split("\\")[-1]
    list_tmp = ["mean_" + file.split("\\")[-1], "", "", "", "", "", "", "" ,"" ,""]
    dict = dataDictionary(file, 5)
    # print(dict)
    for test_number in row_Tests:
        # print(test_number)
        try: 
            list_tmp.append(dict[test_number])
        except KeyError:
            continue
    # print(list_tmp)
    
    row_tmp = []

    for i in range(0,len(row_Parameter),1):
        if num == 0:
            try:  
                row_tmp.append(row_Parameter[i])
                row_tmp.append(row_Tests[i])
                row_tmp.append(row_Patterns[i])
                row_tmp.append(row_Unit[i])
                row_tmp.append(row_HighL[i])
                row_tmp.append(row_LowL[i])
                row_tmp.append(list_tmp[i])
                # print(row_tmp)
                row_final.append(row_tmp)
                row_tmp = []
            except IndexError:
                continue    
        else:
            try:
                row_tmp = (list_tmp[i])
                row_final[i].append(row_tmp)
                row_tmp = []
            except IndexError:
                continue       
    num = num + 1    
# print(row_final)
with open("C:\\Users\\Brian.tsai\\Desktop\\Python\\Tool\\data_transpose\\correlation.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for row in row_final: 
        # print(row)
        writer.writerow(row) 

