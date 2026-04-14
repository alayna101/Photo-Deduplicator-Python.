import os
import hashlib
from PIL import Image
import shutil

# Paths
source_dir = '/sdcard/Pictures'
target_dir = '/sdcard/Potential_Duplicates'
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

def get_visual_hash(image_path):
    try:
        with Image.open(image_path) as img:
            # Resize and grayscale to make it size-independent
            img = img.convert('L').resize((8, 8), Image.Resampling.LANCZOS)
            pixels = list(img.getdata())
            avg = sum(pixels) / len(pixels)
            # Create a 64-bit fingerprint
            return "".join(['1' if p >= avg else '0' for p in pixels])
    except Exception:
        return None

hashes = {}
duplicates_count = 0

print(f"Scanning {source_dir}...")

for root, dirs, files in os.walk(source_dir):
    # Skip the duplicates folder if it's inside Pictures
    if target_dir in root:
        continue
        
    for filename in files:
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            path = os.path.join(root, filename)
            v_hash = get_visual_hash(path)
            
            if v_hash:
                if v_hash in hashes:
                    # Handle name collisions in target_dir
                    base_name = os.path.basename(filename)
                    dest_path = os.path.join(target_dir, base_name)
                    counter = 1
                    name_part, ext_part = os.path.splitext(base_name)
                    while os.path.exists(dest_path):
                        dest_path = os.path.join(target_dir, f"{name_part}_sim_{counter}{ext_part}")
                        counter += 1
                    
                    print(f"[DUPE FOUND] Moving: {filename}")
                    shutil.move(path, dest_path)
                    duplicates_count += 1
                else:
                    hashes[v_hash] = path

print(f"\nFinished! Found and moved {duplicates_count} potential duplicates to {target_dir}")
