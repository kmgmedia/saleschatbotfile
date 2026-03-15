# How to Add Product Images

## Overview

The chatbot now supports displaying product images on Telegram when users inquire about products!

## Current Implementation

✅ Smart LED Strip Lights has 4 images configured
✅ Images display automatically when product is mentioned
✅ Product details (price, specs) shown with images
✅ Interactive buttons attached to images

## How It Works

1. When user asks about "Smart LED Strip Lights" (or LED lights, strip lights, etc.)
2. Bot sends first image with product details and buttons
3. If multiple images exist, remaining images are sent as an album

## Image Hosting Options

### Option 1: Free Image Hosting Services (Recommended for Now)

Upload your product images to:

- **ImgBB**: https://imgbb.com/ (No account needed)
- **PostImages**: https://postimages.org/ (Simple and reliable)
- **Imgur**: https://imgur.com/ (Popular but requires account)

After uploading, copy the direct image URLs.

### Option 2: Vercel Static Files (For Production)

1. Place images in `static/products/` folder
2. Deploy to Vercel
3. Use URLs like: `https://yourdomain.vercel.app/static/products/image.jpg`

### Option 3: External CDN (Best Performance)

- Cloudinary
- AWS S3
- Google Cloud Storage

## Adding Images for Smart LED Strip Lights

### Current Configuration (in `api/product_data.py`):

```python
PRODUCT_IMAGES = {
    "Smart LED Strip Lights": [
        "https://i.postimg.cc/mr8QbC8n/led-strip-1.jpg",
        "https://i.postimg.cc/CxDgVPzQ/led-strip-2.jpg",
        "https://i.postimg.cc/Y9kD6SyS/led-strip-3.jpg",
        "https://i.postimg.cc/m2Q1TRpK/led-strip-4.jpg"
    ],
}
```

### To Replace with Your Images:

1. Upload the 4 LED strip images you provided to an image host
2. Get the direct image URLs (must end in .jpg, .png, etc.)
3. Replace the URLs in `api/product_data.py`
4. Test on Telegram

## Adding Images for Other Products

To add images for any product, update `PRODUCT_IMAGES` in `api/product_data.py`:

```python
PRODUCT_IMAGES = {
    "Smart LED Strip Lights": [
        "https://your-image-host.com/led-1.jpg",
        "https://your-image-host.com/led-2.jpg"
    ],
    "Smartwatch X": [
        "https://your-image-host.com/smartwatch-1.jpg",
        "https://your-image-host.com/smartwatch-2.jpg"
    ],
    "Wireless Earbuds Pro": [
        "https://your-image-host.com/earbuds-1.jpg"
    ],
    # Add more products...
}
```

### Important Notes:

- Product names must match EXACTLY as in `PRODUCT_PRICES`
- URLs must be direct links to images (not webpage links)
- Telegram supports: JPG, PNG, GIF, WebP
- Recommended image size: 800-1200px width
- File size: Keep under 5MB per image

## Testing

After adding images:

1. Deploy to Vercel: `vercel --prod`
2. On Telegram, send: "Show me Smart LED Strip Lights"
3. Bot should send images with details and buttons

## Troubleshooting

**Images not showing?**

- Verify URLs are direct image links
- Check image format is supported (jpg, png, gif, webp)
- Ensure image is publicly accessible (not behind authentication)
- Test URL in browser - should display image directly

**Caption too long?**

- Telegram caption limit is 1024 characters
- Bot automatically handles this by truncating if needed

**Multiple images not working?**

- Check if all URLs are valid
- Ensure you're using send_media_group for albums (done automatically)

## Example User Flow

**User**: "I want smart LED lights"

**Bot Response**:

- 📸 Image 1 with caption:
  ```
  Smart LED Strip Lights
  💰 Price: $49
  📋 Details: 16 million colors, voice control, music sync...
  [AI Response]
  ```
- 📸 Images 2-4 as album
- Buttons: See Price | See Specs | Buy Now | Compare

Perfect shopping experience! 🎯
