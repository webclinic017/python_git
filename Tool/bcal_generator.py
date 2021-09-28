import tkinter as tk
from tkinter import filedialog
from natsort import natsorted
from os import listdir
from os.path import join
import os
import csv
import re
import shutil 

datalog_file_path = ""
ori_bcal_file_name = ""
def open_datalog_dir():
    global datalog_file_path
    datalog_file_path = filedialog.askdirectory()
    print(datalog_file_path)
    var_datalog_path.set(datalog_file_path)

def open_ori_bcal_file():
    global ori_bcal_file_name
    ori_bcal_file_name = filedialog.askopenfilename()
    print(ori_bcal_file_name)
    var_original_board_cal.set(ori_bcal_file_name)

def gen_pathList(path, flag): 
  if flag == "csv":
    pattern_csv = r'\w*csv\w*'
    path_list = []
    files = listdir(path)
    for f in files:
      # 產生檔案的絕對路徑
        fullpath = join(path, f)
      # 判斷 fullpath 是檔案還是目錄
        if re.search(pattern_csv, fullpath) != None:
            path_list.append(fullpath)
    # print(natsorted(path_list))
    return natsorted(path_list)
  elif flag == "xlsx":
    pattern_xlsx = r'\w*xlsx\w*'
    path_list = []
    files = listdir(path)
    for f in files:
      # 產生檔案的絕對路徑
        fullpath = join(path, f)
      # 判斷 fullpath 是檔案還是目錄
        if re.search(pattern_xlsx, fullpath) != None:
            path_list.append(fullpath)
    print(natsorted(path_list))
    return natsorted(path_list)
  elif flag == "txt":
    pattern_xlsx = r'\w*txt\w*'
    path_list = []
    files = listdir(path)
    for f in files:
      # 產生檔案的絕對路徑
        fullpath = join(path, f)
      # 判斷 fullpath 是檔案還是目錄
        if re.search(pattern_xlsx, fullpath) != None:
            path_list.append(fullpath)
    print(natsorted(path_list))
    return natsorted(path_list)  
  elif flag == "stdf":
    pattern_stdf = r'\w*stdf\w*'
    path_list = []
    files = listdir(path)
    for f in files:
      # 產生檔案的絕對路徑
        fullpath = join(path, f)
      # 判斷 fullpath 是檔案還是目錄
        if re.search(pattern_stdf, fullpath) != None:
            path_list.append(fullpath)
    print(natsorted(path_list))
    return natsorted(path_list) 
# gen_pathList("C:\\Users\\Brian.tsai\\Desktop\\project\\MT6177M\\datalog\\20201204_test")

def conversion():
    # bcal_name_final = "BoardCal_forJason_final.csv"
    try:
        os.remove(ori_bcal_file_name.replace(".csv", "_final.csv"))
    except OSError as e:
        print(e)
    else:
        print("File is deleted successfully")

    golden_start = int(golden_start_entry.get())
    path_list = gen_pathList(datalog_file_path,"csv")
    golden_number = golden_start
    # print(path_list)
    shutil.copyfile(ori_bcal_file_name, ori_bcal_file_name.replace(".csv", "_backup.csv"))
    for file in natsorted(path_list):
        print(file)
        gen_bcal_file(file, golden_number)
        golden_number = golden_number + 1
    os.remove(ori_bcal_file_name)    
    os.rename(ori_bcal_file_name.replace(".csv", "_backup.csv"), ori_bcal_file_name)

def gen_bcal_file(file, golden_start):
  avarege =   int(average_entry.get())
  pattern_testNumber_bcal = r'\w*TestNumber\w*'
  bcal_list = []  
  dict_Bcal = dataDictionary (file, avarege) # test number, data 鍵值對
  with open(ori_bcal_file_name, newline='') as csvfile_bcal: # 打開原始bcal file
    test_number_index = 0
    test_number_bcal_list = []
    rows = csv.reader(csvfile_bcal)
    index = 0
    for row in rows:        
      for i in range (0, len(row), 1):
        if re.search(pattern_testNumber_bcal, row[i]) != None: 
          test_number_index = i # 找出test number 是在第幾欄           
      test_number_bcal_list.append(row[test_number_index]) # 將 "TestNumber"和test number append進去list, index數必須和原始bcal file row數一樣
      try:
        if index == 0:
          row.append("Gold" + str(golden_start)) # 將算出來的平均data append在原始bcal file後面
          print("Gold: " +  str(golden_start) ) # 印出目前是第幾個golden sample, 做記號用
          # print(row)
          bcal_list.append(row)
          index = index +1
        else:
          row.append(str(dict_Bcal[test_number_bcal_list[index]])) # 將算出來的平均data append在原始bcal file後面
          bcal_list.append(row)
          index = index +1
      except KeyError:  
        bcal_list.append(row) # 發生KeyError(因為test_number_bcal_list裡有"")
        index = index +1    
    # print(bcal_list)
    # print(test_number_bcal_list)    
  with open(ori_bcal_file_name, 'w', newline='') as csvfile_bcal_write:    
    writer = csv.writer(csvfile_bcal_write)
    for row in bcal_list:
      # print(row)
      writer.writerow(row) 
  with open(ori_bcal_file_name.replace(".csv", "_final.csv"), 'w', newline='') as csvfile_bcal_write_final:    
    writer = csv.writer(csvfile_bcal_write_final)
    for row in bcal_list:
      # print(row)
      writer.writerow(row)  

