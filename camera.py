import cv2
import os, sys
from threading import Thread

class Camera():
    """
    Represents a camera connected to a computer 
    capable of spawing a new thread for each
    """
    def __init__(self, width:int, height:int, source:str) -> None:
        self.wdth = width
        self.height = height
        (self.grabbed, self.frames) = cv2.VideoCapture(source)
        self.is_running = False


    def start():
        pass


    def getStrema():
        pass



if __name__ == "__main__":
    pass