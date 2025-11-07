# Theme Customization

This folder contains MkDocs Material theme customizations for the LPIC-1 documentation.

## Structure

The theme uses MkDocs Material's [template overriding](https://squidfunk.github.io/mkdocs-material/customization/#overriding-template-blocks) feature. Only specific blocks need to be overridden; the rest is inherited from the base Material theme.

### Files

- **main.html**: Main template override
  - Extends the base Material theme template
  - Adds Vazirmatn Persian font from CDN
  - Provides proper RTL (Right-to-Left) support

## How It Works

MkDocs Material uses Jinja2 templates. By setting `custom_dir: theme` in `mkdocs.yml`, MkDocs will:

1. First look for templates in this directory
2. Fall back to the base Material theme for any files not found here

This allows minimal customization while maintaining all Material theme features.

## Adding More Customizations

To override additional templates or blocks:

1. Check the [Material theme structure](https://github.com/squidfunk/mkdocs-material/tree/master/src)
2. Copy the template you want to customize to this folder
3. Modify only the blocks you need to change
4. The rest will automatically use the base theme

Example template overrides you might add:
- `partials/header.html` - Customize header
- `partials/footer.html` - Customize footer
- `404.html` - Custom 404 page

## CSS and JavaScript

Custom CSS and JavaScript files are located in `content/assets/` and referenced in `mkdocs.yml`:

```yaml
extra_css:
  - assets/css/custom.css

extra_javascript:
  - assets/js/custom.js
```
