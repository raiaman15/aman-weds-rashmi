#!/usr/bin/env python3
from PIL import Image
import os

# Path to images
img_dir = "assets/img"
images = {
    "venue-day.png": (1466, 1080),
    "venue-night.png": (1466, 1080),
    "wedding-invitation-card.png": None  # Keep original size
}

for img_name, target_size in images.items():
    img_path = os.path.join(img_dir, img_name)
    
    if os.path.exists(img_path):
        # Get original size
        original_size = os.path.getsize(img_path) / (1024 * 1024)  # MB
        
        # Open and compress image
        img = Image.open(img_path)
        original_dims = img.size
        
        # Resize if target size specified
        if target_size:
            img = img.resize(target_size, Image.Resampling.LANCZOS)
        
        # Convert to RGB if necessary (removes alpha channel for better compression)
        if img.mode in ('RGBA', 'LA', 'P'):
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = rgb_img
        
        # Save with compression
        img.save(img_path, 'PNG', optimize=True, quality=85)
        
        # Get new size
        new_size = os.path.getsize(img_path) / (1024 * 1024)  # MB
        reduction = ((original_size - new_size) / original_size) * 100
        
        print(f"{img_name}:")
        print(f"  Original: {original_size:.2f} MB ({original_dims[0]}x{original_dims[1]})")
        if target_size:
            print(f"  Resized to: {target_size[0]}x{target_size[1]}")
        print(f"  Compressed: {new_size:.2f} MB")
        print(f"  Reduction: {reduction:.1f}%\n")
