import pygame
import sys

# Init
pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (200, 50, 50)
BLUE = (50, 50, 200)
GREEN = (50, 200, 50)
characters = []
characters1 = []


# Troop
class Troop:
    def __init__(self, path, health, damage, attckRad, detectRad):
        self.size = 20
        self.rect = pygame.Rect(0, 0, self.size, self.size,)
        self.path = path
        self.pos_index = 0
        self.speed = 3
        self.rect.center = self.path[0]
        self.col = BLUE
        self.health = health
        self.damage = damage
        self.attacking = False
        self.attckRad = attckRad
        self.attackBox = pygame.Rect(self.rect.x-self.attckRad/4, self.rect.y-self.attckRad/4, self.attckRad, self.attckRad)
        self.detectRad = detectRad
        self.detectBox = pygame.Rect(self.rect.centerx-self.detectRad/2, self.rect.centery-self.detectRad/2, self.detectRad, self.detectRad)
        self.isFollowing = False

    def update(self, ox, oy):
        if self.detectBox.collidepoint(ox, oy):
            self.isFollowing = True
            # print(self.isFollowing)
        else:
            self.isFollowing = False
        if self.isFollowing == False:
            if not self.path or self.pos_index >= len(self.path):
                return  

            target_x, target_y = self.path[self.pos_index]
            dx = target_x - self.rect.centerx
            dy = target_y - self.rect.centery
            dist = (dx**2 + dy**2) ** 0.5
            if dist < 2:
                self.rect.center = self.path[self.pos_index]
                self.pos_index += 1
            else:
                if self.attacking:
                    self.rect.x += 0
                    self.rect.y += 0
                else:
                    self.rect.centerx += int(self.speed * dx/dist)
                    self.attackBox.centerx += int(self.speed * dx/dist)
                    self.detectBox.centerx += int(self.speed * dx/dist)
                    self.rect.centery += int(self.speed * dy/dist)
                    self.attackBox.centery += int(self.speed * dy/dist)
                    self.detectBox.centery += int(self.speed * dy/dist)
        
        else:
            dx = ox - self.rect.centerx
            dy = oy - self.rect.centery
            dist = (dx**2 + dy**2) ** 0.5
            
            if self.attacking:
                    self.rect.x += 0
                    self.rect.y += 0
            else:
                self.rect.centerx += int(self.speed * dx/dist)
                self.attackBox.centerx += int(self.speed * dx/dist)
                self.detectBox.centerx += int(self.speed * dx/dist)
                self.rect.centery += int(self.speed * dy/dist)
                self.attackBox.centery += int(self.speed * dy/dist)
                self.detectBox.centery += int(self.speed * dy/dist)
            
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.col, self.rect)
        pygame.draw.ellipse(surface, (128, 0, 128), (self.attackBox), 2)
        pygame.draw.rect(surface, GREEN, self.detectBox, 3)
    
    def attack(self, opponent):
        if self.attackBox.colliderect(opponent.rect) and opponent.health > 0:
            self.col = RED
            self.attacking = True 
            opponent.health -= self.damage
        else:
            self.col = BLUE
            self.attacking = False
        


tower = pygame.Rect((WIDTH // 4)-25, 75, 50, 50)
# Define a fixed "lane" path: Middle bottom → top lane → target
path = [
    (WIDTH // 2, HEIGHT - 50),   # Start middle bottom
    (WIDTH // 2, HEIGHT // 2),   # Move vertically to center
    (WIDTH // 4, HEIGHT // 2),   # Move left into top lane
    (WIDTH // 4, 100)            # Final target (enemy)
]
# path1 = [
#     (WIDTH // 3, HEIGHT - 25),   # Start middle bottom
#     (WIDTH // 3, HEIGHT // 2),   # Move vertically to center
#     (WIDTH // 5, HEIGHT // 2),   # Move left into top lane
#     (WIDTH , 20)            # Final target (enemy)
# ]

characters.append(Troop(path, 100,  5, 40, 160))
# characters1.append(Troop(path1, 50, 9, 40))
# troop = Troop(path)
count = 0

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i and path:
                characters.append(Troop(path[:], 100,  5, 40))
            # if event.key == pygame.K_u and path1:
            #     characters1.append(Troop(path1[:], 50, 9, 40))
    
    
    mx, my = pygame.mouse.get_pos()        
    for troop in characters:
        troop.update(mx, my)
            # print("updae")
    for troop in characters:
        if troop.health <= 0:
            characters.remove(troop)
    # for troop in characters1:
    #     troop.update()
    # for troop in characters1:
    #     if troop.health <= 0:
    #         characters1.remove(troop)

    WIN.fill(WHITE)
    
    mb = pygame.mouse.get_pressed()
    
    if mb[1]:
        path.append((mx, my))
    if mb[2]:
        troop.rect.center = (mx, my)
    

    if count > 5:
        pygame.draw.rect(WIN, WHITE, tower)
        path.append((800, 600))
    else:
        pygame.draw.rect(WIN, (0, 0, 0), tower)
    
    for troop in characters:
        troop.draw(WIN)
    for troop in characters1:
        troop.draw(WIN)


    for red in characters:
        red.attacking = False  
        red.col = BLUE  
        for blue in characters1:
            if red.attackBox.colliderect(blue.rect) and blue.health > 0:
                red.attack(blue)
                break  
    # for blue in characters1:
    #     blue.attacking = False
    #     blue.col = BLUE
    #     for red in characters:
    #         if blue.attackBox.colliderect(red.rect) and red.health > 0:
    #             blue.attack(red)
    #             break
            
    # print("huh")


    # Draw the path for visualization
    for point in path:
        pygame.draw.circle(WIN, GREEN, point, 5)
    # for point in path1:
    #     pygame.draw.circle(WIN, GREEN, point, 5)

    pygame.display.update()
    CLOCK.tick(FPS)
