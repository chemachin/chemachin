# Chemachin Photography Portfolio

A bilingual (EN/ES) photography portfolio website built with Hugo.

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

## Prerequisites

- Hugo v0.150.0-extended (required for SCSS processing)
- Git

The site uses the [Hugo Gallery Theme](https://github.com/nicokaiser/hugo-theme-gallery/) (included as git submodule) with custom overrides for bilingual support, photo persistence via localStorage, and responsive gallery layout.

## Setup

```bash
# Clone repository
git clone https://github.com/chemachin/chemachin.git
cd chemachin

# Initialize submodule
git submodule update --init --recursive

# Add your images to content/gallery/
# (1-8.jpg recommended)
```

## Building

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

## Deployment

The site is deployed to GitHub Pages (https://chemachin.es) via commits to `main` branch. The `docs/` folder contains the published site.

## License

© 2026 Chemachin. All rights reserved.
