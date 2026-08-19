import pygame 
import random 
 
pygame.init() 
 
WIDTH, HEIGHT = 400, 600 
player_size = 60 
 
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Doodle Jump") 
clock = pygame.time.Clock() 
 
background = pygame.image.load("background.png").convert() 
background = pygame.transform.scale(background, (WIDTH, HEIGHT)) 
 
player_img = pygame.image.load(r"d:\Tôi\player.png").convert_alpha() 
player_img = pygame.transform.scale(player_img, (player_size, player_size)) 

enemy_img = pygame.image.load("monster.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (70, 70))

star_img = pygame.image.load("star.png").convert_alpha()
star_img = pygame.transform.scale(star_img, (30, 30))
 
WHITE = (255, 255, 255) 
GREEN = (0, 200, 0) 
BLUE = (0, 100, 255) 
YELLOW = (255, 220, 0) 
RED = (220, 50, 50) 
BLACK = (0, 0, 0) 
 
player_x = WIDTH // 2 - player_size // 2 
player_y = HEIGHT - 150 
player_vel_y = 0 
gravity = 0.5 
jump_power = -11 
speed = 6 
 
plat_width = 100 
plat_height = 60 
 
platforms = [] 
plat_speed = [] 
 
platform_img = pygame.image.load("platform.png").convert_alpha() 
platform_img = pygame.transform.scale(platform_img, (plat_width, plat_height)) 
 
for i in range(10): 
    plat_x = random.randint(0, WIDTH - plat_width) 
    plat_y = i * (HEIGHT // 10) 
 
    platforms.append(pygame.Rect(plat_x, plat_y, plat_width, plat_height)) 
    plat_speed.append(random.choice([-2, 2])) 
 
stars = [] 
enemies = [] 
enemy_speeds = [] 
 
for i in range(2): 
    star_x = random.randint(0, WIDTH - 30) 
    star_y = random.randint(0, HEIGHT) 
    stars.append(pygame.Rect(star_x, star_y, 25, 25)) 
 
for i in range(1): 
    enemy_x = random.randint(0, WIDTH - 50) 
    enemy_y = random.randint(0, HEIGHT) 
    enemies.append(pygame.Rect(enemy_x, enemy_y, 50, 50)) 
    enemy_speeds.append(1) 
 
running = True 
score = 0 
 
while running: 
    clock.tick(60) 
 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False 
 
    keys = pygame.key.get_pressed() 
 
    if keys[pygame.K_LEFT] or keys[pygame.K_a]: 
        player_x -= speed 
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]: 
        player_x += speed 
 
    if player_x > WIDTH: 
        player_x = -player_size 
    elif player_x < -player_size: 
        player_x = WIDTH 
 
    player_vel_y += gravity 
    player_y += player_vel_y 
 
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size) 
 
   
    for i in range(len(stars) - 1, -1, -1): 
        if player_rect.colliderect(stars[i]): 
            stars.pop(i) 
            score += 50
 

    for i in range(len(enemies)): 
        enemies[i].x += enemy_speeds[i] 
 
        if enemies[i].right >= WIDTH: 
            enemies[i].right = WIDTH 
            enemy_speeds[i] = -2 
        elif enemies[i].left <= 0: 
            enemies[i].left = 0 
            enemy_speeds[i] = 2 
 
        if player_rect.colliderect(enemies[i]): 
            print(f"Game Over! Score: {score}") 
            running = False 
 

    if player_vel_y > 0: 
        for plat in platforms: 
            if player_rect.colliderect(plat): 
                player_y = plat.top - player_size 
                player_vel_y = jump_power 
 

    for i in range(len(platforms)): 
        platforms[i].x += plat_speed[i] 
        if platforms[i].left <= 0: 
            platforms[i].left = 0 
            plat_speed[i] *= -1 
        elif platforms[i].right >= WIDTH: 
            platforms[i].right = WIDTH 
            plat_speed[i] *= -1 
 

    if player_y < HEIGHT // 2: 
        player_y = HEIGHT // 2 
 
        for i in range(len(platforms)): 
            platforms[i].y -= player_vel_y 
        for star in stars: 
            star.y -= player_vel_y 
        for enemy in enemies: 
            enemy.y -= player_vel_y 

   
    for i in range(len(enemies) - 1, -1, -1):
        if enemies[i].y > HEIGHT:
            enemies.pop(i)
            enemy_speeds.pop(i)

            enemy_x = random.randint(0, WIDTH - 50)
            enemy_y = random.randint(-300, -100)
            
            enemies.append(pygame.Rect(enemy_x, enemy_y, 50, 50))
            enemy_speeds.append(random.choice([-2, 2]))


    for i in range(len(stars) - 1, -1, -1):
        if stars[i].y > HEIGHT:
            stars.pop(i)

            star_x = random.randint(0, WIDTH - 30)
            star_y = random.randint(-300, -50)
            
            stars.append(pygame.Rect(star_x, star_y, 25, 25))
 

    for i in range(len(platforms) - 1, -1, -1): 
        if platforms[i].y > HEIGHT: 
            platforms.pop(i) 
            plat_speed.pop(i) 
 
            new_x = random.randint(0, WIDTH - plat_width) 
            new_y = random.randint(-50, 0) 
 
            platforms.append(pygame.Rect(new_x, new_y, plat_width, plat_height)) 
            plat_speed.append(random.choice([-2, 2])) 
            score += 10 
 

    if player_y > HEIGHT: 
        print(f"Game Over! Score: {score}") 
        running = False 
 
    screen.blit(background, (0, 0)) 
 
    for plat in platforms: 
        screen.blit(platform_img, plat) 

    for star in stars: 
        screen.blit(star_img, star)
 
    for enemy in enemies:
        screen.blit(enemy_img, enemy)
 
    screen.blit(player_img, player_rect) 
 
    pygame.display.update() 
 
pygame.quit()
