"""
批量添加：在第add_position个默认块后添加or（添加后）移除指定魔数，并重命名文件后缀（可选）
add_position=0时在文件头添加，该参数默认为0, 1, 100（分别破坏文件魔数，文件头结构，以及文件内容）
支持多层嵌套添加与移除
"""
import os

'''在此调整模式'''
# 增加魔数为True，移除魔数为False
mode_add = True

'''在此调整默认参数，模式更改前后需保持一致！'''
# 插入的魔数
magic_number = bytes.fromhex("17 02 06 00")
# 是否重命名
rename = True
# IO读写默认块大小
default_buffer_size = 512
# 针对较大文件的高性能模式，不开较稳妥但是慢，开了可能内存爆炸但速度快
high_performance = True


def addNumber(filepath, add_position):
    with open(filepath, "rb") as f_src:

        file_size = os.stat(filepath).st_size + len(magic_number)
        current_size = 0
        with open(filepath + "temp", "wb") as f_dst:

            if add_position == 0:
                f_dst.write(magic_number)
                current_size += len(magic_number)

            n = 0
            while current_size < file_size:
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

    os.remove(filepath)
    os.rename(filepath + "temp", filepath)


def delNumber(filepath, add_position):
    with open(filepath, "rb") as f_src:

        file_size = os.stat(filepath).st_size
        current_size = 0
        with open(filepath + "temp", "wb") as f_dst:
            # 用n记录已写的块数
            n = 0
            if add_position == n:
                # 移动读文件指针
                f_src.read(len(magic_number))

            while current_size + len(magic_number) < file_size:
                data = f_src.read(default_buffer_size)
                f_dst.write(data)
                current_size += len(data)
                n += 1
                if n == add_position:
                    # 移动读指针到下一块首
                    f_src.read(len(magic_number))

                if n == add_position and high_performance:
                    data = f_src.read()
                    f_dst.write(data)
                    break

    os.remove(filepath)
    os.rename(filepath + "temp", filepath)


def renameFile_ADD(filepath, *add_position):
    fst_portion = os.path.splitext(filepath)[0]
    sec_portion = os.path.splitext(filepath)[1]

    for addP in add_position:
        filepath = fst_portion + sec_portion
        sec_portion += 'S' + addP
        os.rename(filepath, fst_portion + sec_portion)

    print(os.path.basename(fst_portion + sec_portion))


def renameFile_DEL(filepath):
    fst_portion = os.path.splitext(filepath)[0]
    sec_portion = os.path.splitext(filepath)[1]
    sec_portion = sec_portion.partition('S')[0]

    os.rename(filepath, fst_portion + sec_portion)
    print(os.path.basename(fst_portion + sec_portion))


if __name__ == "__main__":
    path = r'D:\Downloads\test'
    filenames = os.listdir(path)

    # 添加魔数位置
    add_position_a = 0
    add_position_b = 1
    add_position_c = 100

    for i in filenames:
        file_path = os.path.join(path, i)
        if mode_add:
            addNumber(file_path, add_position_a)
            addNumber(file_path, add_position_b)
            addNumber(file_path, add_position_c)
            if rename:
                print(i + " -> ", end='')
                renameFile_ADD(file_path, str(add_position_a), str(add_position_b), str(add_position_c))

        else:
            # 顺序倒过来
            delNumber(file_path, add_position_c)
            delNumber(file_path, add_position_b)
            delNumber(file_path, add_position_a)
            if rename:
                print(i + " -> ", end='')
                renameFile_DEL(file_path)

    print("done.")
