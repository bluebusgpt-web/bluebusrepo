class Person:
    # 사람을 나타내는 상자(틀)입니다.
    # id랑 name을 가집니다.
    # 아이 설명: "사람"이라는 상자에 숫자표(id)와 이름(name)을 넣을 수 있어요.
    def __init__(self, id, name):
        # 이 줄은 상자에 값을 넣는 부분이에요.
        # id는 사람을 구별하는 숫자나 글자, name은 사람 이름이에요.
        self.id = id
        self.name = name

    def printInfo(self):
        """사람 정보를 보기 쉬운 글자로 만듭니다.

        주석(아이용): 이 함수는 상자 속에 든 이름과 번호를
        "Person(id=번호, name=이름)" 같은 글자로 보여주고
        그 글자를 화면에 출력하고 돌려줘요.
        """
        info = f"Person(id={self.id}, name={self.name})"
        # 화면에 글자 보여주기
        print(info)
        # 테스트를 위해 같은 문자열을 돌려줘요(리턴)
        return info


class Manager(Person):
    # Manager는 Person을 물려받아요(=사람이면서 특별한 직함을 가짐)
    # 아이 설명: '관리자'는 사람 상자와 같지만 'title'이라는 작은 표지가 추가돼요.
    def __init__(self, id, name, title):
        # 부모(Person)에서 id랑 name을 받아와요
        super().__init__(id, name)
        # title은 관리자 이름표 같은 거예요 (예: 팀장)
        self.title = title

    def printInfo(self):
        # 관리자 정보를 읽기 쉬운 글자로 만들어요
        info = f"Manager(id={self.id}, name={self.name}, title={self.title})"
        print(info)
        return info


class Employee(Person):
    # Employee는 Person을 물려받아요(=사람이면서 기술이 있음)
    # 아이 설명: '직원'은 사람 상자와 같지만 'skill'이라는 재주 표시가 있어요.
    def __init__(self, id, name, skill):
        super().__init__(id, name)
        # skill은 잘 하는 것(예: 'Python')을 적는 곳이에요.
        self.skill = skill

    def printInfo(self):
        # 직원 정보를 읽기 쉬운 글자로 만들어요
        info = f"Employee(id={self.id}, name={self.name}, skill={self.skill})"
        print(info)
        return info
