import os

# 读取文件路径，一般来说路径过长，因此分成两段
path1 = "D:/Downloads/压缩包/"
path2 = "vvv2"
path = path1 + path2
# 输出到txt文件，txt文件的路径
path_txt = "D:/Downloads/压缩包/list.txt"


if __name__ == '__main__':
    # 打开txt文件
    file_handle = open(path_txt, mode='a', encoding='utf-8')
    file_handle.write("\n" + path2 + ':\n')
    # 打开目标路径
    dataNames = os.listdir(path)
    for i in dataNames:
        filename = os.path.splitext(i)[0]
        print(filename)
        # 第一个 '-' 删除/替换成''
        # filename = filename.replace('-', '') + '\n'
        filename = filename + '\n'
        #       指定位置删除/替换
        #        filename = filename[:3] + '' + filename[4:] + '\n'
        #        print(filename)
        file_handle.write(filename)
