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
ELIXERCOLOR = (176, 122, 255)
myClock=time.Clock()
running=True

#used for animations
frameCounter = 0

# Define the paths that troops will follow for both red and blue sides
redTopTowerPath = [(770, 371), (690, 370), (615, 371), (300, 250)]
redBotTowerPath = [(770, 471), (690, 470), (615, 471), (300, 560)]
redKingTowerPos = (260, 400)

blueTopTowerPath = [(615, 371), (690, 370), (770, 371), (1060, 250)]
blueBotTowerPath = [(615, 470), (690, 470), (770, 470), (1060, 560)]
blueKingTowerPos = (1100, 400)


def determinePath(troops, topPath, botPath, kingPos, towers):
    for troop in troops:
        if not troop.pathFound:
        # Calculate distance to top and bottom path starting points
            topDist = ((troop.sizeRect.centerx - topPath[0][0])**2 + (troop.sizeRect.centery - topPath[0][1])**2) ** 0.5
            botDist = ((troop.sizeRect.centerx - botPath[0][0])**2 + (troop.sizeRect.centery - botPath[0][1])**2) ** 0.5
            # Choose the closer path           
            if topDist < botDist:
                troop.path = topPath
            else:
                troop.path = botPath
        # If the side tower is destroyed go to king tower path
            troop.pathFound = True
    if len(towers) !=0:
        if towers[0].image != sideTower and troop.path == topPath:
            troop.path[-1] = kingPos
            if troop.posIndex >= len(troop.path):
                troop.posIndex = len(troop.path) - 1
        elif towers[-1].image != sideTower and troop.path == botPath:
            troop.path[-1] = kingPos
            if troop.posIndex >= len(troop.path):
                troop.posIndex = len(troop.path) - 1
    else:
        return

                
        
        
            

        
        
    




def findKeys(value, dict):
    for troop, cards in dict.items():
        for card, attributes in cards.items():
            for attrName, attribute in attributes.items():
                if value == attribute:
                    return [troop, card, attrName]
                



