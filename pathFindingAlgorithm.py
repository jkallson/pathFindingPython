import time
import pygame

#Array where all nodes will be held
positions = []
#Method which is used to build a grid
def buildGrid(y,w):
    #Distance used for infinity
    maxInt = 99999
    #Creating a grid
    for z in range(0, 500, w):
        row = []
        for x in range(0, y, w):
            #Creating a rectangle
            rect = pygame.Rect(x, z, w - 1, w - 1)
            #Adding this retangle to row
            row.append([rect, (0, 0, 0),maxInt,False])
        #Adding created row to the positions list
        positions.append(row)

#Method which is used to update the screen
def screenUpdate():
    for row in positions:
        for item in row:
            rect, color, distance, visited = item
            pygame.draw.rect(screen, color, rect)
    pygame.display.flip()

#Function which is used to decide if distance needs to be changed
def changeDistance(row,rowElement,distance):
    #If distance through some node is smaller that the existing distance, then change it
    if(distance+1 < positions[row][rowElement][2]):
        positions[row][rowElement][2] = distance + 1

#todo Kontrolli, et pole jõudnud paremasse äärde
def checkNeighBours(row,rowElement, distance):
    #4 neighbours
    if(row-1>=0 and rowElement-1>= 0):
        changeDistance(row,rowElement+1,distance)
        changeDistance(row+1, rowElement, distance)
        changeDistance(row-1, rowElement, distance)
        changeDistance(row, rowElement - 1, distance)
    #Left upper corner
    elif (row -1 == -1 and rowElement-1 == -1):
        changeDistance(row, rowElement + 1, distance)
        changeDistance(row+1, rowElement, distance)
    #Top row
    elif (row -1 == -1 and rowElement-1 >= 0):
        changeDistance(row, rowElement + 1, distance)
        changeDistance(row+1, rowElement, distance)
        changeDistance(row, rowElement - 1, distance)
    #Left column
    elif (row -1 >= 0 and rowElement-1 == -1):
        changeDistance(row, rowElement + 1, distance)
        changeDistance(row+1, rowElement, distance)
        changeDistance(row-1, rowElement, distance)

    #Left bottom corner
    elif (row == 24 and rowElement-1 == -1):
        positions[row][rowElement + 1][2] = distance + 1
        positions[row + 1][rowElement][2] = distance + 1

#Function which is used to find the lowest node
def findLowestNode():
    lowestX = 0
    lowestY = 0
    currentBestDistance = 999999
    #Iterating through all rows
    for i,row in enumerate(positions):
        #Iterating through all row nodes
        for j,item in enumerate(row):
            rect, color, distance, visited = item
            #If we have not visited the node and it has smaller best distance then lets keep that in memory
            if distance < currentBestDistance and not visited:
                #Row number
                lowestX = i
                # Row item number
                lowestY = j
                currentBestDistance = distance
    return lowestX,lowestY

#Dijkstra algorithm
def dijkstra(startx, starty, endx, endy):
    #Define the starting point
    startNode = positions[startx][starty]
    #Define the ending point
    endNode = positions[endx][endy]

    #Changing end and start point color
    startNode[1] = (123, 52, 126)
    endNode[1] = (123,52,126)

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
    endNode[1] = (255, 0, 0)

#Creating the game
pygame.init()

#Creating a screen
screen = pygame.display.set_mode((800,500))
screen.fill([255, 255, 255])
pygame.display.update()
#Building the grid
buildGrid(800,20)
running = True

dijkstra(10,10,7,8)
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