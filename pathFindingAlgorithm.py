import time
import pygame

#Method which is used to build a grid
def buildGrid(y,w):
    # Array where all nodes will be held
    positions = []
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
    return positions

#Method which is used to update the screen
def screenUpdate(screen, positions):
    for row in positions:
        for item in row:
            rect, color, distance, visited,previousNode = item
            pygame.draw.rect(screen, color, rect)
    pygame.display.flip()

#Function which is used to decide if distance needs to be changed
def changeDistance(row,rowElement,distance,previousRow,previousElement,positions):
    #If distance through some node is smaller that the existing distance, then change it
    if(distance+1 < positions[row][rowElement][2]):
        positions[row][rowElement][2] = distance + 1
        positions[row][rowElement][4][0] = previousRow
        positions[row][rowElement][4][1] = previousElement
#Find neighbours
def checkNeighBours(row,rowElement, distance,positions):
    #4 neighbours
    if(row-1>=0 and rowElement-1>= 0 and row != len(positions)-1 and rowElement != len(positions[0])-1):
        changeDistance(row,rowElement+1,distance,row,rowElement,positions)
        changeDistance(row+1, rowElement, distance,row,rowElement,positions)
        changeDistance(row-1, rowElement, distance,row,rowElement,positions)
        changeDistance(row, rowElement - 1, distance,row,rowElement,positions)
    #Left upper corner
    elif (row -1 == -1 and rowElement-1 == -1):
        changeDistance(row, rowElement + 1, distance,row,rowElement,positions)
        changeDistance(row+1, rowElement, distance,row,rowElement,positions)
    #Top row
    elif (row -1 == -1 and rowElement-1 >= 0 and rowElement != len(positions[0])-1):
        changeDistance(row, rowElement + 1, distance,row,rowElement,positions)
        changeDistance(row+1, rowElement, distance,row,rowElement,positions)
        changeDistance(row, rowElement - 1, distance,row,rowElement,positions)

    # Left bottom corner
    elif (row == len(positions)-1 and rowElement - 1 == -1):
        changeDistance(row, rowElement + 1, distance,row,rowElement,positions)
        changeDistance(row - 1, rowElement, distance,row,rowElement,positions)

    #Left column
    elif (row -1 >= 0 and rowElement-1 == -1):
        changeDistance(row, rowElement + 1, distance,row,rowElement,positions)
        changeDistance(row+1, rowElement, distance,row,rowElement,positions)
        changeDistance(row-1, rowElement, distance,row,rowElement,positions)
    #Top right
    elif (row == 0 and rowElement  == len(positions[0])-1):
        changeDistance(row, rowElement-1, distance,row,rowElement,positions)
        changeDistance(row +1, rowElement, distance,row,rowElement,positions)
    #Bottom right
    elif (row == len(positions)-1 and rowElement == len(positions[0])-1):
        changeDistance(row, rowElement - 1, distance,row,rowElement,positions)
        changeDistance(row - 1, rowElement, distance,row,rowElement,positions)

    #Right column
    elif (row > 0 and rowElement == len(positions[0])-1):
        changeDistance(row, rowElement - 1, distance,row,rowElement,positions)
        changeDistance(row + 1, rowElement, distance,row,rowElement,positions)
        changeDistance(row - 1, rowElement, distance,row,rowElement,positions)

    #Bottom row
    elif (row == len(positions)-1 and rowElement > 0):
        changeDistance(row, rowElement + 1, distance,row,rowElement,positions)
        changeDistance(row, rowElement-1, distance,row,rowElement,positions)
        changeDistance(row - 1, rowElement, distance,row,rowElement,positions)

#Function which returns the shortest path elements
def findShortestPathElements(endRow,endElement,positions):
    shortestPathElements = []
    #Getting the ending node
    node = positions[endRow][endElement]
    shortestPathElements.append([endRow,endElement])
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
def visualizeShortestPath(shortestPath,screen,positions):
    #This loop will go through all of the elements that are in the shortest path and change their color
    for item in shortestPath:
        #Selecting a node
        row = item[0]
        rowElement = item[1]
        #Changing its color to yellow
        positions[row][rowElement][1] = [255,0,0]
        #Updating the screen
        screenUpdate(screen,positions)

