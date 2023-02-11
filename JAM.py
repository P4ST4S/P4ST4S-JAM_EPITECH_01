import pygame
import random

# Initialize pygame
pygame.init()

# Create the screen
height = 800
width = 600
screen = pygame.display.set_mode((height, width))

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Define speed of game elements
player_speed = 5
speed_shoot = 10
speed_enemy = 1

# Load images
player_img = pygame.image.load('assets/player.png')
player_img = pygame.transform.scale(player_img, (50, 50))
enemy_img = pygame.image.load('assets/enemy.png')
enemy_img = pygame.transform.scale(enemy_img, (50, 50))
shoot_img = pygame.image.load('assets/shoot.png')
shoot_img = pygame.transform.scale(shoot_img, (10, 20))

# Define player


class Player:
    def __init__(self, x, y):
        self.img = player_img
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move_left(self):
        self.rect.x -= player_speed

    def move_right(self):
        self.rect.x += player_speed

    def shoot(self):
        return Shoot(self.rect.x + self.rect.width / 2 - shoot_img.get_width() / 2, self.rect.y)


# Define shoot


class Shoot:
    def __init__(self, x, y):
        self.img = shoot_img
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self):
        self.rect.y -= speed_shoot

    def draw(self):
        screen.blit(self.img, self.rect)

# Define enemy


class Enemy:
    def __init__(self, x, y):
        self.img = enemy_img
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self):
        self.rect.y += speed_enemy

    def draw(self):
        screen.blit(self.img, self.rect)


player = Player(height / 2 - player_img.get_width() /
                2, width - player_img.get_height())
shoots = []
enemies = []
for i in range(5):
    for j in range(5):
        enemy = Enemy(width / 2 - enemy_img.get_width() +
                      j * 100, i * 100 - height / 2)
        enemies.append(enemy)

# Define game loop
running = True
clock = pygame.time.Clock()
last_shoot = 0
while running:
    # Set framerate
    clock.tick(30)

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Check for pressed keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.rect.x > 0:
        player.move_left()
    if keys[pygame.K_RIGHT] and player.rect.x < height - player.rect.width:
        player.move_right()
    if keys[pygame.K_SPACE]:
        now = pygame.time.get_ticks()
        if now - last_shoot > 500:
            last_shoot = now
            shoots.append(player.shoot())

    # Update game elements
    for shoot in shoots:
        shoot.move()
    for enemy in enemies:
        enemy.move()
        if enemy.rect.y > width:
            enemies.remove(enemy)

    # Check for collisions between shoots and enemies
    for shoot in shoots:
        for enemy in enemies:
            if shoot.rect.colliderect(enemy.rect):
                enemies.remove(enemy)
                shoots.remove(shoot)
                break

    # Draw game elements
    screen.fill(RED)
    screen.blit(player.img, player.rect)
    for shoot in shoots:
        shoot.draw()
    for enemy in enemies:
        enemy.draw()

    # Update display
    pygame.display.update()
