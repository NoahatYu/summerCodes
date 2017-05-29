class Board(object):
    a = [["*", "*", "*"], ["*", "*", "*"], ["*", "*", "*"]]

    def __init__(self, a):
        self.a = a

    def printboard(self):
        a = [["*", "*", "*"], ["*", "*", "*"], ["*", "*", "*"]]
        print(a[0][0] + "|" + a[0][1] + "|" + a[0][2])
        print(a[1][0] + "|" + a[1][1] + "|" + a[1][2])
        print(a[2][0] + "|" + a[2][1] + "|" + a[2][2])

    ####   a[x][y] = "Y"


    printboard(self)