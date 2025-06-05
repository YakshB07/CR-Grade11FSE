
from pygame import *

width,height=800,600
screen=display.set_mode((width,height))
RED=(255,0,0)
GREY=(127,127,127)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)
WHITE=(255,255,255)
myClock=time.Clock()
running=True


jackAttack = []
jackDead = []
jackRun = []




for i in range(1,5):
    jackAttack.append(image.load("assets/jack-attack/jack-attack"+ str(i) +".png"))

for i in range(1,5):
    jackDead.append(image.load("assets/jack-dead/jack-dead"+ str(i) +".png"))

for i in range(1,7):
    jackRun.append(image.load("assets/jack-run/jack-run"+ str(i) +".png"))



runbutton = Rect(50,200,100,100)
attackButton = Rect(450, 200 , 100, 100)




jackRunIndex = 0
frameCounter = 0
jackFrameSpeed = 0.1  # adjust for animation speed
runningAnimation = False  # flag to keep running
attackAnimation = False




while running:
    screen.fill(WHITE)
    for evt in event.get():
        if evt.type==QUIT:
            running=False
    if evt.type == MOUSEBUTTONDOWN:
        if runbutton.collidepoint(evt.pos):
            runningAnimation = True
            attackAnimation =False
            print('ht')
        if attackButton.collidepoint(evt.pos):
            runningAnimation = False
            attackAnimation =True


    draw.rect(screen,BLACK,runbutton)
    draw.rect(screen,BLACK,attackButton)


    if runningAnimation:
        frameCounter += jackFrameSpeed
        if frameCounter >= len(jackRun):
            frameCounter = 0
        jackRunIndex = int(frameCounter)
        screen.blit(jackRun[jackRunIndex], (300, 350))

    if attackAnimation:
        frameCounter += jackFrameSpeed
        if frameCounter >= len(jackAttack):
            frameCounter = 0
        jackRunIndex = int(frameCounter)
        screen.blit(jackAttack[jackRunIndex], (300, 350))

    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
      
    myClock.tick(60)
    display.flip()
            
quit()