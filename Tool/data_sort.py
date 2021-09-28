from tool_function import gen_pathList
from tool_function import dataDictionary
from natsort import natsorted
import csv
import os


try:
    os.remove("C:\\Users\\Brian.tsai\\Desktop\\Python\\Tool\\data_analysis\\data.csv")
except OSError as e:
    print(e)
else:
    print("File is deleted successfully")

path_list = gen_pathList("C:\\Users\\Brian.tsai\\Desktop\\Python\\Tool\\data_analysis","csv")
# print(path_list)
num_dict = 0
num = 0
dict_sort = {}
i = 0
for file in path_list:
    # print(file)
    dict = dataDictionary(file, 10)
    dict_sort[len(dict)] = file
print(dict_sort)
sort_key = sorted(dict_sort.keys(), reverse=True)
print(sort_key)
lists = [[] for _ in range(len(sort_key))] #建出新的空list
# print(lists)
list_dict =  [{} for _ in range(len(sort_key))] #建出新的空dict
# print(list_dict)
# print( dataDictionary(dict_sort[1193], 10))

for i in sort_key:
    list_dict[num_dict] = dataDictionary(dict_sort[i], 10)
    num_dict = num_dict + 1
# print(list_dict)        

list_tmp=[]
for i in range(num_dict):
    lists[num].append(["Test#", "mean"])
    for key in list_dict[num].keys():
        list_tmp.append(key)
        list_tmp.append(list_dict[num][key])
        lists[num].append(list_tmp)
        list_tmp=[]
    num = num +1    
# print(lists)

for key in range (sort_key[0]):
    for i in range (1,num_dict,1):
        try:
            lists[0][key].append(lists[i][key][0]) 
            lists[0][key].append(lists[i][key][1]) 
        except:
            continue    
print(lists[0])            
with open("C:\\Users\\Brian.tsai\\Desktop\\Python\\Tool\\data_analysis\\data.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for row in lists[0]: 
        # print(row)
        writer.writerow(row) 
 