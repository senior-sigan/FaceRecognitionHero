# -*- coding: utf-8 -*-
from random import choice

import pygame
from pygame import Surface, Color, image, Rect
from pygame.locals import *
from pygame.sprite import Sprite

WIN_WIDTH = 800
WIN_HEIGHT = 640
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#004400"


class Face(Sprite):
    def __init__(self, x, y, name):
        Sprite.__init__(self)
        width, height = 512, 512
        self.name = name
        self.image = image.load("assets/faces/{}.png".format(name))
        self.rect = Rect(x - width // 2, y - height // 2, width, height)


class Answer(Sprite):
    def __init__(self, x, y, name):
        Sprite.__init__(self)
        width, height = 512, 512
        self.name = name
        self.image = image.load("assets/{}.png".format(name))
        self.rect = Rect(x - width // 2, y - height // 2, width, height)


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

    timer = pygame.time.Clock()
    time = 0

    def next_face():
        entities.empty()
        entities.add(choice(faces))

    def answer():
        entities.empty()
        entities.add(choice(answers))

    time = 0
    changed = False
    while True:
        delta = timer.tick(60)
        time += delta
        if 2000 < time < 3000 and not changed:
            answer()
            changed = True
        elif time > 3000:
            next_face()
            time = 0
            changed = False

        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit("QUIT")

        screen.blit(bg, (0, 0))
        entities.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
