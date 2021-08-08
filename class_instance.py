# -*- coding: utf-8 -*-
class Person(object):
    def __init__(self, initial_age):
        """
        :param initial_age: Gets a int input
        """
        if not isinstance(initial_age, int):
            assert False, 'Input is not a integer'
        self.age = initial_age

    def what_am_i(self):
        """
        :return: returns age group based on age.
        """
        if self.age < 13:
            return 'You are young'
        elif 18 > self.age >= 13:
            return 'You are a teenager'
        else:
            return 'You are an adult'

    def year_passed(self):
        """
        Adds 1 to self.age
        """
        self.age = self.age + 1


age = Person('16')
age.year_passed()
print(age.age)
print(age.what_am_i())
