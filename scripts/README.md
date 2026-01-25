# Image Processing Scripts

## Watermark

### Description
Script to add logo watermark to gallery images. Creates watermarked versions for lightbox/downloads while keeping original thumbnails clean.

### Usage

**Process all images with default settings:**
```bash
python scripts/create_watermarked_versions.py
```

### How It Works

- Original images in `content/gallery/` remain clean (used for thumbnails)
- Watermarked versions are created in `static/gallery-watermarked/`
- The lightbox displays watermarked versions
- When users download, they get the watermarked version

### Current Settings

- **Logo**: Chemachineb.png
- **Opacity**: 65% (0.65)
- **Size**: 40% of image width
- **Position**: Centered
- **Quality**: 95 (high quality)

### Adjusting Watermark

To change opacity or size, edit the script:

```python
# In create_watermarked_versions.py, line ~85:
add_watermark_logo(..., opacity=0.65, size_percent=40)

# Opacity examples:
# 0.35 - Subtle
# 0.50 - Moderate
# 0.65 - Visible (current)
# 0.80 - Very prominent

# Size examples:
# 30 - Small
# 40 - Medium (current, matches background)
# 50 - Large
# 60 - Very large
```

### Supported Formats

JPG, JPEG, PNG, GIF, WebP

### Recommended Workflow

```bash
# 1. Add new images to content/gallery/
# 2. Process with watermark
python scripts/create_watermarked_versions.py

# 3. Regenerate site
hugo

# 4. Check changes
git status

# 5. Commit
git add content/gallery static/gallery-watermarked docs/
git commit -m "Add new gallery images with watermark"
git push
```

### Notes

- Script does NOT modify original images
- Watermark is embedded in the image file (persists on download)
- Hugo automatically copies static files to docs/ during build
