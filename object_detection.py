# -----------------------------------------------------------
# This app demonstrates the webcam detecting objects into the frame using cv2
# and generates interactive data visualization (graph) using Bokeh library.
#
# email dhruvdave61@gmail.com
# ----------------------------------------------------------


from datetime import datetime

import cv2
import pandas

first_frame = None
status_list = [None, None]
times = []
df = pandas.DataFrame(columns=["Start", "End"])

# it captures the different frames of the video
video = cv2.VideoCapture(0)

while True:
    # this two variables read the frames of the video
    check, frame = video.read()
    status = 0

    # it makes the video frame gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # it makes the video frame blur, so it removes noise and get the accuracy to detect the object
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if first_frame is None:
        first_frame = gray
        continue

    # delta frame gives us the difference between first_frame and gray scale frame
    delta_frame = cv2.absdiff(first_frame, gray)

    # threshold method used to detect the object from the frame and this method returns the tuple with 2 items
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]

    # dilate method is used to smooth the thresh_frame
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # find the contours of the object, and it returns the tuple
    (cnts, _) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # filtering the object contours which has area of 10000 pixels
    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        status = 1

        # creating the rectangle around the object detected
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
    status_list.append(status)

    status_list = status_list[-2:]

    # According to the status_list value getting time of the object enters the frame
    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())

    # According to the status_list value getting time of the object exits the frame
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())

    cv2.imshow("delta frame", delta_frame)
    cv2.imshow("ThreshHold frame", thresh_frame)
    cv2.imshow("Color frame", frame)
    key = cv2.waitKey(1)

    # 'q' key is used to quit from the screen
    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break

print(status_list)
print(times)

# iterate through the time of the object in the frame and append it to the dataframe in times.csv file
for i in range(0, len(times), 2):
    df = df.append({"Start": times[i], "End": times[i + 1]}, ignore_index=True)

df.to_csv("Times.csv")
video.release()
cv2.destroyAllWindows()
