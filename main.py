import cv2
import numpy as np
import Codebook as cb
import matplotlib.pyplot as plt

FRAME_DELAY = 1
TRAINING_FRAMES = 50

def main():
    books = [cb.Codebook(320,240,cb.CODEWORD_MULTIMINMAX) for x in range(3)]
    cap = cv2.VideoCapture('walk.mp4')
    #loop through video
    plots = [4,7,1]

    fig = plt.gcf()
    fig.show()
    fig.canvas.draw()

    currentFrame = 0
    while True:
        ret, frame = cap.read()
        if ret == True:

            plots.append(currentFrame % 3)
            plt.plot(plots)
            fig.canvas.draw()

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
            h,s,v = cv2.split(frame)
            channels = np.array([h,s,v])
            if currentFrame < TRAINING_FRAMES:
                #train each channel with new frame
                for i in range(3):
                    books[i].addFrame(channels[i])
            else:
                #process all 3 channels
                for i in range(3):
                    channels[i] = books[i].processFrame(channels[i])
                #process the results
                out = channels[0]/3 + channels[1]/3 + channels[2]/3
                # _,out = cv2.threshold(out,3*84,255,cv2.THRESH_BINARY)
                # out = cv2.medianBlur(out,5)
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