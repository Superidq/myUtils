"""
批量添加：在第add_position个默认块后添加or（添加后）移除指定魔数，并重命名文件后缀 \n
add_position=0时在文件头添加，该参数默认为0, 1, 100（分别破坏文件魔数，文件头结构，以及文件内容）\n
支持多层嵌套添加与移除\n
"""
import os
import time

'''在此调整模式'''
# 增加魔数为True，移除魔数为False
mode_add = True

'''在此调整默认参数，模式更改前后需保持一致！'''
# 插入的魔数
magic_number = bytes.fromhex("17 02 06 00")
# IO读写默认块大小
default_buffer_size = 512
# 针对较大文件的高性能模式，不开较稳妥但是慢，开了可能内存爆炸但速度快
high_performance = True


def addNumber(filepath, add_position):
    if default_buffer_size * add_position > os.stat(filepath).st_size or os.stat(filepath).st_size == 0:
        return False

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
    return True


def delNumber(filepath, add_position):
    # 判断add_position参数与实际已添加的魔数是否一致，不一致则直接结束
    file_suffix = str(os.path.splitext(filepath)[1])
    if not file_suffix.endswith('S' + str(add_position)):
        return -1

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
    return filepath


def renameFile_ADD(filepath, *add_position):
    fst_portion = os.path.splitext(filepath)[0]
    sec_portion = os.path.splitext(filepath)[1]

    for addP in add_position:
        filepath = fst_portion + sec_portion
        sec_portion += 'S' + addP
        os.rename(filepath, fst_portion + sec_portion)

    print(os.path.basename(fst_portion + sec_portion), end=' ')


def renameFile_DEL(filepath, add_position):
    fst_portion = os.path.splitext(filepath)[0]
    sec_portion = str(os.path.splitext(filepath)[1])

    if sec_portion.endswith('S' + str(add_position)):
        sec_portion = sec_portion.rpartition('S')[0]
        os.rename(filepath, fst_portion + sec_portion)
        return fst_portion + sec_portion

    return ''


if __name__ == "__main__":
    # TODO: 加进度条
    start_time = time.perf_counter()

    path = r'D:\Downloads\test1'
    filenames = os.listdir(path)

    # 添加魔数位置
    add_position_a = 0
    add_position_b = 1
    add_position_c = 100

    for i in filenames:
        time_1 = time.perf_counter()
        print(i + " -> ", end='')

        file_path = os.path.join(path, i)
        if mode_add:
            a = addNumber(file_path, add_position_a)
            b = addNumber(file_path, add_position_b)
            c = addNumber(file_path, add_position_c)
            if a and b and c:
                renameFile_ADD(file_path, str(add_position_a), str(add_position_b), str(add_position_c))
            elif a and b and not c:
                renameFile_ADD(file_path, str(add_position_a), str(add_position_b))
            elif a and not b:
                renameFile_ADD(file_path, str(add_position_a))
            elif not a:
                print(i + " 文件过小，跳过", end=' ')

        else:
            # 顺序倒过来
            delNumber(file_path, add_position_c)
            # 更新file_path，方可进入下次
            file_path = renameFile_DEL(file_path, add_position_c)

            delNumber(file_path, add_position_b)
            file_path = renameFile_DEL(file_path, add_position_b)

            delNumber(file_path, add_position_a)
            str1 = (renameFile_DEL(file_path, add_position_a))

            print(os.path.basename(str1), end=' ')

        time_2 = time.perf_counter()
        print("处理时间：%.5f秒" % (time_2 - time_1))

    end_time = time.perf_counter()
    print("\n done. 总处理时间：%.5f秒" % (end_time - start_time))
