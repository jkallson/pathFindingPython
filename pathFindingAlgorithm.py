import time

import pygame

positions = []
maxint = 99999
#Method which is used to build a grid
def buildGrid(y,w):
    #Creating a grid
    for z in range(0, 500, w):
        row = []
        for x in range(0, y, w):
            #Creating a rectangle
            rect = pygame.Rect(x, z, w - 1, w - 1)
            #Adding this retangle to row
            if(z == 0 and x == 0):
                row.append([rect, (0, 0, 0),0,False])
            else: row.append([rect, (0, 0, 0),maxint,False])
        #Adding created row to the positions list
        positions.append(row)

#Method which is used to update the screen
def screenUpdate():
    for row in positions:
        for item in row:
            rect, color, distance, visited = item
            pygame.draw.rect(screen, color, rect)
    pygame.display.flip()

def colorAll():
    for row in positions:
        for item in row:
            rect, color, distance, visited = item
            pygame.draw.rect(screen, [123,12,63], rect)
            time.sleep(0.1)
            pygame.display.update()

#todo Kontrolli, et pole jõudnud paremasse äärde
def checkNeighBours(row,rowElement, distance):
    #4 neighbours
    if(row-1>=0 and rowElement-1>= 0):
        positions[row][rowElement + 1][2] = distance + 1
        positions[row + 1][rowElement][2] = distance + 1
        positions[row-1][rowElement][2] = distance + 1
        positions[row -1][rowElement-1][2] = distance + 1
    #Left upper corner
    elif (row -1 == -1 and rowElement-1 == -1):
        positions[row][rowElement+1][2] = distance + 1
        positions[row+1][rowElement][2] = distance + 1
    #Top row
    elif (row -1 == -1 and rowElement-1 >= 0):
        positions[row][rowElement + 1][2] = distance + 1
        positions[row + 1][rowElement][2] = distance + 1
        positions[row][rowElement-1][2] = distance + 1
    #Left column
    elif (row -1 == -1 and rowElement-1 >= 0):
        positions[row][rowElement + 1][2] = distance + 1
        positions[row + 1][rowElement][2] = distance + 1
        positions[row][rowElement - 1][2] = distance + 1

    #Left bottom corner
    elif (row == 24 and rowElement-1 == -1):
        positions[row][rowElement + 1][2] = distance + 1
        positions[row + 1][rowElement][2] = distance + 1

def findLowestNode():
    lowestX = 0
    lowestY = 0
    currentBestDistance = 999999
    for i,row in enumerate(positions):
        for j,item in enumerate(row):
            rect, color, distance, visited = item
            if distance < currentBestDistance and not visited:
                lowestY = j
                lowestX = i
                currentBestDistance = distance
    #Row number, Place
    return lowestX,lowestY

def dijkstra(startx, starty, endx, endy):
    #Define the starting point
    startNode = positions[startx][starty]
    #Define the ending point
    endNode = positions[endx][endy]

    #Changing end and start point color
    startNode[1] = (123, 52, 126)
    endNode[1] = (123,52,126)

    screenUpdate()

    #Changing the starting point distance to 0
    startNode[2] = 0

    #While loop which will work until we have reached the end node
    while endNode[3] is False:
        #Getting the node coordinates and distances
        nodeX,nodeY = findLowestNode()
        #Getting a new node
        node = positions[nodeX][nodeY]
        #Finding out what that node distance is
        distance = node[2]
        # Finding all of its neighbours and updating their distance
        checkNeighBours(nodeX,nodeY, distance)

        #Mark that node is visited
        node[3] = True
        #Change node color
        node[1] = [18,243,243]
        screenUpdate()

        time.sleep(0.04)


#Creating the game
pygame.init()

#Creating a screen
screen = pygame.display.set_mode((800,500))
screen.fill([255, 255, 255])
pygame.display.update()
#Building the grid
buildGrid(800,20)
running = True


dijkstra(0,0,24,39)
while running:

    #When program is closed
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False

        #When user clicks somewhere in the grid
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #Check which rect was clicked and change its color on list
            for row in positions:
                for item in row:
                    rect, color,distance,visited = item
                    if rect.collidepoint(event.pos):
                        if color == (0, 255, 0):
                            item[1] = (255, 0, 0)
                        else:
                            item[1] = (0, 255, 0)

    #Updates the screen
    screenUpdate()