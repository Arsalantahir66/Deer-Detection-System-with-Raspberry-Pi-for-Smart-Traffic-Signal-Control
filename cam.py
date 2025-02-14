import cv2
import argparse

from ultralytics import YOLO
import supervision as sv
import numpy as np
import os

df_percent=80
# Load YOLOv4 model
# Function to perform object detection and draw bounding boxes
model=YOLO('best.pt')
 
def rescale_frame(frame, percent):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)
# Read video file
cap = cv2.VideoCapture(0)
# Get video frame width and height
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_width = int(frame_width * df_percent/ 100)
frame_height = int(frame_height * df_percent/ 100)

# Create sidebar to display detection results
sidebar_width = 300
output_width = frame_width + sidebar_width
output_height = frame_height
image_path_1 = 's1.jpg'
sidebar_image_1 = cv2.imread(image_path_1)
image_path_2 = 's2.jpg'
sidebar_image_2 = cv2.imread(image_path_2)
# Resize sidebar image to fit the sidebar
sidebar_image_on = cv2.resize(sidebar_image_1, (sidebar_width, frame_height))
sidebar_image_of = cv2.resize(sidebar_image_2, (sidebar_width, frame_height))
# Video writer
out = cv2.VideoWriter('output_video_web.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 5, (output_width, output_height))
box_annotator = sv.BoxAnnotator(
    thickness=2,
    text_thickness=2,
    text_scale=1
)
sidebar = np.zeros((frame_height, sidebar_width, 3), dtype=np.uint8)

c=0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = rescale_frame(frame, percent=df_percent)

    result = model(frame, agnostic_nms=True)[0]
    detections = sv.Detections.from_yolov8(result)
    #mask=zone.trigger(detections=detections)
    detections = detections[(detections.class_id == 0) & (detections.confidence > 0.5) ]
    labels = [
        f"{model.model.names[class_id]} {confidence:0.2f}"
        for _, confidence, class_id, _
        in detections
    ]
    frame = box_annotator.annotate(
        scene=frame, 
        detections=detections, 
        labels=labels
    )
    if len(detections.class_id)>= 1:
        sidebar[0:sidebar_image_on.shape[0], 0:sidebar_image_on.shape[1]] = sidebar_image_on
        #v2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),2) 
        #cv2.putText(frame, "person", (x1,y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)          
    else:
        sidebar[0:sidebar_image_of.shape[0], 0:sidebar_image_of.shape[1]] = sidebar_image_of
    output_frame = np.concatenate((frame, sidebar), axis=1)
    out.write(output_frame)
        # Display the processed frame
    cv2.imshow('Video', output_frame)
        # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
