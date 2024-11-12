import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle
paddle_width = 100
paddle_height = 10
paddle = pygame.Rect(WIDTH // 2 - paddle_width // 2, HEIGHT - 30, paddle_width, paddle_height)
paddle_speed = 6

# Ball
ball_radius = 10
ball = pygame.Rect(WIDTH // 2 - ball_radius, HEIGHT // 2 - ball_radius, ball_radius * 2, ball_radius * 2)
ball_speed = [4, -4]

# Bricks
brick_width = WIDTH // 10
brick_height = 20


def create_bricks(pattern):
    bricks = []
    if pattern == 1:
        for row in range(5):
            for col in range(10):
                brick = pygame.Rect(col * brick_width, row * brick_height, brick_width, brick_height)
                bricks.append(brick)
    elif pattern == 2:
        for row in range(5):
            for col in range(5):
                brick = pygame.Rect(col * brick_width * 2, row * brick_height, brick_width, brick_height)
                bricks.append(brick)
    elif pattern == 3:
        for row in range(5):
            for col in range(10):
                if (row + col) % 2 == 0:
                    brick = pygame.Rect(col * brick_width, row * brick_height, brick_width, brick_height)
                    bricks.append(brick)
    return bricks


brick_pattern = 1
bricks = create_bricks(brick_pattern)

# Load textures
paddle_img = pygame.image.load('Assets/Paddle.png')
ball_img = pygame.image.load('Assets/Ball.png')
brick_img = pygame.image.load('Assets/Brick.png')

# Resize textures if necessary
paddle_img = pygame.transform.scale(paddle_img, (paddle_width, paddle_height))
ball_img = pygame.transform.scale(ball_img, (ball_radius * 2, ball_radius * 2))
brick_img = pygame.transform.scale(brick_img, (brick_width, brick_height))

# Game over flag
game_over = False


def draw_game_over():
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text, text_rect)

    button_font = pygame.font.Font(None, 50)
    button_text = button_font.render("Try Again", True, WHITE)
    button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    pygame.draw.rect(screen, BLACK, button_rect.inflate(20, 20))
    screen.blit(button_text, button_rect)
    return button_rect


def reset_game():
    global paddle, ball, bricks, ball_speed, brick_pattern
    paddle.topleft = (WIDTH // 2 - paddle_width // 2, HEIGHT - 30)
    ball.topleft = (WIDTH // 2 - ball_radius, HEIGHT // 2 - ball_radius)
    ball_speed = [4, -4]
    brick_pattern = (brick_pattern % 3) + 1
    bricks = create_bricks(brick_pattern)


# Main game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if try_again_button.collidepoint(event.pos):
                game_over = False
                reset_game()

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.left -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.right += paddle_speed

        # Move ball
        ball.left += ball_speed[0]
        ball.top += ball_speed[1]

        # Ball collision with walls
        if ball.left <= 0 or ball.right >= WIDTH:
            ball_speed[0] = -ball_speed[0]
        if ball.top <= 0:
            ball_speed[1] = -ball_speed[1]
        if ball.colliderect(paddle):
            ball_speed[1] = -ball_speed[1]

        # Ball collision with bricks
        for brick in bricks[:]:
            if ball.colliderect(brick):
                ball_speed[1] = -ball_speed[1]
                bricks.remove(brick)

        if ball.bottom >= HEIGHT:
            game_over = True

        if not bricks:
            reset_game()

        # Drawing
        screen.blit(paddle_img, paddle.topleft)
        screen.blit(ball_img, ball.topleft)
        for brick in bricks:
            screen.blit(brick_img, brick.topleft)
    else:
        try_again_button = draw_game_over()

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
