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

