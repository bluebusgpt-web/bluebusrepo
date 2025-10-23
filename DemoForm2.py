#Chap10_DemoForm2.py
#Chap10_DemoForm2.ui(화면을 XML문서 저장) + Chap10_DemoForm2.py(로직 코딩) 
import sys 
from PyQt5.QtWidgets import *
from PyQt5 import uic 
import urllib.request
from bs4 import BeautifulSoup  
import re

#디자인 문서를 로딩(파일명을 수정)
form_class = uic.loadUiType("DemoForm2.ui")[0]

#윈도우 클래스 정의(QMainWindow로 상속)
class DemoForm2(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    

    #슬롯메서드 추가
    def firstClick(self):
        #파일에 저장
        f = open("clien.txt", "wt", encoding="utf-8")

        for n in range(0,10):
        #웹사이트 요청
            url = "https://www.clien.net/service/board/sold?&od=T31&category=0&po=" + str(n)
            print(url)

            #페이지 실행 결과
            data = urllib.request.urlopen(url).read()

            #검색이 용이한 객체
            soup = BeautifulSoup(data, 'html.parser')

            list = soup.find_all('span', attrs={"data-role":"list-title-text"})
            for item in list:
                title = item.text.strip()
                print(title)
                f.write(title + "\n")

        f.close()
        self.label.setText("클리앙 중고장터 크롤링 완료")    

    def secondClick(self):
        self.label.setText("두번째 버튼이 클릭되었음")
    
    def thirdClick(self):
        self.label.setText("세번째 버튼이 클릭되었음")


#모듈을 직접 실행했는지를 체크
if __name__ == "__main__":
    app = QApplication(sys.argv)
    demoForm = DemoForm2()
    demoForm.show()
    app.exec_()
