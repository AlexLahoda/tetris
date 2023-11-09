import pygame

pygame.init()
pygame.mixer.music.load("audio/back_music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.25)
s_clear = pygame.mixer.Sound('audio/stage_clear.mp3')
s_over = pygame.mixer.Sound("audio/game_over.mp3")
s_clear.set_volume(0.1)
s_over.set_volume(0.1)
