import pygame
from random import randint
import random
from sys import exit

# Screen setup ------------------------------------------------------------------------------------
pygame.init()
screen = pygame.display.set_mode((700, 800))
pygame.display.set_caption('SkyDivers')
pygame_icon = pygame.image.load('Files/PANDA.png')
pygame.display.set_icon(pygame_icon)
clock = pygame.time.Clock()
pygame.display.set_caption('SkyDivers')

# Font
font = pygame.font.Font('Files/CutePixel.ttf', 50)

# Game Elements ------------------------------------------------------------------------------------
# Cloud surfaces and rects
cloud1_surf = pygame.image.load('Files/Nube.png').convert_alpha()
cloud1_surf = pygame.transform.scale(cloud1_surf, (400, 300))
cloud2_surf = pygame.image.load('Files/Nube2.png').convert_alpha()
cloud2_surf = pygame.transform.scale(cloud2_surf, (400, 300))
cloud3_surf = pygame.image.load('Files/Nube2.png').convert_alpha()
cloud3_surf = pygame.transform.scale(cloud3_surf, (400, 300))
cloud_list = []
cloud_timer = pygame.USEREVENT + 2
pygame.time.set_timer(cloud_timer, 4500)

# Panda player
panda_surf = pygame.image.load('Files/PANDA.png').convert_alpha()
panda_surf = pygame.transform.scale(panda_surf, (80, 130))
panda_rect = panda_surf.get_rect(topleft=(300, 200))
panda_mask = pygame.mask.from_surface(panda_surf)

# Obstacles
obstacle_rect_list = []
obstacle_surf = pygame.image.load('Files/rocket.png').convert_alpha()
obstacle_surf = pygame.transform.scale(obstacle_surf, (80, 240))
obstacle_mask = pygame.mask.from_surface(obstacle_surf)

obstacle_surf2 = pygame.image.load('Files/Plane.png').convert_alpha()
obstacle_surf2 = pygame.transform.scale(obstacle_surf2, (220, 140))
obstacle_mask2 = pygame.mask.from_surface(obstacle_surf2)

obstacle_surf3 = pygame.image.load('Files/plane2.png').convert_alpha()
obstacle_surf3 = pygame.transform.scale(obstacle_surf3, (200, 100))
obstacle_mask3 = pygame.mask.from_surface(obstacle_surf3)

# Game difficulty
speed = 2
timer_obstacles = 2500

# Obstacle timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, timer_obstacles)

# Background
screen_surf = pygame.image.load('Files/background.png').convert()
homescreen_surf = pygame.image.load('Files/homescreen.png').convert()

# Game over screen
game_over_text = font.render("Game Over!", True, (224, 95, 20))
game_over_textRect = game_over_text.get_rect(center=(350, 100))
game_over_surf = pygame.image.load('Files/EndPage.png').convert_alpha()
game_over_surf = pygame.transform.scale(game_over_surf, (700, 800))
game_over_rect = game_over_surf.get_rect(topleft=(0, 0))

# Buttons ------------------------------------------------------------------------------------
button1 = pygame.image.load('Files/restart.png').convert_alpha()
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
game_state = "home"
start_time = 0
final_score = 0  # ✅ New variable to store final score

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = font.render(f'Score: {current_time}', True, (36, 43, 54))
    score_rect = score_surf.get_rect(center=(120, 50))
    screen.blit(score_surf, score_rect)

def game_reset():
    global start_time, speed, timer_obstacles, final_score
    start_time = int(pygame.time.get_ticks() / 1000)
    panda_rect.x, panda_rect.y = 300, 200
    obstacle_rect_list.clear()
    cloud_list.clear()
    speed = 2
    timer_obstacles = 3000
    final_score = 0
    pygame.time.set_timer(obstacle_timer, timer_obstacles)

def cloud_movement(clouds):
    new_clouds = []
    for surf, rect in clouds:
        rect.y -= speed - 1
        if rect.y > -300:
            screen.blit(surf, rect)
            new_clouds.append((surf, rect))
    return new_clouds

def panda_movement():
    screen.blit(panda_surf, panda_rect)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        panda_rect.x = max(0, panda_rect.x - 5)
    if keys[pygame.K_RIGHT]:
        panda_rect.x = min(700 - panda_rect.width, panda_rect.x + 5)
    if keys[pygame.K_UP]:
        panda_rect.y = max(0, panda_rect.y - 3)
    if keys[pygame.K_DOWN]:
        panda_rect.y = min(800 - panda_rect.height, panda_rect.y + 3)

