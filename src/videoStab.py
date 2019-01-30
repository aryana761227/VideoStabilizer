import time
import os
import sys

from functs.stabFuncts import *
from functs.frameTransformation import getTrans
from functs.videoReconstruction import reconVideo
from functs.kalman import KalmanFilter

start_time = time.time()

# video path
videoInPath = ""
if len(sys.argv) > 1:
    try:
        videoInPath = sys.argv[1]
        FILT = sys.argv[2]
    except:
        print "Error at loading video"
        sys.exit()

videoInName, videoExt = os.path.splitext(videoInPath)
# videoBaseName = os.path.basename(videoInName)

# detector and matcher
detector = cv2.ORB_create()
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# parameters
MATCH_THRES = float('Inf')
RANSAC_THRES = 0.000001
BORDER_CUT = 1
is_kalman = False
FILT_WIDTH = 9
FILT_SIGMA = 0.2

new_video_name = ""
filt = np.array([])
textbox = getVideoDeltaFrame("../Outputs/Vibrated2.txt")
if FILT == "square":
    filt = (1.0 / FILT_WIDTH) * np.ones(FILT_WIDTH)

elif FILT == "gauss":
    filtx = np.linspace(-3 * FILT_SIGMA, 3 * FILT_SIGMA, FILT_WIDTH)
    filt = np.exp(-np.square(filtx) / (2 * FILT_SIGMA**2))
    # filt = 1. / (np.sum(filt)) * filt
    filt = 1./((2 * np.pi)**0.5 * FILT_SIGMA) * filt
elif FILT == 'kalman':
    is_kalman = True
    filt = (1.0 / FILT_WIDTH) * np.ones(FILT_WIDTH)
    N_FRAMES = textbox.shape[0]
    dt = 1.0 / 60
    FILT_WIDTH = filt.size
    dt = 1.0 / 60
    F = np.array([[1, dt, 0], [0, 1, dt], [0, 0, 1]])
    H = np.array([1, 0, 0]).reshape(1, 3)
    Q = np.array([[0.05, 0.05, 0.0], [0.05, 0.05, 0.0], [0.0, 0.0, 0.0]])
    R = np.array([0.5]).reshape(1, 1)

    kf_x = KalmanFilter(F=F, H=H, R=R)
    kf_y = KalmanFilter(F=F, H=H, R=R)

    #stable video dx and dy
    predictions = []
    for dxy in textbox:
        predictions.append([float(np.dot(H, kf_x.predict())[0]), float(np.dot(H, kf_y.predict())[0])])
        kf_y.update(dxy[1])
        kf_x.update(dxy[0])

    # vibration amount
    dstablized = []
    for i in range(len(textbox)):
        dstablized.append([textbox[i, 0] - predictions[i][0], textbox[i, 1] - predictions[i][1]])
    writeVideoStabilizedDeltaFrame(dstablized, '../Outputs')
new_video_name = "_Filter:  " + FILT + "_FWidth: " + str(
    FILT_WIDTH) + "_FSigma: " + str(FILT_SIGMA)
videoOutPath = videoInName + "_Stabilized" + new_video_name + videoExt

# get video array
videoArr = getVideoArray(videoInPath)

# get transformation
trans = getTrans(videoArr, detector, bf, RANSAC_THRES, filt, is_kalman=is_kalman)

# print new video Address
print videoOutPath

# video reconstruction
reconVideo(videoInPath, videoOutPath, trans, BORDER_CUT)
# compute elapsed time
elapsed_time = time.time() - start_time
print "Total time tests: " + str(elapsed_time) + " [s]"
# f = open('times.txt', 'a')
# f.write(videoOutPath + ": " + str(elapsed_time) + "\n")
