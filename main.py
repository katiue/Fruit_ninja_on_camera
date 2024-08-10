import pygame
import random

#setup openCV capture and window size
# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
FRUIT_SIZE = 90
BOMB_SIZE = 90
GRAVITY = 0.2

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Fruit Ninja')
# Load images
fruit_types = ['apple.png', 'mango.png', 'orange.png', 'pearl.png', 'pineapple.png', 'strawberry.png', 'watermelon.png']

bomb_image = pygame.image.load('bomb.png')
bomb_image = pygame.transform.scale(bomb_image, (BOMB_SIZE, BOMB_SIZE))

# Fruit and bomb lists
fruits = []
bombs = []

score = 0
gameOver = False
Restart = False

def choose_fruit():    
    chosen_fruit = random.randint(0, len(fruit_types) - 1)
    fruit_image = pygame.image.load(fruit_types[chosen_fruit])
    fruit_image = pygame.transform.scale(fruit_image, (FRUIT_SIZE, FRUIT_SIZE))
    return fruit_image

font = pygame.font.SysFont(None, 36)

# Function to draw text
def draw_text(surface, text, color, rect):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, rect)

# Function to add a fruit
def add_fruit():
    x = random.randint(0, WIDTH)
    y = HEIGHT
    if(x < WIDTH/2):
        vx = random.uniform(1, 3)
    else:
        vx = random.uniform(-3, -1)  # Horizontal velocity
    vy = -random.uniform(10, 15)  # Vertical velocity
    fruit_image = choose_fruit()
    fruit_rect = fruit_image.get_rect(center=(x, y))
    fruits.append({'rect': fruit_rect, 'vx': vx, 'vy': vy, 'image': fruit_image})

# Function to add a bomb
def add_bomb():
    x = random.randint(0, WIDTH)
    y = HEIGHT
    if(x < WIDTH/2):
        vx = random.uniform(1, 3)
    else:
        vx = random.uniform(-3, -1)  # Horizontal velocity
    vy = -random.uniform(10, 15)  # Vertical velocity
    bomb_rect = bomb_image.get_rect(center=(x, y))
    bombs.append({'rect': bomb_rect, 'vx': vx, 'vy': vy})

# Main game loop
running = True
while running:
    clock.tick(60)
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(WHITE)
    # Get the current mouse position
    mouse_pos = pygame.mouse.get_pos()
    # Add new fruits and bombs
    if score < 10:
        if random.random() < 0.0075:
            add_fruit()
        if random.random() < 0.001:
            add_bomb()
    elif score < 20:
        if random.random() < 0.015:
            add_fruit()
        if random.random() < 0.005:
            add_bomb()
    else:
        if random.random() < 0.025:
            add_fruit()
        if random.random() < 0.01:
            add_bomb()

    # Update fruits
    for fruit in fruits[:]:
        fruit['vy'] += GRAVITY
        fruit['rect'].x += int(fruit['vx'])
        fruit['rect'].y += int(fruit['vy'])
        if fruit['rect'].top > HEIGHT or fruit['rect'].right < 0 or fruit['rect'].left > WIDTH:
            fruits.remove(fruit)
    
    # Update bombs
    for bomb in bombs[:]:
        bomb['vy'] += GRAVITY
        bomb['rect'].x += int(bomb['vx'])
        bomb['rect'].y += int(bomb['vy'])
        if bomb['rect'].top > HEIGHT or bomb['rect'].right < 0 or bomb['rect'].left > WIDTH:
            bombs.remove(bomb)
    
    # Draw fruits and bombs
    for fruit in fruits:
        screen.blit(fruit['image'], fruit['rect'])
    for bomb in bombs:
        screen.blit(bomb_image, bomb['rect'])
    
    # Update the display
    pygame.display.flip()
    
    for fruit in fruits[:]:
        if fruit['rect'].collidepoint(mouse_pos):
            fruits.remove(fruit)
            score += 1
    for bomb in bombs[:]:
        if bomb['rect'].collidepoint(mouse_pos):
            running = False  # Game over

pygame.quit()