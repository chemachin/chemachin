#!/usr/bin/env python3
"""
Crea versiones watermarked de las imágenes para usar en lightbox.
Las originales permanecen limpias para thumbnails.
Usa el logo Chemachinb.png como watermark.
"""

import os
from pathlib import Path
from PIL import Image

def add_watermark_logo(image_path, output_path, logo_path, opacity=0.35, size_percent=65):
    """Agrega logo como watermark a una imagen."""
    try:
        # Abrir imagen base
        img = Image.open(image_path)
        
        # Convertir a RGB si es necesario
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Convertir a RGBA para soportar transparencia
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Abrir logo
        logo = Image.open(logo_path)
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')
        
        # Calcular nuevo tamaño del logo (% del ancho de la imagen)
        logo_width = int(img.width * (size_percent / 100))
        aspect_ratio = logo.height / logo.width
        logo_height = int(logo_width * aspect_ratio)
        logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
        
        # Ajustar opacidad del logo
        alpha = logo.split()[3]
        alpha = alpha.point(lambda p: int(p * opacity))
        logo.putalpha(alpha)
        
        # Calcular posición central
        x = (img.width - logo_width) // 2
        y = (img.height - logo_height) // 2
        
        # Crear capa para compositar
        watermark_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
        watermark_layer.paste(logo, (x, y), logo)
        
        # Compositar logo sobre imagen
        img = Image.alpha_composite(img, watermark_layer)
        
        # Guardar como JPG
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
    project_dir = script_dir.parent
    gallery_dir = project_dir / 'content' / 'gallery'
    watermarked_dir = project_dir / 'static' / 'gallery-watermarked'
    logo_path = project_dir / 'themes' / 'gallery' / 'static' / 'images' / 'Chemachineb.png'
    
    # Verificar que existe el logo
    if not logo_path.exists():
        print(f"✗ Logo no encontrado: {logo_path}")
        return
    
    # Crear carpeta para versiones watermarked
    watermarked_dir.mkdir(parents=True, exist_ok=True)
    
    # Procesar imágenes
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    files = [f for f in gallery_dir.glob('*') if f.suffix.lower() in image_extensions]
    
    print(f"Creando versiones con logo watermark para lightbox...")
    print(f"Logo: {logo_path.name}")
    print(f"Originales (limpias): content/gallery/")
    print(f"Watermarked: static/gallery-watermarked/\n")
    
    success = 0
    for img_file in sorted(files):
        output_file = watermarked_dir / img_file.name
        if add_watermark_logo(str(img_file), str(output_file), str(logo_path), opacity=0.35, size_percent=65):
            print(f"✓ {img_file.name}")
            success += 1
    
    print(f"\n✓ {success}/{len(files)} versiones con logo creadas")

if __name__ == '__main__':
    main()
