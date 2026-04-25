import pygame
import random
import sys

#  INITIAL SETUP 
pygame.init()

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game (Wrap Around)")

clock = pygame.time.Clock()

#  COLORS 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

#  FONT 
font = pygame.font.SysFont("Arial", 24)


#  SNAKE SETUP 
snake = [(100, 100), (80, 100), (60, 100)]
direction = "RIGHT"

#  FOOD 
def generate_food():
    """Generate food not on the snake"""
    while True:
        x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        if (x, y) not in snake:
            return (x, y)

food = generate_food()

#  GAME VARIABLES 
score = 0
level = 1
speed = 8
foods_to_level = 3

running = True

#  MAIN GAME LOOP 
while running:

    #  EVENTS 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"

    #  MOVE SNAKE HEAD 
    head_x, head_y = snake[0]

    if direction == "UP":
        head_y -= CELL_SIZE
    elif direction == "DOWN":
        head_y += CELL_SIZE
    elif direction == "LEFT":
        head_x -= CELL_SIZE
    elif direction == "RIGHT":
        head_x += CELL_SIZE

    #  WRAP AROUND LOGIC 
    # If snake goes out of bounds, it appears on the opposite side
    if head_x < 0:
        head_x = WIDTH - CELL_SIZE
    elif head_x >= WIDTH:
        head_x = 0

    if head_y < 0:
        head_y = HEIGHT - CELL_SIZE
    elif head_y >= HEIGHT:
        head_y = 0

    new_head = (head_x, head_y)

    #  SELF COLLISION 
    if new_head in snake:
        running = False  # game over

    snake.insert(0, new_head)

    #  FOOD EATING 
    if new_head == food:
        score += 1
        food = generate_food()

        # level up system
        if score % foods_to_level == 0:
            level += 1
            speed += 2
    else:
        snake.pop()

    #  DRAW EVERYTHING 
    screen.fill(BLACK)

    # draw snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

    # draw apple 
    pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))

    # draw score and level
    text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.update()
    clock.tick(speed)

pygame.quit()
sys.exit()