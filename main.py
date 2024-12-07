import pygame
import random

# Initialize PyGame
pygame.init()

# Screen Dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("KAMPITELLO")

# Clock and Font
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Load Images
hand_image = pygame.image.load("hand.png")
hand_image = pygame.transform.scale(hand_image, (120, 60))  # Resize the hand image
hand_width, hand_height = hand_image.get_size()
candy_images = {
    "kitkat": pygame.transform.scale(pygame.image.load("kitkat.png"), (60, 30)),
    "snickers": pygame.transform.scale(pygame.image.load("snickers.png"), (60, 60)),
    "broccoli": pygame.transform.scale(pygame.image.load("broccoli.png"), (60, 60))
}

# Player Hand
hand = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - hand_height - 20, hand_width, hand_height)
hand_speed = 10

# Candies
candies = []
for _ in range(10):
    candy_type = random.choice(list(candy_images.keys()))
    candies.append({
        "rect": pygame.Rect(random.randint(0, SCREEN_WIDTH - 30), random.randint(-1000, 0), 30, 30),
        "image": candy_images[candy_type],
        "type": candy_type
    })

candy_speed = 5

# Score and Timer
score = 0
game_time = 30  # seconds
start_ticks = pygame.time.get_ticks()

# Scoring Rules
scoring = {
    "kitkat": 20,
    "snickers": 10,
    "broccoli": -10
}

# Game Loop
running = True
while running:
    screen.fill(WHITE)

    # Timer Calculation
    elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000
    remaining_time = max(0, game_time - elapsed_time)

    # Check for Game Over
    if remaining_time == 0:
        running = False

    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and hand.left > 0:
        hand.move_ip(-hand_speed, 0)
    if keys[pygame.K_RIGHT] and hand.right < SCREEN_WIDTH:
        hand.move_ip(hand_speed, 0)

    # Move Candies
    for candy in candies:
        candy["rect"].move_ip(0, candy_speed)
        if candy["rect"].top > SCREEN_HEIGHT:
            candy["rect"].x = random.randint(0, SCREEN_WIDTH - 30)
            candy["rect"].y = random.randint(-100, 0)

        # Collision Detection
        if hand.colliderect(candy["rect"]):
            score += scoring[candy["type"]]
            candy["rect"].x = random.randint(0, SCREEN_WIDTH - 30)
            candy["rect"].y = random.randint(-100, 0)

    # Draw Elements
    screen.blit(hand_image, hand.topleft)
    for candy in candies:
        screen.blit(candy["image"], candy["rect"].topleft)

    # Display Score and Timer
    score_text = font.render(f"Score: {score}", True, BLACK)
    timer_text = font.render(f"Time: {remaining_time}s", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(timer_text, (10, 50))

    # Update Screen
    pygame.display.flip()
    clock.tick(30)

# Game Over Screen
screen.fill(WHITE)
game_over_text = font.render(f"Sening kampitellolaryn: {score}", True, BLACK)
screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
pygame.display.flip()
pygame.time.wait(3000)

# Quit PyGame
pygame.quit()
