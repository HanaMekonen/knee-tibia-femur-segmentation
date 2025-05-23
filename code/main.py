#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import SimpleITK as sitk

# ==== Import your custom modules ====
from segmentation import segment_bones
from expansion import expand_mask_by_mm
from randomization import randomize_mask_distance_based
from landmark_utils import find_medial_lateral_lowest, voxel_to_phys
from visualize import visualize_labeled_mask, visualize_mask_only

# ==== Paths ====
DATA_PATH = "3702_left_knee.nii.gz"
RESULT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../results'))
FIGURE_DIR = os.path.join(RESULT_DIR, "figures")
os.makedirs(FIGURE_DIR, exist_ok=True)

# ==== Step 1: Segment Femur and Tibia ====
print("🔍 Segmenting bones...")
labeled_mask, tibia_mask, femur_mask, ct_image = segment_bones(DATA_PATH)

# ==== Step 2: Save Expanded Masks ====
print("📏 Expanding tibia mask...")
tibia_2mm = expand_mask_by_mm(tibia_mask, 2.0)
tibia_4mm = expand_mask_by_mm(tibia_mask, 4.0)
sitk.WriteImage(tibia_2mm, os.path.join(RESULT_DIR, "mask_tibia_expanded_2mm.nii.gz"))
sitk.WriteImage(tibia_4mm, os.path.join(RESULT_DIR, "mask_tibia_expanded_4mm.nii.gz"))

# ==== Step 3: Generate Randomized Masks ====
print("🎲 Generating randomized masks...")
rand_tibia_1 = randomize_mask_distance_based(tibia_mask, ct_image, max_mm=2.0, seed=1)
rand_tibia_2 = randomize_mask_distance_based(tibia_mask, ct_image, max_mm=2.0, seed=2)
sitk.WriteImage(rand_tibia_1, os.path.join(RESULT_DIR, "mask_tibia_random_1.nii.gz"))
sitk.WriteImage(rand_tibia_2, os.path.join(RESULT_DIR, "mask_tibia_random_2.nii.gz"))

# ==== Step 4: Landmark Extraction ====
print("📌 Extracting tibial landmarks...")
masks = {
    "Original": tibia_mask,
    "Expanded_2mm": tibia_2mm,
    "Expanded_4mm": tibia_4mm,
    "Random_1": rand_tibia_1,
    "Random_2": rand_tibia_2
}

landmark_file = os.path.join(RESULT_DIR, "tibial_landmarks.txt")
with open(landmark_file, "w") as f:
    f.write("Mask\tmed_x\tmed_y\tmed_z\tmed_mm_x\tmed_mm_y\tmed_mm_z\t"
            "lat_x\tlat_y\tlat_z\tlat_mm_x\tlat_mm_y\tlat_mm_z\n")
    for name, mask in masks.items():
        medial_vox, lateral_vox = find_medial_lateral_lowest(mask)
        medial_mm = voxel_to_phys(mask, medial_vox)
        lateral_mm = voxel_to_phys(mask, lateral_vox)
        f.write(f"{name}\t"
                f"{medial_vox[0]}\t{medial_vox[1]}\t{medial_vox[2]}\t"
                f"{medial_mm[0]:.2f}\t{medial_mm[1]:.2f}\t{medial_mm[2]:.2f}\t"
                f"{lateral_vox[0]}\t{lateral_vox[1]}\t{lateral_vox[2]}\t"
                f"{lateral_mm[0]:.2f}\t{lateral_mm[1]:.2f}\t{lateral_mm[2]:.2f}\n")
print(f"✅ Landmarks saved to: {landmark_file}")

# ==== Step 5: Save visualizations ====
print("🖼 Saving visualizations...")
visualize_labeled_mask(ct_image, labeled_mask, os.path.join(FIGURE_DIR, "bone_segmented_overlay.png"))
visualize_mask_only(tibia_2mm, os.path.join(FIGURE_DIR, "tibia_expanded_2mm.png"))
visualize_mask_only(rand_tibia_1, os.path.join(FIGURE_DIR, "tibia_random_1.png"))
visualize_mask_only(rand_tibia_2, os.path.join(FIGURE_DIR, "tibia_random_2.png"))

print("✅ Pipeline completed successfully!")


# In[ ]:


import os
import SimpleITK as sitk

# ==== Import your custom modules ====
from segmentation import segment_bones
from expansion import expand_mask_by_mm
from randomization import randomize_mask_distance_based
from landmark_utils import find_medial_lateral_lowest, voxel_to_phys
from run_landmark_pipeline import run_landmark_extraction  # Optional helper wrapper

# ==== Paths ====
DATA_PATH = "3702_left_knee.nii.gz"
RESULT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../results'))
os.makedirs(RESULT_DIR, exist_ok=True)

# ==== Step 1: Segment Femur and Tibia ====
print("🔍 Segmenting bones...")
bone_segmented, tibia_mask, femur_mask, ct_image = segment_bones(DATA_PATH)

# ==== Step 2: Save Expanded Masks ====
print("📏 Expanding bone mask...")
mask_expanded_2mm = expand_mask_by_mm(bone_segmented, 2.0)
sitk.WriteImage(mask_expanded_2mm, os.path.join(RESULT_DIR, "mask_bone_expanded_2mm.nii.nii.gz"))


# ==== Step 3: Generate Randomized Masks ====
print("🎲 Generating randomized masks...")
rand_bone= randomize_mask_distance_based(bone_segmented, ct_image, max_mm=2.0, seed=1)
sitk.WriteImage(rand_tibia_1, os.path.join(RESULT_DIR, "bone_segmented_randomized.nii.gz"))

# ==== Step 4: Landmark Extraction (from masks) ====
print("📌 Extracting tibial landmarks...")
masks = {
    "Original": tibia_mask,
    "Expanded_2mm": tibia_2mm,
    "Expanded_4mm": tibia_4mm,
    "Random_1": rand_tibia_1,
    "Random_2": rand_tibia_2
}

landmark_file = os.path.join(RESULT_DIR, "tibial_landmarks.txt")
with open(landmark_file, "w") as f:
    f.write("Mask\tmed_x\tmed_y\tmed_z\tmed_mm_x\tmed_mm_y\tmed_mm_z\t"
            "lat_x\tlat_y\tlat_z\tlat_mm_x\tlat_mm_y\tlat_mm_z\n")
    for name, mask in masks.items():
        medial_vox, lateral_vox = find_medial_lateral_lowest(mask)
        medial_mm = voxel_to_phys(mask, medial_vox)
        lateral_mm = voxel_to_phys(mask, lateral_vox)
        f.write(f"{name}\t"
                f"{medial_vox[0]}\t{medial_vox[1]}\t{medial_vox[2]}\t"
                f"{medial_mm[0]:.2f}\t{medial_mm[1]:.2f}\t{medial_mm[2]:.2f}\t"
                f"{lateral_vox[0]}\t{lateral_vox[1]}\t{lateral_vox[2]}\t"
                f"{lateral_mm[0]:.2f}\t{lateral_mm[1]:.2f}\t{lateral_mm[2]:.2f}\n")

print(f"✅ Landmarks saved to: {landmark_file}")
print("✅ Pipeline completed successfully.")

