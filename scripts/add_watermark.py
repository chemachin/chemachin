#!/usr/bin/env python3
"""
Script para agregar watermark a imágenes de la galería.
Procesa las imágenes en content/gallery/ y agrega un watermark de texto "CHEMACHIN"
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import shutil

def add_watermark(image_path, output_path, watermark_text="CHEMACHIN", opacity=0.3):
    """
    Agrega un watermark de texto a una imagen.
    
    Args:
        image_path: Ruta de la imagen original
        output_path: Ruta donde guardar la imagen con watermark
        watermark_text: Texto del watermark
        opacity: Opacidad del watermark (0.0 a 1.0)
    """
    try:
        # Abrir imagen
        img = Image.open(image_path)
        
        # Convertir a RGB si es necesario
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Crear capa para el watermark
        watermark_layer = Image.new('RGBA', img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(watermark_layer)
        
        # Intentar usar una fuente grande, si no disponible usar default
        try:
            # Calcular tamaño de fuente basado en ancho de imagen
            font_size = int(img.width / 5)
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            # Si no encuentra fuente, usar default
            font = ImageFont.load_default()
            font_size = 40
        
        # Calcular posición del texto (centro)
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (img.width - text_width) // 2
        y = (img.height - text_height) // 2
        
        # Calcular color con opacidad
        alpha = int(255 * opacity)
        watermark_color = (255, 255, 255, alpha)
        
        # Dibujar texto
        draw.text((x, y), watermark_text, font=font, fill=watermark_color)
        
        # Convertir imagen a RGBA si es necesario
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Compositar watermark sobre la imagen
        img = Image.alpha_composite(img, watermark_layer)
        
        # Convertir de vuelta a RGB para JPEG
        if output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
            img = img.convert('RGB')
        
        # Guardar imagen
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path, quality=95)
        print(f"✓ Watermark agregado a: {os.path.basename(image_path)}")
        return True
        
    except Exception as e:
        print(f"✗ Error procesando {image_path}: {e}")
        return False

def process_gallery(gallery_dir, watermark_text="CHEMACHIN", opacity=0.3):
    """
    Procesa todas las imágenes en la carpeta de galería.
    
    Args:
        gallery_dir: Ruta de la carpeta content/gallery/
        watermark_text: Texto del watermark
        opacity: Opacidad del watermark
    """
    gallery_path = Path(gallery_dir)
    
    if not gallery_path.exists():
        print(f"✗ La carpeta {gallery_dir} no existe")
        return
    
    # Buscar todas las imágenes
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    image_files = [f for f in gallery_path.glob('*') if f.suffix.lower() in image_extensions]
    
    if not image_files:
        print(f"✗ No se encontraron imágenes en {gallery_dir}")
        return
    
    print(f"\nProcesando {len(image_files)} imagen(es) en {gallery_dir}")
    print(f"Watermark: '{watermark_text}' con opacidad {opacity}\n")
    
    successful = 0
    for image_file in sorted(image_files):
        if add_watermark(str(image_file), str(image_file), watermark_text, opacity):
            successful += 1
    
    print(f"\n✓ {successful}/{len(image_files)} imagen(es) procesadas exitosamente")

if __name__ == '__main__':
    import sys
    
    # Obtener ruta de la carpeta del proyecto
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    gallery_dir = project_dir / 'content' / 'gallery'
    
    # Parámetros ajustables
    watermark_text = "CHEMACHIN"
    opacity = 0.25  # 0.0 a 1.0 (0.25 = 25% opaque)
    
    # Procesar galería
    process_gallery(str(gallery_dir), watermark_text, opacity)
