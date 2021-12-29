import numpy
import random
import pygame
import time
from hexalattice.hexalattice import *
import matplotlib.pyplot as plt


SCREEN_HEIGHT = 800
SCREEN_WIDTH = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Trap The Mouse')

start_img = pygame.image.load('img/start_btn.png').convert_alpha()
quit_img = pygame.image.load('img/quit_btn.png').convert_alpha()
easy_img = pygame.image.load('img/easy_btn.png').convert_alpha()
medium_img = pygame.image.load('img/medium_btn.png').convert_alpha()
hard_img = pygame.image.load('img/hard_btn.png').convert_alpha()
pvsp_img = pygame.image.load('img/pvsp_btn.png').convert_alpha()
free_hex = pygame.image.load('img/green.png').convert_alpha()
mouse_hex = pygame.image.load('img/red.png').convert_alpha()
block_hex = pygame.image.load('img/brown.png').convert_alpha()

class Button():
    def __init__(self,x,y,image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale ), (int(height * scale))))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def draw(self):

        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False :
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action
start_button = Button(SCREEN_WIDTH / 2 -50,300,start_img, 0.5)
quit_button = Button(SCREEN_WIDTH / 2 -50,400,quit_img, 0.5)
easy_button = Button(SCREEN_WIDTH / 2 -50,100,easy_img, 0.5)
medium_button = Button(SCREEN_WIDTH / 2 -50,200,medium_img, 0.5)
hard_button = Button(SCREEN_WIDTH / 2 -50,300,hard_img, 0.5)
plvspl_button = Button(SCREEN_WIDTH / 2 -50,400,pvsp_img, 0.5)

clock = pygame.time.Clock()
block = 3
mouse = 2
out = 1
# tabla goala = 0
# iesire = 1
# mouse = 2
# blocat = 3
bckg = (144, 238, 144)
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
surface = pygame.Surface(size)
surface.fill(bckg)

class Game:
    #screen.blit(surface, (0, 0))
    #screen.update()
    def __init__(self, x):

        runn = True
        while runn:
            screen.fill((144, 238, 144))
            pygame.display.update()
            p1, p2 = 6, 6
            self.Tabla = numpy.zeros((13, 13))
            for i in range(13):
                self.Tabla[0][i] = out
                self.Tabla[12][i] = out
                self.Tabla[i][0] = out
                self.Tabla[i][12] = out
            self.Spawn_Blocks(x)
            self.Mouse_On_Board(p1, p2)
            bongo = list()

            xx = 150 # i = rand , j = coloana, xx =coloana  yy = rand
            for i in range(13):
                yy = 150
                for j in range(13):
                    if j % 2 == 1:
                        xx -= 20
                    if self.Tabla[i][j] == 0:
                        screen.blit(free_hex, (xx, yy))
                        bongo.append((pygame.Rect((xx + 2, yy + 2), (43, 43)), i, j))
                    elif self.Tabla[i][j] == 3:
                        screen.blit(block_hex, (xx, yy))
                        bongo.append((pygame.Rect((xx + 2, yy + 2), (43, 43)), i, j))
                    elif self.Tabla[i][j] == 2:
                        screen.blit(mouse_hex, (xx, yy))
                        bongo.append((pygame.Rect((xx + 2, yy + 2), (43, 43)), i, j))
                    if j % 2 == 1:
                        xx += 20
                    yy += 36
                xx += 40
            pygame.display.update()



            while(1):
                pygame.display.update()
                #self.Generate_Blocks()
                #self.Verify_If_Win_Mouse(p1, p2)
                #p1, p2 = self.Possible_Moves(p1, p2)
                # self.Mouse_On_Board(p1,p2)
                pygame.event.set_blocked(None)
                pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN])
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        runn = False
                        exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        for i in range(len(bongo)):
                            if (pygame.Rect.collidepoint(bongo[i][0], event.pos)):
                                print(f"Hexagon {i} de tip {self.Tabla[bongo[i][1]][bongo[i][2]]}")
                                if(self.Tabla[bongo[i][1]][bongo[i][2]] == 0):
                                    screen.blit(block_hex, (bongo[i][0].topleft[0] - 2, bongo[i][0].topleft[1] - 2))
                                    self.Generate_Blocks(bongo[i][1],bongo[i][2])
                                break
                        print(f"Mouse Clicked {event}")

                    else:
                        print (event)
                    pygame.display.update()

    def Mouse_On_Board(self, p1, p2):
        self.Tabla[p1][p2] = mouse
        print(self.Tabla)
        return p1, p2

    def Verify_If_Win_Mouse(self, p1, p2):
        j = p1
        i = p2
        if self.Tabla[j - 1][i] == out:
            print("The Mouse escaped the TRAP !")
            exit()
        if self.Tabla[j - 1][i + 1] == out:
            print("The Mouse escaped the TRAP !")
            exit()
        if self.Tabla[j][i - 1] == out:
            print("The Mouse escaped the TRAP !")
            exit()
        if self.Tabla[j][i + 1] == out:
            print("The Mouse escaped the TRAP !")
            exit()
        if self.Tabla[j + 1][i] == out:
            print("The Mouse escaped the TRAP !")
            exit()
        if self.Tabla[j + 1][i + 1] == out:
            print("The Mouse escaped the TRAP !")
            exit()

    def Possible_Moves(self, p1, p2):
        j = p1
        i = p2
        self.Tabla[p1][p2] = 0
        lista = [1, 2, 3, 4, 5, 6]
        if self.Tabla[j - 1][i] == block:
            lista.remove(1)
        if self.Tabla[j - 1][i + 1] == block:
            lista.remove(2)
        if self.Tabla[j][i - 1] == block:
            lista.remove(3)
        if self.Tabla[j][i + 1] == block:
            lista.remove(4)
        if self.Tabla[j + 1][i] == block:
            lista.remove(5)
        if self.Tabla[j + 1][i + 1] == block:
            lista.remove(6)
        if len(lista) < 1:
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
        return self.Mouse_On_Board(p1, p2)
        #self.Tabla[p1][p2] = mouse
        # print(self.Tabla)
        # return p1, p2

    def Spawn_Blocks(self, x):
        r = random.sample(range(1, 12), x)
        p = random.sample(range(1, 12), x)
        if (r == 6) and (p == 6):
            r = random.randint(1, 12)
            p = random.randint(1, 12)
        for i in range(x):
            self.Tabla[r[i]][p[i]] = block

    # def #pozitia in coloana si rand

    def Generate_Blocks(self, a, b):
        # a = int(input("Randul : "))
        # b = int(input("Coloana : "))
        if (self.Tabla[a][b] == mouse) or (self.Tabla[a][b] == block) or (a > 12) or (a < 1) or (b > 12) or (b < 1):
            print("Imposibila aceasta miscare, incercati alte valori ")
            a = int(input("Randul : "))
            b = int(input("Coloana : "))
        self.Tabla[a][b] = block

def main_menu():
    run = True
    while run:
        screen.fill((144, 238, 144))
        if start_button.draw():
            clock.tick(60)
            start()
        if quit_button.draw():
            run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()

    pygame.quit()

def start():
    running = True
    while running:
        screen.fill((144, 238, 144))
        if easy_button.draw():
            clock.tick(60)
            Game(8)
        if medium_button.draw():
            clock.tick(60)
            Game(5)
        if hard_button.draw():
            print("hard")
        if plvspl_button.draw():
            print("pvp")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

if __name__ == '__main__':
    main_menu()
