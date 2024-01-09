import cv2 as cv
import os, sys
from threading import Thread
import threading
from multiprocessing import Process, Queue

import numpy as np
import pytesseract as ocr

from camera import Camera
# from queue import Queue

# TODO get camera devices in list
# TODO read in camera data
# TODO run OCR on vidoe frames
# TODO optmise -> https://stackoverflow.com/questions/55494331/recording-video-with-opencv-python-multithreading

cap = cv.VideoCapture("/dev/video0")

frame_queue = Queue()

def main():
    count = 0
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    try:
        print("Reading Frames")
        while cap.isOpened():
            count += 1
            ret, frames = cap.read()    
            # TODO - process this on seprate thread
            #gray scaling the image made the OCR a bit more accurate
            frames = cv.cvtColor(frames, cv.COLOR_BGR2GRAY)
            if (count % 2 == 0):
                frame_queue.put(frames)
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            cv.imshow('frame', frames)
            if cv.waitKey(1) == ord('q'):
                break
    except KeyboardInterrupt:
        print("\nProgramed exit\n")
        cap.release()
        cv.destroyAllWindows()
    

def read_text(data, q):
    while True:
        text = ocr.image_to_string(data.get(), lang="eng")
        q.put(text)


if __name__ == "__main__":

    print(os.getpid())
    print(threading.active_count())
    #list devices on cimputer
    print(Camera.list_devices())
    ct = Camera(600, 620, "/dev/video0").start()
    print(threading.active_count())

    #start the thread
    
    # p = Process()
    try:
        while True:
            cool = ct.read()
            print(cool)
    except KeyboardInterrupt:
        print("stop")




    # text_queue = Queue()
    # cam = Camera(480, 620, "/dev/video0").start()
    # t2 = Process(target=read_text, args=(frame_queue, text_queue)).start()
    # 
# 
    # while True:
        # _, frames = cam.read()
        # frame_queue.put(frames)
        # print(text_queue.get())
    # 
    # t2.join()
    
