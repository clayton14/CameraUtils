import pytesseract
import numpy as np
import cv2
import os, sys
from camera import Camera

class OCR(Camera):
    def __init__(self, width: int, height: int, source: str) -> None:
        self.is_running = True
        self.boxes = None
        self.frameBuff = 1
        self.read_lock = threading.Lock()

    def detect_words(self) -> object:
        """
        accesses the queus and passes frames to pytesseract.image_to_string() method
        """
        
        frames = self.queue.get()
        self.text = pytesseract.image_to_string(frames)
        return self

    def detect_symbols(self):
        """
        Draws boxes atound each symbol present in the current frame
        """
        # TODO - read data in from Queue or pipe and draw
        frames = frame_buff.get()
        print(frames)
        img_h, img_w, _ = frames.shape
        words = []
        ## Decets chargers in image\
        config=r"--psm 6 --oem 3"
        boxes = pytesseract.image_to_boxes(frames, lang="eng")
        print(boxes)
        for box in boxes.splitlines():
            box = box.split(" ")
            char = box[0]
            words.append(char) 
            x, y, w, h = int(box[1]), int(box[2]), int(box[3]), int(box[4])
            pos1 = (x, img_h - y)
            pos2 = (w, img_h - h)
            #print(f"box x:{x}, y:{y}, w:{w}, h:{h}")
            img_b = cv2.rectangle(frame, pos1, pos2, color=(0, 0, 255), thickness=1)
            return img_b



    @staticmethod
    def test():
        CWD = os.getcwd()
        img_path = (os.path.join(
            CWD, "test_img",
        ))
        img = cv2.imread(os.path.join(img_path, "testocr.png"))
        img_h, img_w, _ = img.shape
        print(img.shape)
        words = []
        ## Decets chargers in image
        boxes = pytesseract.image_to_boxes(img, lang="eng", config=r"--psm 6 --oem 3")
        print(boxes)
        
        for box in boxes.splitlines():
            box = box.split(" ")
            char = box[0]
            words.append(char) 
            x, y, w, h = int(box[1]), int(box[2]), int(box[3]), int(box[4])
            pos1 = (x, img_h - y)
            pos2 = (w, img_h - h)
            #print(f"box x:{x}, y:{y}, w:{w}, h:{h}")
            img_b = cv2.rectangle(img, pos1, pos2, color=(0, 0, 255), thickness=1)
            # img_t = cv2.putText(img_b, char, pos1, fontScale=9)
            
        print("".join(words))
        cv2.imwrite("test.png", img_b)


    def read(self):
        # TODO - get data from tesseract
        pass


    def start(self):
        Thread(target=self.read, daemon=False)