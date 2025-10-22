from bs4 import BeautifulSoup

page = open("web_test1.html", "rt", encoding="utf-8").read()

soup = BeautifulSoup(page, "html.parser")

print(soup.prettify())

plist = soup.find_all("p")
print(soup.find_all("p", class_="title"))


for tag in soup.find_all("p"):
    title = tag.text_strip()
    print(title)    

