from pygame import *
from random import *

init()

width,height=1400,700
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


redLeftTowerPath = [(770, 371), (690, 375), (615, 370), (300, 200)]


class Wizard:
    def __init__(self, health, damage, width, speed, path, spwnX, spwxY):
        self.health = health
        self.damage = damage
        self.speed = speed
        self.sizeRect = Rect(35, 35, width, width)
        self.path = path
        self.sizeRect.center = (spwnX, spwxY)
        self.posIndex = 0
    
    def updatePos(self):
        if self.posIndex >= len(self.path):
            return
        targetX, targetY = self.path[self.posIndex]
        # print(targetX, targetY)
        dx = targetX - self.sizeRect.centerx
        dy = targetY - self.sizeRect.centery
        # print(targetY, self.sizeRect.y, dy)
        dist = (dx**2 + dy**2) **0.5
        
        if dist < 10:
            self.posIndex += 1
            self.sizeRect.center == self.path[-1]
            print("reached")
        else:
            
            self.sizeRect.centerx += int(self.speed * dx/dist)
            self.sizeRect.centery += int(self.speed * dy/dist)
            
        
    def drawSprite(self):
        draw.rect(screen, RED, self.sizeRect)
        
redTroops = []
wizard1 = Wizard(100, 100, 100, 2, redLeftTowerPath, 100, 100)

assassinAttack=[]
assassinDead = []
assassinRun = []

femaleWizardAttack = []
femaleWizardDead = []
femaleWizardRun = []

firemenAttack = []
firemenDead = []
firemenRun = []


icemenAttack = []
icemenDead = []
icemenRun = []


golemAttack = []
golemDead = []
golemRun = []

jackAttack = []
jackDead = []
jackRun = []

knightAttack = []
knightDead = []
knightRun = []

maleWizardAttack = []
maleWizardDead = []
maleWizardRun = []

spearmenAttack = []
spearmenDead = []
spearmenWalk = []


faceCards = []
blueRandom = []
redRandom = []

for i in range(1,9):
    assassinAttack.append(image.load("assets/assassin-attack/assassin-attack"+ str(i) +".png"))

for i in range(1,5):
    assassinDead.append(image.load("assets/assassin-dead/assassin-dead"+ str(i) +".png"))

for i in range(1,9):
    assassinRun.append(image.load("assets/assassin-run/assassin-run"+ str(i) +".png"))



for i in range(1,8):
    femaleWizardAttack.append(image.load("assets/femaleWizard-attack/femaleWizard-attack"+ str(i) +".png"))

for i in range(1,6):
    femaleWizardDead.append(image.load("assets/femaleWizard-dead/femaleWizard-dead"+ str(i) +".png"))

for i in range(1,9):
    femaleWizardRun.append(image.load("assets/femaleWizard-run/femaleWizard-run"+ str(i) +".png"))



for i in range(1,4):
    firemenAttack.append(image.load("assets/firemen-attack/" + str(i) + ".png"))
for i in range(1,6):
    firemenDead.append(image.load("assets/firemen-dead/"+ str(i) +".png"))

for i in range(1,8):
    firemenRun.append(image.load("assets/firemen-run/"+ str(i) +".png"))


for i in range(1,4):
    icemenAttack.append(image.load("assets/iceman-attack/" + str(i) + ".png"))
for i in range(1,7):
    icemenDead.append(image.load("assets/iceman-dead/"+ str(i) +".png"))

for i in range(1,6):
    icemenRun.append(image.load("assets/iceman-run/"+ str(i) +".png"))



for i in range(1,7):
    golemAttack.append(image.load("assets/golem-attack/" + str(i) + ".png"))
for i in range(1,6):
    golemDead.append(image.load("assets/golem-dead/"+ str(i) +".png"))

for i in range(1,8):
    golemRun.append(image.load("assets/golem-run/"+ str(i) +".png"))



for i in range(1,5):
    jackAttack.append(image.load("assets/jack-attack/jack-attack"+ str(i) +".png"))

for i in range(1,5):
    jackDead.append(image.load("assets/jack-dead/jack-dead"+ str(i) +".png"))

for i in range(1,7):
    jackRun.append(image.load("assets/jack-run/jack-run"+ str(i) +".png"))



for i in range(1,5):
    knightAttack.append(image.load("assets/knight-attack/knight-attack"+ str(i) +".png"))

for i in range(1,5):
    knightDead.append(image.load("assets/knight-dead/knight-dead"+ str(i) +".png"))

