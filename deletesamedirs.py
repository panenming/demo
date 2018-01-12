import os
import shutil

if __name__ == '__main__':
    path1 = 'E:/Go/src'
    path2 = 'E:/gopath/src'
    for file in os.listdir(path1):
        #获取文件夹下所有文件，删除另一个文件夹下对应名称的文件
        path = path1 + "/" + file
        if os.path.isdir(path):
            try:
                shutil.rmtree(path2 + "/" + file)
            except Exception as e:
                print(e)
            print(path2 + "/" + file + " 删除")
        if os.path.isfile(path):
            try:
                os.remove(path2 + "/" + file)
            except Exception as e:
                print(e)
            print(path2 + "/" + file  + " 删除")