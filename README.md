# Chemachin Photography Portfolio

A bilingual (EN/ES) photography portfolio website built with Hugo.

## Features

- **Responsive Gallery**: Modern slideshow gallery with thumbnail navigation
- **Bilingual Support**: English and Spanish with seamless language switching
- **Photo Persistence**: Maintains selected photo when switching languages
- **Optimized Images**: Hugo processes images locally (1200x800px for web)
- **Clean Design**: Minimalist layout with centered navigation and language flags

## Project Structure

```
chemachin/
├── content/           # Page content (EN/ES)
│   ├── _index.md/.es.md
│   ├── about/
│   └── gallery/       # Gallery images (ignored in git)
├── layouts/           # Hugo templates
│   ├── _default/section.html  # Gallery layout
│   └── partials/      # Header and menu
├── assets/css/        # Styles
├── themes/gallery/    # Gallery theme (submodule)
├── docs/              # Published site (GitHub Pages)
└── hugo.toml          # Hugo configuration
```

## Local Development

### Prerequisites
- Hugo (v0.150.0+)
- Git

### Setup

```bash
# Clone repository
git clone https://github.com/chemachin/chemachin.git
cd chemachin

# Initialize submodule
git submodule update --init --recursive

# Add your images to content/gallery/
# (1-8.jpg recommended)
```

### Building

```bash
# Development server
hugo server

# Build static site
hugo

# Publishing (auto via GitHub Actions to docs/)
git add .
git commit -m "your message"
git push origin main
```

## Image Management

### Adding Photos

1. Place high-resolution images (JPG/PNG) in `content/gallery/`
2. Update `content/gallery/_index.md` and `_index.es.md` with photo metadata
3. Hugo automatically processes and optimizes images for web (1200x800px)

### Image Protection

- Original images in `content/gallery/` are **not committed to git** (see `.gitignore`)
- Only optimized versions are published on the website
- This keeps your repository clean and protects original file sizes

## Customization

### Navigation
Edit `layouts/partials/header.html` to modify menu items or language switcher.

### Styles
Edit `assets/css/custom.scss` for custom CSS (background logo, colors, etc.).

### Content
- English: `content/` files (default)
- Spanish: Add `.es.md` suffix to translations

## Deployment

The site is deployed to GitHub Pages (https://chemachin.es) via commits to `main` branch. The `docs/` folder contains the published site.

## License

© 2024 Chemachin. All rights reserved.