for i in range(1,7):
    knightRun.append(image.load("assets/knight-run/knight-run"+ str(i) +".png"))



for i in range(1,8):
    maleWizardAttack.append(image.load("assets/maleWizard-attack/maleWizard-attack"+ str(i) +".png"))

for i in range(1,7):
    maleWizardDead.append(image.load("assets/maleWizard-dead/maleWizard-dead"+ str(i) +".png"))

for i in range(1,9):
    maleWizardRun.append(image.load("assets/maleWizard-run/maleWizard-run"+ str(i) +".png"))




for i in range(1,8):
    maleWizardAttack.append(image.load("assets/maleWizard-attack/maleWizard-attack"+ str(i) +".png"))

for i in range(1,7):
    maleWizardDead.append(image.load("assets/maleWizard-dead/maleWizard-dead"+ str(i) +".png"))

for i in range(1,9):
    maleWizardRun.append(image.load("assets/maleWizard-run/maleWizard-run"+ str(i) +".png"))



for i in range(1,4):
    spearmenAttack.append(image.load("assets/spearmen-attack/spearmen-attack"+ str(i) +".png"))

for i in range(1,5):
    spearmenDead.append(image.load("assets/spearmen-dead/spearmen-dead"+ str(i) +".png"))

for i in range(1,6):
    spearmenWalk.append(image.load("assets/spearmen-walk/spearman-walk"+ str(i) +".png"))



for i in range(9):
    faceCards.append(image.load("assets/mainFace/mainface"+ str(i+1) +".png"))


for i in range(9):
    faceCards[i] = transform.scale(faceCards[i], (130,130))


logo = image.load("assets/mainScreenAssets/FSELogo.png")
logo = transform.scale(logo, (1024/4, 1024/4))
mainBackground = image.load("assets/mainScreenAssets/FSEMainBackground.png", "png")
mainBackground = transform.scale(mainBackground, (980*1.5, 626*1.5))

# mixer.music.load("assets/mainScreenAssets/Pufino - Swing (freetouse.com).mp3", "mp3")
# mixer.music.play(10)
gameBackground = image.load("assets/mainScreenAssets/GameBackground.png", "png")
gameBackground = transform.scale(gameBackground, (gameBackground.get_width()*1, gameBackground.get_height()*1))
# mixer.music.load("assets\\mainScreenAssets\Pufino - Swing (freetouse.com).mp3", "mp3")
# mixer.music.play(10)

# Main screen boxes 
PlayBox = Rect(50, 500, 400, 100)
HowToPlayBox = Rect(500, 500, 400, 100)
SettingsBox = Rect(950, 500, 400, 100)
draw.rect(screen, GREEN, PlayBox)
draw.rect(screen, BLUE, HowToPlayBox)
draw.rect(screen, GREY, SettingsBox)


# Card Shown
continueBox = Rect(1175, 575, 200, 100)


bluePlayerCard =[Rect(100,45,135,150),Rect(285,45,135,150), Rect(470,45,135,150), Rect(200,225,135,150), Rect(385,225,135,150)]
RedPlayerCard =[Rect(795,45,135,150),Rect(980,45,135,150), Rect(1165,45,135,150), Rect(895,225,135,150), Rect(1080,225,135,150)]

blueReshuffle = Rect(240,450,225,75)
blueConfirm = Rect(240,550,225,75)
textfont = font.Font("assets/Clash-Royale-Font/font.ttf", 20)
reshuffletext = textfont.render("RESHUFFLE", True, BLACK)
readyText = textfont.render("Ready!!" ,True, BLACK)
waitingText = textfont.render("Waiting...", True, BLACK)
frontFont = font.Font("assets/Clash-Royale-Font/font.ttf", 40)
playText = frontFont.render("Play", True, BLACK)
HowToPlayText = frontFont.render("How to Play", True, BLACK)
settingsText = frontFont.render("Settings", True, BLACK)

backFont = font.Font("assets/Clash-Royale-Font/font.ttf", 30)
backText = backFont.render("Back", True,WHITE)

gameDescriptionFont = font.Font("assets/Clash-Royale-Font/font.ttf", 20)

gameDescription = """How to Play: Knight Royale

Knight Royale is a fast-paced 2-player strategy game where you use random cards to destroy your opponent's towers.

Step 1: Card Selection
    At the start, you'll get a random deck. You can reshuffle up to 3 times. Click 'Ready' when     you're set.

Step 2: The Battle
    - Player 1: W, A, S, D to place cards
    - Player 2: I, J, K, L to place cards
    Each card costs elixir — manage it wisely and play smart to attack and defend.

Step 3: Destroy the Towers
    Break through your opponent's defense and destroy their towers before they destroy 
    yours!
"""

