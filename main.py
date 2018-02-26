import cv2
import numpy as np
import Codebook as cb

FRAME_DELAY = 1
TRAINING_FRAMES = 50



def main():
    books = [cb.Codebook(320,240,cb.CODEWORD_MINMAX) for x in range(3)]
    cap = cv2.VideoCapture('walk.mp4')

    #loop through video
    currentFrame = 0
    while True:
        ret, frame = cap.read()
        if ret == True:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
            h,s,v = cv2.split(frame)
            channels = np.array([h,s,v])
            if currentFrame < TRAINING_FRAMES:#num frames to process
                for i in range(3):
                    books[i].addFrame(channels[i])
            else:
                for i in range(3):
                    channels[i] = books[i].processFrame(channels[i])
                #process the results
                out = channels[0]/3 + channels[1]/3 + channels[2]/3
                # _,out = cv2.threshold(out,2*84,255,cv2.THRESH_BINARY)
                out = cv2.medianBlur(out,5)
                cv2.imshow('fgmask',out)
            currentFrame += 1

            if currentFrame >= TRAINING_FRAMES:
                cv2.waitKey(FRAME_DELAY)

        else:
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()