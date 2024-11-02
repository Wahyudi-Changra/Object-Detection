import cv2
from ultralytics import YOLO

# Variables:
# Actual width of the object W(cm)
real_width = 15
# Actual distance from the object to the camera D(cm)
real_distance = 68

# Face detection
CascadeClass = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Initialize YOLO model and webcam
model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)

# Function to calculate focal length
def focalLength(pixel_width, real_distance, real_width):
    return (pixel_width * real_distance) / real_width

# Function to calculate distance
def distanceCal(focal_length, real_width, width):
    return (focal_length * real_width) / width

# Function to calculate width in the image P(pixel)
def detectFace(img):
    width = 0
    BGRgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = CascadeClass.detectMultiScale(BGRgray)
    for face in faces:
        a, b, c, d = face
        cv2.rectangle(img, (a, b), (a + c, b + d), (255, 255, 0), 3)
        width = c
    return width

# Check if the webcam cannot be opened
if not cap.isOpened():
    print("Error: Could not open webcam.")

# Variable to keep track of detected objects
last_detected_objects = set()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image.")
        break

    results = model.predict(source=frame, save=False, conf=0.2, iou=0.5)

    if len(results) > 0:
        result = results[0]
        if len(result.boxes) > 0:
            plot = result.plot()
            cv2.imshow("Webcam Detection", plot)

            # Retrieve names and positions of detected objects
            detected_objects = set()
            for box in result.boxes:
                # Get the name of the object
                object_name = model.names[int(box.cls[0])]

                # Calculate the position of the bounding box
                x_center = (box.xywh[0][0] + box.xywh[0][2] / 2) / frame.shape[1]

            # Find new objects that have not been detected before
            new_objects = detected_objects - last_detected_objects
            if new_objects:
                description = ', '.join(new_objects)
                last_detected_objects = detected_objects  # Update the list of detected objects

    # Check if the 'q' key is pressed to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()