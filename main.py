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
ELIXIR_COLOR = (176, 122, 255)
myClock=time.Clock()
running=True

frameCounter = 0
redLeftTowerPath = [(770, 371), (690, 375), (615, 370), (300, 250)]
blueTopTowerPath = [(615, 370), (690, 375), (770, 371), (1060, 250)]

def findKeys(value, dict):
    for troop, cards in dict.items():
        for card, attributes in cards.items():
            for attrName, attribute in attributes.items():
                if value == attribute:
                    return [troop, card, attrName]

class Tower:
    def __init__(self, side, x, y, image, health=200):
        self.side = side  
        self.x = x
        self.y = y
        self.image = image
        self.health = health
        self.max_health = health
        self.damage = 20
        self.attack_range = 100
        self.sizeRect = Rect(x, y, image.get_width(), image.get_height())
        self.frameCounter = 0
        self.attackSpeed = 1  
        self.lastAttack = 0

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        bar_width = self.image.get_width()
        bar_height = 8
        health_ratio = max(self.health / self.max_health, 0)
        health_bar_rect = Rect(self.x, self.y - 12, int(bar_width * health_ratio), bar_height)
        border_rect = Rect(self.x, self.y - 12, bar_width, bar_height)
        draw.rect(surface, (0, 255, 0), health_bar_rect)
        draw.rect(surface, (255, 0, 0), Rect(self.x + health_bar_rect.width, self.y - 12, bar_width - health_bar_rect.width, bar_height))
        draw.rect(surface, (255, 255, 255), border_rect, 2)

    def attack(self, enemy_troops):
        now = time.get_ticks()
        if now - self.lastAttack < 1000 / self.attackSpeed:
            return  
        for troop in enemy_troops:
            if not troop.dead:
                dx = (troop.sizeRect.centerx - (self.x + self.image.get_width() // 2))
                dy = (troop.sizeRect.centery - (self.y + self.image.get_height() // 2))
                dist = (dx ** 2 + dy ** 2) ** 0.5
                if dist <= self.attack_range:
                    troop.health -= self.damage
                    self.lastAttack = now
                    break  
class Wizard:
    def __init__(self, side, health, damage, width, speed, path, spwnX, spwxY, frameCounter, frameSpeed, runAnim, attackAnim, animIndex, deadAnim=None):
        self.side = side
        self.health = health
        self.damage = damage
        self.attacking = False
        self.dead = False
        self.deadAnim = deadAnim if deadAnim else []
        self.deadFrameCounter = 0
        self.speed = speed
        self.sizeRect = Rect(35, 35, width, width)
        self.path = path
        self.sizeRect.center = (spwnX, spwxY)
        self.posIndex = 0
        self.frameCounter = frameCounter
        self.frameSpeed = frameSpeed
        self.runAnim = runAnim
        self.attackAnim = attackAnim  
        self.animationList = self.runAnim
        self.animationIndex = animIndex
        self.attackCooldown = 0
        self.attackCooldownMax = len(self.attackAnim)
        self.attackRadius = 60
        self.hasDealtDamage = False
        self.elixir = 5

    def updatePos(self):
        if self.dead:
            return
        if self.posIndex >= len(self.path):
            return
        targetX, targetY = self.path[self.posIndex]
        dx = targetX - self.sizeRect.centerx
        dy = targetY - self.sizeRect.centery
        dist = (dx**2 + dy**2) **0.5
        print()
        if dist < 1:
            self.posIndex += 1
            # print("reached")
        else:
            if self.attacking:
               pass
            else:
                self.sizeRect.centerx += int(self.speed * dx/dist)
                self.sizeRect.centery += int(self.speed * dy/dist)
            
        
    def drawSprite(self):
        if self.dead and self.deadAnim:
            frame = int(self.deadFrameCounter)
            if frame < len(self.deadAnim):
                img = self.deadAnim[frame]
                if self.side == "red":
                    img = transform.flip(img, True, False)
                screen.blit(img, (self.sizeRect.centerx-25, self.sizeRect.centery-25))
                self.deadFrameCounter += 0.15  
            return
        if self.attacking:
            self.animationList = self.attackAnim
        else:
            self.animationList = self.runAnim

        self.frameCounter += self.frameSpeed
        if self.frameCounter >= len(self.animationList):
            self.frameCounter = 0
            self.hasDealtDamage = False  
        self.animationIndex = int(self.frameCounter)
        if self.side == "red":
            screen.blit(transform.flip(self.animationList[self.animationIndex], True, False), (self.sizeRect.centerx-25, self.sizeRect.centery-25))
        elif self.side == "blue":
            screen.blit(transform.flip(self.animationList[self.animationIndex], False, False), (self.sizeRect.centerx-25, self.sizeRect.centery-25))


    def attack(self, enemies):
        if self.dead:
            self.attacking = False
            return
        attackRange = 75  
        closestEnemy = None
        minDist = attackRange + 1
        for enemy in enemies:
            if not enemy.dead:
                dx = self.sizeRect.centerx - enemy.sizeRect.centerx
                dy = self.sizeRect.centery - enemy.sizeRect.centery
                dist = (dx**2 + dy**2) ** 0.5
                if dist < minDist:
                    minDist = dist
                    closestEnemy = enemy

        if closestEnemy and minDist <= attackRange:
            self.attacking = True
            if int(self.frameCounter) == len(self.attackAnim) - 1 and not self.hasDealtDamage:
                closestEnemy.health -= self.damage
                self.hasDealtDamage = True
        else:
            self.attacking = False
            self.hasDealtDamage = False

class Barbarian:
    def __init__(self, side, health, damage, width, speed, path, spwnX, spwxY, frameCounter, frameSpeed, runAnim, attackAnim, animIndex, deadAnim=None):
        self.side = side
        self.health = health
        self.damage = damage
        self.dead = False
        self.deadAnim = deadAnim if deadAnim else []
        self.deadFrameCounter = 0
        self.attacking = False
        self.speed = speed
        self.sizeRect = Rect(35, 35, width, width)
        self.path = path
        self.sizeRect.center = (spwnX, spwxY)
        self.posIndex = 0
        self.frameCounter = frameCounter
        self.frameSpeed = frameSpeed
        self.runAnim = runAnim
        self.attackAnim = attackAnim  
        self.animationList = self.runAnim
        self.animationIndex = animIndex
        self.attackCooldown = 0
        self.attackCooldownMax = len(self.attackAnim)
        self.hasDealtDamage = False
        self.elixir = 5
    
    def updatePos(self):
        if self.dead:
            return
        if self.attacking:
            self.animationList = self.attackAnim
        else:
            self.animationList = self.runAnim

        if self.posIndex >= len(self.path):
            return
        targetX, targetY = self.path[self.posIndex]
        dx = targetX - self.sizeRect.centerx
        dy = targetY - self.sizeRect.centery
        dist = (dx**2 + dy**2) **0.5
        
        if dist < 1:
            self.posIndex += 1
            # print("reached")
        else:
            if self.attacking:
                pass
            else:
                self.sizeRect.centerx += int(self.speed * dx/dist)
                self.sizeRect.centery += int(self.speed * dy/dist)
            
        
    def drawSprite(self):
        if self.dead and self.deadAnim:
            frame = int(self.deadFrameCounter)
            if frame < len(self.deadAnim):
                img = self.deadAnim[frame]
                if self.side == "red":
                    img = transform.flip(img, True, False)
                screen.blit(img, (self.sizeRect.centerx-25, self.sizeRect.centery-25))
                self.deadFrameCounter += 0.15
            return
        if self.attacking:
            self.animationList = self.attackAnim
        else:
            self.animationList = self.runAnim
        self.frameCounter += self.frameSpeed
        if self.frameCounter >= len(self.animationList):
            self.frameCounter = 0
        self.animationIndex = int(self.frameCounter)
        if self.side == "red":
            screen.blit(transform.flip(self.animationList[self.animationIndex], True, False), (self.sizeRect.centerx-25, self.sizeRect.centery-25))
        elif self.side == "blue":
            screen.blit(transform.flip(self.animationList[self.animationIndex], False, False), (self.sizeRect.centerx-25, self.sizeRect.centery-25))
        

    def attack(self, opponent):
        if self.sizeRect.colliderect(opponent.sizeRect) and not self.dead and not opponent.dead:
            self.attacking = True
            if int(self.frameCounter) == len(self.attackAnim) - 1 and not self.hasDealtDamage:
                opponent.health -= self.damage
                self.hasDealtDamage = True
        else:
            self.attacking = False
            self.hasDealtDamage = False

        self.frameCounter += self.frameSpeed
        if self.frameCounter >= len(self.attackAnim):
            self.frameCounter = 0
            self.hasDealtDamage = False

class Golem:
    def __init__(self, side, health, damage, width, speed, path, spwnX, spwxY, frameCounter, frameSpeed, runAnim, attackAnim, animIndex, deadAnim=None):
        self.side = side
        self.health = health
        self.damage = damage
        self.dead = False
        self.deadAnim = deadAnim if deadAnim else []
        self.deadFrameCounter = 0
        self.attacking = False
        self.speed = speed
        self.sizeRect = Rect(35, 35, width, width)
        self.path = path
        self.sizeRect.center = (spwnX, spwxY)
        self.posIndex = 0
        self.frameCounter = frameCounter
        self.frameSpeed = frameSpeed
        self.runAnim = runAnim
        self.attackAnim = attackAnim  
        self.animationList = self.runAnim
        self.animationIndex = animIndex
        self.attackCooldown = 0
        self.attackCooldownMax = len(self.attackAnim)
        self.hasDealtDamage = False
        self.elixir = 5
    
    def updatePos(self):
        if self.dead:
            return
        if self.attacking:
            self.animationList = self.attackAnim
        else:
            self.animationList = self.runAnim

        if self.posIndex >= len(self.path):
            return
        targetX, targetY = self.path[self.posIndex]
        dx = targetX - self.sizeRect.centerx
        dy = targetY - self.sizeRect.centery
        dist = (dx**2 + dy**2) **0.5
        
        if dist < 1:
            self.posIndex += 1
        else:
            if self.attacking:
                pass
            else:
                self.sizeRect.centerx += int(self.speed * dx/dist)
                self.sizeRect.centery += int(self.speed * dy/dist)
            
    def drawSprite(self):
        if self.dead and self.deadAnim:
            frame = int(self.deadFrameCounter)
            if frame < len(self.deadAnim):
                img = self.deadAnim[frame]
                if self.side == "red":
                    img = transform.flip(img, True, False)
                screen.blit(img, (self.sizeRect.centerx-25, self.sizeRect.centery-25))
                self.deadFrameCounter += 0.15
            return
        if self.attacking:
            self.animationList = self.attackAnim
        else:
            self.animationList = self.runAnim
        self.frameCounter += self.frameSpeed
        if self.frameCounter >= len(self.animationList):
            self.frameCounter = 0
        self.animationIndex = int(self.frameCounter)
        if self.side == "red":
            screen.blit(transform.flip(self.animationList[self.animationIndex], True, False), (self.sizeRect.centerx-25, self.sizeRect.centery-25))
        elif self.side == "blue":
            screen.blit(transform.flip(self.animationList[self.animationIndex], False, False), (self.sizeRect.centerx-25, self.sizeRect.centery-25))        

 
    def attack(self, opponent):
        if self.sizeRect.colliderect(opponent.sizeRect) and not self.dead and not opponent.dead:
            self.attacking = True
            if int(self.frameCounter) == len(self.attackAnim) - 1 and not self.hasDealtDamage:
                opponent.health -= self.damage
                self.hasDealtDamage = True
        else:
            self.attacking = False
            self.hasDealtDamage = False

        self.frameCounter += self.frameSpeed
        if self.frameCounter >= len(self.attackAnim):
            self.frameCounter = 0
            self.hasDealtDamage = False
        
    
        
        
# Blue Towers  
        screen.blit(sideTower, (270, 190))      
        screen.blit(mainTower, (250, 325))
        screen.blit(sideTower, (270, 510))
        
        # Red Towers
        screen.blit(sideTower, (1070, 190))      
        screen.blit(mainTower, (1050, 325))
        screen.blit(sideTower, (1070, 510))

mainTower = transform.scale(image.load("assets/towers/mainTower.png", "png"), (193/2, 254/2))
sideTower = transform.scale(image.load("assets/towers/miniTower.png", "png"), (106/2, 178/2))
blueTroops = []
blueTowers = [
    Tower("blue", 270, 190, sideTower),
    Tower("blue", 250, 325, mainTower),
    Tower("blue", 270, 510, sideTower)
]
redTroops = []
redTowers = [
    Tower("red", 1070, 190, sideTower),
    Tower("red", 1050, 325, mainTower),
    Tower("red", 1070, 510, sideTower)
]

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
faceCardsPath = []
blueRandom = []
redRandom = []

for i in range(1, 9):
    assassinAttack.append(transform.scale(image.load("assets/assassin-attack/assassin-attack"+ str(i) +".png"), (50, 50)))

for i in range(1, 5):
    assassinDead.append(transform.scale(image.load("assets/assassin-dead/assassin-dead"+ str(i) +".png"), (50, 50)))

for i in range(1, 9):
    assassinRun.append(transform.scale(image.load("assets/assassin-run/assassin-run"+ str(i) +".png"), (50, 50)))


for i in range(1, 8):
    femaleWizardAttack.append(transform.scale(image.load("assets/femaleWizard-attack/femaleWizard-attack"+ str(i) +".png"), (50, 50)))

for i in range(1, 6):
    femaleWizardDead.append(transform.scale(image.load("assets/femaleWizard-dead/femaleWizard-dead"+ str(i) +".png"), (50, 50)))

for i in range(1, 9):
    femaleWizardRun.append(transform.scale(image.load("assets/femaleWizard-run/femaleWizard-run"+ str(i) +".png"), (50, 50)))


for i in range(1, 4):
    firemenAttack.append(transform.scale(image.load("assets/firemen-attack/" + str(i) + ".png"), (50, 50)))

for i in range(1, 6):
    firemenDead.append(transform.scale(image.load("assets/firemen-dead/"+ str(i) +".png"), (50, 50)))

for i in range(1, 8):
    firemenRun.append(transform.scale(image.load("assets/firemen-run/"+ str(i) +".png"), (50, 50)))


for i in range(1, 4):
    icemenAttack.append(transform.scale(image.load("assets/iceman-attack/" + str(i) + ".png"), (50, 50)))

for i in range(1, 7):
    icemenDead.append(transform.scale(image.load("assets/iceman-dead/"+ str(i) +".png"), (50, 50)))

for i in range(1, 6):
    icemenRun.append(transform.scale(image.load("assets/iceman-run/"+ str(i) +".png"), (50, 50)))


for i in range(1, 7):
    golemAttack.append(transform.scale(image.load("assets/golem-attack/" + str(i) + ".png"), (50, 50)))

for i in range(1, 6):
    golemDead.append(transform.scale(image.load("assets/golem-dead/"+ str(i) +".png"), (50, 50)))

for i in range(1, 8):
    golemRun.append(transform.scale(image.load("assets/golem-run/"+ str(i) +".png"), (50, 50)))


for i in range(1, 5):
    jackAttack.append(transform.scale(image.load("assets/jack-attack/jack-attack"+ str(i) +".png"), (50, 50)))

for i in range(1, 5):
    jackDead.append(transform.scale(image.load("assets/jack-dead/jack-dead"+ str(i) +".png"), (50, 50)))

for i in range(1, 7):
    jackRun.append(transform.scale(image.load("assets/jack-run/jack-run"+ str(i) +".png"), (50, 50)))


for i in range(1, 5):
    knightAttack.append(transform.scale(image.load("assets/knight-attack/knight-attack"+ str(i) +".png"), (50, 50)))

for i in range(1, 5):
    knightDead.append(transform.scale(image.load("assets/knight-dead/knight-dead"+ str(i) +".png"), (50, 50)))

for i in range(1, 7):
    knightRun.append(transform.scale(image.load("assets/knight-run/knight-run"+ str(i) +".png"), (50, 50)))


for i in range(1, 8):
    maleWizardAttack.append(transform.scale(image.load("assets/maleWizard-attack/maleWizard-attack"+ str(i) +".png"), (50, 50)))

for i in range(1, 7):
    maleWizardDead.append(transform.scale(image.load("assets/maleWizard-dead/maleWizard-dead"+ str(i) +".png"), (50, 50)))

for i in range(1, 9):
    maleWizardRun.append(transform.scale(image.load("assets/maleWizard-run/maleWizard-run"+ str(i) +".png"), (50, 50)))

for i in range(1, 8):
    maleWizardAttack.append(transform.scale(image.load("assets/maleWizard-attack/maleWizard-attack"+ str(i) +".png"), (50, 50)))

for i in range(1, 7):
    maleWizardDead.append(transform.scale(image.load("assets/maleWizard-dead/maleWizard-dead"+ str(i) +".png"), (50, 50)))

for i in range(1, 9):
    maleWizardRun.append(transform.scale(image.load("assets/maleWizard-run/maleWizard-run"+ str(i) +".png"), (50, 50)))


for i in range(1, 4):
    spearmenAttack.append(transform.scale(image.load("assets/spearmen-attack/spearmen-attack"+ str(i) +".png"), (50, 50)))

for i in range(1, 5):
    spearmenDead.append(transform.scale(image.load("assets/spearmen-dead/spearmen-dead"+ str(i) +".png"), (50, 50)))

for i in range(1, 6):
    spearmenWalk.append(transform.scale(image.load("assets/spearmen-walk/spearman-walk"+ str(i) +".png"), (50, 50)))




    
# Assassin - Wizard
assassinRunIndex = 0
assassinAttackIndex = 0
assassinFrameCounter = 0
assassinFrameSpeed = 0.05
assassinRunningAnimation = False
assassinAttackAnimation = False

# Female Wizard - Wizard
femaleWizardRunIndex = 0
femaleWizardAttackIndex = 0
femaleWizardFrameCounter = 0
femaleWizardFrameSpeed = 0.05
femaleWizardRunningAnimation = False
femaleWizardAttackAnimation = False

# Firemen - Golem
firemenRunIndex = 0
firemenAttackIndex = 0
firemenFrameCounter = 0
firemenFrameSpeed = 0.05
firemenRunningAnimation = False
firemenAttackAnimation = False

# Icemen - Golem
icemenRunIndex = 0
icemenAttackIndex = 0
icemenFrameCounter = 0
icemenFrameSpeed = 0.05
icemenRunningAnimation = False
icemenAttackAnimation = False

# Golem - Golem
golemRunIndex = 0
golemAttackIndex = 0
golemFrameCounter = 0
golemFrameSpeed = 0.05
golemRunningAnimation = False
golemAttackAnimation = False

# Jack - Barb
jackRunIndex = 0
jackAttackIndex = 0
jackFrameCounter = 0
jackFrameSpeed = 0.05
jackRunningAnimation = False
jackAttackAnimation = False

# Knight - Barb
knightRunIndex = 0
knightAttackIndex = 0
knightFrameCounter = 0
knightFrameSpeed = 0.05
knightRunningAnimation = False
knightAttackAnimation = False

# Male Wizard - Wizard
maleWizardRunIndex = 0
maleWizardAttackIndex = 0
maleWizardFrameCounter = 0
maleWizardFrameSpeed = 0.05
maleWizardRunningAnimation = False
maleWizardAttackAnimation = False

# Spearmen - Barb
spearmenRunIndex = 0
spearmenAttackIndex = 0
spearmenFrameCounter = 0
spearmenFrameSpeed = 0.05
spearmenRunningAnimation = False
spearmenAttackAnimation = False

runIndex = 0
attackIndex = 0
frameCounter = 0
frameSpeed = 0.1




for i in range(9):
    faceCards.append(image.load("assets/mainFace/mainface"+ str(i+1) +".png"))
    faceCardsPath.append("assets/mainFace/mainface"+ str(i+1) +".png")


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
blueInd = 0
screenNum = 1



blueElixir = 6
redElixir = 6
blueElixirLastUpdate = time.get_ticks()
redElixirLastUpdate = time.get_ticks()
elixirMax = 10

animationPicker = {
    "Wizard": {
        "Assasin": {
            "runAnim": assassinRun,
            "runIndex": assassinRunIndex,
            "attackIndex": assassinAttackIndex,
            "attackAnim": assassinAttack, 
            "frameCounter": assassinFrameCounter,
            "frameSpeed": assassinFrameSpeed,
            "runningAnimation": assassinRunningAnimation,
            "attackAnimation": assassinAttackAnimation,
            "deadAnim": assassinDead,
            "spriteFacecard": "assets/mainFace/mainface1.png"
        },
        "MaleWizard": {
            "runAnim": maleWizardRun,
            "runIndex": maleWizardRunIndex,
            "attackIndex": maleWizardAttackIndex,
            "attackAnim": maleWizardAttack,
            "frameCounter": maleWizardFrameCounter,
            "frameSpeed": maleWizardFrameSpeed,
            "runningAnimation": maleWizardRunningAnimation,
            "attackAnimation": maleWizardAttackAnimation,
            "deadAnim": maleWizardDead,
            "spriteFacecard": "assets/mainFace/mainface8.png"
        },
        "FemaleWizard": {
            "runAnim": femaleWizardRun,
            "runIndex": femaleWizardRunIndex,
            "attackIndex": femaleWizardAttackIndex,
            "attackAnim": femaleWizardAttack,
            "frameCounter": femaleWizardFrameCounter,
            "frameSpeed": femaleWizardFrameSpeed,
            "runningAnimation": femaleWizardRunningAnimation,
            "attackAnimation": femaleWizardAttackAnimation,
            "deadAnim": femaleWizardDead,
            "spriteFacecard": "assets/mainFace/mainface2.png"
        }
    },
    "Barbarian": {
        "Jack": {
            "runAnim": jackRun,
            "runIndex": jackRunIndex,
            "attackIndex": jackAttackIndex,
            "attackAnim": jackAttack,
            "frameCounter": jackFrameCounter,
            "frameSpeed": jackFrameSpeed,
            "runningAnimation": jackRunningAnimation,
            "attackAnimation": jackAttackAnimation,
            "deadAnim": jackDead,
            "spriteFacecard": "assets/mainFace/mainface6.png"
        },
        "Knight": {
            "runAnim": knightRun,
            "runIndex": knightRunIndex,
            "attackIndex": knightAttackIndex,
            "attackAnim": knightAttack,
            "frameCounter": knightFrameCounter,
            "frameSpeed": knightFrameSpeed,
            "runningAnimation": knightRunningAnimation,
            "attackAnimation": knightAttackAnimation,
            "deadAnim": knightDead,
            "spriteFacecard": "assets/mainFace/mainface7.png"
        },
        "Spearmen": {
            "runAnim": spearmenWalk,
            "runIndex": spearmenRunIndex,
            "attackIndex": spearmenAttackIndex,
            "attackAnim": spearmenAttack,
            "frameCounter": spearmenFrameCounter,
            "frameSpeed": spearmenFrameSpeed,
            "runningAnimation": spearmenRunningAnimation,
            "attackAnimation": spearmenAttackAnimation,
            "deadAnim": spearmenDead,
            "spriteFacecard": "assets/mainFace/mainface9.png"
        }
    },
    "Golem": {
        "Firemen": {
            "runAnim": firemenRun,
            "runIndex": firemenRunIndex,
            "attackIndex": firemenAttackIndex,
            "attackAnim": firemenAttack,
            "frameCounter": firemenFrameCounter,
            "frameSpeed": firemenFrameSpeed,
            "runningAnimation": firemenRunningAnimation,
            "attackAnimation": firemenAttackAnimation,
            "deadAnim": firemenDead,
            "spriteFacecard": "assets/mainFace/mainface3.png"
        },
        "Icemen": {
            "runAnim": icemenRun,
            "runIndex": icemenRunIndex,
            "attackIndex": icemenAttackIndex,
            "attackAnim": icemenAttack,
            "frameCounter": icemenFrameCounter,
            "frameSpeed": icemenFrameSpeed,
            "runningAnimation": icemenRunningAnimation,
            "attackAnimation": icemenAttackAnimation,
            "deadAnim": icemenDead,
            "spriteFacecard": "assets/mainFace/mainface5.png"
        },
        "DefaultGolem": {
            "runAnim": golemRun,
            "runIndex": golemRunIndex,
            "attackIndex": golemAttackIndex,
            "attackAnim": golemAttack,
            "frameCounter": golemFrameCounter,
            "frameSpeed": golemFrameSpeed,
            "runningAnimation": golemRunningAnimation,
            "attackAnimation": golemAttackAnimation,
            "deadAnim": golemDead,
            "spriteFacecard": "assets/mainFace/mainface4.png"
        }
    }
}




                


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

        # After each new line, move to new line
        x = rect.left
        y += font.get_linesize()

for i in range(5):
    blueRandom = sample(range(1, 9), 5)  
    redRandom = sample(range(1, 9), 5) 

parentKeys = []
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
                blueInd = 0
            if evt.key == K_2:
                blueInd = 1
            if evt.key == K_3:
                blueInd = 2
            if evt.key == K_4:
                blueInd = 3
            if evt.key == K_7:
                redInd = 0
            if evt.key == K_8:
                redInd = 1
            if evt.key == K_9:
                redInd = 2
            if evt.key == K_0:
                redInd = 3
            if evt.key == K_e:
                currDeckBlue = [blueFinalCards[i] for i in range(4)]
                bIndex = faceCards.index(currDeckBlue[blueInd])
                parentKeys = findKeys(faceCardsPath[bIndex], animationPicker)
                troopType = parentKeys[0]
                cardType = parentKeys[1]
                if troopType == "Wizard":
                    elixirCost = 5
                elif troopType == "Barbarian":
                    elixirCost = 3
                elif troopType == "Golem":
                    elixirCost = 7
                else:
                    elixirCost = 5
                if blueElixir >= elixirCost:
                    if troopType == "Wizard":
                        blueTroops.append(Wizard("blue", 20000000000, 50, 20, 2, blueTopTowerPath, bluePlayerSelect.centerx, bluePlayerSelect.centery,
                                                frameCounter, 
                                                animationPicker[troopType][cardType]["frameSpeed"],
                                                animationPicker[troopType][cardType]["runAnim"],
                                                animationPicker[troopType][cardType]["attackAnim"],
                                                animationPicker[troopType][cardType]["runIndex"],
                                                animationPicker[troopType][cardType]["deadAnim"]))
                    elif troopType == "Barbarian":
                        blueTroops.append(Barbarian("blue", 100, 10, 20, 2, blueTopTowerPath, bluePlayerSelect.centerx, bluePlayerSelect.centery,
                                                frameCounter, 
                                                animationPicker[troopType][cardType]["frameSpeed"],
                                                animationPicker[troopType][cardType]["runAnim"],
                                                animationPicker[troopType][cardType]["attackAnim"],
                                                animationPicker[troopType][cardType]["runIndex"],
                                                animationPicker[troopType][cardType]["deadAnim"]))
                    elif troopType == "Golem":
                        blueTroops.append(Golem("blue", 200, 20, 20, 2, blueTopTowerPath, bluePlayerSelect.centerx, bluePlayerSelect.centery,
                                                frameCounter, 
                                                animationPicker[troopType][cardType]["frameSpeed"],
                                                animationPicker[troopType][cardType]["runAnim"],
                                                animationPicker[troopType][cardType]["attackAnim"],
                                                animationPicker[troopType][cardType]["runIndex"],
                                                animationPicker[troopType][cardType]["deadAnim"]))

                    blueElixir -= elixirCost 
                    for a in blueFinalCards:
                        if currDeckBlue.count(a) == 0:
                            blueFinalCards[blueInd], blueFinalCards[4] = blueFinalCards[4], blueFinalCards[blueInd]


            if evt.key == K_u:
                currDeckRed = [redFinalCards[i] for i in range(4)]
                rIndex = faceCards.index(currDeckRed[redInd])
                parentKeys = findKeys(faceCardsPath[rIndex], animationPicker)
                troopType = parentKeys[0]
                cardType = parentKeys[1]
                if troopType == "Wizard":
                    elixirCost = 5
                elif troopType == "Barbarian":
                    elixirCost = 3
                elif troopType == "Golem":
                    elixirCost = 7
                # else:
                #     elixir_cost = 5
                if redElixir >= elixirCost:
                    if troopType == "Wizard":
                        redTroops.append(Wizard("red", 150, 15, 20, 2, redLeftTowerPath, redPlayerSelect.centerx, redPlayerSelect.centery,
                                                frameCounter, 
                                                animationPicker[troopType][cardType]["frameSpeed"],
                                                animationPicker[troopType][cardType]["runAnim"],
                                                animationPicker[troopType][cardType]["attackAnim"],
                                                animationPicker[troopType][cardType]["runIndex"],
                                                animationPicker[troopType][cardType]["deadAnim"]))
                    elif troopType == "Barbarian":
                        redTroops.append(Barbarian("red", 100, 10, 20, 2, redLeftTowerPath, redPlayerSelect.centerx, redPlayerSelect.centery,
                                                frameCounter, 
                                                animationPicker[troopType][cardType]["frameSpeed"],
                                                animationPicker[troopType][cardType]["runAnim"],
                                                animationPicker[troopType][cardType]["attackAnim"],
                                                animationPicker[troopType][cardType]["runIndex"],
                                                animationPicker[troopType][cardType]["deadAnim"]))
                    elif troopType == "Golem":
                        redTroops.append(Golem("red", 200, 20, 20, 2, redLeftTowerPath, redPlayerSelect.centerx, redPlayerSelect.centery,
                                                frameCounter, 
                                                animationPicker[troopType][cardType]["frameSpeed"],
                                                animationPicker[troopType][cardType]["runAnim"],
                                                animationPicker[troopType][cardType]["attackAnim"],
                                                animationPicker[troopType][cardType]["runIndex"],
                                                animationPicker[troopType][cardType]["deadAnim"]))
                redElixir -= elixirCost  
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
        if not blueFinalCards:
            for i in range(5):
                blueFinalCards.append(faceCards[blueRandom[i]])
        if not redFinalCards:
            for i in range(5):
                redFinalCards.append(faceCards[redRandom[i]])
        for i in range(5):
            draw.rect(screen, WHITE, bluePlayerCard[i], 5)
            screen.blit(faceCards[blueRandom[i]], bluePlayerCard[i])
        for i in range(5):
            draw.rect(screen, WHITE, RedPlayerCard[i], 5)
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
        
        # # Left Grid 
        # for i in range(10):
        #     draw.line(screen, GREEN, (350, i*46.5+210), (628, i*46.5+210), 2)
        # for i in range(7):
        #     draw.line(screen, GREEN, (i*47+347, 210), (i*47+347, 630), 2)

        # # Right Grid
        # for i in range(10):
        #     draw.line(screen, GREEN, (760, i*46.5+210), (1040, i*46.5+210), 2)
        # for i in range(7):
        #     draw.line(screen, GREEN, (i*46.5+760, 210), (i*46.5+760, 630), 2)
        
        # Blue player
        for i in range(9):
            for j in range(6):
                if grid1[i][j] == 1:
                    bluePlayerSelect = Rect(j*47+347, i*46.5+210, 50,50)
                    draw.rect(screen, BLUE, (j*47+347, i*46.5+210, 50,50), 5)

        # Red player       
        for i in range(9):
            for j in range(6):
                if grid2[i][j] == 1:
                    redPlayerSelect = Rect(j*47+755, i*46.5+210, 50, 50)
                    draw.rect(screen, RED, (j*47+755, i*46.5+210, 50, 50), 5)
            
        # # Red Towers  
        # screen.blit(sideTower, (270, 190))      
        # screen.blit(mainTower, (250, 325))
        # screen.blit(sideTower, (270, 510))
# Draw and update blue towers
        for tower in blueTowers[:]:
            if tower.health > 0:
                tower.draw(screen)
                tower.attack(redTroops)
            else:
                blueTowers.remove(tower)  # Remove destroyed tower

        # Draw and update red towers
        for tower in redTowers[:]:
            if tower.health > 0:
                tower.draw(screen)
                tower.attack(blueTroops)
            else:
                redTowers.remove(tower)
                
        # # BLue Towers
        # screen.blit(sideTower, (1070, 190))      
        # screen.blit(mainTower, (1050, 325))
        # screen.blit(sideTower, (1070, 510))
                        
        draw.rect(screen,BLUE,(0,147,183,406),2)
        draw.line(screen,WHITE,(40,150),(40,550))

        now = time.get_ticks()
        if now - blueElixirLastUpdate >= 1000:
            if blueElixir < elixirMax:
                blueElixir += 1
            blueElixirLastUpdate = now
        if now - redElixirLastUpdate >= 1000:
            if redElixir < elixirMax:
                redElixir += 1
            redElixirLastUpdate = now

        for i in range(10):
            draw.rect(screen,WHITE,(0,150,40,i*40+40),2)
        for i in range(10):
            color = ELIXIR_COLOR if i < blueElixir else (50, 50, 50)
            draw.rect(screen, color, (0, 150 + i*40, 40, 40))
            draw.rect(screen, WHITE, (0, 150 + i*40, 40, 40), 2)

        for i in range(4):
            screen.blit(transform.scale(blueFinalCards[i], (100, 100)), (60, i*100+150, 140, 100))
            draw.rect(screen, WHITE, (40, i*100+150, 140, 100), 2)
            blueCardSelectRect = Rect(40, i*100+150, 140, 100)
            if i == blueInd:
                draw.rect(screen, BLUE, blueCardSelectRect, 10)
            else:
                draw.rect(screen, WHITE, blueCardSelectRect, 2)
            bIndex = faceCards.index(blueFinalCards[i])
            parentKeys = findKeys(faceCardsPath[bIndex], animationPicker)
            troopType = parentKeys[0]
            if troopType == "Wizard":
                elixirCost = 5
            elif troopType == "Barbarian":
                elixirCost = 3
            elif troopType == "Golem":
                elixirCost = 7
            else:
                elixirCost = 5
            if blueElixir < elixirCost:
                overlay = Surface((140, 100), SRCALPHA)
                overlay.fill((200, 200, 200, 180))
                screen.blit(overlay, (40, i*100+150))
                costText = textfont.render(str(elixirCost), True, (100, 100, 100))
                screen.blit(costText, (40 + 70, i*100+150 + 40))  # Centered


        draw.rect(screen,RED,(1217,147,183,406),2)
        draw.line(screen,WHITE,(1360,150),(1360,550))

        for i in range(10):
            if i < blueElixir:
                color = ELIXIR_COLOR
            else:
                color = (50, 50, 50)
            draw.rect(screen, color, (0, 150 + i*40, 40, 40))
            draw.rect(screen, WHITE, (0, 150 + i*40, 40, 40), 2)

        for i in range(10):
            if i < redElixir:
                color = ELIXIR_COLOR
            else:
                color = (50, 50, 50)
            draw.rect(screen, color, (1360, 150 + i*40, 40, 40))
            draw.rect(screen, WHITE, (1360, 150 + i*40, 40, 40), 2)
        for i in range(10):
            draw.rect(screen, WHITE, (1360, 150, 1360, i*40+40), 2)


        for i in range(4):
            screen.blit(transform.scale(redFinalCards[i], (100, 100)), (1240, i*100+150, 140, 100))
            redCardSelectRect = Rect(1220, i*100+150, 140, 100)
            if i == redInd:
                draw.rect(screen, RED, redCardSelectRect, 10)
            else:
                draw.rect(screen, WHITE, redCardSelectRect, 2)
            rIndex = faceCards.index(redFinalCards[i])
            parentKeys = findKeys(faceCardsPath[rIndex], animationPicker)
            troopType = parentKeys[0]
            if troopType == "Wizard":
                elixirCost = 5
            elif troopType == "Barbarian":
                elixirCost = 3
            elif troopType == "Golem":
                elixirCost = 7
            else:
                elixirCost = 5
            if redElixir < elixirCost:
                overlay = Surface((140, 100), SRCALPHA)
                overlay.fill((200, 200, 200, 180))
                screen.blit(overlay, (1220, i*100+150))
                costText = textfont.render(str(elixirCost), True, (100, 100, 100))
                screen.blit(costText, (1220 + 70, i*100+150 + 40))  


        for p in redLeftTowerPath:
            draw.circle(screen, RED, p, 10)
        for p in blueTopTowerPath:
            draw.circle(screen, BLUE, p, 10)


        for troop in redTroops[:]:
            if troop.health <= 0 and not troop.dead:
                troop.dead = True
                troop.deadFrameCounter = 0
            if troop.dead and (not troop.deadAnim or troop.deadFrameCounter >= len(troop.deadAnim)):
                redTroops.remove(troop)
            else:
                troop.updatePos()

        for troop in blueTroops[:]:
            if troop.health <= 0 and not troop.dead:
                troop.dead = True
                troop.deadFrameCounter = 0
            if troop.dead and (not troop.deadAnim or troop.deadFrameCounter >= len(troop.deadAnim)):
                blueTroops.remove(troop)
            else:
                troop.updatePos()


        for troop in redTroops:
            troop.drawSprite()
        for troop in blueTroops:
            troop.drawSprite()

        for red in redTroops:
            if isinstance(red, Wizard):
                red.attack(blueTroops)
            else:
                for blue in blueTroops:
                    red.attack(blue)
        for blue in blueTroops:
            if isinstance(blue, Wizard):
                blue.attack(redTroops)
            else:
                for red in redTroops:
                    blue.attack(red)

        towerAttackRadius = 50  

        # Blue troops attack red towers
        for troop in blueTroops:
            if troop.dead:
                continue
            attacked = False
            for tower in redTowers:
                if tower.health > 0:
                    dx = troop.sizeRect.centerx - (tower.x + tower.image.get_width() // 2)
                    dy = troop.sizeRect.centery - (tower.y + tower.image.get_height() // 2)
                    dist = (dx ** 2 + dy ** 2) ** 0.5
                    if dist <= towerAttackRadius:
                        troop.attacking = True
                        attacked = True
                        troop.animationList = troop.attackAnim
                        troop.frameCounter += troop.frameSpeed
                        if troop.frameCounter >= len(troop.attackAnim):
                            troop.frameCounter = 0
                            troop.hasDealtDamage = False 
                        if int(troop.frameCounter) == len(troop.attackAnim) - 1 and not troop.hasDealtDamage:
                            tower.health -= troop.damage
                            troop.hasDealtDamage = True
                        break
            if not attacked:
                troop.attacking = False
                troop.hasDealtDamage = False
                troop.animationList = troop.runAnim
                troop.frameCounter += troop.frameSpeed
                if troop.frameCounter >= len(troop.runAnim):
                    troop.frameCounter = 0


        for troop in redTroops:
            if troop.dead:
                continue
            attacked = False
            for tower in blueTowers:
                if tower.health > 0:
                    dx = troop.sizeRect.centerx - (tower.x + tower.image.get_width() // 2)
                    dy = troop.sizeRect.centery - (tower.y + tower.image.get_height() // 2)
                    dist = (dx ** 2 + dy ** 2) ** 0.5
                    if dist <= towerAttackRadius:
                        troop.attacking = True
                        attacked = True
                        troop.animationList = troop.attackAnim
                        troop.frameCounter += troop.frameSpeed
                        if troop.frameCounter >= len(troop.attackAnim):
                            troop.frameCounter = 0
                            troop.hasDealtDamage = False
                        if int(troop.frameCounter) == len(troop.attackAnim) - 1 and not troop.hasDealtDamage:
                            tower.health -= troop.damage
                            troop.hasDealtDamage = True
                        break
            if not attacked:
                troop.attacking = False
                troop.hasDealtDamage = False
                troop.animationList = troop.runAnim
                troop.frameCounter += troop.frameSpeed
                if troop.frameCounter >= len(troop.runAnim):
                    troop.frameCounter = 0

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
