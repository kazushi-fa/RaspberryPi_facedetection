#!/usr/bin/env python
# -*- coding: utf-8 -*-

from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2, time

# �t���[���T�C�Y
FRAME_W = 320
FRAME_H = 192

# ���ʂ̊猟�o�p
cascPath = 'lbpcascade_frontalface.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

camera = PiCamera()
camera.resolution = (FRAME_W, FRAME_H)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(FRAME_W, FRAME_H))
time.sleep(0.1)

fourcc = cv2.cv.CV_FOURCC(*'DIVX')
out = cv2.VideoWriter('output.avi', fourcc, camera.framerate/10, (540,300))

for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    frame = image.array
    # frame = cv2.flip(frame, -1) # �㉺���]����ꍇ

    # Convert to greyscale for detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist( gray )

    # �猟�o
    faces = faceCascade.detectMultiScale(gray, 1.1, 3, 0, (10, 10))

    # ���o������ɘg������
    for (x, y, w, h) in faces:
        # �������������`�ň͂�
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    frame = cv2.resize(frame, (540,300))
    out.write(frame)
    
    # �r�f�I�ɕ\�� 
    cv2.imshow('Video', frame)
    
    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if key == ord("q"):
        break
out.release()
cv2.destroyAllWindows()