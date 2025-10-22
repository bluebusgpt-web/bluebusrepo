# coding:utf-8
from bs4 import BeautifulSoup
import urllib.request
import re 

#User-Agent를 조작하는 경우(아이폰에서 사용하는 사파리 브라우져의 헤더) 
hdr = {'User-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.23 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1'}

for n in range(1,11):
        #클리앙의 중고장터 주소 
        data ='https://www.todayhumor.co.kr/board/list.php?table=bestofbest&page=' + str(n)
        #웹브라우져 헤더 추가 
        req = urllib.request.Request(data, headers = hdr)
        data = urllib.request.urlopen(req).read()

        #한글이 깨지는 경우
        page = data.decode('utf-8', 'ignore')
        soup = BeautifulSoup(page, 'html.parser')
        list = soup.findAll('td', attrs={"class":"subject"})

        for item in list:
                try:
                    title = item.find("a").text.strip()
                    print(title)
                    if (re.search('한국', title)):
                        print(title.strip())
                except:
                        pass
# <td class="subject"><a href="/board/view.php?table=bestofbest&amp;no=480941&amp;s_no=480941&amp;page=2" target="_top">새벽 출근</a><span class="list_memo_count_span"> [20]</span>  <span style="margin-left:4px;"><img src="//www.todayhumor.co.kr/board/images/list_icon_photo.gif" style="vertical-align:middle; margin-bottom:1px;"> </span><img src="//www.todayhumor.co.kr/board/images/list_icon_pencil.gif?2" alt="창작글" style="margin-right:3px;top:2px;position:relative"> </td>
