from openpyxl import Workbook
 
wb = Workbook
ws = wb.active
row = [-15,-14,-13,-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]    
ws.cell(row = 4, column = 2).value = 'test'
ws.append(row)     
wb.save("C:\\Users\\Brian.tsai\\Desktop\\Python\\STDF\\mapping.xslx")