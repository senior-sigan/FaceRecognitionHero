# -*- coding: utf-8 -*-


import cv2
import numpy as np
import pygame
from pygame import Surface, Color, image
from pygame.locals import *
from pygame.sprite import Sprite

camera = cv2.VideoCapture(0)

WIN_WIDTH = 800
WIN_HEIGHT = 720
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#FFFFFF"
FPS = 30

SHOW_TIME = 3000
ANSWER_TIME = 1000

MINI_FACE = 72


class Face(Sprite):
    def __init__(self, x, y, name, path, width=512, height=512):
        Sprite.__init__(self)
        self.name = name
        img = image.load("assets/faces/{}".format(path))
        self.image = pygame.transform.scale(img, (width, height))
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


def freq_count(arr):
    offset = len(arr) // 3
    arr = arr[offset:]  # skip first elements because nobody will be able to detect it
    uniq, counts = np.unique(arr, return_counts=True)
    i = np.argmax(counts)
    return uniq[i]


def choicer():
    from random import choice
    prev_choices = {}

    def smart_choice(arr):
        if len(prev_choices) == len(arr):
            prev_choices.clear()
        to_choice = [el for el in arr if prev_choices.get(el) is None]
        el = choice(to_choice)
        prev_choices[el] = True
        return el

    return smart_choice


def main():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Troll Faces")
    bg = Surface(DISPLAY)
    bg.fill(Color(BACKGROUND_COLOR))

    from random_face_classification import FaceClassification
    # from face_classification import FaceClassification
    fc = FaceClassification()

    x, y = WIN_WIDTH // 2, WIN_HEIGHT // 2
    faces = (Face(x, y, "angry", "angry.png"),
             Face(x, y, "neutral", "neutral.png"),
             Face(x, y, "sad", "sad.png"),
             Face(x, y, "happy", "happy.png"),
             Face(x, y, "fear", "fear.png"),
             Face(x, y, "surprise", "surprise.png"),

             Face(x, y, "angry", "angry1.png"),
             Face(x, y, "neutral", "neutral1.jpg"),
             Face(x, y, "sad", "sad1.jpg"),
             Face(x, y, "happy", "happy1.png"),
             Face(x, y, "fear", "fear1.png"),
             Face(x, y, "surprise", "surprise1.jpg"),

             Face(x, y, "angry", "angry2.jpg"),
             Face(x, y, "neutral", "neutral2.png"),
             Face(x, y, "sad", "sad2.png"),
             Face(x, y, "happy", "happy2.jpg"),
             Face(x, y, "fear", "fear2.png"),
             Face(x, y, "surprise", "surprise2.jpg")
             )
    face_choicer = choicer()

    small_faces = {
        "angry": Face(x, y, "angry", "angry.png", MINI_FACE, MINI_FACE),
        "neutral": Face(x, y, "neutral", "neutral.png", MINI_FACE, MINI_FACE),
        "sad": Face(x, y, "sad", "sad.png", MINI_FACE, MINI_FACE),
        "happy": Face(x, y, "happy", "happy.png", MINI_FACE, MINI_FACE),
        "fear": Face(x, y, "fear", "fear.png", MINI_FACE, MINI_FACE),
        "surprise": Face(x, y, "surprise", "surprise.png", MINI_FACE, MINI_FACE)
    }

    answers = {True: Answer(x, y, "correct"), False: Answer(x, y, "wrong")}

    current_face = None
    faces_classified = []

    entities = pygame.sprite.Group()

    answers_background = pygame.sprite.Group()
    answers_history = pygame.sprite.Group()
    n = 10
    answer_size = 64

    for i in range(n):
        answers_background.add(EmptyAnswer((WIN_WIDTH - n * answer_size) // 2 + i * answer_size, 12, 48, 48))

    def next_face():
        nonlocal current_face
        current_face = face_choicer(faces)
        print("Should show: {}".format(current_face.name))
        entities.empty()
        entities.add(current_face)

    def answer():
        nonlocal faces_classified
        main_face = freq_count(faces_classified)
        print(faces_classified)
        print("{} == {}".format(main_face, current_face.name))
        a = answers[main_face == current_face.name]

        faces_classified = []
        entities.empty()

        offset = (WIN_WIDTH - n * answer_size - 64 - 18) // 2
        if len(answers_history) >= n:
            answers_history.empty()
        j = len(answers_history) + 1
        answers_history.add(Answer(offset + j * answer_size, 36, a.name, 48, 48))
        entities.add(a)

    next_face()

    time = 0
    changed = False
    timer = pygame.time.Clock()
    while True:
        delta = timer.tick(FPS)
        time += delta
        if SHOW_TIME < time <= SHOW_TIME + ANSWER_TIME and not changed:
            answer()
            changed = True
        elif time > SHOW_TIME + ANSWER_TIME:
            next_face()
            time = 0
            changed = False

        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit("QUIT")

        ret, frame = camera.read()
        res = fc.recognise(frame)
        faces_classified.append(res)
        frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)

        screen.blit(bg, (0, 0))
        screen.blit(frame, (0, WIN_HEIGHT - 180))
        screen.blit(small_faces[res].image, (0, 0))
        entities.draw(screen)
        answers_background.draw(screen)
        answers_history.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
