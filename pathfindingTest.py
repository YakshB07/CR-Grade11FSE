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
    def __init__(self, path, health, damage):
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

    def update(self):
        if self.pos_index >= len(self.path):
            return  # done

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
                self.rect.x += dx/dist * self.speed
                self.rect.y += dy/dist * self.speed
            # print(self.rect.x)
            # print(target_x, target_y)
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.col, self.rect)
    
    def attack(self, opponent):
        if self.rect.colliderect(opponent.rect):
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
path1 = [
    (WIDTH // 3, HEIGHT - 25),   # Start middle bottom
    (WIDTH // 3, HEIGHT // 2),   # Move vertically to center
    (WIDTH // 5, HEIGHT // 2),   # Move left into top lane
    (WIDTH , 20)            # Final target (enemy)
]

# troop = Troop(path)
count = 0

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if tower.collidepoint(mx, my):
                    count += 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:
                characters.append(Troop(path, 100,  5))
            if event.key == pygame.K_i:
                characters1.append(Troop(path1, 50, 9))
            

    for troop in characters:
        troop.update()
        if troop.health <= 0:
            characters.remove(troop)
    for troop in characters1:
        troop.update()

    WIN.fill(WHITE)
    
    mb = pygame.mouse.get_pressed()
    mx, my = pygame.mouse.get_pos()
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
        for blue in characters1:
            red.attack(blue)
            blue.attack(red)
    

    # Draw the path for visualization
    for point in path:
        pygame.draw.circle(WIN, GREEN, point, 5)
    for point in path1:
        pygame.draw.circle(WIN, GREEN, point, 5)

    pygame.display.update()
    CLOCK.tick(FPS)