#Function which is used to find the lowest node
def findLowestNode(positions):
    lowestX = 0
    lowestY = 0
    currentBestDistance = 999999
    #Iterating through all rows
    for i,row in enumerate(positions):
        #Iterating through all row nodes
        for j,item in enumerate(row):
            rect, color, distance, visited,previousNode = item
            #If we have not visited the node and it has smaller best distance then lets keep that in memory
            if distance < currentBestDistance and not visited and color != (255,255,255):
                #Row number
                lowestX = i
                # Row item number
                lowestY = j
                currentBestDistance = distance
    return lowestX,lowestY

#Dijkstra algorithm
def dijkstra(startx, starty, endx, endy,screen,positions):
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
        nodeX,nodeY = findLowestNode(positions)
        #Getting a new node
        node = positions[nodeX][nodeY]
        #Finding out what that node distance is
        distance = node[2]
        # Finding all of its neighbours and updating their distance
        checkNeighBours(nodeX,nodeY, distance,positions)
        #Mark that node is visited
        node[3] = True
        #Change node color
        node[1] = [18,243,243]
        screenUpdate(screen,positions)

        time.sleep(0.003)
    #Changing end node color
    endNode[1] = (255, 0, 0)
    #Getting the shortest path elements and then visualizing it
    shortestPath = findShortestPathElements(endx,endy,positions)
    visualizeShortestPath(shortestPath,screen,positions)

def nodeFinder(positions, color):
    X = 0
    Y = 0
    # Iterating through all rows
    for i, row in enumerate(positions):
        # Iterating through all row nodes
        for j, item in enumerate(row):
            rect, nodeColor, distance, visited, previousNode = item
            #If the node has the same color as the node that we are looking then lets remember it
            if nodeColor == color:
                # Row number
                X = i
                # Row item number
                Y = j
                break

    return X, Y

def main(screenLength, screenWidth, nodeSize):
    #Creating the game
    pygame.init()


    #Creating a screen
    screen = pygame.display.set_mode((screenLength,screenWidth))
    screen.fill([255, 255, 255])
    pygame.display.update()
    #Building the grid
    positions = buildGrid(screenLength,nodeSize)
    running = True


    while running:
        #When program is closed
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                running = False

            #When user clicks somewhere in the grid
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #To build a wall
                for row in positions:
                    for item in row:
                        rect, color, distance, visited,previousNode = item
                        if rect.collidepoint(event.pos):
                            item[1] = (255, 255, 255)

            #Key press handling
            elif event.type == pygame.KEYDOWN:
                # To activate Dijkstra algorithm
                if(event.key == pygame.K_SPACE):
                    startNode = nodeFinder(positions,(0, 255, 34))
                    endNode = nodeFinder(positions,(34, 0, 255))
                    dijkstra(startNode[0],startNode[1],endNode[0],endNode[1],screen,positions)
                #To reset the screen user has to press "r"
                elif(event.key == pygame.K_r):
                    positions = buildGrid(screenLength,nodeSize)
                elif (event.key == pygame.K_s):
                    for row in positions:
                        for item in row:
                            rect, color, distance, visited, previousNode = item
                            if rect.collidepoint(pygame.mouse.get_pos()):
                                item[1] = (0, 255, 34)
                            elif item[1] == (0, 255, 34):
                                item[1] = (0, 0, 0)

                elif (event.key == pygame.K_e):
                    for row in positions:
                        for item in row:
                            rect, color, distance, visited, previousNode = item
                            if rect.collidepoint(pygame.mouse.get_pos()):
                                item[1] = (34, 0, 255)
                            elif item[1] == (34, 0, 255):
                                item[1] = (0, 0, 0)
        #Updates the screen
        screenUpdate(screen,positions)

main(800,500,20)