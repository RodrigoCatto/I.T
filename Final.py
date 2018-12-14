# import the necessary packages
import time
import cv2
import numpy as np
import wiringpi
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import imutils

print("[INFO] sampling THREADED frames from webcam...")
vs = WebcamVideoStream(src=0).start()
fps = FPS().start()

wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)
wiringpi.pinMode(12, wiringpi.GPIO.PWM_OUTPUT)
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)

while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 360 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=360, height=240)

	output = frame.copy()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# detect rectangles in the image
	ret,thresh = cv2.threshold(gray,125,255,cv2.THRESH_BINARY) #180
	contours,h = cv2.findContours(thresh ,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	for c in contours:
                approx = cv2.approxPolyDP(c, 0.01*cv2.arcLength(c,True),True)
                if((len(approx)) == 4 and cv2.contourArea(c)>1000):
                    cv2.drawContours(output, [c], 0,(0,0,255),1)
                    M = cv2.moments(c)
                    cx = int((M["m10"] / (M["m00"]+0.0001)))
                    cy = int((M["m01"] / (M["m00"]+0.0001)))
                    #print("X ", cx, "Y ", cy)
                    cv2.circle(output, (cx,cy), 2, (0,255,255), -1)
                    
        if True:
                
		cv2.imshow("Frame", output)
		#cv2.imshow("output", np.hstack([frame, output]))
		key = cv2.waitKey(1) & 0xFF
		if key == ord('q'):
                        vs.stop()
                        break

	# update the FPS counter
	fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()




        
