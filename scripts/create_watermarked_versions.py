#!/usr/bin/env python3
"""
Create watermarked versions of images for lightbox usage.
Original images remain clean for thumbnails.
Uses Chemachinb.png logo as watermark.
"""

import os
from pathlib import Path
from PIL import Image

def add_watermark_logo(image_path, output_path, logo_path, opacity=0.35, size_percent=65):
    """Add logo as watermark to an image."""
    try:
        # Open base image
        img = Image.open(image_path)
        
        # Convert to RGB if needed
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Convert to RGBA to support transparency
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Open logo
        logo = Image.open(logo_path)
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')
        
        # Calculate new logo size (% of image width)
        logo_width = int(img.width * (size_percent / 100))
        aspect_ratio = logo.height / logo.width
        logo_height = int(logo_width * aspect_ratio)
        logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
        
        # Adjust logo opacity
        alpha = logo.split()[3]
        alpha = alpha.point(lambda p: int(p * opacity))
        logo.putalpha(alpha)
        
        # Calculate center position
        x = (img.width - logo_width) // 2
        y = (img.height - logo_height) // 2
        
        # Create layer for compositing
        watermark_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
        watermark_layer.paste(logo, (x, y), logo)
        
        # Composite logo over image
        img = Image.alpha_composite(img, watermark_layer)
        
        # Save as JPG
        if output_path.lower().endswith(('.jpg', '.jpeg')):
            img = img.convert('RGB')
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path, quality=95)
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    # Paths
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    originals_dir = project_dir / 'private-originals'  # Private originals (not in repo)
    gallery_dir = project_dir / 'content' / 'gallery'   # Hugo uses these (watermarked)
    watermarked_dir = project_dir / 'static' / 'gallery-watermarked'
    logo_path = project_dir / 'themes' / 'gallery' / 'static' / 'images' / 'Chemachineb.png'
    
    # Check if logo exists
    if not logo_path.exists():
        print(f"✗ Logo not found: {logo_path}")
        return
    
    # Check if originals exist
    if not originals_dir.exists():
        print(f"✗ Originals folder not found: {originals_dir}")
        return
    
    # Create folders
    watermarked_dir.mkdir(parents=True, exist_ok=True)
    gallery_dir.mkdir(parents=True, exist_ok=True)
    
    # Process images
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    files = [f for f in originals_dir.glob('*') if f.suffix.lower() in image_extensions]
    
    print(f"Creating logo watermarked versions...")
    print(f"Logo: {logo_path.name}")
    print(f"Originals (private): private-originals/")
    print(f"Output for Hugo: content/gallery/")
    print(f"Output for lightbox: static/gallery-watermarked/\n")
    
    success = 0
    for img_file in sorted(files):
        # Create watermarked version for lightbox
        watermarked_file = watermarked_dir / img_file.name
        # Create watermarked version for Hugo processing
        gallery_file = gallery_dir / img_file.name
        
        if add_watermark_logo(str(img_file), str(watermarked_file), str(logo_path), opacity=0.65, size_percent=40):
            # Copy to gallery folder too
            watermarked_file_obj = Path(watermarked_file)
            if watermarked_file_obj.exists():
                import shutil
                shutil.copy2(str(watermarked_file), str(gallery_file))
            print(f"✓ {img_file.name}")
            success += 1
    
    print(f"\n✓ {success}/{len(files)} watermarked versions created")
    print(f"\nNOTE: Original images are kept private in private-originals/")
    print(f"      Only watermarked versions are published online.")

if __name__ == '__main__':
    main()
