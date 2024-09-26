# Image Compression Script

This Python script provides functionality to compress images in a folder, optimizing them for web use while maintaining quality. It uses PyTorch for image processing and saves the compressed images in WebP format.

## Features

- Compresses images to a target file size (default 100KB) while trying to maintain the highest possible quality
- Uses WebP format for better compression
- Utilizes GPU acceleration if available
- Processes multiple images in parallel using ThreadPoolExecutor
- Automatically resizes very large images before compression

## Requirements

- Python 3.6+
- PyTorch
- torchvision
- Pillow (PIL)

## Installation

1. Ensure you have Python 3.6 or higher installed on your system.

2. Install the required packages using pip:

   ```
   pip install torch torchvision Pillow
   ```

   Note: For GPU support, make sure to install the appropriate CUDA version of PyTorch. Refer to the [official PyTorch website](https://pytorch.org/get-started/locally/) for installation instructions specific to your system.

3. Clone or download this script to your local machine.

## Usage

1. Open the script in a text editor.

2. Modify the `input_folder` and `output_folder` variables at the bottom of the script to point to your input and output directories:

   ```python
   input_folder = "path/to/your/input/folder"
   output_folder = "path/to/your/output/folder"
   ```

3. Run the script:

   ```
   python image_compression_script.py
   ```

   Replace `image_compression_script.py` with the actual name of the script file.

4. The script will process all images in the input folder and save the compressed versions in the output folder.

## Customization

You can adjust the following parameters in the `compress_images_in_folder` function call:

- `quality`: Initial JPEG quality (default: 95)
- `max_size_kb`: Target maximum file size in KB (default: 100)
- `max_workers`: Number of parallel workers for processing (default: 4)

Example:

```python
compress_images_in_folder(input_folder, output_folder, quality=90, max_size_kb=150, max_workers=8)
```

## How It Works

1. The script first attempts to compress the image using high-quality settings.
2. If the resulting file is larger than the target size, it uses a binary search algorithm to find the optimal quality setting.
3. If the image is still too large after quality reduction, it gradually resizes the image until the target size is met.
4. The script utilizes PyTorch for image processing, which allows for GPU acceleration if available.
5. Multiple images are processed in parallel using Python's ThreadPoolExecutor.

## Notes

- The script currently supports PNG, JPG, JPEG, and WebP input formats.
- All output images are saved in WebP format for better compression.
- Very large images (larger than 2048px in any dimension) are automatically resized before compression to improve processing speed.

## License

This script is provided as-is under the MIT License. Feel free to modify and distribute it as needed.
