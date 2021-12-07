import numpy
import random
block = 3
mouse = 2
#tabla goala = 0
#iesire = 1
#mouse = 2
#blocat = 3
class Game:

    def __init__(self,p1,p2):
        self.Tabla = numpy.zeros((13, 13))
        for i in range(13):
            self.Tabla[0][i] = 1
            self.Tabla[12][i] = 1
            self.Tabla[i][0] = 1
            self.Tabla[i][12] = 1
        self.Spawn_Blocks()
        self.Mouse_On_Board(p1,p2)
        print('****************************************')
        self.Generate_Blocks()
        p1,p2 = self.Possible_Moves(p1,p2)
        print('****************************************')
        self.Generate_Blocks()
        p1,p2 = self.Possible_Moves(p1, p2)

    def Mouse_On_Board(self, p1, p2):
        self.Tabla[p1][p2] = mouse
        print(self.Tabla)
        return p1,p2

    def Possible_Moves(self,p1,p2):
        self.Tabla[p1][p2] = 0
        r = random.randint(1,6)
        j = p1
        i = p2
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
        x=5;
        r = random.sample(range(1, 12), x)
        p = random.sample(range(1, 12), x)
        if (r == 6) and (p == 6):
            r = random.randint(1, 12)
            p = random.randint(1, 12)
        for i in range(x):
            self.Tabla[r[i]][p[i]] = block;

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
