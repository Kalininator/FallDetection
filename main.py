import cv2
import numpy as np
from Codebook import Codebook

FRAME_DELAY = 100



def main():
    # c = Codebook(3,3)
    # for i in c.codes.flatten():
    #     print i.min


    # bg = cv2.imread('background.jpg')
    # fg = cv2.imread('foreground_standing.jpg')
    # print bg.shape
    # height,width,channels = bg.shape
    c = Codebook(320,240)
    # c.addFrame(bg)
    cap = cv2.VideoCapture('walk.mp4')
    #loop through video
    frames = 0

    while True:
        ret, frame = cap.read()
        if ret == True:
            #process current frame
            if frames < 20:
                c.addFrame(frame)
                frames += 1
                # first = False
            else:
                frame = c.processFrame(frame)
            cv2.imshow('fgmask',frame)
            if cv2.waitKey(FRAME_DELAY) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()