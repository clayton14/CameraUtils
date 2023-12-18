import sys
import glob
from threading import Thread
import threading
from typing import List
import pytesseract
import cv2
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


    @staticmethod
    def list_devices() -> List[str]:
        # retruns a list of CV2 capture devices
        # TODO - list all the camer deviecs and return list of avlaible devices
        # video = [vid for vid in os.listdir("/dev/") if "video" in vid]
        devices = []
        video = glob.glob("/dev/video*")
        for vid in video:
            cap = cv2.VideoCapture(vid)
            if cap.grab():
                devices.append(vid)
            else:
                # print(f"Cant grab {vid}")
                pass
        return devices

    def set_device(self, source:str):
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
                self.capture.release()
                self.stop()
                sys.exit("exiting")
        except KeyboardInterrupt as ex:
            print("exit")
            self.capture.release()
            cv2.destroyAllWindows()



class OCR:
    #TODO - send data between threads/multiprocess to speed up video
    def __init__(self, lang:str, ) -> None:
        self.lang = lang
        self.is_running = False
        

    def update(self):
        while self.is_running:
            pass

    def read_frame(self, frames:npt.NDArray, lang="eng") -> str:
        frames = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(frames, lang=lang)
        return text


    def draw_box(frames):
        pass
    

if __name__ == "__main__":
    #list devices on cimputer
    print(CameraThread.list_devices())
    # list after camera is used
    ct = CameraThread(1000, 1000, "/dev/video0")
    print(ct.list_devices())
    #start the thread
    ct.start()
    
    while True:
        _, frames = ct.read()
        #text = OCR.read_frame(frames)
        ct.view(frame=frames)

    ct.stop()