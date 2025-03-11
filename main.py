import pygame
import random
from sys import exit

def display_score():
    current_time = int(pygame.time.get_ticks() /1000 ) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (30, 30, 30))
    score_rect = score_surf.get_rect(center=(100, 50))
    screen.blit(score_surf, score_rect)

pygame.init() 
screen = pygame.display.set_mode((700, 800))
clock = pygame.time.Clock()
pygame.display.set_caption('SkyDivers')
game_active = True
test_font = pygame.font.Font('freesansbold.ttf', 40)

# Game states
game_state = "home"  # "home", "playing", "game_over"
start_time = 0

#cloud1
cloud1_surf = pygame.image.load('Files/Cloud1.png').convert_alpha()
cloud1_rect = cloud1_surf.get_rect(midbottom = (120, 200))
cloud1_rect.x = 300
cloud1_rect.y = 200
#cloud2
cloud2_surf = pygame.image.load('Files/cloud2.png').convert_alpha()
cloud2_rect = cloud1_surf.get_rect(midbottom = (120, 200))
cloud2_rect.x = 400
cloud2_rect.y = 300
#cloud3
cloud2_surf = pygame.image.load('Files/cloud3.png').convert_alpha()
cloud2_rect = cloud1_surf.get_rect(midbottom = (120, 200))
cloud2_rect.x = 200
cloud2_rect.y = 100

#panda player
panda_surf = pygame.image.load('Files/panda.png').convert_alpha()
panda_surf = pygame.transform.scale(panda_surf, (120,200))
panda_rect = panda_surf.get_rect(midbottom = (120, 200))
panda_rect.x = 300
panda_rect.y = 200

#obstacles
obstacle_surf = pygame.Surface((25,25))
obstacle_surf.fill('Blue')
obstacle_rect = obstacle_surf.get_rect(midbottom = (25,25))
obstacle_rect.x = 400
obstacle_rect.y = 400

#background 
screen_surf = pygame.Surface((700,800))
screen_surf = pygame.image.load('Files/screen.png').convert()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_state == "home":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = "playing"
                start_time = int(pygame.time.get_ticks() / 1000)

        elif game_state == "game_over":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = "playing"
                start_time = int(pygame.time.get_ticks() / 1000)
                panda_rect.x, panda_rect.y = 300, 200
                obstacle_rect.x, obstacle_rect.y = random.randint(0, 700 - 25), 800

    screen.fill("Black")  # Clear screen for each state

    if game_state == "home":
        # Home Screen
        homescreen_surf = pygame.Surface((700,800))
        homescreen_surf = pygame.image.load('Files/homescreen.PNG').convert()
        screen.blit(homescreen_surf, (0,0))
    

    elif game_state == "playing": 
        # Rendering
        screen.blit(screen_surf, (0, 0))
        display_score()

        #cloud movement
        cloud1_rect.y -= 2
        if cloud1_rect.y < -250:
            cloud1_rect.y = 850
            cloud1_rect.x = random.randint(0, 700)  
        screen.blit(cloud1_surf, cloud1_rect)
        cloud2_rect.y -= 2    
        if cloud2_rect.y < -250:
            cloud2_rect.y = 850
            cloud2_rect.x = random.randint(0, 600)
        screen.blit(cloud2_surf, cloud2_rect)
        cloud2_rect.y -= 2
        if cloud2_rect.y < -250:
            cloud2_rect.y = 850
            cloud2_rect.x = random.randint(0, 500)
        screen.blit(cloud2_surf, cloud2_rect)
        
        screen.blit(panda_surf, panda_rect)

        # Player Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            panda_rect.x -= 5
        if keys[pygame.K_RIGHT]:
            panda_rect.x += 5

       

        # Obstacle Movement
        obstacle_rect.y -= 2
        if obstacle_rect.y < -50:
            obstacle_rect.y = 850
            obstacle_rect.x = random.randint(0, 700 - 25)  # Prevent spawning out of bounds
        screen.blit(obstacle_surf, obstacle_rect)

        # Collision Detection
        if panda_rect.colliderect(obstacle_rect):
            game_state = "game_over"
            print("Game Over")

    elif game_state == "game_over":
        # Game Over Screen
        game_over_surf = test_font.render("Game Over!", True, (255, 0, 0))
        game_over_rect = game_over_surf.get_rect(center=(350, 250))
        restart_surf = test_font.render("Press SPACE to Restart", True, (255, 255, 255))
        restart_rect = restart_surf.get_rect(center=(350, 350))
        screen.blit(game_over_surf, game_over_rect)
        screen.blit(restart_surf, restart_rect)

    pygame.display.update()
    clock.tick(60)  # Keep frame rate at 60 FPS