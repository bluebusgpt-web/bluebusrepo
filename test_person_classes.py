import unittest
from person_classes import Person, Manager, Employee


class TestPersonClasses(unittest.TestCase):
    # 아래 테스트들은 사람 상자와 관리자/직원 상자가 잘 동작하는지 확인해요.
    # 각 테스트는 아주 간단하게 '만들고, 읽고, 바꾸는' 것을 봅니다.

    def test_person_info(self):
        # 테스트: 사람 상자를 만들고 정보를 읽어요
        p = Person(1, 'Alice')
        self.assertEqual(p.printInfo(), 'Person(id=1, name=Alice)')

    def test_manager_info(self):
        # 테스트: 관리자 상자를 만들고 제목(title)이 잘 보이는지 확인
        m = Manager(2, 'Bob', 'Team Lead')
        self.assertEqual(m.printInfo(), 'Manager(id=2, name=Bob, title=Team Lead)')

    def test_employee_info(self):
        # 테스트: 직원 상자를 만들고 재주(skill)가 잘 보이는지 확인
        e = Employee(3, 'Carol', 'Python')
        self.assertEqual(e.printInfo(), 'Employee(id=3, name=Carol, skill=Python)')

    def test_manager_is_person(self):
        # 테스트: 관리자도 사람인지(상속 관계) 확인
        m = Manager(4, 'Dave', 'Director')
        self.assertIsInstance(m, Person)

    def test_employee_is_person(self):
        # 테스트: 직원도 사람인지(상속 관계) 확인
        e = Employee(5, 'Eve', 'Testing')
        self.assertIsInstance(e, Person)

    def test_change_name(self):
        # 테스트: 이름을 바꾸면 printInfo에 반영되는지 확인
        p = Person(6, 'Frank')
        p.name = 'Franklin'
        self.assertEqual(p.printInfo(), 'Person(id=6, name=Franklin)')

    def test_change_manager_title(self):
        # 테스트: 관리자의 title을 바꿔서 반영되는지 확인
        m = Manager(7, 'Grace', 'Manager')
        m.title = 'Senior Manager'
        self.assertEqual(m.printInfo(), 'Manager(id=7, name=Grace, title=Senior Manager)')

    def test_change_employee_skill(self):
        # 테스트: 직원의 skill을 바꿔서 반영되는지 확인
        e = Employee(8, 'Heidi', 'Java')
        e.skill = 'Go'
        self.assertEqual(e.printInfo(), 'Employee(id=8, name=Heidi, skill=Go)')

    def test_ids_unique(self):
        # 테스트: 다른 사람을 만들면 id가 다름(간단 체크)
        p1 = Person(9, 'Ivy')
        p2 = Person(10, 'Jack')
        self.assertNotEqual(p1.id, p2.id)

    def test_strict_types(self):
        # 테스트: id와 name에 어떤 타입을 넣어도 그대로 저장되는지 확인
        # (여기서는 타입 검사를 강제하지 않아요)
        p = Person('id_str', 123)
        self.assertEqual(p.id, 'id_str')
        self.assertEqual(p.name, 123)


if __name__ == '__main__':
    unittest.main()
