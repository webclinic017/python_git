from tool_function import gen_pathList
import csv
import re
path_list = gen_pathList("C:\\Users\\Brian.tsai\\Desktop\\Python\\Tool\\chk_boardcal","csv")
# path_list_csv = path_list[0]
start_col = int(input ("請輸入開始欄位(從0開始算): "))
end_col = int(input ("請輸入結束欄位(從0開始算): "))

pattern_LowerLimit = r'\w*LowerLimit\w*'
pattern_UpperLimit = r'\w*UpperLimit\w*'
for file in path_list:
    LowerLimit_index = 0
    UpperLimit_index = 0
    with open(file, newline='') as csv_file: # 打開原始bcal file
        new_row = []
        header_row = []    
        rows = csv.reader(csv_file)
        index = 0
        for row in rows:
            if index == 0:
                for i in range (0, len(row), 1):
                    if re.search(pattern_LowerLimit, row[i]) != None: 
                        LowerLimit_index = i
                        # print(LowerLimit_index)
                    if re.search(pattern_UpperLimit, row[i]) != None: 
                        UpperLimit_index = i
                        # print(UpperLimit_index)
            if index == 0:
                index = index + 1
                header_row = row
                header_row.append("Marking")
                continue
            # print(row)  
            for i in range (start_col, end_col+1, 1):
                if row[LowerLimit_index] != "" and row[i] != "":
                    if float(row[i]) < float(row[LowerLimit_index]):
                        row.append("V")
                    elif float(row[i]) > float(row[UpperLimit_index]):
                        row.append("V")    
            new_row.append(row)
        # print(new_row)
    with open(file.replace(".csv", "_final.csv") , 'w', newline='') as csvfile_bcal_write:    
        writer = csv.writer(csvfile_bcal_write)
        writer.writerow(header_row)
        for row in new_row:
            writer.writerow(row)             
