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
npc_speed = 3
speed_shoot = 10

# Define mouse usage
mouse_pos = [0, 0]
mouse_button = [0, 0, 0] # lclic, scroll clic, rclic

# Load images
plyr_back = pygame.image.load('assets/plyr_back.png')
plyr_back = pygame.transform.scale(plyr_back, (50, 50))
plyr_front = pygame.image.load('assets/plyr_front.png')
plyr_front = pygame.transform.scale(plyr_front, (50, 50))
girl_img = pygame.image.load('assets/girl.png')
girl_img = pygame.transform.scale(girl_img, (50, 50))
girl_side = pygame.image.load('assets/girl_side.png')
girl_side = pygame.transform.scale(girl_side, (50, 50))
boss_img = pygame.image.load('assets/boss.png')
boss_img = pygame.transform.scale(boss_img, (100, 100))
asteroid_img = pygame.image.load('assets/fireBall.png')
asteroid_img = pygame.transform.scale(asteroid_img, (300, 300))
asteroid_img = pygame.transform.rotate(asteroid_img, 180)
fireBall_img = pygame.image.load('assets/fireBall.png')
fireBall_img = pygame.transform.scale(fireBall_img, (50, 50))
fireBall_img = pygame.transform.rotate(fireBall_img, 180)
shoot_img = pygame.image.load('assets/shoot.png')
shoot_img = pygame.transform.scale(shoot_img, (32, 40))

# Define player
class Player:
    def __init__(self, x, y):
        self.img = plyr_back
        self.rect = self.img.get_rect()
        self.direction = [0, 0, 0, 0]
        self.shoots = []
        self.last_shoot = 0
        self.rect.x = x
        self.rect.y = y

    def move(self):
        if (self.direction[0]):
            self.rect.x -= player_speed
            if (self.rect.x < 0):
                self.rect.x = 0
        if (self.direction[1]):
            self.rect.x += player_speed
            if (self.rect.x + self.rect.width > width):
                self.rect.x = width - self.rect.width
        if (self.direction[2]):
            self.rect.y -= player_speed
            if (self.rect.y < 0):
                self.rect.y = 0
        if (self.direction[3]):
            self.rect.y += player_speed
            if (self.rect.y + self.rect.height > height):
                self.rect.y = height - self.rect.height

    def shoot(self, dest):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > 50:
            self.last_shoot = now
            self.shoots.append(Shoot(self.rect.x + self.rect.width / 2 - shoot_img.get_width() / 2, self.rect.y, dest))

    def draw(self, mouse):
        if (self.rect.y > mouse[1]):
            self.img = plyr_back
        else:
            self.img = plyr_front
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

# Define fire balls
class FireBall:
    def __init__(self, x, y, health, speed, acceleration):
        if (health < 10):
            self.img = fireBall_img
        else:
            self.img = asteroid_img
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.health = health
        self.speed = speed
        self.acceleration = acceleration

    def move(self):
        self.rect.x += self.direction * self.speed
        self.rect.y += self.speed + random.randint(0, self.acceleration)
        if self.rect.x > height - self.rect.width or self.rect.x < 0:
            self.direction *= -1
        if random.randint(0, 100) < 5:
            self.direction *= -1

    def draw(self):
        screen.blit(self.img, self.rect)

# Define boss
class Boss:
    def __init__(self, width, height):
        self.img = boss_img
        self.rect = self.img.get_rect()
        self.fire_balls = []
        self.rect.x = width / 2 - 50
        self.rect.y = height / 20
        self.health = 100
    
    def fire_rain(self, nbr):
        for i in range(nbr):
            self.fire_balls.append(FireBall(random.randint(0, width), -100, 3, 2, 5))
    
    def asteroid(self):
        self.fire_balls.append(FireBall(boss.rect.x, -350, 25, 1, 2))
    
    def apocalypse(self):
        self.asteroid()
        self.fire_rain(30)

    def draw(self):
        screen.blit(self.img, self.rect)

    def draw_fire_balls(self):
        for enemy in self.fire_balls:
            enemy.draw()

# Create NPC

