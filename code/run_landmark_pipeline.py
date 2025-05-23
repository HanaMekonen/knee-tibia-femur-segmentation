#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""
run_landmark_pipeline.py
Generates expanded and randomized tibia masks and computes tibial landmarks.
"""

import os
import SimpleITK as sitk
from landmark_utils import (
    expand_mask_by_mm,
    randomize_mask_distance_based,
    find_medial_lateral_lowest,
    voxel_to_phys
)

def run_landmark_detection(orig_path, ct_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    ct = sitk.ReadImage(ct_path)
    orig = sitk.ReadImage(orig_path)

    # Create variants of the original mask
    masks = {
        "Original":     orig,
        "Expanded_2mm": expand_mask_by_mm(orig, 2.0),
        "Expanded_4mm": expand_mask_by_mm(orig, 4.0),
        "Random_1":     randomize_mask_distance_based(orig, 2.0, seed=1),
        "Random_2":     randomize_mask_distance_based(orig, 2.0, seed=2),
    }

    # Save each mask
    for name, img in masks.items():
        save_path = os.path.join(output_dir, f"mask_tibia_{name.lower()}.nii.gz")
        sitk.WriteImage(img, save_path)
        print(f"✅ Saved {name} mask → {save_path}")

    # Write landmark coordinates
    landmark_txt = os.path.join(output_dir, "tibial_landmarks.txt")
    with open(landmark_txt, "w") as f:
        f.write("Mask\tmed_x\tmed_y\tmed_z\tmed_mm_x\tmed_mm_y\tmed_mm_z\t"
                "lat_x\tlat_y\tlat_z\tlat_mm_x\tlat_mm_y\tlat_mm_z\n")
        for name, img in masks.items():
            medial_vox, lateral_vox = find_medial_lateral_lowest(img)
            medial_mm = voxel_to_phys(img, medial_vox)
            lateral_mm = voxel_to_phys(img, lateral_vox)

            f.write(
                f"{name}\t"
                f"{medial_vox[0]}\t{medial_vox[1]}\t{medial_vox[2]}\t"
                f"{medial_mm[0]:.2f}\t{medial_mm[1]:.2f}\t{medial_mm[2]:.2f}\t"
                f"{lateral_vox[0]}\t{lateral_vox[1]}\t{lateral_vox[2]}\t"
                f"{lateral_mm[0]:.2f}\t{lateral_mm[1]:.2f}\t{lateral_mm[2]:.2f}\n"
            )
    print(f"✅ Landmark coordinates saved to: {landmark_txt}")


if __name__ == "__main__":
    run_landmark_detection(
        orig_path="results/mask_tibia.nii.gz",
        ct_path="3702_left_knee.nii.gz",
        output_dir="results"
    )

