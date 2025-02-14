# Deer-Detection-System-with-Raspberry-Pi-for-Smart-Traffic-Signal-Control

## Installation Guide

Follow these steps to set up the environment and run the project.

### 1. Install Miniconda (Windows)
1. Download Miniconda from [Miniconda Official Site](https://docs.conda.io/en/latest/miniconda.html).
2. Install Miniconda following the on-screen instructions.
3. Open the Command Prompt and navigate to the directory where you downloaded this repository.

### 2. Clone the Repository

```sh
git clone https://github.com/your-username/gazelle_delivery.git
cd gazelle_delivery
3. Setup Conda Environment
sh
Copy
Edit
conda create -n gaze python=3.10 -y
conda activate gaze
4. Install Dependencies
sh
Copy
Edit
pip install numpy==1.23.1
pip install ultralytics
pip install supervision==0.2.0
Usage
1. Run Camera Detection
To start real-time object detection from a webcam:

sh
Copy
Edit
python camera.py
2. Run Video File Detection
To process a video file:

sh
Copy
Edit
python video.py --source path_to_video.mp4
