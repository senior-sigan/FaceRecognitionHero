# -*- coding: utf-8 -*-

from random import choice


class FaceClassification:
    def __init__(self) -> None:
        self.labels = ('angry', 'fear', 'happy', 'sad', 'surprise', 'neutral')

    def recognise(self, bgr_image):
        return choice(list(self.labels))
