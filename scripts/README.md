# Scripts de Procesamiento de Imágenes

## Watermark (Marca de Agua)

### Descripción
Script para agregar un watermark de texto a todas las imágenes de la galería. El watermark se incrusta permanentemente en las imágenes, de modo que persiste al descargarlas.

### Uso

**Procesar todas las imágenes con configuración por defecto:**
```bash
python scripts/watermark.py
```

**Procesar con opacidad personalizada (0.0 a 1.0):**
```bash
python scripts/watermark.py --opacity 0.4
```

**Procesar con texto personalizado:**
```bash
python scripts/watermark.py --text "MI MARCA"
```

**Procesar solo una imagen:**
```bash
python scripts/watermark.py --file imagen.jpg
```

**Combinar opciones:**
```bash
python scripts/watermark.py --text "FOTO" --opacity 0.35 --file 1.jpg
```

### Parámetros

- `--text TEXT`: Texto del watermark (default: CHEMACHIN)
- `--opacity VALOR`: Opacidad del watermark entre 0.0 (transparente) y 1.0 (opaco) (default: 0.25)
- `--file ARCHIVO`: Procesar solo un archivo específico

### Ejemplos de Opacidad

- `0.15`: Muy sutil, apenas visible
- `0.25`: Visible pero no intrusivo (recomendado)
- `0.35`: Moderadamente visible
- `0.5`: Muy visible
- `0.75`: Muy prominente

### Notas

- El script modifica las imágenes **en el lugar** (content/gallery/)
- Después de procesar, ejecuta `hugo` para regenerar el sitio
- Guarda imágenes con calidad 95 (buena calidad, tamaño razonable)
- Soporta JPG, PNG, GIF y WebP

### Workflow Recomendado

```bash
# 1. Agregar nuevas imágenes a content/gallery/
# 2. Procesar con watermark
python scripts/watermark.py

# 3. Regenerar sitio
hugo

# 4. Verificar cambios
git status

# 5. Hacer commit
git add content/gallery docs/gallery
git commit -m "Update gallery with new watermarked images"
git push
```
