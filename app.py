import os

from augmentation import convert_greyscale, change_brightness

raw_images= r"D:\Projects\Calories\Raw_Images"
greyscale_folder= r"D:\Projects\Calories\Greyscale_images"
brightness_aug_folder= "D:\Projects\Calories\Brightness_aug"

convert_greyscale(raw_images,greyscale_folder)
change_brightness(greyscale_folder,brightness_aug_folder)