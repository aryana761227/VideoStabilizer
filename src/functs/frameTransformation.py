from stabFuncts import *
import kalman


def getTrans(videoArr, detector, bf, RANSAC_THRES, filt, is_kalman=False):
    N_FRAMES = videoArr.shape[0]
    trans = np.zeros((N_FRAMES, 3, 3))
    localMotion = getLocalMotion(videoArr, filt, detector, bf, RANSAC_THRES)
    if is_kalman:
        pass

    else:
        for i in range(N_FRAMES):
            for x in range(3):
                for y in range(3):
                    trans[i, x, y] = np.dot(filt, localMotion[i, :, x, y])

    return trans


def getLocalMotion(videoArr, filt, detector, bf, RANSAC_THRES):
    N_FRAMES = videoArr.shape[0]
    FILT_WIDTH = filt.size
    halfFilt = FILT_WIDTH / 2
    localMotion = np.zeros((N_FRAMES, FILT_WIDTH, 3, 3))

    # get next frame motion with ORB
    for i in range(N_FRAMES):
        print "frame " + str(i)
        localMotion[i, halfFilt, :, :] = np.identity(3)
        try:
            localMotion[i, halfFilt + 1, :, :] = \
                estMotion(videoArr[i, :, :], videoArr[i + 1, :, :], detector, bf, RANSAC_THRES)
        except IndexError:
            localMotion[i, halfFilt + 1, :, :] = np.identity(3)

    # get n-step frame motion from next step motion
    for j in range(halfFilt+2, FILT_WIDTH):
        for i in range(N_FRAMES):
            try:
                localMotion[i, j, :, :] = np.dot(localMotion[i + 1, j - 1, :, :], localMotion[i, j - 1, :, :])
            except IndexError:
                localMotion[i, j, :, :] = np.identity(3)

    # get past n-step motion (by inversion of forward motion)
    for j in range(halfFilt+2):
        for i in range(N_FRAMES):
            try:
                localMotion[i, j, :, :] = np.linalg.inv(localMotion[i + j - halfFilt, FILT_WIDTH - j - 1, :, :])
            except IndexError:
                localMotion[i, j, :, :] = np.identity(3)

    return localMotion


def estMotion(frame1, frame2, detector, bf, RANSAC_THRES):
        try:
            # get keypoints and descriptors
            kp1, des1 = detector.detectAndCompute(frame1, None)
            kp2, des2 = detector.detectAndCompute(frame2, None)

            # get matches
            matches = bf.match(des1, des2)
            # matches = filterMatches(matches, MATCH_THRES)
            # print kp1[matches[0].queryIdx].pt, kp2[matches[0].trainIdx].pt
            # get affine transform
            src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
            # print src_pts, dst_pts
            M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, RANSAC_THRES)
            # print M

        except:
            M = np.identity(3)

        return M
