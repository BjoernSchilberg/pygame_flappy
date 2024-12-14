import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600

# Colors
BG_COLOR = (0, 125, 255)
FG_COLOR = (255, 255, 255)

# Game variables
gravity = 0.5
bird_y = HEIGHT // 2
bird_x = WIDTH // 4
bird_velocity = 0
bird_width, bird_height = 30, 30

pipe_width = 60
pipe_gap = 150
pipe_velocity = 3
pipes = []

score = 0
font = pygame.font.Font("Ac437_Amstrad_PC.ttf", 36)


# Create initial pipes
def create_pipe():
    pipe_height = random.randint(100, HEIGHT - pipe_gap - 100)
    return [
        pygame.Rect(WIDTH, 0, pipe_width, pipe_height),  # Top pipe
        pygame.Rect(
            WIDTH, pipe_height + pipe_gap, pipe_width, HEIGHT - pipe_height - pipe_gap
        ),  # Bottom pipe
    ]


pipes.append(create_pipe())

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("flap.py")

# Game loop variables
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird_velocity = -8

    # Update bird
    bird_velocity += gravity
    bird_y += bird_velocity

    bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)

    # Update pipes
    for pipe_pair in pipes:
        pipe_pair[0].x -= pipe_velocity
        pipe_pair[1].x -= pipe_velocity

    # Remove pipes that go off-screen
    if pipes[0][0].x + pipe_width < 0:
        pipes.pop(0)
        pipes.append(create_pipe())
        score += 1

    # Check for collisions
    for pipe_pair in pipes:
        if bird_rect.colliderect(pipe_pair[0]) or bird_rect.colliderect(pipe_pair[1]):
            running = False

    # Check if bird is out of bounds
    if bird_y < 0 or bird_y + bird_height > HEIGHT:
        running = False

    # Drawing
    screen.fill(BG_COLOR)

    # Draw bird
    pygame.draw.rect(screen, FG_COLOR, bird_rect)

    # Draw pipes
    for pipe_pair in pipes:
        pygame.draw.rect(screen, FG_COLOR, pipe_pair[0])
        pygame.draw.rect(screen, FG_COLOR, pipe_pair[1])

    # Draw score
    score_text = font.render(f"Score: {score}", True, FG_COLOR)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