class NPC:
    def __init__(self, x, y, img, img_side):
        self.img = img
        self.img_side = img_side
        self.img_side_reverse = pygame.transform.flip(self.img_side, True, False)
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.movement = 0
        self.direction = 0
        self.wait = 0
        self.animation = 0

    def move(self):
        if (self.animation != 0 and self.movement == 0):
            self.animation = 0
        if (self.movement <= 0 and self.wait <= 0):
            self.movement = random.randint(10, 50)
            self.direction = random.randint(0, 1)
            self.wait = random.randint(30, 60)
        if (self.movement > 0 and self.direction):
            self.animation = 2
            self.rect.x -= npc_speed
            if (self.rect.x < 0):
                self.rect.x = 0
        elif (self.movement > 0 and self.direction == 0):
            self.animation = 1
            self.rect.x += npc_speed
            if (self.rect.x + self.rect.width > width):
                self.rect.x = width - self.rect.width
        self.movement -= 1
        self.wait -= 1

    def draw(self):
        if (self.animation == 0):
            screen.blit(self.img, self.rect)
        elif (self.animation == 1):
            screen.blit(self.img_side, self.rect)
        else:
            screen.blit(self.img_side_reverse, self.rect)

# Create player
player = Player(width / 2 - plyr_back.get_width() / 2, height - plyr_back.get_height())

# Create boss and his fireballs
boss = Boss(width, height)

# Create NPCs
girl = NPC(0, height - girl_img.get_height(), girl_img, girl_side)

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
    if keys[pygame.K_q] and player.rect.x > 0:
        player.direction[0] = 1
    if keys[pygame.K_d] and player.rect.x < height - player.rect.width:
        player.direction[1] = 1
    if keys[pygame.K_z] and player.rect.x > 0:
        player.direction[2] = 1
    if keys[pygame.K_s] and player.rect.x < height - player.rect.width:
        player.direction[3] = 1
    if mouse_button[0]:
        player.shoot(mouse_pos)

    if (len(boss.fire_balls) == 0):
        boss.apocalypse()

    # Update game elements
    player.move()
    girl.move()
    for shoot in player.shoots:
        shoot.move()
    for enemy in boss.fire_balls:
        enemy.move()

    # Check for collisions between shoots and fire balls
    for shoot in player.shoots:
        for fireball in boss.fire_balls:
            if shoot.rect.colliderect(fireball.rect):
                fireball.health -= 1
                if (fireball.health <= 0):
                    score_text += 1
                    boss.fire_balls.remove(fireball)
                player.shoots.remove(shoot)
                break
    
    # Check for collision between fire balls and friendly entities
    for fireball in boss.fire_balls:
        if fireball.rect.colliderect(player.rect) or fireball.rect.colliderect(girl.rect):
            lose = True
            break
    
    # Check for collisions between shoots and boss
    for shoot in player.shoots:
        if shoot.rect.colliderect(boss.rect):
            boss.health -= 1
            player.shoots.remove(shoot)

    #Check if fire balls are out of screen
    for fireball in boss.fire_balls:
        if fireball.rect.y > height:
            boss.fire_balls.remove(fireball)
    
    #Check if shoots are out of screen
    for shoot in player.shoots:
        if shoot.rect.y + shoot.rect.height < 0 or shoot.rect.y > height or shoot.rect.x > width or shoot.rect.x + shoot.rect.width < 0:
            player.shoots.remove(shoot)

    # Get mouse position clicks
    mouse_pos[0], mouse_pos[1] = pygame.mouse.get_pos()
    mouse_button[0], mouse_button[1], mouse_button[2] = pygame.mouse.get_pressed(3)

    # Reset player movements
    player.direction[0] = 0
    player.direction[1] = 0
    player.direction[2] = 0
    player.direction[3] = 0 

    # Draw game elements
    screen.fill(GREY)
    if not win and not lose:
        player.draw_shoots()
        boss.draw_fire_balls()
        boss.draw()
        girl.draw()
        player.draw(mouse_pos)

    
    # Draw score
    score = font.render('Score: ' + str(score_text), True, BLACK)
    screen.blit(score, (0, 0))

    if boss.health == 0 and not lose:
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
