"""
Original version:
https://www.edureka.co/blog/snake-game-with-pygame/

Improved(?) by Geoffrey Matthews, 2022
Renewed(?) by James Xia, 2022 CSCI-111
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
purple=(255,0,255)
 
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

#Game states
PLAYING='Playing mode'
MENU="Menu mode"
LOSER='Loser mode'
QUIT="Quit mode"

startSnakeLength=5
nSnakes=1
poisionApples=False



# Global variables that will be changed during play

def initialize(gameStart=True):
    global gameMode, x1, y1, x1Change, y1Change
    global x2, y2, x2Change, y2Change,snake2
    global snake, foodx, foody
    global displayWidth, displayHeight
    global poisionOn, poisionX, poisionY, poisionCount
    global cellSize
    
    x1 = midCell(displayWidth)
    y1 = midCell(displayHeight)
    x2 = midCell(displayWidth)
    y2 = midCell(displayHeight)
    
 
    x1Change = cellSize
    y1Change = 0
    x2Change=cellSize
    y2Change=0

    snake = []
    snake2 = []
    
    foodx = randomCell(displayWidth)
    foody = randomCell(displayHeight)
    
    poisionX=0
    poisionY=0
    poisionOn=False
    poisionCount=0


    createSnake(startSnakeLength)
    createSnake2(startSnakeLength)
        
    gameMode=MENU
def drawScore(score):
    global display
    value = scoreFont.render("Your Score: " + str(score),
                              True,   # antialias
                              yellow) # color
    display.blit(value, [0, 0])    

def drawScore2(score):
    global display
    value = scoreFont.render("Your Score: " + str(score),
                              True,   # antialias
                              yellow) # color
    display.blit(value, [420, 270])


def drawCircle(pos, color):
    global cellSize, display
    radius = cellSize//2
    pos = (pos[0]+radius, pos[1]+radius)
    pygame.draw.circle(display, color, pos, radius)
 
def drawSnake(snake):
    for pos in snake:
        drawCircle(pos, black)
    drawCircle(pos, red)

def drawSnake2(snake2):
    for pos in snake2:
        drawCircle(pos, white)
    drawCircle(pos, yellow)

def drawFood(x, y):
    drawCircle((x,y), green)

def drawPoision(x,y):
    drawCircle((x,y), purple)
 
def message(msg, color,pos_h):
    global display, displayWidth, displayHeight
    mesg = gameOverFont.render(msg, True, color)
    display.blit(mesg, [displayWidth // 6, pos_h // 6])


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

def startMenu(display):
    global displayHeight,startSnakeLength, nSnakes, poisionApples
    display.fill(blue)
    message("Player1:"+str(len(snake))+'    '+"Player2: "+str(len(snake2)),black, displayHeight-240)
    message("Welcome to Snake!",black, displayHeight)
    message("Menu:",black,displayHeight+240)
    message("L/R arrows: change snake length: "+str(startSnakeLength),black,displayHeight+480)
    message("S:change number of snakes: "+str(nSnakes),black,displayHeight+720)
    message("P: position apples "+('yes'if poisionApples else 'no'),black,displayHeight+960)
    message("C: play games",black,displayHeight+1200)
    message("Q: quit",black,displayHeight+1440)
    pygame.display.update()

def createSnake(startLength):
    global snake, x1,y1,cellSize
    for i in range (startLength):
        snake.append((x1-cellSize*(startLength-i-1),y1))
        
def createSnake2(startLength):
    global snake2, x2, y2, cellSize
    for i in range (startLength):
        snake2.append((x2,y2-cellSize*(startLength-i-1)))
        
def checkCollision(snake):
    for x in snake[:-1]:
        if x == snake[-1]:
            return True
    return False

def gameLoop():
    global gameMode, x1, y1, x1Change, y1Change
    global snake, foodx, foody, display, speed
    global cellSize, speed
    global startSnakeLength, nSnakes, poisionApples
    global poisionOn, poisionX, poisionY, poisionCount
    global x2, y2, x2Change, y2Change,snake2
    
    if poisionApples:
        poisonOn=True
        poisionX = randomCell(displayWidth)
        poisionY = randomCell(displayHeight)
        poisionCount=random.randint(10*speed, 20*speed)
        

    while gameMode!=QUIT:
        if poisionApples:
            poisionCount-=1
        # govern speed
        clock.tick(speed)
        # handle user events:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameMode = QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    gameMode = QUIT
                elif event.key == pygame.K_ESCAPE:
                    gameMode = QUIT
                elif event.key == pygame.K_c:
                    initialize()
                    gameMode=PLAYING
                elif event.key == pygame.K_LEFT and gameMode==PLAYING:
                    x1Change = -cellSize
                    y1Change = 0
                elif event.key == pygame.K_LEFT and gameMode==MENU:
                    startSnakeLength-=1
                elif event.key == pygame.K_RIGHT and gameMode==MENU:
                    startSnakeLength+=1
                elif event.key == pygame.K_s and gameMode==MENU:
                    nSnakes=3-nSnakes
                elif event.key == pygame.K_p and gameMode==MENU:
                    poisionApples= False if poisionApples else True
                elif event.key == pygame.K_RIGHT:
                    x1Change = cellSize
                    y1Change = 0
                elif event.key == pygame.K_UP:
                    y1Change = -cellSize
                    x1Change = 0
                elif event.key == pygame.K_DOWN:
                    y1Change = cellSize
                    x1Change = 0#/////nSnake==2
                elif(event.key == pygame.K_w and nSnakes==2 and gameMode==PLAYING):
                    y2Change = -cellSize
                    x2Change = 0
                elif(event.key == pygame.K_a and nSnakes==2 and gameMode==PLAYING):
                    x2Change = -cellSize
                    y2Change = 0
                elif(event.key == pygame.K_s and nSnakes==2 and gameMode==PLAYING):
                    y2Change = cellSize
                    x2Change = 0
                elif(event.key == pygame.K_d and nSnakes==2 and gameMode==PLAYING):
                    x2Change = cellSize
                    y2Change = 0
                
                
                

        # check mode of game
        if gameMode == QUIT:
            return()
        
        if gameMode == LOSER:
            gameMode=MENU
            startMenu(display)
            continue
        
        if gameMode==MENU:
            startMenu(display)
            continue
            
        # gameMode == playing

        # handle game events:
        if not (onBoard(x1, y1) and onBoard(x2,y2)):
            gameMode = LOSER
            continue
        
        if checkCollision(snake)or (checkCollision(snake2)):
            gameMode = LOSER
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
            
        if(poisionApples and poisionOn and ((x1==poisionX and y1==poisionY)or (x2==poisionX and y2==poisionY and nSnakes==2))):
            gameMode=LOSER
            continue
            
        if nSnakes==2:
            x2+=x2Change
            y2+=y2Change
            snake2.append((x2,y2))
            if(x2==foodx and y2==foody):
                foodx=randomCell(displayWidth)
                foody=randomCell(displayHeight)
            else:
                del snake2[0]
 
        # Update screen
        display.fill(blue)
        drawScore(len(snake)-1) 
        drawFood(foodx, foody)
        drawSnake(snake)
        
        if(nSnakes==2):
            drawScore2(len(snake2)-1)
            drawSnake2(snake2)
        
        if(poisionApples==True and poisionOn==True):
            drawPoision(poisionX, poisionY)
        if(poisionApples and poisionCount==0):
            poisionOn=(True if poisionOn==False else False)
            poisionX = randomCell(displayWidth)
            poisionY = randomCell(displayHeight)
            poisionCount=random.randint(10*speed, 20*speed)
            
        pygame.display.update()
        
            

def main():
    initialize()
    gameLoop()
    
if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
        
