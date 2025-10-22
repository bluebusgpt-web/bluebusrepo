class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def printInfo(self):
        """Return a string representation instead of printing so tests can assert on it."""
        info = f"Person(id={self.id}, name={self.name})"
        print(info)
        return info


class Manager(Person):
    def __init__(self, id, name, title):
        super().__init__(id, name)
        self.title = title

    def printInfo(self):
        info = f"Manager(id={self.id}, name={self.name}, title={self.title})"
        print(info)
        return info


class Employee(Person):
    def __init__(self, id, name, skill):
        super().__init__(id, name)
        self.skill = skill

    def printInfo(self):
        info = f"Employee(id={self.id}, name={self.name}, skill={self.skill})"
        print(info)
        return info
