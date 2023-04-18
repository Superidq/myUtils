import os

path0 = r'D:\Downloads\pz'
path1 = r'D:\Downloads\pz' + '\\'

# 列出当前目录下所有的文件
files = os.listdir(path0)
print('files', files)

for filename in files:
    portion = os.path.splitext(filename)
    # 如果后缀是.txt
    if portion[1] == ".zip":
        # 重新组合文件名和后缀名
        newname = portion[0] + '.zip.del'
        filenamedir = path1 + filename
        newnamedir = path1 + newname
        os.rename(filenamedir, newnamedir)
