import pygame
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

pygame.init()

screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])

def load_music(music_path):
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play()

class Key:
    pass

class Note:
    pass

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(WHITE)
    pygame.display.flip()

pygame.quit()