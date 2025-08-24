import pygame
import random
import math

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Neon Arcade Deluxe")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FOOD_COLOR = (255, 255, 0)
NEON_COLORS = [(0, 255, 255), (0, 200, 255), (0, 150, 255), (50, 205, 255)]
GRADIENT_BG = [(10, 10, 30), (30, 0, 50)]  # vertical gradient

# Clock
clock = pygame.time.Clock()

# Fonts
font_small = pygame.font.SysFont('arial', 20)
font_large = pygame.font.SysFont('arial', 40)

# Particle class for food effects
class Particle:
    def __init__(self, x, y):
        self.x = x + CELL_SIZE // 2
        self.y = y + CELL_SIZE // 2
        self.radius = random.randint(2, 4)
        self.color = FOOD_COLOR
        self.life = random.randint(20, 30)
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(1, 3)

    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.life -= 1
        self.radius = max(0, self.radius - 0.1)

    def draw(self, surface):
        if self.life > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.radius))

particles = []

# Draw gradient background
def draw_gradient(surface, colors):
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
        g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
        b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))

def game_over(score):
    screen.fill(BLACK)
    game_over_surface = font_large.render(f'Game Over! Score: {score}', True, (255, 0, 0))
    restart_surface = font_small.render('Press R to Restart or Q to Quit', True, WHITE)
    screen.blit(game_over_surface, (WIDTH // 2 - game_over_surface.get_width() // 2, HEIGHT // 3))
    screen.blit(restart_surface, (WIDTH // 2 - restart_surface.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def main():
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = "RIGHT"
    change_to = direction
    food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
    score = 0
    level = 1
    speed = 10

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    change_to = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    change_to = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    change_to = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    change_to = "RIGHT"

        direction = change_to

        # Move snake
        head_x, head_y = snake[0]
        if direction == "UP":
            head_y -= CELL_SIZE
        elif direction == "DOWN":
            head_y += CELL_SIZE
        elif direction == "LEFT":
            head_x -= CELL_SIZE
        elif direction == "RIGHT":
            head_x += CELL_SIZE

        new_head = (head_x, head_y)
        snake.insert(0, new_head)

        # Check food collision
        if new_head == food:
            score += 1
            for _ in range(20):  # spawn particles
                particles.append(Particle(food[0], food[1]))
            food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
            if score % 5 == 0:
                level = score // 5 + 1
                speed += 2
        else:
            snake.pop()

        # Collision with walls or self
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT or new_head in snake[1:]:
            game_over(score)
            return

        # Draw background gradient
        draw_gradient(screen, GRADIENT_BG)

        # Draw snake with neon gradient trail
        for i, segment in enumerate(snake):
            color = NEON_COLORS[i % len(NEON_COLORS)]
            pygame.draw.rect(screen, color, (*segment, CELL_SIZE, CELL_SIZE))
            # glowing effect
            glow_rect = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(glow_rect, (*color, 50), (0, 0, CELL_SIZE, CELL_SIZE))
            screen.blit(glow_rect, segment)

        # Draw food
        pygame.draw.rect(screen, FOOD_COLOR, (*food, CELL_SIZE, CELL_SIZE))

        # Draw particles
        for particle in particles[:]:
            particle.move()
            particle.draw(screen)
            if particle.life <= 0:
                particles.remove(particle)

        # Display score and level
        score_surface = font_small.render(f'Score: {score}', True, WHITE)
        level_surface = font_small.render(f'Level: {level}', True, (0, 255, 0))
        screen.blit(score_surface, (10, 10))
        screen.blit(level_surface, (WIDTH - level_surface.get_width() - 10, 10))

        pygame.display.update()
        clock.tick(speed)

if __name__ == "__main__":
    main()
