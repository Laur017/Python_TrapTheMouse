import pygame as pg
import random



class Hex:
    def __init__(self, type : int, i : int, j : int) -> None:
       self.type = type
       self.i = i
       self.j = j

    def initSurface(self, pos : tuple, offset : int, image : pg.Surface, screen : pg.Surface) -> None:
        self.screen = screen
        width = image.get_width()
        height = image.get_height()
        self.rect = pg.Rect((pos[0] + offset, pos[1] + offset), (width - offset, height - offset))
        self.surf = image

    def draw(self) -> None:
        if(self.type != 1):
            self.screen.blit(self.surf, self.rect.topleft)


class Button:
    def __init__(self, x : int, y : int, scale : float, image : pg.Surface, screen : pg.Surface) -> None:
        self.screen = screen
        width = image.get_width()
        height = image.get_height()
        self.surf = pg.transform.scale(image, (int(width * scale), (int(height * scale))))
        self.rect = self.surf.get_rect()
        self.rect.topleft = (x, y)

    def draw(self) -> None:
        self.screen.blit(self.surf, self.rect.topleft)


class TTM:
    def __init__(self) -> None:
        self.initColors()
        self.initScreen()
        self.initButtons()
        self.initTable()
        self.game()

    def initColors(self) -> None:
        self.background = (144, 238, 144)

    def initScreen(self) -> None:
        pg.display.set_caption('Trap the Mouse')
        self.screen = pg.display.set_mode((800, 800))
        self.screen.fill(self.background)
        pg.display.update()

    def initButtons(self) -> None:
        width = self.screen.get_width() // 2 - 50
        start_img = pg.image.load("img/start_btn.png").convert_alpha()
        self.start_button = Button(width, 300, 0.5, start_img, self.screen)
        quit_img = pg.image.load("img/quit_btn.png").convert_alpha()
        self.quit_button = Button(width, 400, 0.5, quit_img, self.screen)
        easy_img = pg.image.load("img/easy_btn.png").convert_alpha()
        self.easy_button = Button(width, 300, 0.5, easy_img, self.screen)
        hard_img = pg.image.load("img/hard_btn.png").convert_alpha()
        self.hard_button = Button(width, 400, 0.5, hard_img, self.screen)
        pvp_img = pg.image.load("img/pvsp_btn.png").convert_alpha()
        self.pvp_button = Button(width, 500, 0.5, pvp_img, self.screen)

    def initTable(self) -> None:
        self.table = list()
        matrix = self.generateMatrix()

        for i in range(len(matrix)):
            temp = list()
            for j in range(len(matrix[i])):
                temp.append(Hex(matrix[i][j], i, j))
            self.table.append(temp)

        free_hex = pg.image.load("img/green.png").convert_alpha()
        mouse_hex = pg.image.load("img/red.png").convert_alpha()
        block_hex = pg.image.load("img/brown.png").convert_alpha()

        y = 150
        for i in range(len(self.table)):
            x = 150
            if i % 2 == 1:
                x -= 19
            for j in range(len(self.table[i])):
                if(self.table[i][j].type == 1): continue

                img = None
                if(self.table[i][j].type == 0):
                    img = free_hex
                elif(self.table[i][j].type == 3):
                    img = block_hex
                elif(self.table[i][j].type == 2):
                    img = mouse_hex
                else:
                    print(f'Unknown number: {self.table[i][j].type}')
                    exit()

                self.table[i][j].initSurface((x, y), 2, img, self.screen)
                x += 40
            if i % 2 == 1:
                x += 19
            y += 36

    def generateMatrix(self) -> list:
        matrix = list()
        for i in range(13):
            temp = list()
            for j in range(13):
                temp.append(0)
            matrix.append(temp)

        for i in range(13):
            matrix[0][i] = 1
            matrix[12][i] = 1
            matrix[i][0] = 1
            matrix[i][12] = 1

        matrix = self.spawnBlocks(matrix, 6)
        matrix[6][6] = 2

        return matrix

    def spawnBlocks(self, matrix : list, x : int) -> list:
        r = random.sample(range(1, 12), x)
        p = random.sample(range(1, 12), x)
        if (r == 6) and (p == 6):
            r = random.randint(1, 12)
            p = random.randint(1, 12)

        for i in range(x):
            matrix[r[i]][p[i]] = 3

        return matrix

    def drawMenu(self) -> None:
        self.screen.fill(self.background)
        self.start_button.draw()
        self.quit_button.draw()

    def drawDifficulty(self) -> None:
        self.screen.fill(self.background)
        self.easy_button.draw()
        self.hard_button.draw()
        self.pvp_button.draw()

    def printTable(self) -> None:
        for i in range(len(self.table)):
            temp = list()
            for j in range(len(self.table[i])):
                temp.append(self.table[i][j].type)
            print(temp)

    def drawTable(self) -> None:
        self.screen.fill(self.background)
        for i in range(len(self.table)):
            for j in range(len(self.table[i])):
                self.table[i][j].draw()

    def game(self) -> None:
        self.drawMenu()
        clock = pg.time.Clock()
        pg.event.set_blocked(None)
        pg.event.set_allowed([pg.QUIT, pg.MOUSEBUTTONDOWN])
        screen = 1
        redraw = False
        while(True):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if(screen == 1):
                            if(pg.Rect.collidepoint(self.quit_button.rect, event.pos)):
                                exit()
                            elif(pg.Rect.collidepoint(self.start_button.rect, event.pos)):
                                screen = 2
                                redraw = True
                        elif(screen == 2):
                            if(pg.Rect.collidepoint(self.easy_button.rect, event.pos)):
                                print('Easy')
                                screen = 3
                                redraw = True
                            elif(pg.Rect.collidepoint(self.hard_button.rect, event.pos)):
                                print('Hard')
                                screen = 3
                                redraw = True
                            elif(pg.Rect.collidepoint(self.pvp_button.rect, event.pos)):
                                print('PVP')
                                screen = 3
                                redraw = True
                        elif(screen == 3):
                            for i in range(len(self.table)):
                                for j in range(len(self.table[i])):
                                    if(self.table[i][j].type == 1): continue
                                    if(pg.Rect.collidepoint(self.table[i][j].rect, event.pos)):
                                        print(i, j)
                if(redraw):
                    if(screen == 1):
                        self.drawMenu()
                    elif(screen == 2):
                        self.drawDifficulty()
                    elif(screen == 3):
                        self.drawTable()
                    else:
                        print(f'Unknown screen type: {screen}')
                        exit()
                    redraw = False

                pg.display.update()
                clock.tick(60)


if __name__ == '__main__':
    game = TTM()