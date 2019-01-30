# VideoStabilizer
# install this packages in terminal:
  opencv
  numpy
 
 to run the code run this command in terminal:
 # python videoStab.py <video address> <filter type>
 for example:
  python2 videoStab.py ../Output/Vibreated2.avi gauss
  python2 videoStab.py ../Output/Vibrated2.txt kalman
 
 # gauss and square filters:
 we can make a video with this filters and stabilize them with this filters.
 
 # kalman:
 we just input a text file contains dx and dy each frame relative to  the previous frame and predict them with kalman filter.
 then we find differences between stable and unstable Videos dx and dy frame to frame.
 finally we write this vibration amount numbers in Output.txt
 
 delete output.txt after each time run with kalman filter to show you correct numbers.
