import numpy as np
import cv2 as cv
import pytesseract as ocr
import os, sys

import threading
from queue import Queue

# TODO get camera devices in list
# TODO read in camera data
# TODO run OCR on vidoe frames
# TODO optmise -> https://stackoverflow.com/questions/55494331/recording-video-with-opencv-python-multithreading

print_lock = threading.Lock()
cap = cv.VideoCapture(0)

def read_text():
   
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    try:
        print("Reading Frames")
        while cap.isOpened():
            ret, frames = cap.read()
            
            # TODO - process this on seprate thread
            #gray scaling the image made the OCR a bit more accurate
            frames = cv.cvtColor(frames, cv.COLOR_BGR2GRAY)
            text = ocr.image_to_string(frames, lang="eng")
            print(text)
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
    


# def display_videp(frames):
#     cv.imshow('frame', frames)
#     if cv.waitKey(1) == ord('q'):
#         break
#     # When everything done, release the capture
#     cap.release()
#     cv.destroyAllWindows()
    



if __name__ == "__main__":
    
    read_text()




#class OCRThread(threading.Thread):

#     '''
#     Pass video frame to second thread for porcessing
#     hopefully this 
#     '''

#     def __init__(self, queue, args=(), kwargs=None):
#         threading.Thread.__init__(self, args=(), kwargs=None)
#         self.queue = queue
#         self.daemon = True
#         self.receive_messages = args

#     def run(self):
#         print (threading.currentThread().getName(), self.receive_messages)
#         val = self.queue.get()
#         while True:
#             val = self.queue.get()
#             if val is None:
#                 return
#             self.get_text(val)


#     def get_text(self, message):
#         if self.receive_messages:
#                 # text = ocr.image_to_string(frames, lang="eng")
#                 # print(text)
#             print(message)
#             with print_lock:
#                 print (threading.currentThread().getName(), "Received {}".format(message))
