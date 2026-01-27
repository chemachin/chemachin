# Chemachin.es — Photography Portfolio

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

## Deployment

The site is deployed to GitHub Pages (https://chemachin.es) via commits to `main` branch. The `docs/` folder contains the published site.

Repository: https://github.com/chemachin/chemachin.es

**Technology Stack:**
- **Hugo v0.150.0-extended**: Static site generator with SCSS processing
- **Git**: Version control and deployment
- **[Hugo Gallery Theme](https://github.com/nicokaiser/hugo-theme-gallery/)**: Base theme (git submodule)
- **Custom overrides**: Bilingual support, photo persistence via localStorage, responsive gallery layout

## License

© 2026 Chemachin. All rights reserved.
