# Image Processing Scripts

## Watermark

### Description
Script to add logo watermark to gallery images. **Keeps original full-size images private** (not published online or in repo). Only watermarked versions are published.

### Security Model

**Private (Not Published):**
- `private-originals/` - Full-size original images without watermark
- This folder is in `.gitignore` - never committed to repo
- Your original photos remain secure

**Published (Public):**
- `content/gallery/` - Watermarked versions for Hugo to process (creates thumbnails)
- `static/gallery-watermarked/` - Watermarked versions for lightbox downloads
- `docs/` - Generated site with only watermarked images

### Usage

**Process all images with default settings:**
```bash
python scripts/create_watermarked_versions.py
```

### How It Works

1. Place original images in `private-originals/` (not in repo)
2. Script reads from `private-originals/`
3. Creates watermarked versions in both:
   - `content/gallery/` (Hugo processes these for thumbnails)
   - `static/gallery-watermarked/` (served in lightbox)
4. Hugo generates site with only watermarked images
5. Original images never leave your local machine

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
# 1. Add new original images to private-originals/ (not tracked by git)
# 2. Process with watermark
python scripts/create_watermarked_versions.py

# 3. Regenerate site
hugo

# 4. Check changes (only watermarked versions)
git status

# 5. Commit (originals stay private)
git add content/gallery static/gallery-watermarked docs/
git commit -m "Add new gallery images (watermarked)"
git push
```

### Notes

- **Originals are NEVER committed to repo** (protected by .gitignore)
- **Originals are NEVER published online** (Hugo only processes watermarked versions)
- Watermark is embedded in the image file (persists on download)
- Hugo automatically copies static files to docs/ during build
- Thumbnails and lightbox images are both watermarked
