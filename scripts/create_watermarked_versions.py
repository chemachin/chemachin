#!/usr/bin/env python3
"""
Crea versiones watermarked de las imágenes para usar en lightbox.
Las originales permanecen limpias para thumbnails.
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def add_watermark(image_path, output_path, watermark_text="CHEMACHIN", opacity=0.25):
    """Agrega watermark a una imagen."""
    try:
        img = Image.open(image_path)
        
        # Convertir a RGB si es necesario
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Crear capa para watermark
        watermark_layer = Image.new('RGBA', img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(watermark_layer)
        
        # Usar fuente del sistema
        try:
            font_size = int(img.width / 5)
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Calcular posición central
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (img.width - text_width) // 2
        y = (img.height - text_height) // 2
        
        # Color con opacidad
        alpha = int(255 * opacity)
        watermark_color = (255, 255, 255, alpha)
        
        # Dibujar texto
        draw.text((x, y), watermark_text, font=font, fill=watermark_color)
        
        # Compositar
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        img = Image.alpha_composite(img, watermark_layer)
        
        # Guardar
        if output_path.lower().endswith(('.jpg', '.jpeg')):
            img = img.convert('RGB')
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path, quality=95)
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    # Rutas
    script_dir = Path(__file__).parent
    gallery_dir = script_dir.parent / 'content' / 'gallery'
    watermarked_dir = script_dir.parent / 'static' / 'gallery-watermarked'
    
    # Crear carpeta para versiones watermarked
    watermarked_dir.mkdir(parents=True, exist_ok=True)
    
    # Procesar imágenes
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    files = [f for f in gallery_dir.glob('*') if f.suffix.lower() in image_extensions]
    
    print(f"Creando versiones watermarked para lightbox...")
    print(f"Originales (limpias): content/gallery/")
    print(f"Watermarked: static/gallery-watermarked/\n")
    
    success = 0
    for img_file in sorted(files):
        output_file = watermarked_dir / img_file.name
        if add_watermark(str(img_file), str(output_file), "CHEMACHIN", 0.25):
            print(f"✓ {img_file.name}")
            success += 1
    
    print(f"\n✓ {success}/{len(files)} versiones watermarked creadas")

if __name__ == '__main__':
    main()
