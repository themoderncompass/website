# Open Graph Image Specifications

## Required Dimensions
- **Size**: 1200 x 630 pixels
- **Aspect Ratio**: 1.91:1
- **Format**: PNG or JPG
- **File size**: Under 8MB (ideally under 300KB)
- **Filename**: `og-image.png`
- **Location**: `/public/og-image.png`

## Design Guidelines

### What to Include
1. **Modern Compass logo** (centered or left-aligned)
2. **Tagline**: "Find Direction in Life's Key Moments"
3. **Visual element**: Compass icon or gradient background
4. **Brand colors**: Purple (#8b5cf6), Blue (#3b82f6), Yellow (#facc15), Orange (#f97316)

### Safe Zone
- Keep important content within **1200x600px** center area
- Leave 30px margin on all sides
- Text should be readable at small sizes (thumbnails)

### Typography
- **Headline**: 72-90px, bold, high contrast
- **Subtext**: 36-48px, medium weight
- **Font**: Clean, sans-serif (system fonts work great)

## Design Tools

### Quick Options
1. **Canva**:
   - Use "Facebook Post" template (1200x630)
   - Free templates available
   - Easy to customize

2. **Figma**:
   - Create 1200x630 frame
   - Export as PNG
   - Free for individual use

3. **Photoshop**:
   - New file: 1200x630px, 72 DPI
   - RGB color mode
   - Save for Web (PNG-24)

### Template Idea
```
+------------------------------------------+
|                                          |
|  [Logo]   MODERN COMPASS                |
|                                          |
|  Find Direction in Life's Key Moments   |
|                                          |
|  Self • Trust • Character • Relationships|
|                                          |
+------------------------------------------+
```

## Testing Your OG Image

After creating the image:

1. Save as `/public/og-image.png`
2. Build the site: `npm run build`
3. Test with these tools:
   - Facebook Debugger: https://developers.facebook.com/tools/debug/
   - Twitter Card Validator: https://cards-dev.twitter.com/validator
   - LinkedIn Post Inspector: https://www.linkedin.com/post-inspector/

## Current Status
- ✅ SEO component configured to use `/og-image.png`
- ⏳ Using logo.png as temporary placeholder (1024x1024)
- 🎯 Need to create proper 1200x630px branded image

## Quick Win
If you don't have time for custom design, you can:
1. Use your logo centered on a solid color background (brand purple)
2. Add white text overlay with tagline
3. Keep it simple and clean
