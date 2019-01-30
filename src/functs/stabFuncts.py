import numpy as np
import cv2

def getVideoArray (videoPath):
    # video in info
    video = cv2.VideoCapture(videoPath)
    N_FRAMES = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    VID_WIDTH = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    VID_HEIGHT = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print "N_FRAMES: " + str(N_FRAMES)

    # numpy array
    videoArr = np.zeros((int(N_FRAMES), int(VID_HEIGHT), int(VID_WIDTH)), dtype=np.uint8)
    # fill array
    for i in range(N_FRAMES):
        _, videoArr[i,:,:] = readVideoGray(video)
    video.release()
    return videoArr


def getVideoDeltaFrame (textPath):
    with open(textPath) as text:
        content = text.readlines()

    content = [x.strip() for x in content]
    N_Frames = len(content)
    cords = np.zeros((N_Frames,2))
    count = 0
    while count < len(content):
        cord = np.zeros(2)
        x = float(content[count].split(',')[0])
        y = float(content[count].split(',')[1])
        cord[0] = x
        cord[1] = y
        cords[count, :] = cord
        count += 1

    return cords


def writeVideoStabilizedDeltaFrame(textBox, textPath):
    text = open(textPath + '/output.txt', 'a+')
    for i in textBox:
        text.write(str(i[0]) + ' , ' + str(i[1]) + '\n')


def readVideoGray (video):
    _, frame = video.read()
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return _, frameGray


def maskMatches (matches, mask):
    goodMatches = []
    for i in range(len(matches)):
        if mask[i] == 1:
            goodMatches.append(matches[i])
    return goodMatches

