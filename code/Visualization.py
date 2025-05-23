#!/usr/bin/env python
# coding: utf-8

# ### Display coronal view of tibia and femur segmentation.

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
import SimpleITK as sitk

def show_bone_overlay(ct, labeled_img):
    """
    Show coronal mid-slice with overlay for tibia (red) and femur (green).
    """
    ct_arr = sitk.GetArrayFromImage(ct)
    label_arr = sitk.GetArrayFromImage(labeled_img)

    y_mid = ct_arr.shape[1] // 2
    slice_img = ct_arr[:, y_mid, :]
    slice_label = label_arr[:, y_mid, :]

    rgb = np.stack([slice_img]*3, axis=-1)
    rgb = (rgb - rgb.min()) / (rgb.max() - rgb.min())

    overlay = np.zeros_like(rgb)
    overlay[slice_label == 1] = [1, 0.5, 0.5]   # Tibia = light red
    overlay[slice_label == 2] = [0.5, 1, 0.5]   # Femur = light green

    alpha = 0.5
    rgb = (1 - alpha) * rgb + alpha * overlay

    plt.figure(figsize=(6, 6))
    plt.imshow(rgb)
    plt.title("Segmented Bones: Tibia (Light Red), Femur (Light Green)")
    plt.axis('off')
    plt.show()


# In[ ]:


# Run from code folder or main script
from segmentation import segment_bones
from visualize import show_bone_overlay

labeled_img, ct = segment_bones("3702_left_knee.nii.gz")
show_bone_overlay(ct, labeled_img)


# ### Displays a coronal slice with the expanded mask overlaid on CT.

# In[ ]:


import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt

def show_coronal_overlay(ct_image: sitk.Image, mask: sitk.Image, overlay_color='spring', title='Coronal Overlay'):
    """
    Displays the coronal mid-slice of CT with a colored mask overlay.

    Args:
        ct_image (sitk.Image): CT volume.
        mask (sitk.Image): Expanded or original mask.
        overlay_color (str): Matplotlib colormap for the overlay.
        title (str): Plot title.
    """
    ct_array = sitk.GetArrayFromImage(ct_image)
    mask_array = sitk.GetArrayFromImage(mask)

    y_mid = ct_array.shape[1] // 2
    ct_slice = ct_array[:, y_mid, :]
    mask_slice = mask_array[:, y_mid, :]

    plt.figure(figsize=(6, 6))
    plt.imshow(ct_slice, cmap='gray')
    plt.imshow(
        np.ma.masked_where(mask_slice == 0, mask_slice),
        cmap=overlay_color,
        alpha=0.5
    )
    plt.title(title)
    plt.axis('off')
    plt.show()


# In[ ]:


from expansion import expand_and_save
from visualize_expansion import show_coronal_overlay
import SimpleITK as sitk

# Load input
ct = sitk.ReadImage("3702_left_knee.nii.gz")
mask = sitk.ReadImage("results/bone_segmented.nii.gz")

# Expand and save
expanded_mask = expand_and_save(mask, expansion_mm=2.0, save_path="results/mask_bone_expanded_2mm.nii.gz")

# Display
show_coronal_overlay(ct_image=ct, mask=expanded_mask, title="bone Mask Expanded by 2mm")


# ### Visualizes coronal view of randomized tibia and femur masks

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
import SimpleITK as sitk

def show_randomized_overlay(ct_image: sitk.Image, labeled_mask: sitk.Image):
    """
    Displays the randomized tibia (blue) and femur (green) overlay in coronal view.

    Args:
        ct_image (sitk.Image): CT volume.
        labeled_mask (sitk.Image): Labeled mask with 1=tibia, 2=femur.
    """
    ct_arr = sitk.GetArrayFromImage(ct_image)
    mask_arr = sitk.GetArrayFromImage(labeled_mask)

    y_mid = ct_arr.shape[1] // 2
    ct_slice = ct_arr[:, y_mid, :]
    mask_slice = mask_arr[:, y_mid, :]

    rgb = np.stack([ct_slice]*3, axis=-1)
    rgb = (rgb - rgb.min()) / (rgb.max() - rgb.min())

    overlay = np.zeros_like(rgb)
    overlay[mask_slice == 1] = [0.4, 0.8, 1.0]  # Tibia = Blue
    overlay[mask_slice == 2] = [0.5, 1.0, 0.5]  # Femur = Green

    alpha = 0.5
    rgb = (1 - alpha) * rgb + alpha * overlay

    plt.figure(figsize=(6, 6))
    plt.imshow(rgb)
    plt.title("Randomized Contours: Tibia (Blue), Femur (Green)")
    plt.axis('off')
    plt.show()


# In[ ]:


from randomization import randomize_mask_distance_based, combine_and_save_masks
import SimpleITK as sitk

# Load inputs
ct = sitk.ReadImage("3702_left_knee.nii.gz")
labeled_mask = sitk.ReadImage("results/bone_segmented.nii.gz")

# Split tibia and femur masks
labeled_arr = sitk.GetArrayFromImage(labeled_mask)
tibia_arr = (labeled_arr == 1).astype(np.uint8)
femur_arr = (labeled_arr == 2).astype(np.uint8)

tibia_mask = sitk.GetImageFromArray(tibia_arr)
femur_mask = sitk.GetImageFromArray(femur_arr)
tibia_mask.CopyInformation(labeled_mask)
femur_mask.CopyInformation(labeled_mask)

# Randomize masks
rand_tibia = randomize_mask_distance_based(tibia_mask, ct, max_mm=2.0, seed=42)
rand_femur = randomize_mask_distance_based(femur_mask, ct, max_mm=2.0, seed=7)

# Combine and save
output_path = "results/bone_segmented_randomized.nii.gz"
combined_mask = combine_and_save_masks(ct, rand_tibia, rand_femur, output_path)

# Visualize
show_randomized_overlay(ct, combined_mask)


# ### Display Coronal Mid-Slice of Tibia Masks

# In[ ]:


import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt
import os

# Paths to the five tibia masks
mask_paths = [
    "results/mask_tibia.nii.gz",
    "results/mask_tibia_expanded_2mm.nii.gz",
    "results/mask_tibia_expanded_4mm.nii.gz",
    "results/mask_tibia_random_1.nii.gz",
    "results/mask_tibia_random_2.nii.gz",
]
titles = ["Original", "Expanded 2 mm", "Expanded 4 mm", "Random 1", "Random 2"]

def load_coronal_slice(mask_path):
    """
    Load the coronal mid-slice of a binary mask.
    Returns a 2D NumPy array of shape [Z, X].
    """
    img = sitk.ReadImage(mask_path)
    arr = sitk.GetArrayFromImage(img)  # [Z, Y, X]
    y_mid = arr.shape[1] // 2
    return arr[:, y_mid, :]

# Prepare the figure: 1 row × 5 columns
fig, axes = plt.subplots(1, 5, figsize=(15, 4))
for ax, path, title in zip(axes, mask_paths, titles):
    slice_2d = load_coronal_slice(path)
    ax.imshow(slice_2d, cmap='gray')
    ax.set_title(title)
    ax.axis('off')

plt.suptitle("Coronal Mid-Slice of Tibia Masks")
plt.tight_layout()
plt.show()

