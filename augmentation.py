'''
1. greyscale
2. brightness adjustments
3. contrast adjustments
4. gaussian blur
5. rotation
6. add shadows
7. scaling

Introduce cropping by the user

Use libraries like Pillow, OpenCV, albumentations or imgaug for image augmentation. Use whichever is easiest to implement.
'''

from PIL import Image, ImageEnhance
import os

def convert_greyscale(folder_path, save_dir):
    try:
        for filename in os.listdir(folder_path):
            image_path = os.path.join(folder_path, filename)
            image = Image.open(image_path)
            greyscale_image = image.convert("L")
            name, ext = os.path.splitext(filename)
            new_filename = f"{name}_greyscale{ext}"
            save_path = os.path.join(save_dir, new_filename)
            greyscale_image.save(save_path)
        print("Converted all images to greyscale successfully.")
    except Exception as e:
        print(f"Error during greyscale conversion: {e}")

def change_brightness(folder_path, save_dir):
    try:
        for filename in os.listdir(folder_path):
            image_path = os.path.join(folder_path, filename)
            image = Image.open(image_path)
            enhancer = ImageEnhance.Brightness(image)
            name, ext = os.path.splitext(filename)
            for factor in [0.2, 0.4, 1.2, 1.4]:
                enhanced_image = enhancer.enhance(factor)
                new_filename = f"{name}_brightness_{factor}{ext}"
                save_path = os.path.join(save_dir, new_filename)
                enhanced_image.save(save_path)
        print("Brightness augmentation done successfully on all images.")
    except Exception as e:
        print(f"Error during brightness augmentation: {e}")


