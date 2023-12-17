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
        #self.capture = cv2.VideoCapture(source)

        self.wdth = width
        self.height = height
        self.is_running = False
        # self.grabbed = False
 

        # TODO test to see if this works to set resloution of vido
        # self.frames.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        # self.frames.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


    def run(self):
        #TODO - implement run method
        self.get_frames()


    def get_devices(self):
        # TODO - list all the camer deviecs and return list of avlaible devices
        index = 0
        cameras = []
        try:
            while True:
                print("INDEX ", index)
                cam = cv2.VideoCapture(f"/dev/video{index}")
                print("IS OPENED ", cam.isOpened())
                if cam.isOpened():
                    check, _ = cam.read()
                    print("CHECK " , check)
                    if check:
                        cameras.append(cam)
                        print(f"Cmaera found on /dev/video{index}")
                        index += 2
                else:
                    return cameras    
        except Exception as e:
            print(e)
            

    def get_frames(self):
        # print(self.capure.isOpened())
        try:
            while self.capture.isOpened():
                if self.is_running:
                    (grabbed, frames) = self.capture.read()
                    print(frames)
                    # print(self.grabbed)
                    # print(f"{self.name}: ", self.frames)
                    np.append(self.frames, frames)
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
            self.capture.release()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    #create a list of cameras
    #camers = [Camera(480, 620, 0), Camera(480, 620, 2)]
    # start each camera in lisr
    cam = Camera(480, 620, 0)
    x = cam.get_devices()
    print(x)
    
    

