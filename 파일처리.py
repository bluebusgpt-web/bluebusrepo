f = open("demo.txt", "wt", encoding="utf-8")
f.write("첫번째\n두번째\n세번째\n")
f.close()

f = open("demo.txt", "rt", encoding="utf-8")
result = f.read()
print(result)
f.close() 

