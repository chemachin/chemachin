#!/usr/bin/env python3
"""
Utilidad para agregar watermark a nuevas imágenes de la galería.
Uso:
  python scripts/watermark.py              # Procesa todas las imágenes
  python scripts/watermark.py --opacity 0.4 # Ajusta opacidad (0.0-1.0)
  python scripts/watermark.py --text "MI MARCA" # Texto personalizado
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import argparse

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
    parser = argparse.ArgumentParser(
        description='Agregar watermark a imágenes de la galería'
    )
    parser.add_argument('--text', default='CHEMACHIN', 
                        help='Texto del watermark (default: CHEMACHIN)')
    parser.add_argument('--opacity', type=float, default=0.25,
                        help='Opacidad 0.0-1.0 (default: 0.25)')
    parser.add_argument('--file', help='Procesar solo un archivo específico')
    
    args = parser.parse_args()
    
    # Validar opacidad
    if not (0.0 <= args.opacity <= 1.0):
        print("✗ Opacidad debe estar entre 0.0 y 1.0")
        sys.exit(1)
    
    # Obtener ruta de galería
    script_dir = Path(__file__).parent
    gallery_dir = script_dir.parent / 'content' / 'gallery'
    
    if not gallery_dir.exists():
        print(f"✗ Galería no encontrada: {gallery_dir}")
        sys.exit(1)
    
    # Procesar archivo específico o todos
    if args.file:
        file_path = gallery_dir / args.file
        if not file_path.exists():
            print(f"✗ Archivo no encontrado: {file_path}")
            sys.exit(1)
        files = [file_path]
        print(f"Procesando: {args.file}")
    else:
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        files = [f for f in gallery_dir.glob('*') if f.suffix.lower() in image_extensions]
        print(f"Procesando {len(files)} imagen(es)...")
    
    # Procesar
    success = 0
    for img_file in sorted(files):
        if add_watermark(str(img_file), str(img_file), args.text, args.opacity):
            print(f"✓ {img_file.name}")
            success += 1
    
    print(f"\n✓ {success}/{len(files)} completadas")

if __name__ == '__main__':
    main()