# Tower class with all its attributes and methods
class Tower:
    def __init__(self, side, x, y, image, health=800):
        self.side = side  
        self.x = x
        self.y = y
        self.image = image
        self.health = health
        self.max_health = health
        self.damage = 30
        self.attack_range = 100
        self.sizeRect = Rect(x, y, image.get_width(), image.get_height())
        self.frameCounter = 0
        self.attackSpeed = 1  
        self.lastAttack = 0
    # Draw the tower and its health bar
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        barWidth = self.image.get_width()
        barHeight = 8
        healthRatio = max(self.health / self.max_health, 0)
        healthBarRect = Rect(self.x, self.y - 12, int(barWidth * healthRatio), barHeight)
        borderRect = Rect(self.x, self.y - 12, barWidth, barHeight)
        draw.rect(surface, (0, 255, 0), healthBarRect)
        draw.rect(surface, (255, 0, 0), Rect(self.x + healthBarRect.width, self.y - 12, barWidth - healthBarRect.width, barHeight))
        draw.rect(surface, (255, 255, 255), borderRect, 2)

    # Attack enemy troops if they are in range
    def attack(self, enemy_troops):
        now = time.get_ticks()
        if now - self.lastAttack < 1000 / self.attackSpeed:
            return  
        for troop in enemy_troops:
            if not troop.dead:
                #calculate distance to the troop
                dx = (troop.sizeRect.centerx - (self.x + self.image.get_width() // 2))
                dy = (troop.sizeRect.centery - (self.y + self.image.get_height() // 2))
                dist = (dx ** 2 + dy ** 2) ** 0.5
                # If the troop is within attack range deal damage
                if dist <= self.attack_range:
                    troop.health -= self.damage
                    self.lastAttack = now
                    break  # Only attack one troop per cycle

# Wizard class with all its attributes and methods       
class Wizard:
    def __init__(self, side, health, damage, width, speed, path, spwnX, spwxY, frameCounter, frameSpeed, runAnim, attackAnim, animIndex, deadAnim=None):
        self.side = side
        self.health = health
        self.maxHealth = health
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
        self.attackRad = 100
        self.attackBox = Rect(self.sizeRect.centerx-self.attackRad/2, self.sizeRect.centery-self.attackRad*2, self.attackRad*2, self.attackRad*2)
        self.animationList = self.runAnim
        self.animationIndex = animIndex
        self.attackCooldown = 0
        self.attackCooldownMax = len(self.attackAnim)
        self.attackRadius = 60
        self.detectRad = 120
        self.detectBox = Rect(self.sizeRect.centerx-self.detectRad/2, self.sizeRect.centery-self.detectRad/2, self.detectRad, self.detectRad)
        self.hasDealtDamage = False
        self.elixir = 5
        self.isFollowing = False
        self.lastAttack = 0
        self.attackSpeed = 1 
        self.pathFound = False


# Update the wizard's position along its path or towards an enemy
    def updatePos(self):
        if self.dead:
            return
        # If not following an enemy, move along the path to the tower
        if self.isFollowing == False:
            if self.posIndex >= len(self.path):
                return
            targetX, targetY = self.path[self.posIndex]
            dx = targetX - self.sizeRect.centerx
            dy = targetY - self.sizeRect.centery
            dist = (dx**2 + dy**2) **0.5
            if dist < 5:
                self.center = self.path[self.posIndex]
                self.posIndex += 1
                
            else:
                if self.attacking:
                    pass
                else:
                    self.sizeRect.centerx += int(self.speed * dx/dist)
                    self.attackBox.centerx += int(self.speed * dx/dist)
                    self.detectBox.centery += int(self.speed * dy/dist)
                    self.sizeRect.centery += int(self.speed * dy/dist)
                    self.attackBox.centery += int(self.speed * dy/dist)
                    self.detectBox.centery += int(self.speed * dy/dist)
       
        # If following an enemy move towards it
        else:
            wox = opponent.sizeRect.centerx - self.sizeRect.centerx
            woy = opponent.sizeRect.centery - self.sizeRect.centery
            wdist = (wox**2 + woy**2) ** 0.5
            
            if self.attacking:
                self.sizeRect.centerx += 0
                self.attackBox.centerx += 0
                self.detectBox.centerx += 0
                self.sizeRect.centery += 0
                self.attackBox.centery += 0
                self.detectBox.centery += 0
            else:
                self.sizeRect.centerx += int(self.speed * wox/wdist)
                self.attackBox.centerx += int(self.speed * wox/wdist)
                self.detectBox.centerx += int(self.speed * wox/wdist)
                self.sizeRect.centery += int(self.speed * woy/wdist)
                self.attackBox.centery += int(self.speed * woy/wdist)
                self.detectBox.centery += int(self.speed * woy/wdist)
            
# Draw the wizard and its health bar 
    def drawSprite(self):
        if self.dead and self.deadAnim:
            frame = int(self.deadFrameCounter)
            if frame < len(self.deadAnim):
                img = self.deadAnim[frame]
        # Flip the image if the wizard is on the red team
                if self.side == "red":
                    img = transform.flip(img, True, False)
                screen.blit(img, (self.sizeRect.centerx-25, self.sizeRect.centery-25))
                self.deadFrameCounter += 0.15
            return
        # Choose the correct animation (attack or run)
        if self.attacking:
            self.animationList = self.attackAnim
        else:
            self.animationList = self.runAnim
        # Update the frame counter and draw the current frame
        prevFrame = int(self.frameCounter)
        self.frameCounter += self.frameSpeed
        currFrame = int(self.frameCounter)
        if currFrame != prevFrame and currFrame == 0:
            self.hasDealtDamage = False
        if self.frameCounter >= len(self.animationList):
            self.frameCounter = 0
        self.animationIndex = int(self.frameCounter)
        # Draw the wizard sprite, flipping if red
        if self.side == "red":
            screen.blit(transform.flip(self.animationList[self.animationIndex], True, False), (self.sizeRect.centerx-25, self.sizeRect.centery-25))
        elif self.side == "blue":
            screen.blit(transform.flip(self.animationList[self.animationIndex], False, False), (self.sizeRect.centerx-25, self.sizeRect.centery-25))
        
        # Draw the health bar above the wizard
        barWidth = 50
        barHeight = 6
        x = self.sizeRect.centerx - barWidth // 2
        y = self.sizeRect.centery - 40
        health_ratio = max(self.health / self.maxHealth, 0)
        health_bar_rect = Rect(x, y, int(barWidth * health_ratio), barHeight)
        border_rect = Rect(x, y, barWidth, barHeight)
        if self.side == "red":
            self.attackBox = Rect(self.sizeRect.centerx-self.attackRad/2, self.sizeRect.centery-self.attackRad, self.attackRad*2.2, self.attackRad*2)
            draw.rect(screen, (255, 0, 0), health_bar_rect)
            draw.rect(screen, (105, 5, 5), Rect(x + health_bar_rect.width, y, barWidth - health_bar_rect.width, barHeight))
            draw.rect(screen, (105, 8, 8), border_rect, 2)
        elif self.side == "blue":
            self.attackBox = Rect(self.sizeRect.centerx-self.attackRad/2, self.sizeRect.centery-self.attackRad, self.attackRad*2.2, self.attackRad*2)
            draw.rect(screen, (0, 0, 255), health_bar_rect)
            draw.rect(screen, (5, 5, 105), Rect(x + health_bar_rect.width, y, barWidth - health_bar_rect.width, barHeight))
            draw.rect(screen, (8, 8, 105), border_rect, 2)


    def attackTower(self, towers):
            # Checks if any tower is in range to attack
            inRange = False
            for tower in towers[:]:
                if not self.dead and tower.health > 0:
                    # Calculate distance to the center of the tower
                    dx = tower.x + tower.image.get_width() // 2 - self.sizeRect.centerx
                    dy = tower.y + tower.image.get_height() // 2 - self.sizeRect.centery
                    dist = (dx**2 + dy**2) ** 0.5
                    # If within attack radius, attack the tower
                    if dist <= self.attackRad:
                        inRange = True
                        now = time.get_ticks()
                        # Check if enough time has passed to attack again
                        if now - self.lastAttack >= 1000 / self.attackSpeed:
                            tower.health -= self.damage
                            self.lastAttack = now
                        break

            self.attackingTower = inRange
            if inRange:
                # Start attack animation if not already attacking
                if not self.attacking:
                    self.hasDealtDamage = False
                self.attacking = True
                self.animationList = self.attackAnim
                return True
            else:
                return False

    def attack(self, enemies):
            # Check if the wizard is dead
            if self.dead:
                self.attacking = False
                return

            inRange = False
            # Check if any enemy is within the attack box if yes then set inRange to True
            for enemy in enemies:
                if not enemy.dead and self.attackBox.colliderect(enemy.sizeRect):
                    inRange = True
                    targetEnemy = enemy
                    break
            # If an enemy is in range, attack them
            if inRange:
                    self.attacking = True
                # only deal damage if the wizard is attacking and the frame counter is at the last frame of the attack animation
                    if int(self.frameCounter) == len(self.attackAnim) - 1 and not self.hasDealtDamage:
                        targetEnemy.health -= self.damage  
                        self.hasDealtDamage = True 
                        print("Attacked")
                    else:
                        self.hasDealtDamage = False
            else:
                self.attacking = False
                self.hasDealtDamage = False

# Barbarian class with all its attributes and methods
class Barbarian:
    def __init__(self, side, health, damage, width, speed, path, spwnX, spwxY, frameCounter, frameSpeed, runAnim, attackAnim, animIndex, deadAnim=None):
        self.side = side
        self.health = health
        self.maxHealth = health
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
        self.attackRad = 40
        self.attackBox = Rect(self.sizeRect.centerx-self.attackRad/2, self.sizeRect.centery-self.attackRad/2, self.attackRad*2, self.attackRad*1.2)
        self.animationList = self.runAnim
        self.detectRad = 100
        self.detectBox = Rect(self.sizeRect.centerx-self.detectRad/2, self.sizeRect.centery-self.detectRad/2, self.detectRad, self.detectRad)
        self.animationIndex = animIndex
        self.attackCooldown = 0
        self.attackCooldownMax = len(self.attackAnim)
        self.hasDealtDamage = False
        self.elixir = 5
        self.isFollowing = False
        self.lastAttack = 0
        self.attackSpeed = 1
        self.attackingTower = None
        self.pathFound = False
    
    def updatePos(self):
        if self.dead:
            return
        if self.attacking:
            self.animationList = self.attackAnim
        else:
            self.animationList = self.runAnim
        # for enemy in enemies:
        #     if self.detectBox.colliderect(enemy.sizeRect):
        #         self.isFollowing = True
        #         opponent = enemy
        #         break
        #     else:
        #         self.isFollowing == True
        if self.isFollowing == False:
            if self.posIndex >= len(self.path):
                return
            targetX, targetY = self.path[self.posIndex]
            dx = targetX - self.sizeRect.centerx
            dy = targetY - self.sizeRect.centery
            dist = (dx**2 + dy**2) **0.5
            
            if dist < 5:
                self.posIndex += 1
                # print("reached")
            else:
                if self.attacking:
                    pass
                else:
                    self.sizeRect.centerx += int(self.speed * dx/dist)
                    self.attackBox.centerx += int(self.speed * dx/dist)
                    self.detectBox.centerx += int(self.speed * dx/dist)
                    self.sizeRect.centery += int(self.speed * dy/dist)
                    self.attackBox.centery += int(self.speed * dy/dist)
                    self.detectBox.centery += int(self.speed * dy/dist)
        else:
            
            box = opponent.sizeRect.centerx - self.sizeRect.centerx
            boy = opponent.sizeRect.centery - self.sizeRect.centery
            bdist = (boy**2 + box**2) ** 0.5
            
            if self.attacking:
                self.sizeRect.centerx += 0
                self.attackBox.centerx += 0
                self.detectBox.centerx += 0
                self.sizeRect.centery += 0
                self.attackBox.centery += 0
                self.detectBox.centery += 0
            else:
                self.sizeRect.centerx += int(self.speed * box/bdist)
                self.attackBox.centerx += int(self.speed * box/bdist)
                self.detectBox.centerx += int(self.speed * box/bdist)
                self.sizeRect.centery += int(self.speed * boy/bdist)
                self.attackBox.centery += int(self.speed * boy/bdist)
                self.detectBox.centery += int(self.speed * boy/bdist)
            
        
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
        prevFrame = int(self.frameCounter)
        self.frameCounter += self.frameSpeed
        currFrame = int(self.frameCounter)
        if currFrame != prevFrame and currFrame == 0:
            self.hasDealtDamage = False
        prevFrame = int(self.frameCounter)
        self.frameCounter += self.frameSpeed
        currFrame = int(self.frameCounter)
        if currFrame != prevFrame and currFrame == 0:
            self.hasDealtDamage = False
        if self.frameCounter >= len(self.animationList):
            self.frameCounter = 0
        self.animationIndex = int(self.frameCounter)
        if self.side == "red":
            screen.blit(transform.flip(self.animationList[self.animationIndex], True, False), (self.sizeRect.centerx-25, self.sizeRect.centery-25))
        elif self.side == "blue":
            screen.blit(transform.flip(self.animationList[self.animationIndex], False, False), (self.sizeRect.centerx-25, self.sizeRect.centery-25))
        bar_width = 50
        bar_height = 6
        x = self.sizeRect.centerx - bar_width // 2
        y = self.sizeRect.centery - 40
        health_ratio = max(self.health / self.maxHealth, 0)
        health_bar_rect = Rect(x, y, int(bar_width * health_ratio), bar_height)
        border_rect = Rect(x, y, bar_width, bar_height)
        if self.side == "red":
            self.attackBox = Rect(self.sizeRect.centerx-self.attackRad*1.5, self.sizeRect.centery-self.attackRad/2, self.attackRad*2, self.attackRad*1.2)
            draw.rect(screen, (255, 0, 0), health_bar_rect)
            draw.rect(screen, (105, 5, 5), Rect(x + health_bar_rect.width, y, bar_width - health_bar_rect.width, bar_height))
            draw.rect(screen, (105, 8, 8), border_rect, 2)
        elif self.side == "blue":
            self.attackBox = Rect(self.sizeRect.centerx-self.attackRad/2, self.sizeRect.centery-self.attackRad/2, self.attackRad*2, self.attackRad*1.2)
            draw.rect(screen, (0, 0, 255), health_bar_rect)
            draw.rect(screen, (5, 5, 105), Rect(x + health_bar_rect.width, y, bar_width - health_bar_rect.width, bar_height))
            draw.rect(screen, (8, 8, 105), border_rect, 2)

    def attack(self, opponent):
        if self.attackBox.colliderect(opponent.sizeRect) and not self.dead and not opponent.dead:
            self.attackingTroop = True
            self.attacking = True
            if int(self.frameCounter) == len(self.attackAnim) - 1 and not self.hasDealtDamage:
                opponent.health -= self.damage
                self.hasDealtDamage = True
        else:
            self.attackingTroop = False
            if not self.attackingTower:
                self.attacking = False
                self.hasDealtDamage = False


    def attackTower(self, towers):
        inRange = False
        for tower in towers[:]:
            if not self.dead and tower.health > 0:
                dx = tower.x + tower.image.get_width() // 2 - self.sizeRect.centerx
                dy = tower.y + tower.image.get_height() // 2 - self.sizeRect.centery
                dist = (dx**2 + dy**2) ** 0.5
                if dist <= self.attackRad:
                    inRange = True
                    now = time.get_ticks()
                    if now - self.lastAttack >= 1000 / self.attackSpeed:
                        tower.health -= self.damage
                        self.lastAttack = now
                    break

        self.attackingTower = inRange
        if inRange:
            if not self.attacking:
                self.hasDealtDamage = False
            self.attacking = True
            self.animationList = self.attackAnim
            return True
        else:
            self.attacking = False
            self.hasDealtDamage = False
            self.animationList = self.runAnim
            return False


class Golem:
    def __init__(self, side, health, damage, width, speed, path, spwnX, spwxY, frameCounter, frameSpeed, runAnim, attackAnim, animIndex, deadAnim=None):
        self.side = side
        self.health = health
        self.health = health
        self.maxHealth = health
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
        self.attackRad = 80
        self.attackBox = Rect(self.sizeRect.centerx-self.attackRad/2, self.sizeRect.centery-self.attackRad/2, self.attackRad*2, self.attackRad)
        self.detectRad = 80
        self.detectBox = Rect(self.sizeRect.centerx-self.detectRad/2, self.sizeRect.centery-self.detectRad/2, self.detectRad, self.detectRad)
        self.animationList = self.runAnim
        self.animationIndex = animIndex
        self.attackCooldown = 0
        self.attackCooldownMax = len(self.attackAnim)
        self.hasDealtDamage = False
        self.elixir = 5
        self.isFollowing = False
        self.attackingTroop = False
        self.attackingTower = False        
        self.lastAttack = 0
        self.attackSpeed = 1 
        self.pathFound = False
    
    def updatePos(self):
        global opponent
        if self.dead:
            return
        if self.attacking:
            self.animationList = self.attackAnim
        else:
            self.animationList = self.runAnim
        
        if self.isFollowing == False:
            if self.posIndex >= len(self.path):
                return
            targetX, targetY = self.path[self.posIndex]
            dx = targetX - self.sizeRect.centerx
            dy = targetY - self.sizeRect.centery
            dist = (dx**2 + dy**2) **0.5
            
            if dist < 5:
                self.posIndex += 1
            else:
                if self.attacking:
                    pass
                else:
                    self.sizeRect.centerx += int(self.speed * dx/dist)
                    self.attackBox.centerx += int(self.speed * dx/dist)
                    self.detectBox.centerx += int(self.speed * dx/dist)
                    self.sizeRect.centery += int(self.speed * dy/dist)
                    self.attackBox.centery += int(self.speed * dy/dist)
                    self.detectBox.centery += int(self.speed * dy/dist)
        else:
            gox = opponent.sizeRect.centerx - self.sizeRect.centerx
            goy = opponent.sizeRect.centery - self.sizeRect.centery
            gdist = (gox**2 + goy**2) ** 0.5
            
            if self.attacking:
                self.sizeRect.centerx += 0
                self.attackBox.centerx += 0
                self.detectBox.centerx += 0
                self.sizeRect.centery += 0
                self.attackBox.centery += 0
                self.detectBox.centery += 0
            else:
                self.sizeRect.centerx += int(self.speed * gox/gdist)
                self.attackBox.centerx += int(self.speed * gox/gdist)
                self.detectBox.centerx += int(self.speed * gox/gdist)
                self.sizeRect.centery += int(self.speed * goy/gdist)
                self.attackBox.centery += int(self.speed * goy/gdist)
                self.detectBox.centery += int(self.speed * goy/gdist)
                
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

        prevFrame = int(self.frameCounter)
        self.frameCounter += self.frameSpeed
        currFrame = int(self.frameCounter)
        if currFrame != prevFrame and currFrame == 0:
            self.hasDealtDamage = False
        if self.frameCounter >= len(self.animationList):
            self.frameCounter = 0
        self.animationIndex = int(self.frameCounter)
        if self.side == "red":
            screen.blit(transform.flip(self.animationList[self.animationIndex], True, False), (self.sizeRect.centerx-25, self.sizeRect.centery-25))
        elif self.side == "blue":
            screen.blit(transform.flip(self.animationList[self.animationIndex], False, False), (self.sizeRect.centerx-25, self.sizeRect.centery-25))
        bar_width = 50
        bar_height = 6
        x = self.sizeRect.centerx - bar_width // 2
        y = self.sizeRect.centery - 40
        health_ratio = max(self.health / self.maxHealth, 0)
        health_bar_rect = Rect(x, y, int(bar_width * health_ratio), bar_height)
        border_rect = Rect(x, y, bar_width, bar_height)
        if self.side == "red":
            draw.rect(screen, (255, 0, 0), health_bar_rect)
            draw.rect(screen, (105, 5, 5), Rect(x + health_bar_rect.width, y, bar_width - health_bar_rect.width, bar_height))
            draw.rect(screen, (105, 8, 8), border_rect, 2)
        elif self.side == "blue":
            draw.rect(screen, (0, 0, 255), health_bar_rect)
            draw.rect(screen, (5, 5, 105), Rect(x + health_bar_rect.width, y, bar_width - health_bar_rect.width, bar_height))
            draw.rect(screen, (8, 8, 105), border_rect, 2)

    def attack(self, opponent):
        if self.attackBox.colliderect(opponent.sizeRect) and not self.dead and not opponent.dead:
            self.attackingTroop = True
            self.attacking = True
            if int(self.frameCounter) == len(self.attackAnim) - 1 and not self.hasDealtDamage:
                opponent.health -= self.damage
                self.hasDealtDamage = True
        else:
            self.attackingTroop = False
            if not self.attackingTower:
                self.attacking = False
                self.hasDealtDamage = False

    def attackTower(self, towers):
        inRange = False
        for tower in towers[:]:
            if not self.dead and tower.health > 0:
                dx = tower.x + tower.image.get_width() // 2 - self.sizeRect.centerx
                dy = tower.y + tower.image.get_height() // 2 - self.sizeRect.centery
                dist = (dx**2 + dy**2) ** 0.5
                if dist <= self.attackRad:
                    inRange = True
                    now = time.get_ticks()
                    if now - self.lastAttack >= 1000 / self.attackSpeed:
                        tower.health -= self.damage
                        self.lastAttack = now
                    break

        self.attackingTower = inRange
        if inRange:
            if not self.attacking:
                self.hasDealtDamage = False
            self.attacking = True
            self.animationList = self.attackAnim
            return True
        else:
            self.attacking = False
            self.hasDealtDamage = False
            self.animationList = self.runAnim
            return False




mainTower = transform.scale(image.load("assets/towers/mainTower.png", "png"), (193/2, 254/2))
sideTower = transform.scale(image.load("assets/towers/miniTower.png", "png"), (106/2, 178/2))
blueTroops = []
blueTopTower = Tower("blue", 270, 190, sideTower)
blueKingTower = Tower("blue", 250, 325, mainTower)
blueBotTower = Tower("blue", 270, 510, sideTower)
blueTowers = [
    blueTopTower,
    blueKingTower,
    blueBotTower
]
redTroops = []
redTopTower = Tower("red", 1070, 190, sideTower)
redKingTower = Tower("red", 1050, 325, mainTower)
redBotTower = Tower("red", 1070, 510, sideTower)
redTowers = [
    redTopTower,
    redKingTower,
    redBotTower
]

# Lists to hold the animations for each troop type
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

# Load the animations for each troop type and append them to the lists
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

HowToPlaypic = transform.scale(image.load("assets/howto.png"), (400, 100))
settingspic = transform.scale(image.load("assets/settings.png"), (400, 100))
playpic = transform.scale(image.load("assets/play.png"), (400, 100))

settingsbg = transform.scale(image.load("assets/settingsbg.jpg"), (1400, 700))


# Variables for each troop type's animation
# Assassin - Wizard
assassinRunIndex = 0
assassinAttackIndex = 0
assassinFrameCounter = 0
assassinFrameSpeed = 0.075
assassinRunningAnimation = False
assassinAttackAnimation = False

# Female Wizard - Wizard
femaleWizardRunIndex = 0
femaleWizardAttackIndex = 0
femaleWizardFrameCounter = 0
femaleWizardFrameSpeed = 0.075
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
maleWizardFrameSpeed = 0.075
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



# Load the face cards
for i in range(9):
    faceCards.append(image.load("assets/mainFace/mainface"+ str(i+1) +".png"))
    faceCardsPath.append("assets/mainFace/mainface"+ str(i+1) +".png")


for i in range(9):
    faceCards[i] = transform.scale(faceCards[i], (130,130))

# Load the main screen assets
logo = image.load("assets/mainScreenAssets/FSELogo.png")
logo = transform.scale(logo, (1024/4, 1024/4))
mainBackground = image.load("assets/mainScreenAssets/FSEMainBackground.png", "png")
mainBackground = transform.scale(mainBackground, (980*1.5, 626*1.5))

mixer.music.load("assets/mainScreenAssets/Pufino - Swing (freetouse.com).mp3", "mp3")
mixer.music.play(10)
gameBackground = image.load("assets/mainScreenAssets/GameBackground.png", "png")
gameBackground = transform.scale(gameBackground, (gameBackground.get_width()*1, gameBackground.get_height()*1))


# Main screen boxes 
PlayBox = Rect(50, 500, 400, 100)
HowToPlayBox = Rect(500, 500, 400, 100)
SettingsBox = Rect(950, 500, 400, 100)



# Card Shown
continueBox = Rect(1175, 575, 200, 100)

# Card Rectangles
bluePlayerCard =[Rect(100,45,135,150),Rect(285,45,135,150), Rect(470,45,135,150), Rect(200,225,135,150), Rect(385,225,135,150)]
RedPlayerCard =[Rect(795,45,135,150),Rect(980,45,135,150), Rect(1165,45,135,150), Rect(895,225,135,150), Rect(1080,225,135,150)]

# Reshuffle and Confirm Rectangles and other text 
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
    - Player 2: I, J, K, L to selct where to place and U to place your desire
    Each card costs elixir — manage it wisely and play smart to attack and defend.

Step 3: Destroy the Towers
    Break through your opponent's defense and destroy their towers before they destroy 
    yours!
"""

prev_mb = (0, 0, 0)

# Game Variables
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


currentVolume = 0.5
isMuted = False
currentFps = 60
showFps = False


gameStartTime = 0
gameLength = 120  
isGameActive = False



BluevictorText = frontFont.render("Blue WON!", True, WHITE)
RedvictorText = frontFont.render("Red Won!", True, WHITE)
homeText = frontFont.render("Home", True, WHITE)
homeButton = Rect(580, 400, 200, 80)
winner = "" 

# Animation Picker nested dictionary 
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


# Grids for player movement
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


# function to move the player in the grid based on the key they press 

def moveInGrid(dir, w, h, player):
    # If it's player 1
    if player == 1:
        # Moving right
        if dir == "right":
            for i in range(h):  # Loop through each row
                for j in range(w):  # Loop through each column
                    if grid1[i][j] == 1:  # Find where player 1 is
                        grid1[i][j] = 0  # Remove player from current position
                        if j == w-1:  # If at the end of row, wrap to start
                            grid1[i][0] = 1
                        else:
                            grid1[i][j+1] = 1  # Move one step right
                        return  # Stop looping once moved

        # Moving left
        if dir == "left":
            for i in range(h):
                for j in range(w):
                    if grid1[i][j] == 1:
                        grid1[i][j] = 0
                        if j == 0:  # If at the beginning, wrap to end
                            grid1[i][w-1] = 1
                        else:
                            grid1[i][j-1] = 1  # Move one step left
                        return

        # Moving down
        if dir == "down":
            for i in range(h):
                for j in range(w):
                    if grid1[i][j] == 1:
                        grid1[i][j] = 0
                        if i == h-1:  # If at bottom, go to top row
                            grid1[0][j] = 1
                        else:
                            grid1[i+1][j] = 1  # Move one step down
                        return

        # Moving up
        if dir == "up":
            for i in range(h):
                for j in range(w):
                    if grid1[i][j] == 1:
                        grid1[i][j] = 0
                        if i == 0:  # If at top, wrap to bottom row
                            grid1[h-1][j] = 1
                        else:
                            grid1[i-1][j] = 1  # Move one step up
                        return

    # If it's player 2
    elif player == 2:
        # Moving right
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

        # Moving left
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

        # Moving down
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

        # Moving up
        if dir == "up":
            for i in range(h):
                for j in range(w):
                    if grid2[i][j] == 1:
                        grid2[i][j] = 0
                        if i == 0:
                            grid2[h-1][j] = 1
                        else:
                            grid2[i-1][j] = 1
                        return



#function to render text in a given rectangle (used from the paint assignment)
def renderText(surface, text, font, color, rect):
    lines = text.split('\n')  
    space_width = font.size(' ')[0]

    x, y = rect.topleft
    max_width = rect.width

    for line in lines:
        words = line.split(' ')
        for word in words:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()

            if x + word_width >= rect.right:
                x = rect.left
                y += word_height

            surface.blit(word_surface, (x, y))
            x += word_width + space_width

        x = rect.left
        y += font.get_linesize()

# randomly shuffle the cards for both players
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
            #Player 1 controls
            if evt.key == K_d:
                moveInGrid("right", 6, 9, 1)
            if evt.key == K_a:
                moveInGrid("left", 6, 9, 1)
            if evt.key == K_s:
                moveInGrid("down", 6, 9, 1)
            if evt.key == K_w:
                moveInGrid("up", 6, 9, 1)
            #player 2 controls
            if evt.key == K_l:
                moveInGrid("right", 6, 9, 2)
            if evt.key == K_j:
                moveInGrid("left", 6, 9, 2)
            if evt.key == K_k:
                moveInGrid("down", 6, 9, 2)
            if evt.key == K_i:
                moveInGrid("up", 6, 9, 2)
            # player 1 card selection buttons
            if evt.key == K_1:
                blueInd = 0
            if evt.key == K_2:
                blueInd = 1
            if evt.key == K_3:
                blueInd = 2
            if evt.key == K_4:
                blueInd = 3
            # player 2 card selection buttons
            if evt.key == K_7:
                redInd = 0
            if evt.key == K_8:
                redInd = 1
            if evt.key == K_9:
                redInd = 2
            if evt.key == K_0:
                redInd = 3
            if evt.key == K_e:
                # get current selected deck for blue player
                currDeckBlue = [blueFinalCards[i] for i in range(4)]
                # find the index of the selected card
                bIndex = faceCards.index(currDeckBlue[blueInd])
                # get troop type and card type using the animation path
                parentKeys = findKeys(faceCardsPath[bIndex], animationPicker)
                troopType = parentKeys[0]
                cardType = parentKeys[1]
                # set the elixir cost based on troop type
                if troopType == "Wizard":
                    elixirCost = 5
                elif troopType == "Barbarian":
                    elixirCost = 3
                elif troopType == "Golem":
                    elixirCost = 7
                if blueElixir >= elixirCost:
                    # making a new object using the class constructor according to the troop type
                    # passing in all the stats and animations from the animation picker
                    if troopType == "Wizard":
                        blueTroops.append(Wizard("blue", 250, 80, 20, 2, blueTopTowerPath, bluePlayerSelect.centerx, bluePlayerSelect.centery,
                                                frameCounter, 
                                                animationPicker[troopType][cardType]["frameSpeed"],
                                                animationPicker[troopType][cardType]["runAnim"],
                                                animationPicker[troopType][cardType]["attackAnim"],
                                                animationPicker[troopType][cardType]["runIndex"],
                                                animationPicker[troopType][cardType]["deadAnim"]))
                    elif troopType == "Barbarian":
                        blueTroops.append(Barbarian("blue", 120, 35, 20, 2, blueTopTowerPath, bluePlayerSelect.centerx, bluePlayerSelect.centery,
                                                frameCounter, 
                                                animationPicker[troopType][cardType]["frameSpeed"],
                                                animationPicker[troopType][cardType]["runAnim"],
                                                animationPicker[troopType][cardType]["attackAnim"],
                                                animationPicker[troopType][cardType]["runIndex"],
                                                animationPicker[troopType][cardType]["deadAnim"]))
                    elif troopType == "Golem":
                        blueTroops.append(Golem("blue", 400, 100, 20, 2, blueTopTowerPath, bluePlayerSelect.centerx, bluePlayerSelect.centery,
                                                frameCounter, 
                                                animationPicker[troopType][cardType]["frameSpeed"],
                                                animationPicker[troopType][cardType]["runAnim"],
                                                animationPicker[troopType][cardType]["attackAnim"],
                                                animationPicker[troopType][cardType]["runIndex"],
                                                animationPicker[troopType][cardType]["deadAnim"]))
                    # subtract elixir cost
                    blueElixir -= elixirCost
                    # swap card out of deck after using 
                    for a in blueFinalCards:
                        if currDeckBlue.count(a) == 0:
                            blueFinalCards[blueInd], blueFinalCards[4] = blueFinalCards[4], blueFinalCards[blueInd]


            if evt.key == K_u:
                #doing the same for the red same 

                # get current selected deck for red player
                currDeckRed = [redFinalCards[i] for i in range(4)]
                # find the index of the selected card
                rIndex = faceCards.index(currDeckRed[redInd])
                # get troop type and card type using the animation path
                parentKeys = findKeys(faceCardsPath[rIndex], animationPicker)
                troopType = parentKeys[0]
                cardType = parentKeys[1]
                # set the elixir cost based on troop type
                if troopType == "Wizard":
                    elixirCost = 5
                elif troopType == "Barbarian":
                    elixirCost = 3
                elif troopType == "Golem":
                    elixirCost = 7
                # else:
                #     elixir_cost = 5
                if redElixir >= elixirCost:
                    # making a new object using the class constructor according to the troop type
                    # passing in all the stats and animations from the animation picker
                    if troopType == "Wizard":
                        redTroops.append(Wizard("red", 250, 80, 20, 2, redTopTowerPath, redPlayerSelect.centerx, redPlayerSelect.centery,
                                                frameCounter, 
                                                animationPicker[troopType][cardType]["frameSpeed"],
                                                animationPicker[troopType][cardType]["runAnim"],
                                                animationPicker[troopType][cardType]["attackAnim"],
                                                animationPicker[troopType][cardType]["runIndex"],
                                                animationPicker[troopType][cardType]["deadAnim"]))
                    elif troopType == "Barbarian":
                        redTroops.append(Barbarian("red", 120, 35, 20, 2, redTopTowerPath, redPlayerSelect.centerx, redPlayerSelect.centery,
                                                frameCounter, 
                                                animationPicker[troopType][cardType]["frameSpeed"],
                                                animationPicker[troopType][cardType]["runAnim"],
                                                animationPicker[troopType][cardType]["attackAnim"],
                                                animationPicker[troopType][cardType]["runIndex"],
                                                animationPicker[troopType][cardType]["deadAnim"]))
                    elif troopType == "Golem":
                        redTroops.append(Golem("red", 400, 100, 20, 2, redTopTowerPath, redPlayerSelect.centerx, redPlayerSelect.centery,
                                                frameCounter, 
                                                animationPicker[troopType][cardType]["frameSpeed"],
                                                animationPicker[troopType][cardType]["runAnim"],
                                                animationPicker[troopType][cardType]["attackAnim"],
                                                animationPicker[troopType][cardType]["runIndex"],
                                                animationPicker[troopType][cardType]["deadAnim"]))
                    # subtract elixir cost                    
                    redElixir -= elixirCost  
                    # swap card out of deck after using 
                    for a in redFinalCards:
                        if currDeckRed.count(a) == 0:
                            redFinalCards[redInd], redFinalCards[4] = redFinalCards[4], redFinalCards[redInd]

    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
    pressed_keys = key.get_pressed()
    
    if screenNum == 1:
        # Main Menu Screen
        # draw the main background and logo and the button images        
        screen.blit(mainBackground, (0, 0))
        screen.blit(playpic,(PlayBox[0],PlayBox[1]))
        screen.blit(HowToPlaypic,(HowToPlayBox[0],HowToPlayBox[1]))
        screen.blit(settingspic,(SettingsBox[0],SettingsBox[1]))

        #go to respective screens when the buttons are clicked
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
        

        if blueReshuffle.collidepoint(mx, my) and mb[0] and not prev_mb[0] and blueReshuffleCount < 3:
            blueRandom = sample(range(1, 9), 5)
            blueReshuffleCount += 1

        if redReshuffle.collidepoint(mx, my) and mb[0] and not prev_mb[0] and redReshuffleCount < 3:
            redRandom = sample(range(1, 9), 5)
            redReshuffleCount += 1

        if blueReshuffleCount < 3:
            draw.rect(screen, WHITE, blueReshuffle)
        else:
            draw.rect(screen, (100, 100, 100), blueReshuffle)

        if redReshuffleCount < 3:
            draw.rect(screen, WHITE, redReshuffle)
        else:
            draw.rect(screen, (100, 100, 100), redReshuffle)

        draw.rect(screen, GREEN, blueConfirm)
        draw.rect(screen, GREEN, redConfirm)

        screen.blit(reshuffletext, (blueReshuffle[0] + 35, blueReshuffle[1] + 25))
        screen.blit(reshuffletext, (redReshuffle[0] + 35, redReshuffle[1] + 25))
        screen.blit(readyText, (blueConfirm[0] + 55, blueConfirm[1] + 25))
        screen.blit(readyText, (redConfirm[0] + 55, redConfirm[1] + 25))

        blueLeft = textfont.render(f"{3 - blueReshuffleCount} left", True, WHITE)
        redLeft = textfont.render(f"{3 - redReshuffleCount} left", True, WHITE)
        screen.blit(blueLeft, (blueReshuffle[0] + 245, blueReshuffle[1] + 35))
        screen.blit(redLeft, (redReshuffle[0] + 245, redReshuffle[1] + 35))

        if blueConfirm.collidepoint(mx, my) and mb[0] and not prev_mb[0]:
            blueReady = True
            waitBlue = True

        if redConfirm.collidepoint(mx, my) and mb[0] and not prev_mb[0]:
            redReady = True
            waitRed = True

        if waitBlue:
            draw.rect(screen, GREEN, blueConfirm)
            screen.blit(waitingText, (blueConfirm[0] + 55, blueConfirm[1] + 25))

        if waitRed:
            draw.rect(screen, GREEN, redConfirm)
            screen.blit(waitingText, (redConfirm[0] + 55, redConfirm[1] + 25))

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
        

        if not isGameActive:
            gameStartTime = time.get_ticks()
            isGameActive = True
        
        elapsedTime = (time.get_ticks() - gameStartTime) // 1000  
        remainingTime = max(0, gameLength - elapsedTime)
        minutes = remainingTime // 60
        seconds = remainingTime % 60
        
        timeColor = RED if remainingTime <= 10 else WHITE
        timeStr = f"{minutes:02d}:{seconds:02d}"
        timerText = textfont.render(timeStr, True, timeColor)
        
        timerRect = timerText.get_rect(center=(width//2, 30))
        screen.blit(timerText, timerRect)
        
        if remainingTime <= 0:
            isGameActive = False
            screenNum = 1  
     
            blueTroops.clear()
            redTroops.clear()
            blueElixir = 6
            redElixir = 6
            blueTowers = [
                Tower("blue", 270, 190, sideTower),
                Tower("blue", 250, 325, mainTower),
                Tower("blue", 270, 510, sideTower)
            ]
            redTowers = [
                Tower("red", 1070, 190, sideTower),
                Tower("red", 1050, 325, mainTower),
                Tower("red", 1070, 510, sideTower)
            ]
        
        
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
            

        for tower in blueTowers[:]:
            if tower.health > 0:
                tower.draw(screen)
                tower.attack(redTroops)
            else:
                blueTowers.remove(tower) 

        for tower in redTowers[:]:
            if tower.health > 0:
                tower.draw(screen)
                tower.attack(blueTroops)
            else:
                redTowers.remove(tower)
        
        determinePath(blueTroops, blueTopTowerPath, blueBotTowerPath, blueKingTowerPos, redTowers)
        determinePath(redTroops, redTopTowerPath, redBotTowerPath, redKingTowerPos, blueTowers)
        

                        
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
            color = ELIXERCOLOR if i < blueElixir else (50, 50, 50)
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
                color = ELIXERCOLOR
            else:
                color = (50, 50, 50)
            draw.rect(screen, color, (0, 150 + i*40, 40, 40))
            draw.rect(screen, WHITE, (0, 150 + i*40, 40, 40), 2)

        for i in range(10):
            if i < redElixir:
                color = ELIXERCOLOR
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


        for p in redTopTowerPath:
            draw.circle(screen, RED, p, 10)
        for p in redBotTowerPath:
            draw.circle(screen, RED, p, 10)
        # for p in blueTopTowerPath:
        #     draw.circle(screen, BLUE, p, 10)
        # for p in blueBotTowerPath:
        #     draw.circle(screen, BLUE, p, 10)



        for tower in blueTowers[:]:
            if tower.health > 0:
                tower.draw(screen)
                tower.attack(redTroops)
            else:
                blueTowers.remove(tower)  

        for tower in redTowers[:]:
            if tower.health > 0:
                tower.draw(screen)
                tower.attack(blueTroops)
            else:
                redTowers.remove(tower)



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


        for troop in redTroops:
            if isinstance(troop, Wizard):
                troop.attack(blueTroops)
            else:
                for blue in blueTroops:
                    troop.attack(blue)
            if troop.attackTower(blueTowers):
                continue  
        for troop in blueTroops:
            if isinstance(troop, Wizard):
                troop.attack(redTroops)
            else:
                for red in redTroops:
                    troop.attack(red)
            if troop.attackTower(redTowers):
                continue
        for troop in redTroops:
            troop.drawSprite()
        for troop in blueTroops:
            troop.drawSprite() 
        if remainingTime <= 0:
            screenNum = 7
            blueTowerHealth = 0
            redTowerHealth = 0
            for tower in blueTowers:
                blueTowerHealth += tower.health
            for tower in redTowers:
                redTowerHealth += tower.health
            if blueTowerHealth > redTowerHealth:
                winner = "blue"
            elif redTowerHealth > blueTowerHealth:
                winner = "red"
            else:
                winner = "tie"
        elif redKingTower not in redTowers:
            screenNum = 7
            winner = "blue"
        elif blueKingTower not in blueTowers:
            screenNum = 7
            winner = "red"

    elif screenNum == 4:
        # game instructions screen
        screen.fill(BLACK)
        draw.rect(screen, BLACK, backRect)  # draw the back button background
        screen.blit(backText, (backRect[0]+30, backRect[1]+40))  # draw the "back" text

        # draw the game description box
        textRect = Rect(50, 50, 1350, 300)
        renderText(screen, gameDescription, gameDescriptionFont, WHITE, textRect)

        # if player clicks back, go back to main menu
        if backRect.collidepoint(mx, my) and mb[0]:
            screenNum = 1

    elif screenNum == 5:
        # settings screen
        screen.fill(BLACK)
        screen.blit(settingsbg, (0, 0))  # draw the settings background
        screen.blit(backText, (backRect[0]+30, backRect[1]+40))  # draw the "back" text

        # draw volume bar and knob
        volumeBar = Rect(1100, 200, 10, 300)
        knobY = int(200 + (1 - currentVolume) * 300)
        draw.rect(screen, GREY, volumeBar)
        draw.rect(screen, WHITE, (1090, knobY-10, 30, 20))

        # display volume % text
        volText = textfont.render(f"Volume: {int(currentVolume*100)}%", True, WHITE)
        screen.blit(volText, (1000, 150))

        # change volume if user clicks and drags on the bar
        if mb[0]:
            #check if mouse is within the volume bar area
            if mx >= 1100 and mx <= 1110 and my >= 200 and my <= 500:
                # calculate the new volume based on mouse position
                currentVolume = 1 - ((my - 200) / 300)
                # make sure volume stays between 0 and 1
                currentVolume = max(0, min(1, currentVolume))
                #if not muted set teh volume
                if not isMuted:
                    mixer.music.set_volume(currentVolume)

        # mute/unmute button
        muteButton = Rect(1195, 130, 160, 50)
        buttonColor = (0, 200, 0) if isMuted else (200, 0, 0)  # green if muted, red if not
        draw.rect(screen, buttonColor, muteButton)
        buttonText = textfont.render("Unmute" if isMuted else "Mute", True, WHITE)
        screen.blit(buttonText, (1210, 140))

        # toggle mute on click
        if muteButton.collidepoint(mx, my) and mb[0] and not prev_mb[0]:
            isMuted = not isMuted
            if isMuted:
                mixer.music.set_volume(0)
            else:
                mixer.music.set_volume(currentVolume)

        # list of fps buttons to pick how smooth the game runs
        fpsButtons = [(200, 200, 80, 40, 30), 
                    (200, 300, 80, 40, 60),
                    (200, 400, 80, 40, 120)]

        for button in fpsButtons:
            #get the button properties
            x, y, w, h, fps = button
            #make a rectangle for the button
            buttonRect = Rect(x, y, w, h)
            #make the button
            color = GREEN if currentFps == fps else GREY  # highlight selected fps
            draw.rect(screen, color, buttonRect)
            text = textfont.render(str(fps), True, WHITE)
            screen.blit(text, (x+25, y+10))

            # change fps when clicked
            if buttonRect.collidepoint(mx, my) and mb[0] and not prev_mb[0]:
                currentFps = fps
                myClock.tick(fps)

        # toggle to show fps in top right
        toggleButton = Rect(200, 120, 250, 50)
        toggleColor = BLUE if showFps else GREY
        draw.rect(screen, toggleColor, toggleButton)
        toggleText = textfont.render("Show FPS: " + ("ON" if showFps else "OFF"), True, WHITE)
        screen.blit(toggleText, (220, 130))

        # turn fps display on and off
        if toggleButton.collidepoint(mx, my) and mb[0] and not prev_mb[0]:
            showFps = not showFps

        # go back to main menu
        if backRect.collidepoint(mx, my) and mb[0]:
            screenNum = 1

    # if fps toggle is on draw fps on screen at all times
    if showFps:
        fps = int(myClock.get_fps())
        fpsText = textfont.render(f"FPS: {fps}", True, YELLOW)
        screen.blit(fpsText, (width-150, 10))

    elif screenNum == 7:
        # shows the game winner screen 
        screen.fill(BLACK)

        # draw the winner text based on who won
        if winner == "blue":
            screen.blit(BluevictorText, (550, 300))
            draw.rect(screen, BLUE, (0, 0, width, 20)) 
            draw.rect(screen, BLUE, (0, height-20, width, 20))
        elif winner == "red":
            screen.blit(RedvictorText, (550, 300))
            draw.rect(screen, RED, (0, 0, width, 20))
            draw.rect(screen, RED, (0, height-20, width, 20))
        else:
            tieText = frontFont.render("It's a TIE!", True, WHITE)
            screen.blit(tieText, (550, 300))
            draw.rect(screen, YELLOW, (0, 0, width, 20))
            draw.rect(screen, YELLOW, (0, height-20, width, 20))

        # draw home button and text
        draw.rect(screen, GREEN, homeButton)
        screen.blit(homeText, (homeButton.x + 30, homeButton.y + 15))

        # when clicked, reset everything and go to home screen
        if homeButton.collidepoint(mx, my) and mb[0]:
            screenNum = 1
            blueTroops.clear()
            redTroops.clear()
            blueElixir = 6
            redElixir = 6
            blueTowers = [
                Tower("blue", 270, 190, sideTower, 800),  
                Tower("blue", 250, 325, mainTower, 800),
                Tower("blue", 270, 510, sideTower, 800)
            ]
            redTowers = [
                Tower("red", 1070, 190, sideTower, 800),
                Tower("red", 1050, 325, mainTower, 800),
                Tower("red", 1070, 510, sideTower, 800)
            ]
            winner = ""
            isGameActive = False
            blueReady = False
            redReady = False
            waitBlue = False  
            waitRed = False
            blueReshuffleCount = 0
            redReshuffleCount = 0
            blueFinalCards.clear()
            redFinalCards.clear()

    # control the game speed using selected fps
    myClock.tick(currentFps)

    prev_mb = mb

    display.flip()
            
quit()
