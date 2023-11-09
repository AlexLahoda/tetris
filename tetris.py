import pygame
import sys
import random
import pickle
import copy
import audio
from settings import *
from images import point_img
from tetra import Tetra, get_tetra
from button import print_txt, Button


pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()


class Game:
    def __init__(self, score, glass_siev, speed):
        self.score = score
        self.speed = speed
        self.glass_siev = copy.deepcopy(glass_siev)

    def start_new(self):
        """Restart game"""
        self.speed = 20
        self.score = 0
        self.glass_siev = copy.deepcopy(glass_siev)

    @staticmethod
    def save_res(records, score):
        if not len(records):
            records.append(score)
        elif len(records) and len(records) <= 10:
            for i in range(len(records)):
                if score > records[i]:
                    records.insert(i, score)
        else:
            for i in records:
                if score > i:
                    i = score
        with open("records.pickle", 'wb') as f:
            pickle.dump(records, f)

    def start(self):
        """Starts game"""
        clock = pygame.time.Clock()
        tetras = [get_tetra(), get_tetra()]
        tetra = tetras[1]
        n_filled = True
        start_r = 0
        start_l = 0
        try:
            with open("records.pickle", 'rb') as f:
                records = pickle.load(f)
        except:
            records = []
        while n_filled:
            if len(tetras) < 2:
                tetras.insert(0, get_tetra())
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Game.save_res(records, self.score)
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        start_l = pygame.time.get_ticks()
                        tetra.move_left = True
                        tetra.move_x(self.glass_siev)
                    if event.key == pygame.K_RIGHT:
                        start_r = pygame.time.get_ticks()
                        tetra.move_right = True
                        tetra.move_x(self.glass_siev)
                    if event.key == pygame.K_SPACE:
                        tetra.rotate(self.glass_siev)
                    if event.key == pygame.K_DOWN:
                        self.speed *= 4
                    if event.key == pygame.K_ESCAPE:
                        pygame.time.wait(10000)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        tetra.move_left = False
                        start_l = 0
                    if event.key == pygame.K_RIGHT:
                        tetra.move_right = False
                        start_r = 0
                    if event.key == pygame.K_DOWN:
                        self.speed /= 4
            screen.blit(back_img, (0, 0))
            screen.blit(glass, glass_pos)
            glass.fill((0, 0, 0))

            if start_r and pygame.time.get_ticks() - start_r > 100:
                tetra.move_right = True
                tetra.move_x(self.glass_siev)
            if start_l and pygame.time.get_ticks() - start_l > 100:
                tetra.move_left = True
                tetra.move_x(self.glass_siev)
            clock.tick(self.speed)
            # Logic of clearing stage
            tmp = []
            for i in range(len(self.glass_siev)):
                if not 0 in self.glass_siev[i]:
                    tmp.append(i)
            if len(tmp):
                self.score += len(tmp)**2
                audio.s_clear.play()
            for i in tmp:
                for j in range(i, 0, -1):
                    self.glass_siev[j] = copy.deepcopy(self.glass_siev[j-1])
                    print(j)
                self.glass_siev[0] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

            # Filling glass with blocks
            for i in range(len(self.glass_siev)):
                for j in range(len(self.glass_siev[i])):
                    if self.glass_siev[i][j]:
                        glass.blit(point_img, (j*grade, i*grade))

            # Logic of moving, landing and creating new tetra
            ttr = tetra.structure
            tmp = []
            for i in range(len(ttr)-1, -1, -1):
                for j in range(len(ttr[i])):
                    pos_x = j+tetra.grade_x
                    pos_y = i+tetra.grade_y
                    if ttr[i][j]:
                        if pos_y >= len(self.glass_siev) - 1 or self.glass_siev[pos_y+1][pos_x]:
                            for k in range(len(ttr)):
                                for n in range(len(ttr[k])):
                                    if ttr[k][n]:
                                        pos_x = n+tetra.grade_x
                                        pos_y = k+tetra.grade_y
                                        tmp.append((pos_y, pos_x))
                                        glass.blit(
                                            point_img, ((pos_x)*grade, (pos_y)*grade))
                            tetras.pop()
                            tetra = None
                            break
                        glass.blit(point_img, ((pos_x)*grade, (pos_y)*grade))
                if tetra == None:
                    tetra = tetras[0]
                    break

            # Fill in glas with landed tetra structure or finish the game
            for i in tmp:
                if i[0] < 0:
                    n_filled = False
                    audio.s_over.play()
                self.glass_siev[i[0]][i[1]] = 1

            # Move tetra down
            tetra.move_y()

            # Show everything in left side
            print_txt(f"Score: {self.score}", (0, 0, 255), (50, 200))
            screen.blit(tetras[0].image, (100, 50))
            print_txt("Records:", (0, 0, 255), (50, 300))
            for i in range(len(records)):
                print_txt(f"{records[i]}", (0, 0, 255), (50, 330+i*30))
            start_new = Button.new(200, 50, "Start new")
            start_new.draw((50, 700), self.start_new)
            self.speed *= 1.00000001
            pygame.display.update()

        Game.save_res(records, self.score)

        game_over_text = game_font.render(f"Game over", True, 'red')
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (screen_width/2, screen_height/2)
        screen.blit(game_over_text, game_over_rect)
        pygame.display.update()
        pygame.time.wait(5000)


game = Game(score, glass_siev, speed)
game.start()