prev_mb = (0, 0, 0)

blueReshuffleCount = 0
redReshuffleCount = 0
mouseClicked = False


blueReady = False
redReady = False

waitBlue = False
waitRed = False

redReshuffle = Rect(940,450,225,75)
redConfirm = Rect(940,550,225,75)
redFinalCards = []
blueFinalCards = []

backRect = Rect(0,600,200,100)
redInd = 0
screenNum = 1

grid1 = [[0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]]

grid2 = [[0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]]

def moveInGrid(dir, w, h, player):
    if player == 1:
        if dir == "right":
            for i in range(h):
                for j in range(w):
                    if grid1[i][j] == 1:
                        grid1[i][j] = 0
                        if j == w-1:
                            grid1[i][0] = 1
                        else:
                            grid1[i][j+1] = 1
                        return
        if dir == "left":
            for i in range(h):
                for j in range(w):
                    if grid1[i][j] == 1:
                        grid1[i][j] = 0
                        if j == 0:
                            grid1[i][w-1] = 1
                        else:
                            grid1[i][j-1] = 1
                        return
        if dir == "down":
            for i in range(h):
                for j in range(w):
                    if grid1[i][j] == 1:
                        grid1[i][j] = 0
                        if i == h-1:
                            grid1[0][j] = 1
                        else:
                            grid1[i+1][j] = 1
                        return
        if dir == "up":
            for i in range(h):
                for j in range(w):
                    if grid1[i][j] == 1:
                        grid1[i][j] = 0
                        # print(i)
                        if i == 0:
                            grid1[h-1][j] = 1
                        else:
                            grid1[i-1][j] = 1
                        return
    elif player == 2:
        if dir == "right":
            for i in range(h):
                for j in range(w):
                    if grid2[i][j] == 1:
                        grid2[i][j] = 0
                        if j == w-1:
                            grid2[i][0] = 1
                        else:
                            grid2[i][j+1] = 1
                        return
        if dir == "left":
            for i in range(h):
                for j in range(w):
                    if grid2[i][j] == 1:
                        grid2[i][j] = 0
                        if j == 0:
                            grid2[i][w-1] = 1
                        else:
                            grid2[i][j-1] = 1
                        return
        if dir == "down":
            for i in range(h):
                for j in range(w):
                    if grid2[i][j] == 1:
                        grid2[i][j] = 0
                        if i == h-1:
                            grid2[0][j] = 1
                        else:
                            grid2[i+1][j] = 1
                        return
        if dir == "up":
            for i in range(h):
                for j in range(w):
                    if grid2[i][j] == 1:
                        grid2[i][j] = 0
                        # print(i)
                        if i == 0:
                            grid2[h-1][j] = 1
                        else:
                            grid2[i-1][j] = 1
                        return
                    



def renderText(surface, text, font, color, rect):
    lines = text.split('\n')  # Split by manual line breaks first
    space_width = font.size(' ')[0]

    x, y = rect.topleft
    max_width = rect.width

    for line in lines:
        words = line.split(' ')
        for word in words:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()

            # If word doesn't fit, move to next line
            if x + word_width >= rect.right:
                x = rect.left
                y += word_height

            surface.blit(word_surface, (x, y))
            x += word_width + space_width

        # After each \n line, move to new line
        x = rect.left
        y += font.get_linesize()

for i in range(5):
    blueRandom = sample(range(1, 9), 5)  
    redRandom = sample(range(1, 9), 5) 


