import cv2
import numpy as np
from math import pi

def ellipseStats(ellipse):
    angle = ellipse[2]
    if angle > 90:
        angle = angle - 180
    return angle, 0


def largestBlob(frame, **options):
    minArea = 300
    if "minarea" in options:
        minArea = options.get("minarea")

    _, contours, _ = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) != 0:
        cnts = []
        for cnt in contours:
            if cv2.contourArea(cnt) >= minArea:
                cnts.append(cnt)
        if len(cnts) > 0:
            print np.concatenate(cnts)
            return cv2.fitEllipse(np.concatenate(cnts))
        # cnts = np.concatenate(contours)
        # return cv2.fitEllipse(cnts)
        # c = max(contours, key=cv2.contourArea)
        # if cv2.contourArea(c) >= minArea:
        #     ellipse = cv2.fitEllipse(c)
        #     return ellipse
    return None

def largestBlobs(frame,blobCount,**options):
    minArea = 200
    if "minarea" in options:
        minArea = options.get("minarea")
    _, contours, _ = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) != 0:
        #extract big enough contours
        cnts = []
        for cnt in contours:
            if cv2.contourArea(cnt) >= minArea:
                cnts.append(cnt)
        if len(cnts) > 0:
            cnts.sort(key=cv2.contourArea,reverse=True)
            topx = cnts[:blobCount]
            ellipse = cv2.fitEllipse(np.concatenate(topx))
            return ellipse
    return None

def blobByFScore(frame):
    #get all contours
    _, contours, _ = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #remove too small objects
    cnts = []
    for cnt in contours:
        if cv2.contourArea(cnt) > 200:
            cnts.append(cnt)
    contours = cnts

    if len(contours) != 0:
        #sort contours
        contours.sort(key=cv2.contourArea,reverse=True)
        acceptedcontours = []
        currentScore = 0
        currentArea = 0

        for cnt in contours:
            cntArea = cv2.contourArea(cnt)
            #ellipse for accepted + this contour
            cnts = acceptedcontours
            cnts.append(cnt)
            _, (MA, ma),_ = cv2.fitEllipse(np.concatenate(cnts))
            ellipseArea = pi * MA * ma
            newScore = ellipseArea / (currentArea + cntArea)
            if newScore > currentScore * 0.5:
                acceptedcontours.append(cnt)
                currentScore = newScore
                currentArea += cntArea
                break
        print len(acceptedcontours)
        return cv2.fitEllipse(np.concatenate(acceptedcontours))
    return None

def blobDetector(frame, **options):
    params = cv2.SimpleBlobDetector_Params()
    params.minArea = 1500
    params.filterByArea = True
    params.filterByInertia=False
    params.filterByConvexity=False
    params.filterByCircularity=False
    ver = (cv2.__version__).split('.')
    if int(ver[0]) < 3:
        detector = cv2.SimpleBlobDetector(params)
    else:
        detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(frame)
    frame = cv2.drawKeypoints(frame, keypoints, np.array([]), 150, cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    return frame