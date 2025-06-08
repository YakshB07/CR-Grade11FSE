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

# Troop
class Troop:
    def __init__(self, path):
        self.size = 20
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.path = path
        self.pos_index = 0
        self.speed = 3
        self.rect.center = self.path[0]

    def update(self):
        if self.pos_index >= len(self.path):
            return  # done

        target_x, target_y = self.path[self.pos_index]
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        dist = (dx**2 + dy**2) ** 0.5
        # print(dist, dx, dy)
        if dist < 2:
            self.rect.center = self.path[self.pos_index]
            self.pos_index += 1
        else:
            self.rect.x += dx/dist * self.speed
            self.rect.y += dy/dist * self.speed
            # print(self.rect.x)
            # print(target_x, target_y)

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect)


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
            print("click1")
            if event.key == pygame.K_u:
                characters.append(Troop(path))
                print("click2")

    for troop in characters:
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
    
    

    # Draw the path for visualization
    for point in path:
        pygame.draw.circle(WIN, GREEN, point, 5)

    pygame.display.update()
    CLOCK.tick(FPS)
