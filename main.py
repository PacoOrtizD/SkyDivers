import pygame
import random
from sys import exit

def display_score():
    current_time = int(pygame.time.get_ticks() /1000 ) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64,  64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)

pygame.init() 
screen = pygame.display.set_mode((700, 800))
clock = pygame.time.Clock()
pygame.display.set_caption('SkyDivers')
game_active = True
test_font = pygame.font.Font('freesansbold.ttf', 40)
start_time = 0


#panda
panda_surf = pygame.Surface((50,100))
panda_surf.fill('Red')
panda_rect = panda_surf.get_rect(midbottom = (50, 100))
panda_rect.x = 300
panda_rect.y = 300

obstacle_surf = pygame.Surface((25,25))
obstacle_surf.fill('Blue')
obstacle_rect = obstacle_surf.get_rect(midbottom = (25,25))
obstacle_rect.x = 400
obstacle_rect.y = 400

#background 
screen_surf = pygame.Surface((700,800))
screen_surf.fill('Black')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()  

        if not game_active:  # Restart game when Space is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
                panda_rect.x = 300
                panda_rect.y = 300
                obstacle_rect.x = random.randint(0, 700)
                obstacle_rect.y = 800  # Reset obstacle

    if game_active:
        # Player Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            panda_rect.x -= 5  
        if keys[pygame.K_RIGHT]:
            panda_rect.x += 5

        # Rendering
        screen.blit(screen_surf, (0, 0))
        screen.blit(panda_surf, panda_rect)
        display_score()

        # Obstacle Movement
        obstacle_rect.y -= 2
        if obstacle_rect.y < -50:
            obstacle_rect.y = 850
            obstacle_rect.x = random.randint(0, 700)
        screen.blit(obstacle_surf, obstacle_rect)

        # Collision Detection
        if panda_rect.colliderect(obstacle_rect):
            game_active = False
            print('Game Over')  

    else:
        screen.fill('Blue')

    pygame.display.update()
    clock.tick(60)  # Keep frame rate at 60 FPS