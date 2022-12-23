import os
import shutil

dir_path = os.path.dirname(os.path.realpath(__file__))
#↑獲取當前資料夾名稱然後存成dir_path變數

all_file_name = os.listdir(dir_path)
#↑讀取資料夾內所有檔案名稱然後放進all_file_name這個list裡

all_file_name.pop(0)
all_file_name.pop(0)
print(all_file_name)

all_newfile_name = []

# 把所有檔案名稱加上Json存到新的list
for i in all_file_name:
    all_newfile_name.append(i+".json")

for i in range(len(all_file_name)):

    newFileName=shutil.move(all_file_name[i], all_newfile_name[i])

print ("The renamed file has the name:",newFileName)
