# 🦴 Knee Tibia-Femur Segmentation

## 📌 Project Description

This project delivers a comprehensive pipeline for **segmentation**, **contour manipulation**, and **anatomical landmark detection** in knee CT scans using **Python** and **SimpleITK**, addressing critical tasks in orthopedic imaging analysis.  

### ✅ The workflow includes:
- ✅ Bone segmentation of the femur and tibia from the input CT volume  
- ✅ Morphological expansion of masks (e.g., 2mm and 4mm dilations)  
- ✅ Randomized mask generation within a specified expansion margin  
- ✅ Landmark detection for identifying the medial and lateral lowest points on the tibial surface  
- ✅ Coronal view visualizations for verification and presentation  

The pipeline operates on an input CT image, producing masks and landmark data. It supports **reproducibility**, **parameterization** (e.g., expansion radius and random seed), and **modular reuse**.


This work supports researchers in **medical image analysis**, especially in **orthopedics** and **anatomical modeling**.



## 📁 Project Structure

```text
knee-tibia-femur-segmentation/
├── code/                     # Modular Python scripts
│   ├── segmentation.py
│   ├── main.py
│   ├── expansion.py
│   ├── randomization.py
│   ├── visualization.py
│   ├── run_landmark_pipeline.py
│   └── landmark_utils.py
├── results/                  # Output masks, landmarks, and images
│   ├── bone_segmented.nii.gz
│   ├── mask_bone_expanded_2mm.nii.gz
│   ├── bone_segmented_randomized.nii.gz
│   ├── mask_tibia_expanded_2mm.nii.gz
│   ├── mask_tibia_expanded_4mm.nii.gz
│   ├── mask_tibia_random_1.nii.gz
│   ├── mask_tibia_random_2.nii.gz
│   ├── tibial_landmarks.txt
│   ├── mask_femur.nii.gz
│   └── mask_tibia.nii.gz
├── requirements.txt          # Python dependencies
├── .gitignore
└── README.md
```
### Installation

1.Clone the repository:
```
CopyEdit
'git clone https://github.com/< HanaMekonen/>/knee-tibia-femur-segmentation.git'
'cd knee-tibia-femur-segmentation'
```

2. Install dependencies: Ensure you have Python 3.x. Then install required packages:
```
CopyEdit
'pip install -r requirements.txt'
The main dependencies are SimpleITK, numpy, scipy, and matplotlib.
```

## 🚀 Usage
The project is organized into modular scripts located in the codes/ directory. Each script focuses on a specific task in the knee CT analysis pipeline. Most of the modules define reusable functions and should be imported and called via main.py or used in run_landmark_pipeline.py. Only visualization.py is designed to run standalone.
### 🧩 Modular Components
```
•segmentation.py
Contains the segment_bones() function for femur and tibia segmentation.
•expansion.py
Defines expand_mask_by_mm() to perform morphological expansion by a user-defined millimeter radius.
•randomization.py
Provides randomize_mask_distance_based() to generate randomized contours within a specified margin.
•landmark_utils.py
Contains reusable functions for landmark extraction and coordinate transformation.
•run_landmark_pipeline.py
Executes the full workflow: segmentation → expansion → randomization → tibial landmark detection. Ideal for batch automation.
•main.py
Entry-point script to manually control and orchestrate the full segmentation and mask processing pipeline.
•visualization.py
Standalone script to generate coronal slice visualizations of segmentation results and landmarks.
Run directly with:
```
```
bash
CopyEdit
'python codes/visualization.py'
```
### 🏁 To Run the Pipeline
To run the complete tibia-femur segmentation and landmark extraction workflow:
```
bash
CopyEdit
'python codes/main.py'
```
```
This script will:
•	Load the CT scan
•	Perform segmentation of tibia and femur
•	Generate 2 mm and 4 mm expanded masks
•	Generate randomized contour variants
•	Detect tibial landmarks
•	Save results under the results/ directory
```

### 📂 Output Overview
```
After running the pipeline, you will find:
•	Segmented masks (e.g., mask_tibia.nii.gz, mask_femur.nii.gz bone_segmented.nii.gz)
•	Expanded masks (mask_bone_expanded_2mm.nii.gz, etc.)
•	Randomized masks (mask_bone_random_1.nii.gz, etc.)
•	Landmark coordinates in (mask_tibia_expanded_2mm.nii.gz,tibial_landmarks.txt,etc)
•	Visual overlays (from visualization.py) 
```
## 📦 Dependencies
```
•	SimpleITK
•	numpy
•	scipy
•	matplotlib
See requirements.txt for versions.
```
## 📬 Contact
For any questions or feedback, please reach out via GitHub Issues.

