import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 800
BLOCK_SIZE = 35
PROJECTILE_SIZE = 10
ENEMY_SIZE = 50
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
COOLDOWN = 1  # Cooldown in seconds

# Speed variables
PLAYER_SPEED = 15
PROJECTILE_SPEED = 20
ENEMY_SPEED = 7

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Enhanced Game with Timer and Summary')

# Player setup
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 2 * BLOCK_SIZE]

# Projectile setup
projectiles = []
last_shot_time = 0

# Enemy setup
enemies = []
enemy_spawn_chance = 20  # Initial spawn chance
level = 1
points = 0

# Background
background_color = BLACK

# Clock
clock = pygame.time.Clock()

# Timer
start_time = time.time()

def spawn_enemy():
    x_pos = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
    y_pos = 0
    enemies.append([x_pos, y_pos])

def move_enemies():
    for enemy in enemies:
        enemy[1] += ENEMY_SPEED

def move_projectiles():
    for projectile in projectiles:
        projectile[1] -= PROJECTILE_SPEED

def check_collisions():
    global running, points, level, enemy_spawn_chance, enemies
    for enemy in enemies:
        if enemy[1] > SCREEN_HEIGHT:
            enemies.remove(enemy)
        if (enemy[0] < player_pos[0] < enemy[0] + ENEMY_SIZE or enemy[0] < player_pos[0] + BLOCK_SIZE < enemy[0] + ENEMY_SIZE) and \
           (enemy[1] < player_pos[1] < enemy[1] + ENEMY_SIZE or enemy[1] < player_pos[1] + BLOCK_SIZE < enemy[1] + ENEMY_SIZE):
            running = False

    for projectile in projectiles:
        if projectile[1] < 0:
            projectiles.remove(projectile)
        for enemy in enemies:
            if (enemy[0] < projectile[0] < enemy[0] + ENEMY_SIZE or enemy[0] < projectile[0] + PROJECTILE_SIZE < enemy[0] + ENEMY_SIZE) and \
               (enemy[1] < projectile[1] < enemy[1] + ENEMY_SIZE or enemy[1] < projectile[1] + PROJECTILE_SIZE < enemy[1] + ENEMY_SIZE):
                try:
                    projectiles.remove(projectile)
                    enemies.remove(enemy)
                    points += 1
                    if points % 10 == 0:
                        level += 1
                        enemy_spawn_chance = max(1, enemy_spawn_chance // 2)  # Increase spawn rate
                except ValueError:
                    pass

running = True
while running:
    screen.fill(background_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and player_pos[0] < SCREEN_WIDTH - BLOCK_SIZE:
        player_pos[0] += PLAYER_SPEED
    if keys[pygame.K_UP]:
        current_time = time.time()
        if current_time - last_shot_time > COOLDOWN:
            projectiles.append([player_pos[0] + BLOCK_SIZE // 2, player_pos[1]])
            last_shot_time = current_time

    # Spawning enemies
    if random.randint(1, enemy_spawn_chance) == 1:
        spawn_enemy()

    # Move enemies
    move_enemies()

    # Move projectiles
    move_projectiles()

    # Check for collisions
    check_collisions()

    # Draw player
    pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], BLOCK_SIZE, BLOCK_SIZE))

    # Draw projectiles
    for projectile in projectiles:
        pygame.draw.rect(screen, WHITE, (projectile[0], projectile[1], PROJECTILE_SIZE, PROJECTILE_SIZE))

    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], ENEMY_SIZE, ENEMY_SIZE))

    # Display points, level and timer
    font = pygame.font.Font(None, 36)
    points_text = font.render(f"Points: {points}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    elapsed_time = int(time.time() - start_time)
    timer_text = font.render(f"Time: {elapsed_time}s", True, WHITE)
    screen.blit(points_text, (10, 10))
    screen.blit(level_text, (10, 50))
    screen.blit(timer_text, (10, 90))

    pygame.display.flip()
    clock.tick(30)

# Display summary in terminal
print(f"Game Over! You survived for {elapsed_time} seconds.")
print(f"Total Points: {points}")
print(f"Level Reached: {level}")

pygame.quit()
