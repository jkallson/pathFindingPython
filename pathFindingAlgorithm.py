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
            row.append([rect, (0, 0, 0),maxInt,False,[999,999]])
        #Adding created row to the positions list
        positions.append(row)

#Method which is used to update the screen
def screenUpdate():
    for row in positions:
        for item in row:
            rect, color, distance, visited,previousNode = item
            pygame.draw.rect(screen, color, rect)
    pygame.display.flip()

#Function which is used to decide if distance needs to be changed
def changeDistance(row,rowElement,distance,previousRow,previousElement):
    #If distance through some node is smaller that the existing distance, then change it
    if(distance+1 < positions[row][rowElement][2]):
        positions[row][rowElement][2] = distance + 1
        positions[row][rowElement][4][0] = previousRow
        positions[row][rowElement][4][1] = previousElement
#Find neighbours
def checkNeighBours(row,rowElement, distance):
    #4 neighbours
    if(row-1>=0 and rowElement-1>= 0 and row != 24 and rowElement != 39):
        changeDistance(row,rowElement+1,distance,row,rowElement)
        changeDistance(row+1, rowElement, distance,row,rowElement)
        changeDistance(row-1, rowElement, distance,row,rowElement)
        changeDistance(row, rowElement - 1, distance,row,rowElement)
    #Left upper corner
    elif (row -1 == -1 and rowElement-1 == -1):
        changeDistance(row, rowElement + 1, distance,row,rowElement)
        changeDistance(row+1, rowElement, distance,row,rowElement)
    #Top row
    elif (row -1 == -1 and rowElement-1 >= 0 and rowElement != 39):
        changeDistance(row, rowElement + 1, distance,row,rowElement)
        changeDistance(row+1, rowElement, distance,row,rowElement)
        changeDistance(row, rowElement - 1, distance,row,rowElement)

    # Left bottom corner
    elif (row == 24 and rowElement - 1 == -1):
        changeDistance(row, rowElement + 1, distance,row,rowElement)
        changeDistance(row - 1, rowElement, distance,row,rowElement)

    #Left column
    elif (row -1 >= 0 and rowElement-1 == -1):
        changeDistance(row, rowElement + 1, distance,row,rowElement)
        changeDistance(row+1, rowElement, distance,row,rowElement)
        changeDistance(row-1, rowElement, distance,row,rowElement)
    #Top right
    elif (row == 0 and rowElement  == 39):
        changeDistance(row, rowElement-1, distance,row,rowElement)
        changeDistance(row +1, rowElement, distance,row,rowElement)
    #Bottom right
    elif (row == 24 and rowElement == 39):
        changeDistance(row, rowElement - 1, distance,row,rowElement)
        changeDistance(row - 1, rowElement, distance,row,rowElement)

    #Right column
    elif (row > 0 and rowElement == 39):
        changeDistance(row, rowElement - 1, distance,row,rowElement)
        changeDistance(row + 1, rowElement, distance,row,rowElement)
        changeDistance(row - 1, rowElement, distance,row,rowElement)

    #Bottom row
    elif (row == 24 and rowElement > 0):
        changeDistance(row, rowElement + 1, distance,row,rowElement)
        changeDistance(row, rowElement-1, distance,row,rowElement)
        changeDistance(row - 1, rowElement, distance,row,rowElement)

#Function which returns the shortest path elements
def findShortestPathElements(endRow,endElement):
    shortestPathElements = []
    #Getting the ending node
    node = positions[endRow][endElement]
    #While there is still previous elements, lets continue the loop
    while node[4] != [999,999]:
        #Finding previous node position
        element = [node[4][0],node[4][1]]
        #Appending it to the list
        shortestPathElements.append(element)
        #Selecting the previous node as our new node
        node = positions[node[4][0]][node[4][1]]
    #Reversing the list so we will begin from the start node
    shortestPathElements.reverse()
    return shortestPathElements

#Function which is used to visualize the shortest path
def visualizeShortestPath(shortestPath):
    #This loop will go through all of the elements that are in the shortest path and change their color
    for item in shortestPath:
        #Selecting a node
        row = item[0]
        rowElement = item[1]
        #Changing its color to yellow
        positions[row][rowElement][1] = [241,255,31]
        #Updating the screen
        screenUpdate()

#Function which is used to find the lowest node
def findLowestNode():
    lowestX = 0
    lowestY = 0
    currentBestDistance = 999999
    #Iterating through all rows
    for i,row in enumerate(positions):
        #Iterating through all row nodes
        for j,item in enumerate(row):
            rect, color, distance, visited,previousNode = item
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

        time.sleep(0.002)
    #Changing end node color
    endNode[1] = (255, 0, 0)
    #Getting the shortest path elements and then visualizing it
    shortestPath = findShortestPathElements(endx,endy)
    visualizeShortestPath(shortestPath)
#Creating the game
pygame.init()

#Creating a screen
screen = pygame.display.set_mode((800,500))
screen.fill([255, 255, 255])
pygame.display.update()
#Building the grid
buildGrid(800,20)
running = True

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
                    rect, color, distance, visited,previousNode = item
                    if rect.collidepoint(event.pos):
                        if color == (0, 255, 0):
                            item[1] = (255, 0, 0)
                        else:
                            item[1] = (0, 255, 0)

        #Key press handling
        elif event.type == pygame.KEYDOWN:
            # To activate Dijkstra algorithm
            if(event.key == pygame.K_SPACE):
                dijkstra(15,20,0,0)
            #To reset the screen user has to press "r"
            elif(event.key == pygame.K_r):
                positions = []
                buildGrid(800,20)
    #Updates the screen
    screenUpdate()