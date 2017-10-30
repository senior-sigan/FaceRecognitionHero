# -*- coding: utf-8 -*-

from statistics import mode

import cv2
import numpy as np
from keras.models import load_model

from utils.datasets import get_labels
from utils.inference import apply_offsets
from utils.inference import detect_faces
from utils.inference import load_detection_model
from utils.preprocessor import preprocess_input


class FaceClassification:
    def __init__(self) -> None:
        # parameters for loading data and images
        detection_model_path = '../trained_models/detection_models/haarcascade_frontalface_default.xml'
        emotion_model_path = '../trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5'
        self.emotion_labels = get_labels('fer2013')
        print(self.emotion_labels)

        # hyper-parameters for bounding boxes shape
        self.frame_window = 10
        self.emotion_offsets = (20, 40)

        # loading models
        print("Loading model")
        self.face_detection = load_detection_model(detection_model_path)
        self.emotion_classifier = load_model(emotion_model_path, compile=False)

        # getting input model shapes for inference
        self.emotion_target_size = self.emotion_classifier.input_shape[1:3]

        # starting lists for calculating modes
        self.emotion_window = []

        self.emotions = {'angry': 'angry', 'disgust': 'sad', 'fear': 'fear', 'happy': 'happy', 'sad': 'sad',
                         'surprise': 'surprise', 'neutral': 'neutral'}

    def recognise(self, bgr_image):
        gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        faces = detect_faces(self.face_detection, gray_image)

        for face_coordinates in faces:
            x1, x2, y1, y2 = apply_offsets(face_coordinates, self.emotion_offsets)
            gray_face = gray_image[y1:y2, x1:x2]
            try:
                gray_face = cv2.resize(gray_face, tuple(self.emotion_target_size))
            except:
                continue

            gray_face = preprocess_input(gray_face, True)
            gray_face = np.expand_dims(gray_face, 0)
            gray_face = np.expand_dims(gray_face, -1)
            emotion_prediction = self.emotion_classifier.predict(gray_face)
            emotion_probability = np.max(emotion_prediction)
            emotion_label_arg = np.argmax(emotion_prediction)
            emotion_text = self.emotion_labels[emotion_label_arg]
            self.emotion_window.append(emotion_text)

            if len(self.emotion_window) > self.frame_window:
                self.emotion_window.pop(0)
            try:
                emotion_mode = mode(self.emotion_window)
            except:
                continue

            return self.emotions.get(emotion_text, 'neutral')

        return "empty"  # in other cases
