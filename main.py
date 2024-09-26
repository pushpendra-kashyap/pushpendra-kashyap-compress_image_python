import os
import torch
import torchvision.transforms as transforms
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np

def compress_image(input_path, output_path, quality=95, max_size_kb=100):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
   
    # Open and convert image to RGB
    img = Image.open(input_path).convert('RGB')
   
    # Initial resize only if the image is very large
    max_dimension = 2048
    if max(img.size) > max_dimension:
        img.thumbnail((max_dimension, max_dimension), Image.LANCZOS)
   
    # Convert to tensor and move to device
    img_tensor = transforms.ToTensor()(img).unsqueeze(0).to(device)
   
    # Define transformations
    to_pil = transforms.ToPILImage()
   
    # First attempt: high quality compression
    img_pil = to_pil(img_tensor.squeeze(0).cpu())
    img_pil.save(output_path, "webp", quality=quality)
   
    output_size_kb = os.path.getsize(output_path) / 1024
   
    # Binary search for optimal quality
    min_quality, max_quality = 70, 98  # Increased minimum quality
    while output_size_kb > max_size_kb and max_quality - min_quality > 2:
        quality = (min_quality + max_quality) // 2
        img_pil.save(output_path, "webp", quality=quality)
        output_size_kb = os.path.getsize(output_path) / 1024
       
        if output_size_kb > max_size_kb:
            max_quality = quality
        else:
            min_quality = quality
   
    # If still over limit, resize gradually
    if output_size_kb > max_size_kb:
        scale_factor = 0.9
        while output_size_kb > max_size_kb and scale_factor > 0.5:
            new_size = tuple(int(dim * scale_factor) for dim in img.size)
            img_resized = img.resize(new_size, Image.LANCZOS)
            img_resized.save(output_path, "webp", quality=quality)
            output_size_kb = os.path.getsize(output_path) / 1024
            scale_factor -= 0.1
   
    print(f"Compressed {os.path.basename(input_path)}: {output_size_kb:.2f} KB, Quality={quality}%, Size={img.width}x{img.height}")

def compress_images_in_folder(input_folder, output_folder, quality=95, max_size_kb=100, max_workers=4):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
   
    def process_image(filename):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.webp')
            compress_image(input_path, output_path, quality=quality, max_size_kb=max_size_kb)
   
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_image, filename) for filename in os.listdir(input_folder)]
        for future in as_completed(futures):
            future.result()  # This will raise any exceptions that occurred during processing

if __name__ == "__main__":
    input_folder = "C:\\Users\\pushpendra kumar\\OneDrive\\Desktop\\file\\webp_images"
    output_folder = "C:\\Users\\pushpendra kumar\\OneDrive\\Desktop\\file\\output_images"
    compress_images_in_folder(input_folder, output_folder, quality=95, max_size_kb=100, max_workers=4)