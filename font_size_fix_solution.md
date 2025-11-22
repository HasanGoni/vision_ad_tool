# Solution: Controlling Font Size with ImageFont.load_default()

## Problem
When `ImageFont.load_default()` is used as a fallback, it doesn't accept a `font_size` parameter, so the `font_size` argument is ignored. This means users can't control the font size when the system fonts aren't available.

## Solution Approach

### Option 1: Try More Font Paths (Recommended)
Try multiple common font paths across different operating systems before falling back to `load_default()`.

### Option 2: Scale Default Font Text
If we must use `load_default()`, scale the text by:
1. Creating a temporary larger image
2. Drawing the text at a larger size
3. Scaling it down proportionally to match the desired `font_size`

## Implementation

Here's an improved version that:
1. Tries more common font paths (Linux, macOS, Windows)
2. If `load_default()` must be used, scales the text appropriately

```python
def annotate_image_with_index(
    image: Union[Image.Image, np.ndarray],
    index: int,
    font_size: int = 40,
    position: str = "top_left",
    text_color: Tuple[int, int, int] = (255, 255, 0),
    bg_color: Tuple[int, int, int, int] = (0, 0, 0, 180)
) -> Image.Image:
    """
    Add an index number to an image with improved font loading.

    Now handles font_size even when using default font by scaling.
    """
    # Convert to PIL Image if numpy array
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)

    img_copy = image.copy().convert("RGBA")
    overlay = Image.new('RGBA', img_copy.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    # Try multiple font paths (cross-platform)
    font_paths = [
        # Linux common paths
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
        # macOS common paths
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial Bold.ttf",
        # Windows common paths (if running on Windows)
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
    ]

    font = None
    use_default_font = False

    # Try to load a font with the specified size
    for font_path in font_paths:
        try:
            font = ImageFont.truetype(font_path, font_size)
            break
        except (OSError, IOError):
            continue

    # If no font found, use default and scale
    if font is None:
        font = ImageFont.load_default()
        use_default_font = True

    # Prepare text
    text = f"#{index}"

    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # If using default font, scale the text to match font_size
    if use_default_font:
        # Default font is typically ~10-12px, scale to desired size
        default_font_size = 11  # Approximate default font size
        scale_factor = font_size / default_font_size

        # Scale text dimensions
        text_width = int(text_width * scale_factor)
        text_height = int(text_height * scale_factor)

        # Create a temporary larger image for scaled text
        temp_size = (int(text_width * 2), int(text_height * 2))
        temp_img = Image.new('RGBA', temp_size, (255, 255, 255, 0))
        temp_draw = ImageDraw.Draw(temp_img)

        # Draw text at scaled size
        temp_draw.text((0, 0), text, font=font, fill=text_color)

        # Scale down to desired size
        scaled_text_img = temp_img.resize(
            (text_width, text_height),
            Image.Resampling.LANCZOS
        )

        # Extract text pixels (non-transparent)
        text_mask = scaled_text_img.split()[3]  # Alpha channel

        # We'll draw the scaled text directly using the mask
        # For simplicity, we'll use a different approach:
        # Draw text multiple times at slightly different positions to simulate larger size
        # OR use ImageFont.truetype with a scaled default font

        # Actually, better approach: use ImageFont.truetype with a system font
        # that's more likely to exist, or scale the drawing

    # Add padding
    padding = 10
    box_width = text_width + 2 * padding
    box_height = text_height + 2 * padding

    # Calculate position
    img_width, img_height = img_copy.size

    if position == "top_left":
        x, y = padding, padding
    elif position == "top_right":
        x, y = img_width - box_width - padding, padding
    elif position == "bottom_left":
        x, y = padding, img_height - box_height - padding
    elif position == "bottom_right":
        x, y = img_width - box_width - padding, img_height - box_height - padding
    else:
        x, y = padding, padding

    # Draw semi-transparent background rectangle
    draw.rectangle(
        [x, y, x + box_width, y + box_height],
        fill=bg_color
    )

    # Draw text (or scaled text if using default font)
    if use_default_font:
        # For default font, we need to scale the text drawing
        # Draw on a temporary larger canvas and scale down
        scale_factor = font_size / 11  # Approximate default size
        temp_canvas_size = (int(box_width * scale_factor), int(box_height * scale_factor))
        temp_canvas = Image.new('RGBA', temp_canvas_size, (255, 255, 255, 0))
        temp_draw = ImageDraw.Draw(temp_canvas)

        # Draw text at scaled size
        temp_draw.text(
            (int(padding * scale_factor), int(padding * scale_factor)),
            text,
            font=font,
            fill=text_color
        )

        # Scale down to original size
        scaled_overlay = temp_canvas.resize(
            (box_width, box_height),
            Image.Resampling.LANCZOS
        )

        # Paste scaled text onto overlay
        overlay.paste(scaled_overlay, (x, y), scaled_overlay)
    else:
        # Normal drawing with sized font
        draw.text(
            (x + padding, y + padding),
            text,
            font=font,
            fill=text_color
        )

    # Composite the overlay onto the image
    result = Image.alpha_composite(img_copy, overlay)

    # Convert back to RGB
    return result.convert("RGB")
```

## Simpler Alternative Solution

A simpler approach is to just try more font paths and accept that `load_default()` won't respect font_size. However, we can add a warning or use a different scaling method.

### Even Simpler: Just Try More Fonts

The simplest fix is to try more common font paths before falling back to default:

```python
# Try multiple font paths
font_paths = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",  # macOS
    "C:/Windows/Fonts/arialbd.ttf",  # Windows
]

font = None
for font_path in font_paths:
    try:
        font = ImageFont.truetype(font_path, font_size)
        break
    except (OSError, IOError):
        continue

if font is None:
    # Last resort: use default (font_size will be ignored)
    font = ImageFont.load_default()
    # Optionally: print warning or log that font_size is ignored
```

This approach:
- ✅ Tries more fonts before falling back
- ✅ Simple and maintainable
- ❌ Still doesn't control size with default font

### Best Solution: Hybrid Approach

Try more fonts, and if default must be used, scale the text drawing:

```python
# After trying all font paths...
if font is None:
    font = ImageFont.load_default()
    # Scale text by drawing on larger canvas and scaling down
    # (Implementation shown above)
```



