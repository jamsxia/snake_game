"""
Original version:
https://www.edureka.co/blog/snake-game-with-pygame/

Improved(?) by Geoffrey Matthews, 2022
"""

import pygame
import random
 
# Global variables that will never change

# Colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
 
displayWidth = 666
displayHeight = 333

cellSize = 20
speed = 8

pygame.init() # must be called before calling pygame methods:

display = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('Modified Snake Game by Edureka')
 
clock = pygame.time.Clock()
 
gameOverFont = pygame.font.SysFont("bahnschrift", 25)
scoreFont = pygame.font.SysFont("comicsansms", 35)
    
# Global variables that will be changed during play

def initialize(gameStart=True):
    global quitGame, loser, x1, y1, x1Change, y1Change
    global snake, foodx, foody
    global displayWidth, displayHeight
 
    x1 = midCell(displayWidth)
    y1 = midCell(displayHeight)

    quitGame = False
    loser = False
 
    x1Change = 0
    y1Change = 0
 
    snake = [(x1,y1)]
 
    foodx = randomCell(displayWidth)
    foody = randomCell(displayHeight)

def drawScore(score):
    global display
    value = scoreFont.render("Your Score: " + str(score),
                              True,   # antialias
                              yellow) # color
    display.blit(value, [0, 0])

def drawCircle(pos, color):
    global cellSize, display
    radius = cellSize//2
    pos = (pos[0]+radius, pos[1]+radius)
    pygame.draw.circle(display, color, pos, radius)
 
def drawSnake(snake):
    for pos in snake:
        drawCircle(pos, black)
    drawCircle(pos, red)

def drawFood(x, y):
    drawCircle((x,y), green)     
 
def message(msg, color):
    global display, displayWidth, displayHeight
    mesg = gameOverFont.render(msg, True, color)
    display.blit(mesg, [displayWidth // 6, displayHeight // 3])

def randomCell(totalSize):
    global cellSize
    return cellSize*random.randint(0,(totalSize//cellSize)-1)

def midCell(totalSize):
    global cellSize
    n = (totalSize//cellSize)//2
    return cellSize*n

def onBoard(x, y):
    global displayWidth, displayHeight
    onWidth = 0 <= x < displayWidth
    onHeight = 0 <= y < displayHeight
    return onWidth and onHeight

def drawMenu(display, score):
    display.fill(blue)
    message('You Lost!  C: continue    Q: quit', red)
    drawScore(score)
    pygame.display.update()

def gameLoop():
    global quitGame, loser, x1, y1, x1Change, y1Change
    global snake, foodx, foody, display, speed
    global cellSize, speed
           
    while not quitGame:
        # govern speed
        clock.tick(speed)

        # handle user events:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quitGame = True
                elif event.key == pygame.K_ESCAPE:
                    quitGame = True
                elif event.key == pygame.K_c:
                    initialize()
                elif event.key == pygame.K_LEFT:
                    x1Change = -cellSize
                    y1Change = 0
                elif event.key == pygame.K_RIGHT:
                    x1Change = cellSize
                    y1Change = 0
                elif event.key == pygame.K_UP:
                    y1Change = -cellSize
                    x1Change = 0
                elif event.key == pygame.K_DOWN:
                    y1Change = cellSize
                    x1Change = 0

        # check mode of game
        if quitGame:
            return()
        
        if loser:
            drawMenu(display, len(snake)-1)
            continue

        # gameMode == playing

        # handle game events:
        if not onBoard(x1, y1):
            loser = True
            continue
        
        for x in snake[:-1]:
            if x == snake[-1]:
                loser = True
                continue

        # update state of game
        x1 += x1Change
        y1 += y1Change
        snake.append((x1,y1))
        if (x1 == foodx and y1 == foody):
            foodx = randomCell(displayWidth)
            foody = randomCell(displayHeight)
        else:
            del snake[0]
 
        # Update screen
        display.fill(blue)
        drawScore(len(snake)-1) 
        drawFood(foodx, foody)
        drawSnake(snake)
        pygame.display.update()

def main():
    initialize()
    gameLoop()
    
if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
        
