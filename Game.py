import pygame
import random
import time
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
columns, rows = 40, 50
tile_size = 20
screen_width = rows * tile_size
screen_height = columns * tile_size

# Colors
colors = {
  "white": [255, 255, 255],
  "black": [0, 0, 0],
  "red": [255, 0, 0],
  "blue": [0, 0, 255],
  "green": [0, 255, 0]
}

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Game variables
v_value, h_value = 29, 39  # Player position
v1_value, h1_value = 10, 20  # Enemy position
enemy_speed = 1  # Enemy Speed
bullets = [] # List to store bullets, each is a dict
v2_value, h2_value = None, None  # Shot position
continuous_direction = None
direction = "up"
game_over = False

# Randomize enemy position
def randomize_position(max_val):
    return random.randint(2, max_val)

# Set image variables
image1 = pygame.image.load("Assets/Astronaut Left2.png")
image1 = pygame.transform.scale(image1, (tile_size, tile_size))
image2 = pygame.image.load("Assets/Grass1.png")
#image2 = pygame.transform.scale(image2, (tile_size, tile_size))

# Draw the game elements
def draw_board():
    screen.fill(colors["black"])  # Clear the screen
    for a in range(columns):
        for b in range(rows):
            x, y = b * tile_size, a * tile_size
            screen.blit(image2, (x, y))
            if a == v_value and b == h_value: # Player
                screen.blit(image1, (x, y))
            elif a == v1_value and b == h1_value:  # Enemy
                pygame.draw.rect(screen, colors["red"], (x, y, tile_size, tile_size))
            else: # Bullets
                for bullet in bullets:
                    pygame.draw.circle(screen, GREEN, (int(bullet["x"]), int(bullet["y"])), 5)
                

# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and h_value > 1:
        h_value -= 1
        direction = "left"
    if keys[pygame.K_RIGHT] and h_value < rows - 2:
        h_value += 1
        direction = "right"
    if keys[pygame.K_UP] and v_value > 1:
        v_value -= 1
        direction = "up"
    if keys[pygame.K_DOWN] and v_value < columns - 2:
        v_value += 1
        direction = "down"

    # Detect mouse click and create bullets
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Compute the direction vector
        direction_x = mouse_x - h_value * tile_size
        direction_y = mouse_y - v_value * tile_size
        length = math.sqrt(direction_x**2 + direction_y**2)
        if length != 0:
            direction_x /= length  # Normalize direction vector
            direction_y /= length

        # Add bullet at player's position
        bullets.append({
            "x": h_value * tile_size,
            "y": v_value * tile_size,
            "dx": direction_x,
            "dy": direction_y
        })

    # Move bullets
    bullet_speed = 50
    for bullet in bullets:
        bullet["x"] += bullet["dx"] * bullet_speed
        bullet["y"] += bullet["dy"] * bullet_speed

    # Keep only bullets inside the screen
    bullets = [b for b in bullets if 0 < b["x"] < screen_width and 0 < b["y"] < screen_height]


    # Create enemy AI pattern and implement speed
    if enemy_speed % 4 == 0:
        if h1_value <= 2 and v1_value <= 2:
            randy = [2,4]
        elif h1_value >= rows - 1 and v1_value <= 2:
            randy = [1,4]
        elif h1_value <= 2 and v1_value >= columns - 1:
            randy = [2,3]
        elif h1_value >= rows - 1 and v1_value >= columns - 1:
            randy = [1,3]
        elif h1_value <= 2:
            randy = [2,3,4]
        elif h1_value >= rows - 1:
            randy = [1,3,4]
        elif v1_value <= 2:
            randy = [1,2,4]
        elif v1_value >= columns - 1:
            randy = [1,2,3]
        else:
            randy = [1,2,3,4]
        rand = random.choice(randy)
        # Move enemy
        if rand == 1:
            h1_value -= 1
        elif rand == 2:
            h1_value += 1
        elif rand == 3:
            v1_value -= 1
        elif rand == 4:
            v1_value += 1
    enemy_speed += 1 


    # Check for collision
    if (h_value, v_value) == (h1_value, v1_value) or keys[pygame.K_q]:
        game_over = True
    for bullet in bullets:
        if h1_value*tile_size in range(int(bullet["x"]) - 20, int(bullet["x"]) + 20) and v1_value*tile_size in range(int(bullet["y"]) - 20, int(bullet["y"]) + 20):
            (h1_value, v1_value) = randomize_position(rows-1), randomize_position(columns)
            bullets.remove(bullet)



    # Update the screen
    draw_board()
    pygame.display.flip()

    # Control the frame rate
    clock.tick(10)

pygame.quit()
