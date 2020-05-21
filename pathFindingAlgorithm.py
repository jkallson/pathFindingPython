import pygame

positions = []

#Method which is used to build a grid
def buildGrid(y,w):
    #Creating a grid
    for z in range(0, 500, w):
        row = []
        for x in range(0, y, w):
            #Creating a rectangle
            rect = pygame.Rect(x, z, w - 1, w - 1)
            #Adding this retangle to row
            row.append([rect, (0, 0, 0)])
        #Adding created row to the positions list
        positions.append(row)

#Method which is used to update the screen
def screenUpdate():
    for row in positions:
        for item in row:
            rect, color = item
            pygame.draw.rect(screen, color, rect)
    pygame.display.flip()

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
                    rect, color = item
                    if rect.collidepoint(event.pos):
                        if color == (0, 255, 0):
                            item[1] = (255, 0, 0)
                        else:
                            item[1] = (0, 255, 0)
    #Updates the screen
    screenUpdate()