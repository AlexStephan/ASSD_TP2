from typing import List,Union

Couple = List[int,float]


def fun(c: Couple):
    for i in c:
        print(i)


if __name__ == '__main__':
    fun([2, 4, 5])

