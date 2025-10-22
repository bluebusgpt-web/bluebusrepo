import unittest
from person_classes import Person, Manager, Employee

class TestPersonClasses(unittest.TestCase):

    def test_person_info(self):
        p = Person(1, 'Alice')
        self.assertEqual(p.printInfo(), 'Person(id=1, name=Alice)')

    def test_manager_info(self):
        m = Manager(2, 'Bob', 'Team Lead')
        self.assertEqual(m.printInfo(), 'Manager(id=2, name=Bob, title=Team Lead)')

    def test_employee_info(self):
        e = Employee(3, 'Carol', 'Python')
        self.assertEqual(e.printInfo(), 'Employee(id=3, name=Carol, skill=Python)')

    def test_manager_is_person(self):
        m = Manager(4, 'Dave', 'Director')
        self.assertIsInstance(m, Person)

    def test_employee_is_person(self):
        e = Employee(5, 'Eve', 'Testing')
        self.assertIsInstance(e, Person)

    def test_change_name(self):
        p = Person(6, 'Frank')
        p.name = 'Franklin'
        self.assertEqual(p.printInfo(), 'Person(id=6, name=Franklin)')

    def test_change_manager_title(self):
        m = Manager(7, 'Grace', 'Manager')
        m.title = 'Senior Manager'
        self.assertEqual(m.printInfo(), 'Manager(id=7, name=Grace, title=Senior Manager)')

    def test_change_employee_skill(self):
        e = Employee(8, 'Heidi', 'Java')
        e.skill = 'Go'
        self.assertEqual(e.printInfo(), 'Employee(id=8, name=Heidi, skill=Go)')

    def test_ids_unique(self):
        p1 = Person(9, 'Ivy')
        p2 = Person(10, 'Jack')
        self.assertNotEqual(p1.id, p2.id)

    def test_strict_types(self):
        # ensure id and name are stored as provided
        p = Person('id_str', 123)
        self.assertEqual(p.id, 'id_str')
        self.assertEqual(p.name, 123)

if __name__ == '__main__':
    unittest.main()
