'''
1. greyscale DONE
2. brightness adjustments DONE
3. contrast adjustments DONE
4. gaussian blur DONE
5. rotation Applied perspective transform, but need to understadn logic
6. add shadows
7. scaling

Introduce cropping by the user

Use libraries like Pillow, OpenCV, albumentations or imgaug for image augmentation. Use whichever is easiest to implement.
'''

from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
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

def change_contrast(folder_path, save_dir):
    try:
        for filename in os.listdir(folder_path):
            image_path= os.path.join(folder_path,filename)
            image= Image.open(image_path)
            enhancer= ImageEnhance.Contrast(image)
            name,ext= os.path.splitext(filename)
            for factor in [1.2 , 1.4, 1.6, 1.8, 2]:
                enhanced_image= enhancer.enhance(factor)
                new_filename= f"{name}_contrast{factor}{ext}"
                save_path= os.path.join(save_dir, new_filename)
                enhanced_image.save(save_path)
        print("Contrast augmentation done successfully on all images.")
    except Exception as e:
        print(f"Error during contrast augmentation: {e}")

def add_blur(folder_path, save_dir):
    try:
        for filename in os.listdir(folder_path):
            image_path= os.path.join(folder_path,filename)
            image= Image.open(image_path)
            enhanced_image= image.filter(ImageFilter.GaussianBlur(radius=1))
            name,ext= os.path.splitext(filename)
            new_filename= f"{name}_GaussianBlue{ext}"
            save_path= os.path.join(save_dir,new_filename)
            enhanced_image.save(save_path)
        print("Gaussian Blur done successfully on all images ")    
    except Exception as e:
        print("Error during Gaussian Blur")
    
from PIL import Image
import os

def apply_perspective_transform(folder_path, save_dir):
    try:
        for filename in os.listdir(folder_path):
            image_path = os.path.join(folder_path, filename)
            image = Image.open(image_path)
            width, height = image.size

            # Source points (corners of original image)
            src = [
                (0, 0),                       # Top-left
                (width, 0),                   # Top-right
                (width, height),              # Bottom-right
                (0, height)                   # Bottom-left
            ]

            # Destination points (slightly moved corners)
            dst = [
                (0.05 * width, 0.05 * height),    # Top-left inward
                (0.95 * width, 0.08 * height),    # Top-right inward
                (0.9 * width, 0.95 * height),     # Bottom-right inward
                (0.1 * width, 0.9 * height)       # Bottom-left inward
            ]

            # Function to calculate perspective coefficients
            def find_coeffs(pa, pb):
                import numpy as np
                matrix = []
                for p1, p2 in zip(pa, pb):
                    matrix.append([p1[0], p1[1], 1, 0, 0, 0,
                                  -p2[0]*p1[0], -p2[0]*p1[1]])
                    matrix.append([0, 0, 0, p1[0], p1[1], 1,
                                  -p2[1]*p1[0], -p2[1]*p1[1]])
                A = np.array(matrix, dtype=np.float64)
                B = np.array(pb).reshape(8)
                res = np.linalg.lstsq(A, B, rcond=None)[0]
                return res

            coeffs = find_coeffs(dst, src)

            transformed = image.transform(
                (width, height),
                Image.PERSPECTIVE,
                coeffs,
                resample=Image.BICUBIC
            )

            name, ext = os.path.splitext(filename)
            new_filename = f"{name}_perspective{ext}"
            save_path = os.path.join(save_dir, new_filename)
            transformed.save(save_path)

        print("✅ Perspective transformation done successfully on all images.")
    
    except Exception as e:
        print("❌ Error during perspective transformation:", e)

    


    




