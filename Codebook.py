import numpy as np
import cv2


class Codeword:
    def __init__(self):
        self.min = None
        self.max = None

    def addValue(self, val):
        val = val[2]
        if (self.min is None) or (self.max is None):
            self.min = val
            self.max = val
        else:
            if val < self.min:
                self.min = val
            if val > self.max:
                self.max = val



    def checkValue(self, val):
        #extract channel
        val = val[2]
        if val < self.min or val > self.max:
            return False
        else:
            return True



class Codebook:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.codes = [[Codeword() for x in range(height)] for y in range(width)]

    def addFrame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        for x in range(self.width):
            for y in range(self.height):
                # use hue
                self.codes[x][y].addValue(frame[y][x])

    def processFrame(self,frame):
        out = np.zeros((self.height,self.width),np.uint8) + 255
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        for x in range(self.width):
            for y in range(self.height):
                if self.codes[x][y].checkValue(frame[y][x]):
                    out[y][x] = 0
        return out