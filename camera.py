import cv2
import os, sys
from threading import Thread

class Camera(Thread):
    """
    Represents a camera connected to a computer 
    capable of spawing a new thread for each
    """
    def __init__(self, width:int, height:int, source:str) -> None:
        super(Camera, self).__init__()
        self.daemon = True
        self.wdth = width
        self.height = height
        (self.grabbed, self.frames) = cv2.VideoCapture(source)
        self.is_running = False

        # TODO test to see if this works to set resloution of vido
        # self.frames.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        # self.frames.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


    def start():
        pass


    def getStrema():
        pass



if __name__ == "__main__":
    cam = Camera()
    