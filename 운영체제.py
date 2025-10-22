# 운영체제.py

import os
import glob

print("운영체제 정보:", os.name)

fileName = "c:\\python2025\\test.txt"

if os.path.exists(fileName):
    print("파일크기", os.path.getsize(fileName))
else:
    print("파일이 존재하지 않습니다.") 

print(os.path.abspath('test.txt'))
print(os.path.dirname(fileName))

for fileName in glob.glob("c:\\python2025\\*.txt.py"):
    print(fileName)