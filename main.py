from collections import deque
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

    def changeType(self, type, image) -> None:
        if(self.type != 1):
            self.type = type
            self.surf = image
            self.draw()


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
        self.initImages()
        self.initTable()
        pg.font.init()
        self.game()

    def initColors(self) -> None:
        self.backgroundColor = (144, 238, 144)
        self.textColor = (10, 10, 10)

    def initScreen(self) -> None:
        pg.display.set_caption('Trap the Mouse')
        self.screen = pg.display.set_mode((800, 800))
        self.screen.fill(self.backgroundColor)
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
        back_img = pg.image.load("img/back_btn.png").convert_alpha()
        self.back_button = Button(5, 20, 0.5, back_img, self.screen)

    def initImages(self) -> None:
        self.free_hex = pg.image.load("img/green.png").convert_alpha()
        self.mouse_hex = pg.image.load("img/red.png").convert_alpha()
        self.block_hex = pg.image.load("img/brown.png").convert_alpha()
        self.background_img = pg.image.load("img/sobolaur.png").convert()

    def initTable(self) -> None:
        self.table = list()
        matrix = self.generateMatrix()

        for i in range(len(matrix)):
            temp = list()
            for j in range(len(matrix[i])):
                temp.append(Hex(matrix[i][j], i, j))
            self.table.append(temp)

        y = 170
        for i in range(len(self.table)):
            x = 185
            if i % 2 == 1:
                x -= 19
            for j in range(len(self.table[i])):
                if(self.table[i][j].type == 1): continue

                img = None
                if(self.table[i][j].type == 0):
                    img = self.free_hex
                elif(self.table[i][j].type == 3):
                    img = self.block_hex
                elif(self.table[i][j].type == 2):
                    img = self.mouse_hex
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
        self.mouse = [6, 6]
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
        self.screen.fill(self.backgroundColor)
        self.screen.blit(self.background_img, (0, 0))
        self.start_button.draw()
        self.quit_button.draw()

    def drawDifficulty(self) -> None:
        self.screen.fill(self.backgroundColor)
        self.screen.blit(self.background_img, (0, 0))
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
        self.screen.fill(self.backgroundColor)
        self.screen.blit(self.background_img, (0, 0))
        for i in range(len(self.table)):
            for j in range(len(self.table[i])):
                self.table[i][j].draw()

    def resetTable(self) -> None:
        for i in self.table:
            for j in i:
                del(j)
        self.initTable()

    def getFreeSpaces(self) -> list:
        i = self.mouse[0]
        j = self.mouse[1]
        spaces = [1, 2, 3, 4, 5, 6]
        if self.table[i - 1][j].type == 3:
            spaces.remove(1)
        if self.table[i - 1][j - 1].type == 3:
            spaces.remove(2)
        if self.table[i][j + 1].type == 3:
            spaces.remove(3)
        if self.table[i + 1][j - 1].type == 3:
            spaces.remove(4)
        if self.table[i + 1][j].type == 3:
            spaces.remove(5)
        if self.table[i][j - 1].type == 3:
            spaces.remove(6)
        return spaces

    def moveMouseEasy(self, freeSpaces : list) -> None:
        i = self.mouse[0]
        j = self.mouse[1]
        self.table[i][j].changeType(0, self.free_hex)
        space = random.choice(freeSpaces)
        moveX = -1
        moveY = -1
        if space == 1:
            moveX = i - 1
            moveY = j
        if space == 2:
            moveX = i - 1
            moveY = j - 1
        if space == 3:
            moveX = i
            moveY = j + 1
        if space == 4:
            moveX = i + 1
            moveY = j - 1
        if space == 5:
            moveX = i + 1
            moveY = j
        if space == 6:
            moveX = i
            moveY = j - 1
        if(moveX == -1 or moveY == -1):
            print(f'Impossible mouse move')
            exit()
        else:
            self.mouse = [moveX, moveY]
            self.table[moveX][moveY].changeType(2, self.mouse_hex)

    def moveMouseHard(self) -> None:
        def bfs(grid : list, start : tuple) -> list:
            queue = deque([[start]])
            seen = {start}
            while queue:
                path = queue.popleft()
                x, y = path[-1]
                if grid[y][x] == '1':
                    return path
                for x2, y2 in ((x - 1 , y), (x - 1 , y - 1), (x , y - 1), (x, y + 1), (x + 1, y), (x + 1, y - 1)):
                    if (0 <= x2 < 13 and 0 <= y2 < 13 and grid[y2][x2] != '3' and (x2, y2) not in seen):
                        queue.append(path + [(x2, y2)])
                        seen.add((x2, y2))
                        # print(x2, y2)

        grid = list()
        for i in range(len(self.table)):
            temp = str()
            for j in range(len(self.table[i])):
                temp += str(self.table[i][j].type)
            grid.append(temp)

        move = bfs(grid, (self.mouse[0], self.mouse[1]))[1]
        self.table[self.mouse[0]][self.mouse[1]].changeType(0, self.free_hex)
        self.mouse = [move[0], move[1]]
        self.table[move[0]][move[1]].changeType(2, self.mouse_hex)

    def moveMousePvP(self, freeSpaces : list, hex : Hex) -> bool:
        i = self.mouse[0]
        j = self.mouse[1]
        hexI = hex.i
        hexJ = hex.j
        possible = False
        for space in freeSpaces:
            if space == 1:
                if hexI == (i - 1) and hexJ == j:
                    possible = True
            elif space == 2:
                if hexI == (i - 1) and hexJ == (j - 1):
                    possible = True
            elif space == 3:
                if hexI == i and hexJ == (j + 1):
                    possible = True
            elif space == 4:
                if hexI == (i + 1) and hexJ == (j - 1):
                    possible = True
            elif space == 5:
                if hexI == (i + 1) and hexJ == j:
                    possible = True
            elif space == 6:
                if hexI == i and hexJ == (j - 1):
                    possible = True

        if(possible):
            self.mouse = [hexI, hexJ]
            self.table[i][j].changeType(0, self.free_hex)
            self.table[hexI][hexJ].changeType(2, self.mouse_hex)
            return True
        else:
            return False

    def checkMouseWin(self) -> bool:
        i = self.mouse[0]
        j = self.mouse[1]
        if self.table[i - 1][j].type == 1: # Up - Left
            return True
        if self.table[i - 1][j - 1].type == 1: # Up - Right
            return True
        if self.table[i][j + 1].type == 1: # Right
            return True
        if self.table[i + 1][j - 1].type == 1: # Down - Right
            return True
        if self.table[i + 1][j].type == 1: # Down - Left
            return True
        if self.table[i][j - 1].type == 1: # Left
            return True
        return False

    def drawWinScreen(self, text : str) -> None:
        self.screen.fill(self.backgroundColor)
        self.screen.blit(self.background_img, (0, 0))
        font = pg.font.Font(None, 64)
        textSurf = font.render(text, True, self.textColor)
        textpos = textSurf.get_rect(centerx = self.screen.get_width() // 2, y = self.screen.get_height() // 2)
        self.screen.blit(textSurf, textpos)
        self.back_button.draw()

    def game(self) -> None:
        self.drawMenu()
        clock = pg.time.Clock()
        pg.event.set_blocked(None)
        pg.event.set_allowed([pg.QUIT, pg.MOUSEBUTTONDOWN])
        screen = 1
        redraw = False
        difficulty = 1
        player = 1
        winnerText = 'PLACEHOLDER'
        freeSpaces = None
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
                                screen = 3
                                difficulty = 1
                                redraw = True
                            elif(pg.Rect.collidepoint(self.hard_button.rect, event.pos)):
                                screen = 3
                                difficulty = 2
                                redraw = True
                            elif(pg.Rect.collidepoint(self.pvp_button.rect, event.pos)):
                                screen = 3
                                difficulty = 3
                                redraw = True
                        elif(screen == 3):
                            foundHex = False
                            for i in range(len(self.table)):
                                if(foundHex): break
                                for j in range(len(self.table[i])):
                                    if(self.table[i][j].type == 0):
                                        if(pg.Rect.collidepoint(self.table[i][j].rect, event.pos)):
                                            foundHex = True
                                            if(player == 1):
                                                self.table[i][j].changeType(3, self.block_hex)
                                                freeSpaces = self.getFreeSpaces()
                                                if(difficulty == 3):
                                                    player = 0
                                            if(len(freeSpaces) == 0):
                                                winnerText = 'Trapper Won!'
                                                screen = 4
                                                redraw = True
                                                break
                                            else:
                                                if(difficulty == 1):
                                                    self.moveMouseEasy(freeSpaces)
                                                elif(difficulty == 2):
                                                    self.moveMouseHard()
                                                elif(difficulty == 3):
                                                    if(player == 2):
                                                        if(self.moveMousePvP(freeSpaces, self.table[i][j])):
                                                            player = 1
                                                        else:
                                                            break
                                                    elif(player == 0):
                                                        player = 2
                                                        break
                                                    else:
                                                        print(f'Unknown player {player}')
                                                        exit()
                                                else:
                                                    print(f'Unknown difficulty {difficulty}')
                                                    exit()
                                            if(self.checkMouseWin()):
                                                winnerText = 'Mouse Won!'
                                                screen = 4
                                                redraw = True
                                            break
                        elif(screen == 4):
                            if(pg.Rect.collidepoint(self.back_button.rect, event.pos)):
                                screen = 1
                                redraw = True

                if(redraw):
                    if(screen == 1):
                        self.drawMenu()
                    elif(screen == 2):
                        self.drawDifficulty()
                        difficulty = 1
                    elif(screen == 3):
                        self.drawTable()
                    elif(screen == 4):
                        pg.display.update()
                        pg.time.wait(1000)
                        self.drawWinScreen(winnerText)
                        self.resetTable()
                        player = 1
                        winnerText = 'PLACEHOLDER'
                    else:
                        print(f'Unknown screen type: {screen}')
                        exit()
                    redraw = False

                pg.display.update()
                clock.tick(60)


if __name__ == '__main__':
    game = TTM()