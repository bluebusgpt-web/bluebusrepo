# db1.py

import sqlite3

#임시 메모리에서 데이터베이스 연결 작업
con = sqlite3.connect(':memory:')

#구문을 실행할 커서 객체 생성
cur = con.cursor()

#테이블 생성
cur.execute('CREATE TABLE PhoneBook (name text, phonenumber text);')

#
cur.execute("INSERT INTO PhoneBook VALUES ('홍길동', '010-1234-5678');")


#다중의 행 입력
datalist = (("이순신", "010-2345-6789"),("강감찬", "010-3456-7890"))
cur.executemany("INSERT INTO PhoneBook VALUES (?, ?);", datalist)



#데이터 조회
for row in cur.execute('SELECT * FROM PhoneBook;'):
    print(row)  
