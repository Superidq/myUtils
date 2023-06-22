"""
批量添加：在第add_position个默认块后添加指定魔数，并重命名文件后缀（可选）
add_position=0时在文件头添加，默认该参数为1
"""
import os

'''在此调整默认参数'''
# 插入的魔数
magic_number = bytes.fromhex("17 02 06 00")
# 是否重命名
rename = True
# 添加魔数位置
add_position = 1
# IO读写默认块大小
default_buffer_size = 4096
# 针对较大文件的高性能模式，不开较稳妥但是慢，开了可能内存爆炸但速度快
high_performance = True


def addNumber(filepath):
    with open(filepath, "rb") as f_src:

        file_size = os.stat(filepath).st_size + len(magic_number)
        print("filesize: ")
        print(file_size)
        # file_size = os.stat(filepath).st_size
        current_size = 0
        with open(filepath + "temp", "wb") as f_dst:

            if add_position == 0:
                f_dst.write(magic_number)
                current_size += len(magic_number)

            n = 0
            while current_size <= file_size:
                data = f_src.read(default_buffer_size)
                f_dst.write(data)
                current_size += len(data)
                # 记录已写入的块的个数
                n += 1
                if n == add_position:
                    f_dst.write(magic_number)
                    current_size += len(magic_number)
                # 高性能模式
                if n == add_position and high_performance:
                    # 如果内存不够就设定为合适倍数的default_buffer_size
                    data = f_src.read()
                    f_dst.write(data)
                    break


def renameFile(filepath):
    fst_portion = os.path.splitext(filepath)[0]
    sec_portion = os.path.splitext(filepath)[1]
    sec_portion += 'S' + str(add_position)
    os.rename(filepath, fst_portion + sec_portion)


if __name__ == "__main__":
    path = r'D:\Downloads\test'
    filenames = os.listdir(path)

    for i in filenames:
        file_path = os.path.join(path, i)
        addNumber(file_path)
        if rename:
            renameFile(file_path)
        print(i)

    print("done.")
