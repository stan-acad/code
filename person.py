from abc import ABC, abstractmethod

class Person(ABC):
    def __init__(self, first_name, middle_name, last_name, age, gender, email, password, birthday, address, phone_number):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self._email = email
        self._password = password
        self._birthday = birthday
        self.address = address
        self._phone_number = phone_number