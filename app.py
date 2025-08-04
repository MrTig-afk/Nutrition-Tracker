import os
from utils.augmentation import image_augmentation, count_images

raw_images= r"INPUT PATH TO RAW IMAGES HERE" #The directory you used to save the downloaded images
augmented_folder=r"PATH FOR DIRECTORY TO SAVE AUGMENTED IMAGES"

print(f"Number of images: {count_images(augmented_folder)}")

image_augmentation(raw_images, augmented_folder)

print(f"Number of images after new batch: {count_images(augmented_folder)}")