#!/usr/bin/env python
# coding: utf-8

# In[36]:


"""
Segment tibia and femur from CT, save labeled mask and separate bone masks.
"""

import SimpleITK as sitk
import numpy as np
import os

def segment_bones(image_path, output_dir="results"):
    """
    Segments tibia and femur regions from a CT image.
    Saves: labeled mask, tibia mask, femur mask.
    Returns: labeled SimpleITK image.
    """
    ct = sitk.ReadImage(image_path)
    bone_mask = sitk.BinaryThreshold(ct, lowerThreshold=260, upperThreshold=3000, insideValue=1, outsideValue=0)

    closing = sitk.BinaryMorphologicalClosingImageFilter()
    closing.SetKernelRadius(2)
    closing.SetForegroundValue(1)
    bone_mask = closing.Execute(bone_mask)

    bone_arr = sitk.GetArrayFromImage(bone_mask)
    z_split = bone_arr.shape[0] // 2 - 5
    tibia_arr = np.zeros_like(bone_arr)
    femur_arr = np.zeros_like(bone_arr)
    tibia_arr[z_split:] = bone_arr[z_split:]
    femur_arr[:z_split] = bone_arr[:z_split]

    labeled_arr = np.zeros_like(bone_arr)
    labeled_arr[tibia_arr == 1] = 1
    labeled_arr[femur_arr == 1] = 2

    labeled_img = sitk.GetImageFromArray(labeled_arr)
    labeled_img.CopyInformation(ct)

    os.makedirs(output_dir, exist_ok=True)
    sitk.WriteImage(labeled_img, os.path.join(output_dir, "bone_segmented.nii.gz"))

    tibia_img = sitk.GetImageFromArray(tibia_arr.astype(np.uint8))
    femur_img = sitk.GetImageFromArray(femur_arr.astype(np.uint8))
    tibia_img.CopyInformation(ct)
    femur_img.CopyInformation(ct)
    sitk.WriteImage(tibia_img, os.path.join(output_dir, "mask_tibia.nii.gz"))
    sitk.WriteImage(femur_img, os.path.join(output_dir, "mask_femur.nii.gz"))

    print("✅ Saved bone_segmented.nii.gz, mask_tibia.nii.gz, and mask_femur.nii.gz")

    return labeled_img, ct

