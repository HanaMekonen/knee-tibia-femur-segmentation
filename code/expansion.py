#!/usr/bin/env python
# coding: utf-8

# In[39]:


"""
expansion.py
Provides a function to expand a binary mask and save it to a file.
"""

import SimpleITK as sitk
import numpy as np
import os

def expand_mask_by_mm(mask: sitk.Image, expansion_mm: float) -> sitk.Image:
    """
    Expand a binary mask by a specified number of millimeters.

    Args:
        mask (sitk.Image): Binary input mask.
        expansion_mm (float): Expansion distance in mm.

    Returns:
        sitk.Image: Expanded binary mask.
    """
    spacing = np.array(mask.GetSpacing())  # Voxel spacing in (x, y, z)
    radius_voxels = [int(np.ceil(expansion_mm / s)) for s in spacing]
    expanded = sitk.BinaryDilate(mask, radius_voxels)
    return expanded

def expand_and_save(mask: sitk.Image, expansion_mm: float, save_path: str):
    """
    Expands a mask and saves it to a NIfTI file.

    Args:
        mask (sitk.Image): Binary input mask.
        expansion_mm (float): Expansion distance in mm.
        save_path (str): File path to save the expanded mask.
    """
    expanded = expand_mask_by_mm(mask, expansion_mm)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    sitk.WriteImage(expanded, save_path)
    print(f"✅ Expanded mask ({expansion_mm}mm) saved to: {save_path}")
    return expanded

