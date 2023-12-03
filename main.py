import numpy as np
import cv2 as cv
import pytesseract as ocr
import os, sys
import threading


# TODO get camera devices in list
# TODO read in camera data
# TODO run OCR on vidoe frames
# TODO optmise  

print_lock = threading.Lock()
cap = cv.VideoCapture(0)


class OCRThread(threading.Thread):

    '''
    Pass video frame to second thread for porcessing
    hopefully this 
    '''

    def __init__(self, queue, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.queue = queue
        self.daemon = True
        self.receive_messages = args[0]

    def run(self):
        print (threading.currentThread().getName(), self.receive_messages)
        val = self.queue.get()
        self.do_thing_with_message(val)

    def do_thing_with_message(self, message):
        if self.receive_messages:
            with print_lock:
                print (threading.currentThread().getName(), "Received {}".format(message))




def read_text():
    current_text = ""
    count = 0
    img_buff = []
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    try:
        print("Reading Frames")
        while cap.isOpened():
            count += 1
        # Capture frame-by-frame
            ret, frames = cap.read()
            #print(frame)

            #for i, frame in enumerate(frames):
            if frames.all() % 20 == 0:
                #print(frames)
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

