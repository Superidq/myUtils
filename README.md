# 个人小工具集


## 1. 将文件夹内批量视频文件信息导入到Excel中

>把视频文件的信息（文件名、修改日期、文件大小、视频时长）都导入到一个Excel中，带缩略图（最后一列）

### 1.1 环境配置

- Python 3.9
- Windows 10
- 安装的各类库的版本如下：

|        Package        | Version  |
| :-------------------: | :------: |
|        Pillow         |  9.4.0   |
|      XlsxWriter       |  3.0.9   |
|      et-xmlfile       |  1.1.0   |
|         numpy         |  1.24.2  |
| opencv-contrib-python | 4.7.0.72 |
|     opencv-python     | 4.7.0.72 |
|       openpyxl        |  3.1.2   |
|          pip          |  23.0.1  |
|      setuptools       |  57.0.0  |
|         wheel         |  0.36.2  |

## 1.2 注意事项

- XlsxWriter只能创建新的Excel文件而不能在文件末尾追加，所以与openpyxl结合使用
- 视频名称中不要带有额外的"."，否则会识别失败

# 2.将文件夹内批量视频文件信息导入到txt中

> 把视频文件的文件名导入到一个.txt文件中