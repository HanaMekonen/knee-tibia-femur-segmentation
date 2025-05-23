#!/usr/bin/env python
# coding: utf-8

# In[43]:


"""
Randomizes expansion of tibia and femur masks separately and saves combined mask.
"""

import SimpleITK as sitk
import numpy as np
import os
import scipy.ndimage as ndi

def randomize_mask_distance_based(original_mask: sitk.Image, ct_image: sitk.Image, max_mm: float, seed=None) -> sitk.Image:
    """
    Randomly expands a binary mask by a distance ≤ max_mm (in mm), preserving original.

    Args:
        original_mask (sitk.Image): Binary mask (0 or 1).
        ct_image (sitk.Image): Corresponding CT image for spacing.
        max_mm (float): Maximum allowed random expansion in mm.
        seed (int): Optional seed for reproducibility.

    Returns:
        sitk.Image: Randomly expanded binary mask.
    """
    np.random.seed(seed)
    mask_array = sitk.GetArrayFromImage(original_mask)
    spacing = ct_image.GetSpacing()
    dist_map = ndi.distance_transform_edt(mask_array == 0, sampling=spacing)
    r_mm = np.random.uniform(0.0, max_mm)
    new_arr = (mask_array == 1) | (dist_map <= r_mm)

    new_mask = sitk.GetImageFromArray(new_arr.astype(np.uint8))
    new_mask.CopyInformation(original_mask)
    return new_mask

def combine_and_save_masks(ct_image: sitk.Image, tibia_mask: sitk.Image, femur_mask: sitk.Image, save_path: str) -> sitk.Image:
    """
    Combines tibia and femur masks with different labels and saves to NIfTI.

    Args:
        ct_image (sitk.Image): CT scan to copy spatial info.
        tibia_mask (sitk.Image): Binary tibia mask (1).
        femur_mask (sitk.Image): Binary femur mask (1).
        save_path (str): Path to save the labeled mask.
    
    Returns:
        sitk.Image: Combined label image (1=tibia, 2=femur).
    """
    tibia_arr = sitk.GetArrayFromImage(tibia_mask)
    femur_arr = sitk.GetArrayFromImage(femur_mask)

    labeled_arr = np.zeros_like(tibia_arr)
    labeled_arr[tibia_arr == 1] = 1
    labeled_arr[femur_arr == 1] = 2

    labeled_img = sitk.GetImageFromArray(labeled_arr)
    labeled_img.CopyInformation(ct_image)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    sitk.WriteImage(labeled_img, save_path)
    print(f"✅ Combined randomized mask saved at: {save_path}")

    return labeled_img

