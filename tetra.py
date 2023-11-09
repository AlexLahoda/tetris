import pygame
import copy
from settings import glass_height, glass_width, grade
from images import *
import random


pygame.init()


class Tetra:
    """Describe tetra object"""
    structure = [[1, 1]]

    def __init__(self, pos):
        self.x, self.y = pos
        self.grade_x, self.grade_y = self.x//grade, self.y//grade
        self.structure = Tetra.structure
        self.move_left, self.move_right = False, False

    def move_x(self, glass_siev):
        """Make tetra x position move"""
        if self.move_right and self.get_obstacle_to_move('+', glass_siev):
            self.x += grade
        if self.move_left and self.get_obstacle_to_move('-', glass_siev):
            self.x -= grade
        self.grade_x = self.x//grade

    def move_y(self):
        """Make tetra y pos move"""
        self.y += 5
        self.grade_y = self.y//grade

    def get_obstacle_to_rotate(self, glass_siev):
        """Permission to rotate if there is no obstacles"""
        ttr = self.structure
        right_side = len(ttr)+self.grade_x - 1
        if right_side < len(glass_siev[0]) and (glass_siev[self.grade_y][right_side] == 0 if right_side+1 < len(glass_siev[0]) else True):
            return True
        return False

    def get_obstacle_to_move(self, side, glass_siev):
        """Permission to move if there is no obstacles"""
        ttr = self.structure
        ret = False
        right_side = self.grade_x + len(ttr[0])
        if side == '+' and right_side < len(glass_siev[0]):
            ret = True
            if right_side + 1 < len(glass_siev[0]):
                tmp = [0] * len(ttr)
                for i in range(len(ttr)):
                    for j in range(len(ttr[0])-1, -1, -1):
                        if ttr[i][j] == 1:
                            tmp[i] = (i, j)
                            break
                for i in tmp:
                    if not glass_siev[self.grade_y + i[0]][self.grade_x + i[1] + 1] == 0:
                        ret = False
                        break

        if side == '-' and self.grade_x > 0:
            ret = True
            if self.grade_x - 1 > 0:
                tmp = []
                for i in range(len(ttr)):
                    for j in range(len(ttr[0])):
                        if ttr[i][j] == 1:
                            tmp.append((i, j))
                            break
                for i in tmp:
                    if not glass_siev[self.grade_y + i[0]][self.grade_x + i[1] - 1] == 0:
                        ret = False
                        break
        return ret

    def rotate(self, glass_siev):
        """Rotate tetra"""
        ttr = self.structure
        if self.get_obstacle_to_rotate(glass_siev):
            tmp = [[0 for i in range(len(ttr))] for j in range(len(ttr[0]))]
            for i in range(len(ttr)):
                for j in range(len(ttr[i])):
                    tmp[j][len(ttr)-1-i] = ttr[i][j]
            ttr = copy.deepcopy(tmp)
            self.structure = ttr


def get_tetra():
    """Rendim return new tetra"""
    choice = random.choice(Tetra.__subclasses__())
    ret = choice((random.randint(0, glass_width -
                                 (len(choice.structure)+2)*grade), -grade))
    # choice = random.choice(('s', 'b', 'r', 'tr', 'z', 'tz', 't'))
    # match choice:
    #     case 's':
    #         ret = Stick((random.randint(0, glass_width -
    #                     (len(Stick.structure)+2)*grade), -grade))
    #     case 'b':
    #         ret = Block((random.randint(0, glass_width -
    #                     (len(Block.structure)+2)*grade), -grade))
    #     case 'r':
    #         ret = R((random.randint(0, glass_width -
    #                                 (len(R.structure)+2)*grade), -grade))
    #     case 'tr':
    #         ret = TR((random.randint(0, glass_width -
    #                                  (len(TR.structure)+2)*grade), -grade))
    #     case 'z':
    #         ret = Z((random.randint(0, glass_width -
    #                                 (len(Z.structure)+2)*grade), -grade))
    #     case 'tz':
    #         ret = TZ((random.randint(0, glass_width -
    #                                  (len(TZ.structure)+2)*grade), -grade))
    #     case 't':
    #         ret = T((random.randint(0, glass_width -
    #                                 (len(T.structure)+2)*grade), -grade))
    return ret


class Stick(Tetra):
    structure = [[1, 1, 1, 1]]

    def __init__(self, pos):
        super().__init__(pos)
        self.structure = Stick.structure
        self.image = s_img


class Block(Tetra):
    structure = [[1, 1], [1, 1]]

    def __init__(self, pos):
        super().__init__(pos)
        self.structure = Block.structure
        self.image = b_img

    def rotate(self, glass_siev):
        pass


class R(Tetra):
    structure = [[1, 0, 0], [1, 1, 1]]

    def __init__(self, pos):
        super().__init__(pos)
        self.structure = R.structure
        self.image = r_img


class TR(Tetra):
    structure = [[0, 0, 1], [1, 1, 1]]

    def __init__(self, pos):
        super().__init__(pos)
        self.structure = TR.structure
        self.image = tr_img


class Z(Tetra):
    structure = [[1, 1, 0], [0, 1, 1]]

    def __init__(self, pos):
        super().__init__(pos)
        self.structure = Z.structure
        self.image = z_img


class TZ(Tetra):
    structure = [[0, 1, 1], [1, 1, 0]]

    def __init__(self, pos):
        super().__init__(pos)
        self.structure = TZ.structure
        self.image = tz_img


class T(Tetra):
    structure = [[0, 1, 0], [1, 1, 1]]

    def __init__(self, pos):
        super().__init__(pos)
        self.structure = T.structure
        self.image = t_img