while running:
    blueLeft = textfont.render(f"{3 - blueReshuffleCount} left", True, WHITE)
    redLeft = textfont.render(f"{3 - redReshuffleCount} left", True, WHITE)

    for evt in event.get():
        if evt.type==QUIT:
            running=False
        if evt.type == KEYDOWN:
            if evt.key == K_d:
                moveInGrid("right", 6, 9, 1)
            if evt.key == K_a:
                moveInGrid("left", 6, 9, 1)
            if evt.key == K_s:
                moveInGrid("down", 6, 9, 1)
            if evt.key == K_w:
                moveInGrid("up", 6, 9, 1)
            if evt.key == K_l:
                moveInGrid("right", 6, 9, 2)
            if evt.key == K_j:
                moveInGrid("left", 6, 9, 2)
            if evt.key == K_k:
                moveInGrid("down", 6, 9, 2)
            if evt.key == K_i:
                moveInGrid("up", 6, 9, 2)
            if evt.key == K_1:
                redInd = 0
            if evt.key == K_2:
                redInd = 1
            if evt.key == K_3:
                redInd = 2
            if evt.key == K_4:
                redInd = 3
            if evt.key == K_u:
                currDeckRed = [redFinalCards[i] for i in range(4)]
                redTroops.append(Wizard(100, 100, 20, 2, redLeftTowerPath, redPlayerSelect.centerx, redPlayerSelect.centery))
                # redTroops[-1].center = redPlayerSelect.x, redPlayerSelect.y
                # print(redTroops[-1].center)
                for a in redFinalCards:
                    if currDeckRed.count(a) == 0:
                        redFinalCards[redInd], redFinalCards[4] = redFinalCards[4], redFinalCards[redInd]

    
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
    pressed_keys = key.get_pressed()
    
    if screenNum == 1:
        screen.fill(BLACK)
        screen.blit(mainBackground, (0, 0))
        # screen.blit(logo, (700-logo.get_height()/2, 50))
        draw.rect(screen, GREEN, PlayBox)
        screen.blit(playText,(PlayBox[0]+140,PlayBox[1]+20))
        draw.rect(screen, BLUE, HowToPlayBox)
        screen.blit(HowToPlayText,(HowToPlayBox[0]+30,HowToPlayBox[1]+20))
        draw.rect(screen, GREY, SettingsBox)
        screen.blit(settingsText,(SettingsBox[0]+90,SettingsBox[1]+20))

        if PlayBox.collidepoint(mx, my) and mb[0]:
            screenNum = 2
        if HowToPlayBox.collidepoint(mx, my) and mb[0]:
            screenNum = 4
        if SettingsBox.collidepoint(mx,my) and mb[0]:
            screenNum = 5


    elif screenNum == 2:
        screen.fill(BLACK)
        draw.line(screen, RED, (695, 0), (695, 695), 10)
        draw.rect(screen,BLACK,backRect)
        screen.blit(backText,(backRect[0]+40, backRect[1]+40))
        # Draw player cards
        for i in range(5):
            draw.rect(screen, WHITE, bluePlayerCard[i], 5)
            blueFinalCards.append(faceCards[blueRandom[i]])
            screen.blit(faceCards[blueRandom[i]], bluePlayerCard[i])
        for i in range(5):
            draw.rect(screen, WHITE, RedPlayerCard[i], 5)
            redFinalCards.append(faceCards[redRandom[i]])
            screen.blit(faceCards[redRandom[i]], RedPlayerCard[i])
        

        # Handle reshuffles (only once per click, max 3 times)
        if blueReshuffle.collidepoint(mx, my) and mb[0] and not prev_mb[0] and blueReshuffleCount < 3:
            blueRandom = sample(range(1, 9), 5)
            blueReshuffleCount += 1

        if redReshuffle.collidepoint(mx, my) and mb[0] and not prev_mb[0] and redReshuffleCount < 3:
            redRandom = sample(range(1, 9), 5)
            redReshuffleCount += 1

        # Draw reshuffle buttons (gray if used up)
        if blueReshuffleCount < 3:
            draw.rect(screen, WHITE, blueReshuffle)
        else:
            draw.rect(screen, (100, 100, 100), blueReshuffle)

        if redReshuffleCount < 3:
            draw.rect(screen, WHITE, redReshuffle)
        else:
            draw.rect(screen, (100, 100, 100), redReshuffle)

        # Draw confirm buttons
        draw.rect(screen, GREEN, blueConfirm)
        draw.rect(screen, GREEN, redConfirm)

        # Draw button text
        screen.blit(reshuffletext, (blueReshuffle[0] + 35, blueReshuffle[1] + 25))
        screen.blit(reshuffletext, (redReshuffle[0] + 35, redReshuffle[1] + 25))
        screen.blit(readyText, (blueConfirm[0] + 55, blueConfirm[1] + 25))
        screen.blit(readyText, (redConfirm[0] + 55, redConfirm[1] + 25))

        # Draw reshuffles left text (updates every frame)
        blueLeft = textfont.render(f"{3 - blueReshuffleCount} left", True, WHITE)
        redLeft = textfont.render(f"{3 - redReshuffleCount} left", True, WHITE)
        screen.blit(blueLeft, (blueReshuffle[0] + 245, blueReshuffle[1] + 35))
        screen.blit(redLeft, (redReshuffle[0] + 245, redReshuffle[1] + 35))

        # Confirm logic (once per click)
        if blueConfirm.collidepoint(mx, my) and mb[0] and not prev_mb[0]:
            blueReady = True
            waitBlue = True

        if redConfirm.collidepoint(mx, my) and mb[0] and not prev_mb[0]:
            redReady = True
            waitRed = True

        # Waiting state visuals
        if waitBlue:
            draw.rect(screen, GREEN, blueConfirm)
            screen.blit(waitingText, (blueConfirm[0] + 55, blueConfirm[1] + 25))

        if waitRed:
            draw.rect(screen, GREEN, redConfirm)
            screen.blit(waitingText, (redConfirm[0] + 55, redConfirm[1] + 25))

        # Move to next screen if both ready
        if blueReady and redReady:
            screenNum = 3
            blueReady = False
            redReady = False
            waitBlue = False
            waitRed = False
            blueReshuffleCount = 0
            redReshuffleCount = 0

        if backRect.collidepoint(mx,my) and mb[0]:
            screenNum = 1

    elif screenNum == 3:
        screen.fill(BLACK)
        screen.blit(gameBackground, (-50, 0))
        

        #Left Grid 
        for i in range(10):
            draw.line(screen, GREEN, (350, i*46.5+210), (628, i*46.5+210), 2)
        for i in range(7):
            draw.line(screen, GREEN, (i*47+347, 210), (i*47+347, 630), 2)

        #Right Grid
        for i in range(10):
            draw.line(screen, GREEN, (760, i*46.5+210), (1040, i*46.5+210), 2)
        for i in range(7):
            draw.line(screen, GREEN, (i*46.5+760, 210), (i*46.5+760, 630), 2)
        
        #Blue player
        for i in range(9):
            for j in range(6):
                if grid1[i][j] == 1:
                    # print(i, j)
                    bluePlayerSelect = Rect(j*47+347, i*46.5+210, 50,50)
                    draw.rect(screen, BLUE, (j*47+347, i*46.5+210, 50,50), 5)

        #Red Player       
        for i in range(9):
            for j in range(6):
                if grid2[i][j] == 1:
                    # print(i, j)d
                    redPlayerSelect = Rect(j*47+755, i*46.5+210, 50, 50)
                    draw.rect(screen, RED, (j*47+755, i*46.5+210, 50, 50), 5)
                        

        #Blue cards area
        draw.rect(screen,BLUE,(0,147,183,406),2)
        draw.line(screen,WHITE,(40,150),(40,550))
        for i in range(10):
            draw.rect(screen,WHITE,(0,150,40,i*40+40),2)
        for i in range(4):
            screen.blit(transform.scale(blueFinalCards[i], (100, 100)), (60,i*100+150,140,100))
            draw.rect(screen,WHITE,(40,i*100+150,140,100),2)

        #Red cards area
        draw.rect(screen,RED,(1217,147,183,406),2)
        draw.line(screen,WHITE,(1360,150),(1360,550))
        for i in range(10):
            draw.rect(screen,WHITE,(1360,150,1360,i*40+40),2)
        for i in range(4):
            screen.blit(transform.scale(redFinalCards[i], (100, 100)), (1240,i*100+150,140,100))
            redCardSelectRect = Rect(1220,i*100+150,140,100)
            if i == redInd:
                draw.rect(screen,RED,redCardSelectRect,2)
            else:
                draw.rect(screen,WHITE,redCardSelectRect,2)
        for p in redLeftTowerPath:
            draw.circle(screen, GREEN, p, 10)
        for troop in redTroops:
            troop.updatePos()
        for troop in redTroops:
            troop.drawSprite()
        # print(len(redTroops))
        
    elif screenNum == 4:
        screen.fill(BLACK)
        draw.rect(screen,BLACK,backRect)
        screen.blit(backText,(backRect[0]+30, backRect[1]+40))

        textRect = Rect(50, 50, 1350, 300)
        renderText(screen, gameDescription, gameDescriptionFont, WHITE, textRect)

        if backRect.collidepoint(mx, my) and mb[0]:
            screenNum = 1

    elif screenNum == 5:
        screen.fill(BLACK)
        draw.rect(screen,BLACK,backRect)
        screen.blit(backText,(backRect[0]+30, backRect[1]+40))
        if backRect.collidepoint(mx, my) and mb[0]:
            screenNum = 1

    prev_mb = mb
      
    myClock.tick(60)
    display.flip()
            
quit()