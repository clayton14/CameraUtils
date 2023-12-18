import cv2
import sys
from threading import Thread
import threading
from typing import List
import numpy as np
import numpy.typing as npt

class CameraThread:
    """
    Represents a vidoe device connected to a computer.
    Spawns a new thread for reach camera stream and outputs numpy array
    """

    def __init__(self, width: int, height: int, source: str) -> None:
        self.width = width
        self.height = height
        self.read_lock = threading.Lock()
        self.capture = cv2.VideoCapture(source)
        self.grabbed, self.frames = self.capture.read()
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.is_running = False
        

    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()

    def start(self) -> object:
        # TODO - implement run method
        if self.is_running:
            print("Capture is already started")
            return None
        self.is_running = True
        self.thread = Thread(target=self.update, args=(), daemon=True)
        # Thread(target=self.view, args=(), daemon=True)
        self.thread.start()
        return self

    def update(self) -> None:
        # print(self.capure.isOpened())
        try:
            while self.is_running:
                grabbed, frames = self.capture.read()
                with self.read_lock:
                    self.grabbed = grabbed
                    self.frames = frames
        except KeyboardInterrupt as ex:
            print("exit")
            self.capture.release()

    def get_devices(self) -> List[object]:
        # retruns a list of CV2 capture devices
        # TODO - list all the camer deviecs and return list of avlaible devices
        index = 0
        cameras = []
        try:
            while True:
                # print("INDE   X ", index)
                cam = cv2.VideoCapture(f"/dev/video{index}")
                # print("IS OPENED ", cam.isOpened())
                if cam.isOpened():
                    check, _ = cam.read()
                    # print("CHECK " , check)
                    if check:
                        cameras.append(cam)
                        print(f"Cmaera found on /dev/video{index}")
                        index += 2
                else:
                    return cameras
        except Exception as e:
            print(e)

    def set_device(self, source: str):
        self.cv2.VideoCapture(source)

    def read(self) -> bool | npt.NDArray:
        with self.read_lock:
            frame = self.frames.copy()
            grabbed = self.grabbed
        return grabbed, frame

    def stop(self):
        self.is_running = False
        self.thread.join()

    def view(self, frame):
        # print(self.grabbed)
        try:
            cv2.imshow(f" {self.thread.name} ", frame)
            if cv2.waitKey(1) == ord("q"):
                # self.thread.join()
                self.capture.release()
                sys.exit("exiting")
        except KeyboardInterrupt as ex:
            print("exit")
            self.capture.release()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    cam = CameraThread(1000, 1000, "/dev/video0")
    
    cam.start()
    cam2 = CameraThread(480, 620, "/dev/video2")
    cam2.start()
    cam3 = CameraThread(480, 620, "/dev/video4")
    cam3.start()

    while True:
        # _ , frames1 = cam.read()
        # print(f"Frames on {cam.thread.name}:  {frames1}")
        # _ , frames2 = cam.read()

        # print(f"Frames on {cam2.thread.name}:  {frames2}")
        # _ , frames3 = cam.read()

        # print(f"Frames on {cam3.thread.name}:  {frames3}")


        _, frames = cam.read()
        cam.view(frame=frames)
# 
        _, frames2 = cam2.read()
        cam2.view(frame=frames2)
# 
        _, frames3 = cam3.read()
        cam3.view(frame=frames3)