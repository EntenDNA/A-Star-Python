import pygame
import os
pygame.init()

fgröse = 25
gröse = 30
field = [["O" for fb in range(fgröse)] for fb in range(fgröse)]

class Node():
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.g = 0
        self.h = 0
        self.f = 0

        self.parent = None
        self.closed = False
        self.walkable = True

def get_neighbours(cnode):

    global neighbours
    neighbours = []

    mask = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    mask2 = [(-1,0),(0,-1),(0,0),(0,1),(1,0)]

    for tup_mask in mask:

        # tupel
        addx, addy = tup_mask
        addedx, addedy = addx + cnode.x, addy + cnode.y

        if addedx >= 0 and addedy >= 0 and addedx < fgröse and addedy < fgröse and field[addedy][addedx] != "X":
            neighbours.append(Node(addedx, addedy))

    return neighbours

def distance(cnode, enode):

    dstX = abs(cnode.x-enode.x)
    dstY = abs(cnode.y-enode.y)

    if dstX > dstY:
        return 20 * dstY + 10 * (dstX-dstY)
    return 20 * dstX + 10 * (dstY-dstX)

def retrace(startn, endn):
    global path
    path = []
    current = endn
    while (current.x, current.y) != (startn.x, startn.y):
        path.append(current)
        current = current.parent

    path.reverse()
    return path

start = Node(1,1)
end = Node(23,19)

s = 0
z = 0
x = 1
y = 1

LEFT = 1
RIGHT = 3

weis = (255,255,255)
schwarz = (0,0,0)
grün = (50,205,50)
rot = (255,0,0)
blau = (0,0,255)
white2 = (255,235,205)
brown = (139,69,19)

field[start.y][start.x] = "S"
field[end.y][end.x] = "E"

opened = []
closed = []

width = fgröse * gröse + (fgröse - 1) * 1
height = fgröse * gröse + (fgröse - 1) * 1
screen = pygame.display.set_mode((width, height))

opened.append(start)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            os._exit(1)

        if pygame.mouse.get_pressed()[0]:
            try:
                pos = pygame.mouse.get_pos()
                mx, my = pos
                mx = int((mx-(int(mx/gröse)*1))/gröse)
                my = int((my-(int(my/gröse)*1))/gröse)

                if field[my][mx] == "O" and pygame.Surface.get_at(screen, pos) != schwarz:
                    pygame.draw.rect(screen, schwarz, (mx*gröse+(mx*1)+1, my*gröse+(my*1)+1, gröse, gröse))
                    field[my][mx] = "X"

                """elif field[my][mx] == "X":
                    field[my][mx] = "O"
                    pygame.draw.rect(screen, weis, (mx*gröse+(mx*1)+1, my*gröse+(my*1)+1, gröse, gröse))"""
            except:
                pass

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
            while True:
                pygame.time.wait(1)

                global current
                try:
                    current = opened[0]
                except:
                    print("No way found")
                    found = False
                    break

                for i in range(len(opened)):

                    if (opened[i].f < current.f) or (opened[i].f == current.f and opened[i].h < current.h):
                        current = opened[i]

                opened.remove(current)
                closed.append(current)

                if (current.y, current.x) not in [(start.y, start.x), (end.y, end.x)]:
                    pygame.draw.rect(screen, brown, (current.x*gröse+(current.x*1)+1, current.y*gröse+(current.y*1)+1, gröse, gröse))
                    pygame.display.update()
                    pygame.time.wait(10)

                if (current.x, current.y) == (end.x, end.y):
                    end.parent = current
                    found = True
                    retrace(start, end)
                    for node in path[:-2]:
                        y, x = node.y, node.x
                        pygame.draw.rect(screen, blau, (x*gröse+(x*1)+1, y*gröse+(y*1)+1, gröse, gröse))
                        pygame.display.update()
                        pygame.time.wait(30)

                    break

                closed_cords = set()

                for closd in closed:
                    closed_cords.add((closd.y, closd.x))

                for neighbour in get_neighbours(current):
                    if (neighbour.y, neighbour.x) in closed_cords:
                        continue

                    newMovementCost = current.g + distance(current, neighbour)
                    if newMovementCost < neighbour.g or neighbour not in opened:
                        neighbour.g = newMovementCost
                        neighbour.h = distance(neighbour, end)
                        neighbour.f = neighbour.g + neighbour.h
                        neighbour.parent = current

                        opened_cords = set()

                        for opend in opened:
                            opened_cords.add((opend.y, opend.x))

                        if (neighbour.y, neighbour.x) not in opened_cords and field[neighbour.y][neighbour.x] != "X":
                            opened.append(neighbour)
                            if (neighbour.y, neighbour.x) != (end.y, end.x):
                                pygame.draw.rect(screen, white2, (neighbour.x*gröse+(neighbour.x*1)+1, neighbour.y*gröse+(neighbour.y*1)+1, gröse, gröse))
                                pygame.display.update()
                                pygame.time.wait(10)

            if found:
                for node in path[:-2]:
                    field[node.y][node.x] = "P"






    while z != fgröse - 1 and s != fgröse - 1:
        for z in range(len(field)):
            for s in range(len(field[z])):
                if field[z][s] == "S":
                    pygame.draw.rect(screen, grün, (x, y, gröse, gröse))
                elif field[z][s] == "E":
                    pygame.draw.rect(screen, rot, (x, y, gröse, gröse))
                else:
                    pygame.draw.rect(screen, weis, (x, y, gröse, gröse))

                y = y+gröse+1 if s == fgröse-1 else y
                x = x+gröse+1 if s != fgröse-1 else 1

    pygame.display.update()
