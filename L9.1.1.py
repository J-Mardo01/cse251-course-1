import subprocess
import pickle

class Person():
    def __init__(self, name, age, height):
        self.name = name
        self.age = age
        self.height = height
        self.children = []
        self.favorite_child = -1

    def add_child(self, name, age, height):
        self.children.append(Person(name, age, height))

    def favorite_child_award(self, index:int):
        self.favorite_child = index


def main():
    data = {
        "name": "Jon Mardo",
            "age": 24,
            "height": 1.77,
            "children": [
                {
                    "name": "Jon III",
                    "age": 7
                },
                {
                    "name": "Chase",
                    "age": 0
                }
            ],
            "favorite_child": [0]
    }
    b = pickle.dumps(data)
    print(data)
    print(type[data])
    print(b)
    print(type[b])

    with open("jon.json", "w") as file:
        file.write(str(data))
    
    with open("jon.bin", "rb") as file:
        new_bytes = file.read()

    jon = Person("Jon", 24, 1.77)
    jon.add_child("Jon III", 7, 1)
    jon.add_child("Chase", 0, 0)
    jon.favorite_child_award(0)

    jon_bytes = pickle.dumps(jon)
    with open("jon.obj", "wb") as file:
        file.write(jon_bytes)


if __name__ == "__main__":
    main()