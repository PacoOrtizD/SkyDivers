import pygame
import random
from sys import exit

# Screen setup ------------------------------------------------------------------------------------
pygame.init()
screen = pygame.display.set_mode((700, 800))
clock = pygame.time.Clock()
pygame.display.set_caption('SkyDivers')

# Font
font = pygame.font.Font('freesansbold.ttf', 40)

# Game Elements ------------------------------------------------------------------------------------
# Cloud surfaces and rects
cloud1_surf = pygame.image.load('Files/Cloud1.png').convert_alpha()
cloud2_surf = pygame.image.load('Files/cloud2.png').convert_alpha()
cloud3_surf = pygame.image.load('Files/cloud3.png').convert_alpha()
cloud1_rect = cloud1_surf.get_rect(topleft=(300, 200))
cloud2_rect = cloud2_surf.get_rect(topleft=(400, 300))
cloud3_rect = cloud3_surf.get_rect(topleft=(200, 100))

# Panda player
panda_surf = pygame.image.load('Files/panda.png').convert_alpha()
panda_surf = pygame.transform.scale(panda_surf, (120, 200))
panda_rect = panda_surf.get_rect(topleft=(300, 200))

# Obstacles
obstacle_surf = pygame.Surface((25, 25))
obstacle_surf.fill('Blue')
obstacle_rect = obstacle_surf.get_rect(topleft=(400, 400))

# Background
screen_surf = pygame.image.load('Files/screen.png').convert()
homescreen_surf = pygame.image.load('Files/homescreen.PNG').convert()

# Game over screen
game_over_surf = font.render("Game Over!", True, (255, 0, 0))
game_over_rect = game_over_surf.get_rect(center=(350, 250))

# Buttons ------------------------------------------------------------------------------------
button1 = pygame.image.load('Files/start_btn.png').convert_alpha()
button2 = pygame.image.load('Files/exit_btn.png').convert_alpha()
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect(center=(x, y))
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        surface.blit(self.image, self.rect)
        return action

# Game state ------------------------------------------------------------------------------------
game_state = "home"  # "home", "playing", "game_over"
start_time = 0

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = font.render(f'Score: {current_time}', True, (30, 30, 30))
    score_rect = score_surf.get_rect(center=(100, 50))
    screen.blit(score_surf, score_rect)

def game_reset():
    global start_time
    start_time = int(pygame.time.get_ticks() / 1000)
    panda_rect.x, panda_rect.y = 300, 200
    obstacle_rect.x, obstacle_rect.y = random.randint(0, 675), 800

def cloud_movement():
    for cloud_surf, cloud_rect in [(cloud1_surf, cloud1_rect), (cloud2_surf, cloud2_rect), (cloud3_surf, cloud3_rect)]:
        cloud_rect.y -= 2
        if cloud_rect.y < -250:
            cloud_rect.y = 850
            cloud_rect.x = random.randint(0, 600)
        screen.blit(cloud_surf, cloud_rect)

def panda_movement():
    screen.blit(panda_surf, panda_rect)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        panda_rect.x = max(0, panda_rect.x - 5)
    if keys[pygame.K_RIGHT]:
        panda_rect.x = min(700 - panda_rect.width, panda_rect.x + 5)

def obstacle_movement():
    obstacle_rect.y -= 2
    if obstacle_rect.y < -50:
        obstacle_rect.y = 850
        obstacle_rect.x = random.randint(0, 675)
    screen.blit(obstacle_surf, obstacle_rect)

# Button instances
start_button = Button(350, 400, button1, 0.5)
exit_button = Button(350, 500, button2, 0.5)

# Main loop ------------------------------------------------------------------------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill("Black")

    # HOME SCREEN --------------------------------------------------
    if game_state == "home":
        screen.blit(homescreen_surf, (0, 0))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_state = "playing"
            game_reset()

    # PLAYING SCREEN --------------------------------------------------
    elif game_state == "playing":
        screen.blit(screen_surf, (0, 0))

        cloud_movement()

        panda_movement()

        obstacle_movement()

        display_score()

        # Collision Detection
        if panda_rect.colliderect(obstacle_rect):
            game_state = "game_over"

    # GAME OVER SCREEN --------------------------------------------------
    elif game_state == "game_over":
        screen.blit(game_over_surf, game_over_rect)
        if start_button.draw(screen):
            game_state = "playing"
            game_reset()
        if exit_button.draw(screen):
            game_state = "home"
            game_reset()



    pygame.display.update()
    clock.tick(60)  # Keep frame rate at 60 FPS
