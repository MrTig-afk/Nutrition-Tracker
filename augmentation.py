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
        print(f"Error during greyscale conversion for {filename}: {e}")

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
        print(f"Error during brightness augmentation for {filename}: {e}")

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
        print(f"Error during contrast augmentation for {filename}: {e}")

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
        print("Error during Gaussian Blur for {filename}:{e}")

def generate_warps(folder_path, save_dir):

    def find_coeffs(pa, pb):
        matrix = []
        for p1, p2 in zip(pa, pb):
            matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
            matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])
        A = np.array(matrix, dtype=np.float64)
        B = np.array(pb).reshape(8)
        return np.linalg.lstsq(A, B, rcond=None)[0]

    for filename in os.listdir(folder_path):
        try:
            image_path = os.path.join(folder_path, filename)
            image = Image.open(image_path)
            w, h = image.size

            src = [(0, 0), (w, 0), (w, h), (0, h)]

            skew_types = {
                "left_skew": [
                    (0.05 * w, 0.05 * h),
                    (0.95 * w, 0.08 * h),
                    (0.9 * w, 0.95 * h),
                    (0.1 * w, 0.9 * h)
                ],
                "right_skew": [
                    (0.1 * w, 0.1 * h),
                    (0.95 * w, 0),
                    (0.9 * w, 0.9 * h),
                    (0.05 * w, 0.95 * h)
                ],
                "top_skew": [
                    (0.05 * w, 0.0),
                    (0.95 * w, 0.0),
                    (0.9 * w, 0.9 * h),
                    (0.1 * w, 0.9 * h)
                ],
                "bottom_skew": [
                    (0.05 * w, 0.1 * h),
                    (0.95 * w, 0.1 * h),
                    (0.9 * w, h),
                    (0.1 * w, h)
                ]
            }

            for label, dst in skew_types.items():
                coeffs = find_coeffs(dst, src)
                warped = image.transform((w, h), Image.PERSPECTIVE, coeffs, resample=Image.BICUBIC)
                name, ext = os.path.splitext(filename)
                new_filename = f"{name}_{label}{ext}"
                warped.save(os.path.join(save_dir, new_filename))

            print(f"✅ Generated perspective variants for all images")

        except Exception as e:
            print(f"❌ Error with {filename}: {e}")
