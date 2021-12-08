import numpy
import random
import sys
block = 3
mouse = 2
out = 1
#tabla goala = 0
#iesire = 1
#mouse = 2
#blocat = 3
class Game:

    def __init__(self,p1,p2):
        self.Tabla = numpy.zeros((13, 13))
        for i in range(13):
            self.Tabla[0][i] = out
            self.Tabla[12][i] = out
            self.Tabla[i][0] = out
            self.Tabla[i][12] = out
        self.Spawn_Blocks()
        self.Mouse_On_Board(p1,p2)
        print('****************************************')
        self.Generate_Blocks()
        #self.Verify_If_Win_Mouse(p1,p2)
        p1,p2 = self.Possible_Moves(p1,p2)
        print('****************************************')
        self.Generate_Blocks()
        p1,p2 = self.Possible_Moves(p1, p2)

    def Mouse_On_Board(self, p1, p2):
        self.Tabla[p1][p2] = mouse
        print(self.Tabla)
        return p1,p2

    def Verify_If_Win_Mouse(self, p1, p2):
        j = p1
        i = p2
        if self.Mouse_On_Board(j - 1, i) == out:
            print("The Mouse escaped the TRAP !")
            exit()
        if self.Mouse_On_Board(j - 1, i + 1) == out:
            print("The Mouse escaped the TRAP !")
            exit()
        if self.Mouse_On_Board(j, i - 1) == out:
            print("The Mouse escaped the TRAP !")
            exit()
        if self.Mouse_On_Board(j, i + 1) == out:
            print("The Mouse escaped the TRAP !")
            exit()
        if self.Mouse_On_Board(j + 1, i) == out:
            print("The Mouse escaped the TRAP !")
            exit()
        if self.Mouse_On_Board(j + 1, i + 1) == out:
            print("The Mouse escaped the TRAP !")
            exit()

    def Possible_Moves(self,p1,p2):
        j = p1
        i = p2
        self.Tabla[p1][p2] = 0
        lista = [1,2,3,4,5,6]
        if self.Mouse_On_Board(j - 1, i) == block:
            lista.pop(0)
        if self.Mouse_On_Board(j - 1, i + 1) == block:
            lista.pop(1)
        if self.Mouse_On_Board(j, i - 1) == block:
            lista.pop(2)
        if self.Mouse_On_Board(j, i + 1) == block:
            lista.pop(3)
        if self.Mouse_On_Board(j + 1, i) == block:
            lista.pop(4)
        if self.Mouse_On_Board(j + 1, i + 1) == block:
            lista.pop(5)
        if len(lista)<1:
            print("Congratulations, you trapped the mouse ! ")
            exit()
        else:
            r = random.choice(lista)
            if r == 1:
                p1 = j - 1
                p2 = i
            if r == 2:
                p1 = j - 1
                p2 = i + 1
            if r == 3:
                p1 = j
                p2 = i - 1
            if r == 4:
                p1 = j
                p2 = i + 1
            if r == 5:
                p1 = j + 1
                p2 = i
            if r == 6:
                p1 = j + 1
                p2 = i + 1
            print(r)
        return self.Mouse_On_Board(p1,p2)

    def Spawn_Blocks(self):
        x=5
        r = random.sample(range(1, 12), x)
        p = random.sample(range(1, 12), x)
        if (r == 6) and (p == 6):
            r = random.randint(1, 12)
            p = random.randint(1, 12)
        for i in range(x):
            self.Tabla[r[i]][p[i]] = block

    def Generate_Blocks(self):
        a = int(input("Randul : "))
        b = int(input("Coloana : "))
        if (self.Tabla[a][b] == mouse) or (self.Tabla[a][b] == block) or (a>12) or (a<1) or (b>12) or (b<1):
            print("Imposibila aceasta miscare, incercati alte valori ")
            a = int(input("Randul : "))
            b = int(input("Coloana : "))
        self.Tabla[a][b] = block

if __name__ == '__main__':
    game=Game(6,6)
