import pygame

pygame.init()

point_img = pygame.image.load("images/point.png")
back_img = pygame.image.load("images/tetris_backgraund.png")
s_img = pygame.image.load("images/stick.png")
b_img = pygame.image.load("images/block.png")
r_img = pygame.image.load("images/r.png")
r_img.set_colorkey((255, 255, 255))
tr_img = pygame.image.load("images/turned_r.png")
tr_img.set_colorkey((255, 255, 255))
z_img = pygame.image.load("images/z.png")
z_img.set_colorkey((255, 255, 255))
tz_img = pygame.image.load("images/turned_z.png")
tz_img.set_colorkey((255, 255, 255))
t_img = pygame.image.load("images/triangle.png")
t_img.set_colorkey((255, 255, 255))
