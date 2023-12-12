import cv2
import os, sys
from threading import Thread


class Camera(Thread):
    """
    Represents a camera connected to a computer 
    capable of spawing a new thread for each
    """
    def __init__(self, width:int, height:int, source:int) -> None:
        super(Camera, self).__init__()
        self.daemon = True
        self.start()
        self.wdth = width
        self.height = height
        self.capture = cv2.VideoCapture(source)
        self.is_running = True

        # TODO test to see if this works to set resloution of vido
        # self.frames.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        # self.frames.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    def __exit__(self):
        self.capture.release()



    def get_frames(self):
        try:
            while self.capture.isOpened():
                if self.is_running:
                    (self.grabbed, self.frames) = self.capture.read()
                    print(self.frames)
        except KeyboardInterrupt as ex:
            print("exit")



    def getStrema():
        pass



if __name__ == "__main__":
    cam = Camera(480, 620, 0)
    cam.is_running = True
    print(cam.name)
    print(cam.get_frames())
    