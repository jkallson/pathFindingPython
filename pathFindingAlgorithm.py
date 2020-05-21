import pygame

positions = []
def buildGrid(y,w):
    for i in range(1,21):
        x = 20
        y = y+20
        for j in range(1,31):
            pygame.draw.line(screen, [0, 0, 0], [x,y], [x+w,y])
            pygame.draw.line(screen, [0, 0, 0], [x + w, y], [x + w, y+w])
            pygame.draw.line(screen, [0, 0, 0], [x + w, y+w], [x, y+w])
            pygame.draw.line(screen, [0, 0, 0], [x, w+y], [x , y])
            positions.append((x,y))
            x = x+20


    pygame.display.update()
#Loome mängu
pygame.init()

screen = pygame.display.set_mode((650,450))
screen.fill([255, 255, 255])
pygame.display.update()
buildGrid(0,20)
running = True
while running:
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
