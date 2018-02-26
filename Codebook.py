import numpy as np
import cv2

CODEWORD_MINMAX = 1
CODEWORD_VALUELIST = 2


class CodewordMinMax:
    def __init__(self):
        self.min = None
        self.max = None

    def addValue(self, val):
        if (self.min is None) or (self.max is None):
            self.min = val
            self.max = val
        else:
            if val < self.min:
                self.min = val
            if val > self.max:
                self.max = val

    def checkValue(self, val):
        if val < self.min or val > self.max:
            return False
        else:
            return True


class CodewordValueList:
    def __init__(self):
        self.vals = []

    def addValue(self, val):
        if val not in self.vals:
            self.vals.append(val)

    def checkValue(self, val):
        return val in self.vals


class Codebook(object):
    def __init__(self, width, height, type):
        self.width = width
        self.height = height
        self.type = type
        if self.type == CODEWORD_MINMAX:
            self.codes = [[CodewordMinMax() for x in range(height)] for y in range(width)]
        elif self.type == CODEWORD_VALUELIST:
            self.codes = [[CodewordValueList() for x in range(height)] for y in range(width)]

    def addFrame(self, frame):
        for x in range(self.width):
            for y in range(self.height):
                self.codes[x][y].addValue(frame[y][x])

    def processFrame(self, frame):
        out = np.zeros((self.height, self.width), np.uint8) + 255
        for x in range(self.width):
            for y in range(self.height):
                if self.codes[x][y].checkValue(frame[y][x]):
                    out[y][x] = 0
        return out
