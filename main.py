import pygame
from sys import exit

pygame.init() 
screen = pygame.display.set_mode((700, 800))
clock = pygame.time.Clock()
pygame.display.set_caption('SkyDivers')
game_active = True


shape_surf = pygame.Surface((50,100))
shape_surf.fill('Red')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit
    
    screen.blit(shape_surf,(325,300))


    pygame.display.update()
    clock.tick(60)

