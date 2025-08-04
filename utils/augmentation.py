import os
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

def image_augmentation(input_dir, save_dir):
    """
    Applies brightness, contrast, Gaussian blur, and perspective warp augmentations
    on all images in input_dir and saves results to save_dir.
    """

    def find_coeffs(pa, pb):
        matrix = []
        for p1, p2 in zip(pa, pb):
            matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
            matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])
        A = np.array(matrix, dtype=np.float64)
        B = np.array(pb).reshape(8)
        return np.linalg.lstsq(A, B, rcond=None)[0]

    def apply_brightness(image, name, ext):
        for factor in [0.2, 0.4, 1.2, 1.4]:
            enhancer = ImageEnhance.Brightness(image)
            enhanced = enhancer.enhance(factor)
            new_filename = f"{name}_brightness_{factor}{ext}"
            enhanced.save(os.path.join(save_dir, new_filename))

    def apply_contrast(image, name, ext):
        for factor in [1.2, 1.4, 1.6, 1.8, 2]:
            enhancer = ImageEnhance.Contrast(image)
            enhanced = enhancer.enhance(factor)
            new_filename = f"{name}_contrast_{factor}{ext}"
            enhanced.save(os.path.join(save_dir, new_filename))

    def apply_blur(image, name, ext):
        blurred = image.filter(ImageFilter.GaussianBlur(radius=1))
        new_filename = f"{name}_gaussianblur{ext}"
        blurred.save(os.path.join(save_dir, new_filename))

    def apply_perspective_warp(image, name, ext):
        w, h = image.size
        src = [(0, 0), (w, 0), (w, h), (0, h)]

        skew_types = {
            "left_skew": [
                (0.05 * w, 0.05 * h),
                (0.95 * w, 0.08 * h),
                (0.9 * w, 0.95 * h),
                (0.1 * w, 0.9 * h),
            ],
            "right_skew": [
                (0.1 * w, 0.1 * h),
                (0.95 * w, 0),
                (0.9 * w, 0.9 * h),
                (0.05 * w, 0.95 * h),
            ],
            "top_skew": [
                (0.05 * w, 0.0),
                (0.95 * w, 0.0),
                (0.9 * w, 0.9 * h),
                (0.1 * w, 0.9 * h),
            ],
            "bottom_skew": [
                (0.05 * w, 0.1 * h),
                (0.95 * w, 0.1 * h),
                (0.9 * w, h),
                (0.1 * w, h),
            ],
        }

        for label, dst in skew_types.items():
            coeffs = find_coeffs(dst, src)
            warped = image.transform((w, h), Image.PERSPECTIVE, coeffs, resample=Image.BICUBIC)
            new_filename = f"{name}_{label}{ext}"
            warped.save(os.path.join(save_dir, new_filename))

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for filename in os.listdir(input_dir):
        try:
            image_path = os.path.join(input_dir, filename)
            image = Image.open(image_path).convert("RGB")  # Ensure RGB
            name, ext = os.path.splitext(filename)

            apply_brightness(image, name, ext)
            apply_contrast(image, name, ext)
            apply_blur(image, name, ext)
            apply_perspective_warp(image, name, ext)

        except Exception as e:
            print(f"❌ Error with {filename}: {e}")

    print("✅ Image augmentations complete.")

def count_images(directory, extensions={".jpg", ".jpeg", ".png", ".bmp", ".tiff"}):
    image_files = [f for f in os.listdir(directory) if os.path.splitext(f)[1].lower() in extensions]
    return len(image_files)

