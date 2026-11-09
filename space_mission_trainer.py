import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Junior Astronaut Mission Trainer")

# Clock & FPS
clock = pygame.time.Clock()
FPS = 60

# Colors (Retro Sci-Fi Theme)
BLACK = (15, 15, 25)
DARK_GREY = (35, 38, 52)
LIGHT_BLUE = (100, 200, 255)
WHITE = (240, 240, 255)
GREEN = (46, 204, 113)
RED = (231, 76, 60)
YELLOW = (241, 196, 15)
ORANGE = (230, 126, 34)
PURPLE = (155, 89, 182)

# Safe Default Fonts (uses Pygame's built-in scalable font to prevent OS font crash)
font_large = pygame.font.Font(None, 36)
font_med = pygame.font.Font(None, 24)
font_small = pygame.font.Font(None, 18)

class Astronaut:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 32
        self.speed = 4
        self.color = WHITE

    def move(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed

        # Keep astronaut inside the room boundaries
        self.x = max(60, min(SCREEN_WIDTH - 60 - self.size, self.x))
        self.y = max(120, min(SCREEN_HEIGHT - 100 - self.size, self.y))

    def draw(self, surface):
        # Draw a retro pixelated astronaut body
        # Helmet
        pygame.draw.rect(surface, LIGHT_BLUE, (self.x + 8, self.y, 16, 16))
        # Suit body (White/Orange NASA style)
        pygame.draw.rect(surface, ORANGE, (self.x + 6, self.y + 16, 20, 12))
        # Boots
        pygame.draw.rect(surface, DARK_GREY, (self.x + 6, self.y + 28, 8, 4))
        pygame.draw.rect(surface, DARK_GREY, (self.x + 18, self.y + 28, 8, 4))


class Station:
    def __init__(self, name, x, y, width, height, color, key_name):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.key_name = key_name
        self.status = "STABLE"
        self.timer = 100

    def draw(self, surface, astronaut):
        # Check proximity for interaction highlight
        dist = abs((self.x + self.width // 2) - (astronaut.x + astronaut.size // 2)) + \
               abs((self.y + self.height // 2) - (astronaut.y + astronaut.size // 2))
        
        is_near = dist < 75

        # Draw workstation console box
        box_color = self.color if not is_near else WHITE
        pygame.draw.rect(surface, box_color, (self.x, self.y, self.width, self.height), 3 if not is_near else 5)
        pygame.draw.rect(surface, DARK_GREY, (self.x + 3, self.y + 3, self.width - 6, self.height - 6))

        # Text labels
        name_surf = font_med.render(self.name, True, self.color)
        surface.blit(name_surf, (self.x + 10, self.y + 10))

        status_text = f"Level: {int(self.timer)}%"
        stat_color = GREEN if self.timer > 40 else (RED if self.timer < 20 else YELLOW)
        stat_surf = font_small.render(status_text, True, stat_color)
        surface.blit(stat_surf, (self.x + 10, self.y + 35))

        if is_near:
            prompt = font_small.render(f"Press [SPACE] to Fix", True, GREEN)
            surface.blit(prompt, (self.x + 10, self.y + 60))


def main():
    score = 100
    game_time = 60.0  # 60 seconds mission timer
    
    player = Astronaut(400, 350)

    stations = [
        Station("Life Support", 100, 150, 160, 90, LIGHT_BLUE, "OXYGEN"),
        Station("Radiation Shield", 540, 150, 160, 90, PURPLE, "RADIATION"),
        Station("Power Grid", 100, 380, 160, 90, YELLOW, "POWER"),
        Station("Food Hydroponics", 540, 380, 160, 90, GREEN, "FOOD")
    ]

    running = True
    active_message = "Welcome Commander! Walk to any station and press SPACE to maintain systems."

    while running:
        dt = clock.tick(FPS) / 1000.0
        game_time -= dt

        if game_time <= 0:
            running = False

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for st in stations:
                        dist = abs((st.x + st.width // 2) - (player.x + player.size // 2)) + \
                               abs((st.y + st.height // 2) - (player.y + player.size // 2))
                        if dist < 85:
                            st.timer = min(100, st.timer + 35)
                            score += 25
                            active_message = f"Successfully serviced {st.name}! Systems stable."

        for st in stations:
            st.timer -= dt * 6.5
            if st.timer <= 0:
                st.timer = 0
                score -= 1

        player.move(keys)

        # --- DRAWING ---
        screen.fill(BLACK)

        for i in range(30):
            sx = (i * 137) % SCREEN_WIDTH
            sy = (i * 89) % SCREEN_HEIGHT
            screen.set_at((sx, sy), (100, 100, 120))

        title_surf = font_large.render("JUNIOR ASTRONAUT MISSION TRAINER", True, WHITE)
        screen.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 15))

        score_surf = font_med.render(f"Mission Score: {score}", True, GREEN)
        time_surf = font_med.render(f"Time Left: {int(game_time)}s", True, YELLOW)
        screen.blit(score_surf, (40, 55))
        screen.blit(time_surf, (SCREEN_WIDTH - 180, 55))

        for st in stations:
            st.draw(screen, player)

        player.draw(screen)

        # Dialogue / Instruction Box
        pygame.draw.rect(screen, DARK_GREY, (50, 490, SCREEN_WIDTH - 100, 85))
        pygame.draw.rect(screen, GREEN, (50, 490, SCREEN_WIDTH - 100, 85), 2)
        
        msg_title = font_med.render("Mission Control Log:", True, GREEN)
        screen.blit(msg_title, (70, 502))

        msg_body = font_small.render(active_message, True, WHITE)
        screen.blit(msg_body, (70, 532))

        controls_hint = font_small.render("Use Arrow Keys or WASD to move character", True, LIGHT_BLUE)
        screen.blit(controls_hint, (70, 555))

        pygame.display.flip()

    # Game Over Screen
    screen.fill(BLACK)
    go_surf = font_large.render("MISSION COMPLETED!", True, GREEN)
    final_score = font_med.render(f"Final Outpost Score: {score}", True, WHITE)
    restart_hint = font_med.render("Press ESC to exit.", True, LIGHT_BLUE)

    screen.blit(go_surf, (SCREEN_WIDTH // 2 - go_surf.get_width() // 2, 200))
    screen.blit(final_score, (SCREEN_WIDTH // 2 - final_score.get_width() // 2, 260))
    screen.blit(restart_hint, (SCREEN_WIDTH // 2 - restart_hint.get_width() // 2, 330))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()
