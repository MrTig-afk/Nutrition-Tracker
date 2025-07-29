import os

from augmentation import convert_greyscale, change_brightness,change_contrast,add_blur,generate_warps

raw_images= r"D:\Projects\Calories\Raw_Images"
greyscale_folder= r"D:\Projects\Calories\Greyscale_images"
brightness_aug_folder= "D:\Projects\Calories\Brightness_aug"
contrast_aug_folder="D:\Projects\Calories\Contrast_aug"
gaussian_aug_folder="D:\Projects\Calories\Gaussian_aug"
perspective_transform_folder="D:\Projects\Calories\perspective_transform_aug"

#convert_greyscale(raw_images,greyscale_folder)
#change_brightness(greyscale_folder,brightness_aug_folder)
#change_contrast(greyscale_folder, contrast_aug_folder)
#add_blur(greyscale_folder,gaussian_aug_folder)
generate_warps(greyscale_folder, perspective_transform_folder)