#!/usr/bin/env python
# coding: utf-8

# In[46]:


"""
landmark_utils.py
Helper functions for tibial mask expansion, randomization, and landmark extraction.
"""

import SimpleITK as sitk
import numpy as np


def expand_mask_by_mm(mask: sitk.Image, mm: float) -> sitk.Image:
    spacing = np.array(mask.GetSpacing())
    radii = [int(np.ceil(mm / s)) for s in spacing]
    return sitk.BinaryDilate(mask, radii)


def randomize_mask_distance_based(orig_mask: sitk.Image, max_mm: float, seed=None) -> sitk.Image:
    np.random.seed(seed)
    r = float(np.random.uniform(0.0, max_mm))

    dist_map = sitk.SignedMaurerDistanceMap(
        sitk.Cast(orig_mask, sitk.sitkUInt8),
        insideIsPositive=False,
        useImageSpacing=True
    )
    expanded = sitk.LessEqual(dist_map, r)
    randomized = sitk.Or(orig_mask, expanded)
    return sitk.Cast(randomized, sitk.sitkUInt8)


def find_medial_lateral_lowest(mask: sitk.Image):
    arr = sitk.GetArrayFromImage(mask)
    zs = np.where(np.any(arr > 0, axis=(1, 2)))[0]
    if len(zs) == 0:
        raise RuntimeError("Mask is empty.")
    z_low = int(zs.max())
    ys, xs = np.where(arr[z_low] > 0)
    lateral = (int(xs.min()), int(ys[xs.argmin()]), z_low)
    medial = (int(xs.max()), int(ys[xs.argmax()]), z_low)
    return medial, lateral


def voxel_to_phys(mask: sitk.Image, idx):
    return mask.TransformIndexToPhysicalPoint(idx)

