import cv2
import numpy as np
from Codebook import Codebook

FRAME_DELAY = 100



def main():
    c = Codebook(320,240)
    # c.addFrame(bg)
    cap = cv2.VideoCapture('walk.mp4')
    #loop through video
    currentFrame = 0

    while True:
        ret, frame = cap.read()
        if ret == True:
            if currentFrame < 50:#num frames to process
                #used for initial training of codebook
                c.addFrame(frame)
            else:
                cb_out = c.processFrame(frame)
                cv2.imshow('fgmask',cb_out)
            currentFrame += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()