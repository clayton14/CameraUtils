import sys, glob
import threading
from threading import Thread
from multiprocessing import Queue, Process
from typing import List

import pytesseract
import cv2
import numpy.typing as npt


class Camera:
    """
    Initialize the `Camera` class with parameters for capturing frames.

    Args:
        width (int): Desired width of the captured frames.
        height (int): Desired height of the captured frames.
        queue (Queue): A multi-producer, multi-consumer queue to store captured frames.
        source (str): The video source string, either a device index or file path.

    Raises:
        ValueError: If the requested resolution is not supported by the camera.
        RuntimeError: If the camera cannot be opened.

    Attributes:
        width (int): The actual width of the captured frames.
        height (int): The actual height of the captured frames.
        is_running (bool): Whether the camera thread is running.
        queue (Queue): The queue used to store captured frames.
        read_lock (threading.Lock): A lock to synchronize access to the frame buffer.
        capture (cv2.VideoCapture): The OpenCV video capture object.
        grabbed (bool): Whether the first frame was successfully grabbed.
        frames (numpy.ndarray): The latest captured frame, or None if no frame is available.
    """

    def __init__(self, width: int, height: int, source:str) -> None:
        self.width = width
        self.height = height
        self.is_running = False
        # Threading        
        # self.queue = queue
        self.read_lock = threading.Lock()
        # cv2
        self.capture = cv2.VideoCapture(source)
        self.grabbed, self.frames = self.capture.read()
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        


    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()


    def start(self) -> object:
        """
        Starts the camera on new thread
        """
        # TODO - implement run method
        if self.is_running:
            print("Capture is already started")
            return None
        self.is_running = True
        self.thread = Thread(target=self._update, args=(), daemon=True).start()
        return self


    def _update(self) -> None:
        """
        
        """
        try:
            while self.is_running:
                grabbed, frames = self.capture.read()
                with self.read_lock:
                    self.grabbed = grabbed
                    self.frames = frames
                    # self.queue.put(frames)
        except KeyboardInterrupt as ex:
            print("exit")
            self.capture.release()


    def set_device(self, source:str):
        self.cv2.VideoCapture(source)

    
    def read(self) -> bool | npt.NDArray:
        """
        
        """
        with self.read_lock:
            frame = self.frames.copy()
            grabbed = self.grabbed
        return grabbed, frame


    def stop(self):
        """
        
        """
        self.is_running = False
        self.thread.join()
        self.capture.release()
        cv2.destroyAllWindows()


    def view(self, frame):
        """
        
        """
        try:
            cv2.imshow(f" {self.thread.name} ", frame)
            if cv2.waitKey(1) == ord("q"):
                #self.capture.release()
                self.stop()
                sys.exit("exiting")
        except KeyboardInterrupt as ex:
            print("exit")
            self.stop()


    @staticmethod
    def list_devices() -> List[str]:
        # retruns a list of CV2 capture devices
        # TODO - list all the camer deviecs and return list of avlaible devices
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


class VideoProcess():
    # TODO - send data between threads/multiprocess to speed up video
    def __init__(self, queue, view_callback) -> None:
        self.read_lock = threading.Lock()
        self.is_running = True
        self.queue = queue
        self.view_callback = view_callback


    def run(self):
        print(self.name)
        while True:
            frames = self.queue.get()
            text = pytesseract.image_to_string(frames, lang="eng")
            if self.view_callback:
                self.view_callback(frames, text)


    def draw_box(frames):
        #TODO - read data in from Queue or pipe and draw 
        # 
        pass
    



if __name__ == "__main__":
    
    #list devices on cimputer
    print(Camera.list_devices())
    # list after camera is used
    ct = Camera(1000, 1000, "/dev/video0").start()
    print(ct.list_devices())
    #start the thread
    
    # p = Process()

    while True:
        _, frames = ct.read()
        
        #ct.view(frame=ct.queue.get())

    ct.stop()