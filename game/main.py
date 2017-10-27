# -*- coding: utf-8 -*-
from random import choice

import pygame
from pygame import Surface, Color, image
from pygame.locals import *
from pygame.sprite import Sprite

WIN_WIDTH = 800
WIN_HEIGHT = 640
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#004400"
FPS = 60

SHOW_TIME = 2000
ANSWER_TIME = 1000


class Face(Sprite):
    def __init__(self, x, y, name):
        Sprite.__init__(self)
        width, height = 512, 512
        self.name = name
        self.image = image.load("assets/faces/{}.png".format(name))
        self.rect = Rect(x - width // 2, y - height // 2, width, height)


class Answer(Sprite):
    def __init__(self, x, y, name, width=512, height=512):
        Sprite.__init__(self)
        self.name = name
        img = image.load("assets/{}.png".format(self.name))
        self.image = pygame.transform.scale(img, (width, height))
        self.rect = Rect(x - width // 2, y - height // 2, width, height)


class EmptyAnswer(Sprite):
    def __init__(self, x, y, w=48, h=48):
        Sprite.__init__(self)
        color = "#003300"
        self.image = Surface((w, h))
        self.image.fill(Color(color))
        self.rect = Rect(x, y, w, h)


def main():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Troll Faces")
    bg = Surface(DISPLAY)
    bg.fill(Color(BACKGROUND_COLOR))

    x, y = WIN_WIDTH // 2, WIN_HEIGHT // 2
    faces = (Face(x, y, "angry"),
             Face(x, y, "neutral"),
             Face(x, y, "sad"),
             Face(x, y, "smile"),
             Face(x, y, "surprise"))

    answers = (Answer(x, y, "correct"), Answer(x, y, "wrong"))

    entities = pygame.sprite.Group()
    entities.add(choice(faces))

    answers_background = pygame.sprite.Group()
    answers_history = pygame.sprite.Group()
    n = 10
    answer_size = 64

    for i in range(n):
        answers_background.add(EmptyAnswer((WIN_WIDTH - n * answer_size) // 2 + i * answer_size, 12, 48, 48))

    def next_face():
        entities.empty()
        entities.add(choice(faces))

    def answer():
        entities.empty()
        a = choice(answers)
        offset = (WIN_WIDTH - n * answer_size - 64 - 18) // 2
        j = len(answers_history) + 1
        answers_history.add(Answer(offset + j * answer_size, 36, a.name, 48, 48))
        entities.add(a)

    time = 0
    changed = False
    timer = pygame.time.Clock()
    while True:
        delta = timer.tick(FPS)
        time += delta
        if ANSWER_TIME < time <= SHOW_TIME and not changed:
            answer()
            changed = True
        elif time > SHOW_TIME:
            next_face()
            time = 0
            changed = False

        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit("QUIT")

        screen.blit(bg, (0, 0))
        entities.draw(screen)
        answers_background.draw(screen)
        answers_history.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
