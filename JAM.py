import pygame
import random
import math

# Initialize pygame
pygame.init()

# Create the screen
height = 800
width = 600
screen = pygame.display.set_mode((width, height))
font = pygame.font.SysFont(None, 30)
score_text = 0

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (128, 128, 128)

# Define speed of game elements
player_speed = 5
speed_shoot = 10
speed_enemy = 2

# Define mouse usage
mouse_pos = [0, 0]
mouse_button = [0, 0, 0] # lclic, scroll clic, rclic

# Load images
player_img = pygame.image.load('assets/player.png')
player_img = pygame.transform.scale(player_img, (50, 50))
boss_img = pygame.image.load('assets/boss.png')
boss_img = pygame.transform.scale(boss_img, (100, 100))
enemy_img = pygame.image.load('assets/fireBall.png')
enemy_img = pygame.transform.scale(enemy_img, (50, 50))
enemy_img = pygame.transform.rotate(enemy_img, 180)
shoot_img = pygame.image.load('assets/shoot.png')
shoot_img = pygame.transform.scale(shoot_img, (32, 40))

# Define player
class Player:
    def __init__(self, x, y):
        self.img = player_img
        self.rect = self.img.get_rect()
        self.shoots = []
        self.last_shoot = 0
        self.rect.x = x
        self.rect.y = y

    def move_left(self):
        self.rect.x -= player_speed

    def move_right(self):
        self.rect.x += player_speed

    def shoot(self, dest):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > 50:
            self.last_shoot = now
            self.shoots.append(Shoot(self.rect.x + self.rect.width / 2 - shoot_img.get_width() / 2, self.rect.y, dest))

    def draw(self):
        screen.blit(self.img, self.rect)
    
    def draw_shoots(self):
        for shoot in self.shoots:
            shoot.draw()

# Define shoot
def get_rotate_angle(vect):
    rotation = 0
    if (vect[1] > 0):
        rotation += 180
    rotation -= (vect[0] / math.sqrt(math.pow(vect[0], 2) + math.pow(vect[1], 2))) * 90
    return rotation

class Shoot:
    def __init__(self, x, y, dest):
        self.vect = [dest[0] - x, dest[1] - y]
        self.norm_vect = [math.sqrt(math.pow(self.vect[0], 2) + math.pow(self.vect[1], 2)), math.sqrt(math.pow(self.vect[0], 2) + math.pow(self.vect[1], 2))]
        self.speed_x = self.vect[0] / self.norm_vect[0] * speed_shoot
        self.speed_y = self.vect[1] / self.norm_vect[1] * speed_shoot
        self.rotation = get_rotate_angle(self.vect)
        self.img = pygame.transform.rotate(shoot_img, self.rotation)
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
    def draw(self):
        screen.blit(self.img, self.rect)

# Define enemy
class Enemy:
    def __init__(self, x, y):
        self.img = enemy_img
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1

    def move(self):
        self.rect.x += self.direction * speed_enemy
        self.rect.y += speed_enemy
        if self.rect.x > height - self.rect.width or self.rect.x < 0:
            self.direction *= -1
        if random.randint(0, 100) < 5:
            self.direction *= -1

    def draw(self):
        screen.blit(self.img, self.rect)

class Boss:
    def __init__(self, width, height):
        self.img = boss_img
        self.rect = self.img.get_rect()
        self.rect.x = width / 2 - 50
        self.rect.y = height / 20
    
    def draw(self):
        screen.blit(self.img, self.rect)
        

player = Player(height / 2 - player_img.get_width() /
                2, width - player_img.get_height())
boss = Boss(width, height)
enemies = []
for i in range(5):
    for j in range(5):
        enemy = Enemy((width - enemy_img.get_width() * 5) / 2 +
                      j * 100, i * 100 - height / 2)
        enemies.append(enemy)

# Define game loop
running = True
clock = pygame.time.Clock()
win = False
lose = False
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
    if mouse_button[0]:
        player.shoot(mouse_pos)

    # Update game elements
    for shoot in player.shoots:
        shoot.move()
    for enemy in enemies:
        enemy.move()
        if enemy.rect.y > width:
            lose = True
            enemies.remove(enemy)

    # Check for collisions between shoots and enemies
    for shoot in player.shoots:
        for enemy in enemies:
            if shoot.rect.colliderect(enemy.rect):
                score_text += 1
                enemies.remove(enemy)
                player.shoots.remove(shoot)
                break

    # Get mouse position clicks
    mouse_pos[0], mouse_pos[1] = pygame.mouse.get_pos()
    mouse_button[0], mouse_button[1], mouse_button[2] = pygame.mouse.get_pressed(3)

    # Draw game elements
    screen.fill(GREY)
    if not win and not lose:
        player.draw_shoots()
        for enemy in enemies:
            enemy.draw()
        boss.draw()
        player.draw()
    
    # Draw score
    score = font.render('Score: ' + str(score_text), True, BLACK)
    screen.blit(score, (0, 0))

    if len(enemies) == 0 and not lose:
        win = True

    if win:
        win_text = font.render('You win!', True, BLACK)
        screen.blit(win_text, (width / 2.5 - win_text.get_width() /
                    2, height / 3 - win_text.get_height() / 2))
    elif lose:
        lose_text = font.render('You lose!', True, BLACK)
        screen.blit(lose_text, (width / 2.5 - lose_text.get_width() /
                    2, height / 3 - lose_text.get_height() / 2))

    # Update display
    pygame.display.update()
