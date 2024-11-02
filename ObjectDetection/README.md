
# Object Detection and Distance Estimation System

This project uses YOLO (You Only Look Once) for real-time object detection and OpenCV to calculate the distance between the camera and detected objects. This system is useful for a variety of applications, such as security monitoring, distance-based alerts, and more.

## Features

- **Real-Time Object Detection:** Utilizes the YOLO model to detect multiple objects in real-time.
- **Distance Calculation:** Computes the distance between the camera and detected objects based on focal length and object width.
- **Face Detection:** Uses Haar Cascade Classifier to detect faces in the frame and determine object width.
- **Proximity Alerts:** Set up alerts based on object proximity to the camera.
- **Positioning Indicator:** Identifies the position (left, center, right) of objects in relation to the camera.
- **Dynamic Object Logging:** Logs the detected objects along with distance and position data.
- **Modular Design:** Easily extendable to add new features such as geofencing, event recording, and more.

## Prerequisites

Make sure the following dependencies are installed:

- Python 3.7+
- [YOLO Model](https://github.com/ultralytics/yolov5)
- OpenCV
- Ultralytics YOLO
- Webcam (for real-time detection)

## Environment Setup

To set up the environment, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/your-repository-name.git
   cd your-repository-name
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install required packages:**

   ```bash
   pip install -r requirements.txt
   ```

   Make sure the `requirements.txt` file includes the following packages:
   - `opencv-python`
   - `ultralytics`

4. **Download the YOLO model:**
   
   - Download the YOLOv8 model (or any model of your choice) and place it in the project directory.

5. **Setup Camera (if required):**

   - Ensure your webcam is properly connected if you're using this system on a local machine.

## Running the Project

To start the object detection and distance estimation system, run the following command:

```bash
python main.py
```

Replace `main.py` with the name of the script if it’s different.

## Usage Instructions

- **Proximity Alerts:** The system will automatically detect objects within a specified distance threshold.
- **Exit the Program:** Press `q` in the OpenCV window to exit the program.
- **Modifying Object Labels:** Update the `labels_translation` dictionary in the code to map object names to different languages or labels.

## Future Enhancements

This system can be extended with the following features:

- **Geofencing:** Define areas within the frame for specific alerts.
- **Event Recording:** Capture and save videos of detected events for later analysis.
- **Trajectory Prediction:** Implement object tracking and trajectory prediction.
- **UI for Control and Monitoring:** Create a user interface to view and adjust detection settings in real-time.

---

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Contributions

Contributions are welcome! Please fork the repository and create a pull request with your proposed changes.