def dataDictionary (file, average):
  pattern_testNumber = r'\w*Tests#\w*'
  pattern_PID = r'\w*PID\w*'
  dict_Bcal = {}
  index = 0
  testNumber_list = [] # 全部test number
  data_list = []
  data_list_buffer = [] # 每一列IC(不同PID)的raw data
  data_list_mean = [] # 全部IC的data之平均
  with open(file, newline='') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
      try:
        if re.search(pattern_testNumber, row[0]) != None: 
          testNumber_list = row[10:]
          del testNumber_list[-1]
          # print(testNumber_list)
          # print(len(testNumber_list))
          # print("testNumber_list_length: " + str(len(testNumber_list)))
          data_list = [0] * len(testNumber_list)
          data_list_mean = [0] * len(testNumber_list)
        elif re.search(pattern_PID, row[0]) != None:
          # print("testNumber_list_length: " + str(len(testNumber_list)))
          data_list_buffer = row[10:]
          for i in range (0, len(testNumber_list), 1):
            # print(i)
            # print(data_list_buffer[i])
            # print(float(data_list_buffer[i]))
            try:
              data_list[i] = (data_list[i]) + float(data_list_buffer[i])  
            except ValueError:
              # print(str(i) + ": ValueError")
              continue   
          for i in range (0, len(testNumber_list), 1):
            data_list_mean[i] = data_list[i]/average
          for number in testNumber_list:
            # print(index)
            dict_Bcal[number] = data_list_mean[index] # 做出test number, data 鍵值對
            index = index + 1
          index = 0  
      except IndexError:
        continue
  # print(dict_Bcal.items())  
  return dict_Bcal

# 建立主視窗和 Frame（把元件變成群組的容器）
window = tk.Tk()
window.title('Board cal tool')
window.geometry('1024x768')

header_label = tk.Label(window, text='Board cal calculator')
header_label.pack()

var_datalog_path = tk.StringVar()
datalog_path_frame = tk.Frame(window)
datalog_path_frame.pack(side=tk.TOP)
datalog_path_label_left = tk.Label(datalog_path_frame, text='datalog path')
datalog_path_label_left.pack(side=tk.LEFT)
datalog_path_label_right = tk.Label(datalog_path_frame, textvariable=var_datalog_path, bg='white', fg='red', font=('Arial', 8), width=100, height=1)
datalog_path_label_right.pack(side=tk.RIGHT)
datalog_path_button = tk.Button(datalog_path_frame, text='choose data log dir', command = open_datalog_dir)
datalog_path_button.pack()

average_frame = tk.Frame(window)
average_frame.pack(side=tk.TOP)
average_label = tk.Label(average_frame, text='average number')
average_label.pack(side=tk.LEFT)
average_entry = tk.Entry(average_frame)
average_entry.pack()

var_original_board_cal = tk.StringVar()
Original_board_cal_frame = tk.Frame(window)
Original_board_cal_frame.pack(side=tk.TOP)
Original_board_cal_label_left = tk.Label(Original_board_cal_frame, text='Original board cal file')
Original_board_cal_label_left.pack(side=tk.LEFT)
Original_board_cal_label_right = tk.Label(Original_board_cal_frame, textvariable=var_original_board_cal, bg='white', fg='red', font=('Arial', 8), width=100, height=1)
Original_board_cal_label_right.pack(side=tk.RIGHT)
Original_board_cal_button = tk.Button(Original_board_cal_frame, text='choose original bcal file', command = open_ori_bcal_file)
Original_board_cal_button.pack(side=tk.LEFT)

golden_start_frame = tk.Frame(window)
golden_start_frame.pack(side=tk.TOP)
golden_start_label = tk.Label(golden_start_frame, text='golden start number')
golden_start_label.pack(side=tk.LEFT)
golden_start_entry = tk.Entry(golden_start_frame)
golden_start_entry.pack(side=tk.LEFT)

calculate_btn = tk.Button(window, text='Conversion', command = conversion)
calculate_btn.pack()


# 運行主程式
window.mainloop()