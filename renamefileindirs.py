import os
import re

if __name__ == '__main__':
    path = 'D:/iComeBundle-bundle/iComeBundle-bundle'
    for file in os.listdir(path):
        find = re.compile("_[0-9]*x[0-9]*_@[1-9]x.")
        longName = path + '/' + file
        if os.path.isdir(longName):
            print("not file ", file)
            continue
        if os.path.isfile(longName):
            newName = find.subn(".",longName)
            os.rename(longName,newName[0])