def obstacle_movement(obstacle_list):
    new_list = []
    for surf, rect in obstacle_list:
        if surf == obstacle_surf2:
            rect.y -= speed
            rect.x -= 2
        elif surf == obstacle_surf3:
            rect.y -= speed
            rect.x += 2
        else:
            rect.y -= speed

        if rect.y > -300 and -200 <= rect.x <= 900:
            screen.blit(surf, rect)
            new_list.append((surf, rect))
    return new_list

def collisions(player, obstacles):
    global final_score
    for surf, rect in obstacles:
        if surf == obstacle_surf:
            mask = obstacle_mask
        elif surf == obstacle_surf2:
            mask = obstacle_mask2
        elif surf == obstacle_surf3:
            mask = obstacle_mask3
        else:
            continue

        offset = (rect.x - panda_rect.x, rect.y - panda_rect.y)
        if panda_mask.overlap(mask, offset):
            final_score = int(pygame.time.get_ticks() / 1000) - start_time  # ✅ Store final score
            return "game_over"
    return "playing"

# Button instances
start_button = Button(350, 500, button1, 0.5)
exit_button = Button(350, 600, button2, 0.5)

# Main loop ------------------------------------------------------------------------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == obstacle_timer and game_state == "playing":
            elapsed_time = int(pygame.time.get_ticks() / 1000) - start_time

            num_obstacles = random.randint(1, 2)
            for _ in range(num_obstacles):
                rand_type = random.choice(["blue", "red_left", "red_right"])
                if rand_type == "blue":
                    obstacle_rect_list.append(
                        (obstacle_surf, obstacle_surf.get_rect(topleft=(randint(50, 650), 850)))
                    )
                elif rand_type == "red_left":
                    obstacle_rect_list.append(
                        (obstacle_surf2, obstacle_surf2.get_rect(topleft=(randint(750, 900), randint(850, 1000))))
                    )
                elif rand_type == "red_right":
                    obstacle_rect_list.append(
                        (obstacle_surf3, obstacle_surf3.get_rect(topleft=(randint(-200, -100), randint(850, 1000))))
                    )

        if event.type == cloud_timer and game_state == "playing":
            cloud_choice = random.choice([cloud1_surf, cloud2_surf, cloud3_surf])
            cloud_list.append((cloud_choice, cloud_choice.get_rect(topleft=(randint(-50, 650), randint(800, 1000)))))

    screen.fill("Black")

    if game_state == "home":
        screen.blit(homescreen_surf, (0, 0))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_state = "playing"
            game_reset()

    elif game_state == "playing":
        elapsed_time = int(pygame.time.get_ticks() / 1000) - start_time

        if elapsed_time > 160 and speed < 6:
            speed = 6
            timer_obstacles = 1000
            pygame.time.set_timer(obstacle_timer, timer_obstacles)
        elif elapsed_time > 120 and speed < 5:
            speed = 5
            timer_obstacles = 1200
            pygame.time.set_timer(obstacle_timer, timer_obstacles)
        elif elapsed_time > 80 and speed < 4:
            speed = 4
            timer_obstacles = 1500
            pygame.time.set_timer(obstacle_timer, timer_obstacles)
        elif elapsed_time > 40 and speed < 3:
            speed = 3
            timer_obstacles = 2000
            pygame.time.set_timer(obstacle_timer, timer_obstacles)

        screen.blit(screen_surf, (0, 0))

        cloud_list = cloud_movement(cloud_list)

        panda_movement()

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        display_score()

        game_state = collisions(panda_rect, obstacle_rect_list)

    elif game_state == "game_over":
        screen.blit(game_over_surf, game_over_rect)
        screen.blit(game_over_text, game_over_textRect)

        # ✅ Show stored final score below the "Game Over" text
        final_score_surf = font.render(f'Final Score: {final_score}', True, (255, 255, 255))
        final_score_rect = final_score_surf.get_rect(center=(350, game_over_textRect.bottom + 40))
        screen.blit(final_score_surf, final_score_rect)

        if start_button.draw(screen):
            game_state = "playing"
            game_reset()
        if exit_button.draw(screen):
            game_state = "home"
            game_reset()

    pygame.display.update()
    clock.tick(60)
