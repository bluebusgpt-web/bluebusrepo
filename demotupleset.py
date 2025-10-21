# demoTupleset.py

print("set형식")

a = {1,2,3,4}
b = {3,4,5,6}

print(a)
print(b)
print(a.union(a))
print(a.intersection(b))
print(a.difference(b))


print("--tuple---")
tp=(10,20,30)
print(len(tp))

def times(a,b):
    return a+b, a*b


result = times(3,4)
print(result)


print("--- 형식 변환 ---")
a = set((1,2,3))
print(a)
b=list(a)
b.append(4)
print(b)

print("---dict형식---")
fruits={"apple" : "red", "banana":"yellow"}

#검색
print(fruits["apple"])
#입력
fruits["kiwi"]="green"
print(fruits)
#삭제
del fruits["apple"]
#반복문
for item in fruits.items():
    print(item)
