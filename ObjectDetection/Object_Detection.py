import cv2
from ultralytics import YOLO
import os
import pyttsx3
from moviepy.editor import VideoFileClip, CompositeAudioClip, AudioFileClip

# Variables:
# Actual width of the object W(cm)
real_width = 15
# Actual distance from the object to the camera D(cm)
real_distance = 68

# Face detection
CascadeClass = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Initialize YOLO model and webcam
model = YOLO("yolov8n.pt")
input_video_path = "input_video_path"  # Replace with your input video path or change to webcam
output_video_path = "out_video_path"  # Path to save the output video
cap = cv2.VideoCapture(input_video_path)

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

# Initialize pyttsx3 engine for voice announcements
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Set speech rate to make voice slower
audio_clips = []  # List to store audio clips with timestamps
audio_files = []  # List to keep track of temporary audio file paths

# Check if the webcam cannot be opened
if not cap.isOpened():
    print("Error: Could not open webcam.")

# Variable to keep track of detected objects
last_detected_objects = set()

# Set up video output parameters
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
temp_output_path = "temp_output_no_audio.mp4"
out = cv2.VideoWriter(temp_output_path, fourcc, fps, (frame_width, frame_height))

# Variable to keep track of detected objects to ensure each is announced only once
announced_objects = set()  # Set to keep track of announced objects
frame_count = 0  # To calculate timestamp

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image.")
        break

    results = model.predict(source=frame, save=False, conf=0.2, iou=0.5)
    detected_objects = set()
    timestamp = frame_count / fps  # Calculate timestamp based on frame count

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

 # Add object name to the set for announcements if not announced before
                if object_name not in announced_objects:
                    # Generate audio for the new object
                    description = f"{object_name}"
                    print(f"Announcement: {description}")
                    audio_path = f"audio_clip_{object_name}.mp3"
                    engine.save_to_file(description, audio_path)
                    engine.runAndWait()

                    # Save the audio file path for cleanup later
                    audio_files.append(audio_path)

                    # Add the audio clip to play at the calculated timestamp
                    audio_clip = AudioFileClip(audio_path).set_start(timestamp)
                    audio_clips.append(audio_clip)

                    # Mark object as announced
                    announced_objects.add(object_name)

            # Write the frame with bounding boxes to the output video
            out.write(plot)

    # Update frame count
    frame_count += 1

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()

# Load the video file and add audio clips
video_clip = VideoFileClip(temp_output_path)

# Combine audio clips with the video
combined_audio = CompositeAudioClip(audio_clips)

# Set the combined audio to the video and save it
final_clip = video_clip.set_audio(combined_audio)
final_clip.write_videofile(output_video_path)

# Clean up temporary audio files
for audio_file in audio_files:
    try:
        os.remove(audio_file)
        print(f"Deleted temporary audio file: {audio_file}")
    except OSError as e:
        print(f"Error deleting file {audio_file}: {e}")
