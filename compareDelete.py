"""
删除to_delete目录中的同时出现在两个目录（to_find、to_delete）中的相应文件，只要前面的名字相同就删除而不论其后缀名
本实例是将to_find目录下的.mp4文件与to_delete目录下的.ts文件比较，若文件名相同则删除to_delete目录下的.ts文件
"""
import os

filepath_to_find = r'D:\Downloads'
filepath_to_delete = r'D:\Downloads\Video'


if __name__ == '__main__':
    # 获取to_find目录下所有文件，并特化为指定格式的待删除文件列表
    files_specific = os.listdir(filepath_to_find)
    i = 0
    while i < len(files_specific):
        if os.path.splitext(files_specific[i])[1] != '.mp4':
            files_specific.remove(files_specific[i])
            i -= 1
        i += 1

    delete_files = os.listdir(filepath_to_delete)
    for name in files_specific:
        file_path = filepath_to_delete + r'\\' + os.path.splitext(name)[0] + '.ts'
        if os.path.splitext(name)[0] + '.ts' in delete_files:
            os.remove(file_path)
