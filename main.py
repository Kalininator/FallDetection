import cv2
import numpy as np

FRAME_DELAY = 250



def main():
    cap = cv2.VideoCapture('walk.mp4')
    #loop through video
    while True:
        ret, frame = cap.read()
        if ret == True:
            #process current frame

            cv2.imshow('fgmask',frame)
            if cv2.waitKey(FRAME_DELAY) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()