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

# Troop
class Troop:
    def __init__(self, path):
        self.size = 20
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.path = path
        self.pos_index = 0
        self.speed = 2
        self.rect.center = self.path[0]

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
            print(dist)
            self.rect.x += int(self.speed * dx / dist)
            self.rect.y += int(self.speed * dy / dist)

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect)


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

troop = Troop(path)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    troop.update()

    WIN.fill(WHITE)
    troop.draw(WIN)
    mb = pygame.mouse.get_pressed()
    mx, my = pygame.mouse.get_pos()
    if mb[0]:
        path.append((mx, my))
    elif mb[1]:
        troop.path = path1
    elif mb[2]:
        troop.path = path
    

    # Draw the path for visualization
    for point in troop.path:
        pygame.draw.circle(WIN, GREEN, point, 5)

    pygame.display.update()
    CLOCK.tick(FPS)
