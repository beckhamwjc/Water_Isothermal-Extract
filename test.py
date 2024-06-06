import os
import re
import unicodedata

with open("2024-03-19 14H46M11S 50wt-Sucrose_50wt-Water_Isothermal0.txt",'rb') as file0:
    file_con=file0.read()
    file=file_con.decode('latin-1')
    all_lines = file.splitlines()
    match0 = all_lines[1]
    tmpr0 = re.split(r'\ ', match0)
    match1 = re.split("=", tmpr0[5])

print(tmpr0[5])
print(match1[0])