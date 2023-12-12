import cv2
import sys
from threading import Thread
import time
import numpy as np


class Camera(Thread):
    """
    Represents a vidoe device connected to a computer. 
    Spawns a new thread for reach camera stream and outputs numpy array 

    """
    def __init__(self, width:int, height:int, source:int ) -> None:
        super(Camera, self).__init__()
        self.daemon = True
        self.capture = cv2.VideoCapture(source)

        self.wdth = width
        self.height = height

        self.is_running = True
        self.grabbed = False
        self.frames = np.array(0)
        # TODO test to see if this works to set resloution of vido
        # self.frames.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        # self.frames.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


    def run(self):
        #TODO - implement run method
        self.get_frames()


    def get_frames(self):
        # print(self.capure.isOpened())
        try:
            while self.capture.isOpened():
                if self.is_running:
                    (self.grabbed, self.frames) = self.capture.read()
                    print(self.grabbed)
                    print(f"{self.name}: ", self.frames)

        except KeyboardInterrupt as ex:
            print("exit")
            self.capture.release()


    def view(self):
        print(self.grabbed)
        try:
            if not self.grabbed:
                sys.exit(f"Vide capture unable to be grabbed on Thread {self.name}")

            cv2.imshow(f"{self.name}", self.frames) 
            if cv2.waitKey(1) == ord('q'):
                sys.exit("exiting")
        except KeyboardInterrupt as ex:
            print("exit")


if __name__ == "__main__":
    #create a list of cameras
    camers = [Camera(480, 620, 0), Camera(480, 620, 2)]
    # start each camera in lisr
    for cam in camers:
        cam.start()
    
    camers[0].get_frames()


    # cam = Camera(480, 620, 0)
    # cam.start()
    # cam.is_running = True
    # print(cam.name)
    # print(cam.get_frames())

    # cam_1 = Camera(480, 620, 2)
    # cam.start()
    # cam_1.is_running = True
    # print(cam_1.name)
    # print(cam_1.get_frames())
    