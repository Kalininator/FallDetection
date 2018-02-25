import numpy as np
import cv2


class Codeword:
    def __init__(self):
        self.min = None
        self.max = None

    def addValue(self, val):
        if self.min == None or self.max == None:
            self.min = val
            self.max = val
        else:
            if val < self.min:
                self.min = val
            if val > self.max:
                self.max = val

    def checkValue(self, val):
        print str(self.min) + "," + str(self.max) + "," + str(val)
        if val < self.min or val > self.max:
            return False
        else:
            return True


class Codebook:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.codes = np.full((width, height), Codeword())

    def addFrame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        for x in range(self.width):
            for y in range(self.height):
                # print frame.shape
                # print str(x) + "," + str(y)
                # use hue
                self.codes[x][y].addValue(frame[y][x][2])

    def processFrame(self,frame):
        out = np.zeros((self.height,self.width),np.uint8)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        for x in range(self.width):
            for y in range(self.height):
                if self.codes[x][y].checkValue(frame[y][x][2]):
                    out[y][x] = 100
        return out