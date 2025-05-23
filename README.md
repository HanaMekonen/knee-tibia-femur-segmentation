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

### 📦 Output Includes:
- `bone_segmented.nii.gz`: femur and tibia mask  
- `mask_bone_expanded_2mm.nii.gz`, `mask_tibia_expanded_2mm.nii.gz`, `mask_tibia_random_1.nii.gz`, etc.: both bone and tibia mask variants  
- `tibial_landmarks.txt`: coordinates of anatomical landmarks on the tibia  

This work supports researchers in **medical image analysis**, especially in **orthopedics** and **anatomical modeling**.

---

## 📁 Project Structure

```text
knee-tibia-femur-segmentation/
├── code/                          # Modular Python scripts
│   ├── segmentation.py
│   ├── main.py
│   ├── expansion.py
│   ├── randomization.py
│   ├── visualization.py
│   ├── run_landmark_pipeline.py
│   └── landmark_utils.py
├── results/                       # Output masks, landmarks, and images
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
├── requirements.txt              # Python dependencies
├── .gitignore
└── README.md
