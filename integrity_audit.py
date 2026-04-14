import os
import shutil
from PIL import Image

# Paths
source_dir = '/sdcard/Pictures'
dupe_dir = '/sdcard/Potential_Duplicates'

def get_visual_hash(image_path):
    try:
        with Image.open(image_path) as img:
            # Resize and grayscale to make it size-independent
            img = img.convert('L').resize((8, 8), Image.Resampling.LANCZOS)
            pixels = list(img.getdata())
            avg = sum(pixels) / len(pixels)
            return "".join(['1' if p >= avg else '0' for p in pixels])
    except Exception:
        return None

# Map of hash -> (path, size)
kept_files = {}

print(f"Step 1: Indexing files in {source_dir}...")
for root, dirs, files in os.walk(source_dir):
    if dupe_dir in root: continue # Safety check
    for filename in files:
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            path = os.path.join(root, filename)
            v_hash = get_visual_hash(path)
            if v_hash:
                size = os.path.getsize(path)
                # If multiple exist in Pictures, track the largest for comparison
                if v_hash not in kept_files or size > kept_files[v_hash][1]:
                    kept_files[v_hash] = (path, size)

print(f"Step 2: Auditing {dupe_dir} for better versions...")
swapped_count = 0

for filename in os.listdir(dupe_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        dupe_path = os.path.join(dupe_dir, filename)
        v_hash = get_visual_hash(dupe_path)
        
        if v_hash and v_hash in kept_files:
            kept_path, kept_size = kept_files[v_hash]
            dupe_size = os.path.getsize(dupe_path)
            
            # If the "duplicate" we moved is actually LARGER, swap them
            if dupe_size > kept_size:
                print(f"[QUALITY IMPROVEMENT] Swapping {filename} ({dupe_size} bytes) with kept version ({kept_size} bytes)")
                
                # Move kept small version to a temp location
                temp_small_path = os.path.join(dupe_dir, f"smaller_{os.path.basename(kept_path)}")
                # Ensure no collision in dupe_dir
                counter = 1
                while os.path.exists(temp_small_path):
                    temp_small_path = os.path.join(dupe_dir, f"smaller_{counter}_{os.path.basename(kept_path)}")
                    counter += 1
                
                try:
                    shutil.move(kept_path, temp_small_path)
                    shutil.move(dupe_path, kept_path)
                    # Update index to the new larger file
                    kept_files[v_hash] = (kept_path, dupe_size)
                    swapped_count += 1
                except Exception as e:
                    print(f"Error during swap: {e}")

print(f"\nAudit complete! Swapped {swapped_count} files to keep the higher-quality versions.")
