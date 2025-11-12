"""
Generate Teams app icons for Genie Bot.
Creates color.png (192x192) and outline.png (32x32) icons.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_color_icon():
    """Create 192x192 color icon with Databricks/Genie theme"""
    # Create image with transparent background
    size = 192
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Databricks Lava color
    lava = '#FF3621'
    cyan = '#00A8E1'
    navy = '#1B3139'

    # Draw circular background
    circle_margin = 10
    draw.ellipse(
        [circle_margin, circle_margin, size - circle_margin, size - circle_margin],
        fill=lava
    )

    # Draw genie lamp icon (simplified)
    # Base of lamp
    lamp_center_x = size // 2
    lamp_center_y = size // 2 + 10

    # Lamp body (trapezoid shape)
    lamp_points = [
        (lamp_center_x - 30, lamp_center_y + 30),  # bottom left
        (lamp_center_x + 30, lamp_center_y + 30),  # bottom right
        (lamp_center_x + 20, lamp_center_y - 20),  # top right
        (lamp_center_x - 20, lamp_center_y - 20),  # top left
    ]
    draw.polygon(lamp_points, fill='#FFFFFF')

    # Lamp spout (small rectangle)
    spout_width = 15
    spout_height = 25
    draw.rectangle(
        [
            lamp_center_x + 20, lamp_center_y - 20 - spout_height,
            lamp_center_x + 20 + spout_width, lamp_center_y - 20
        ],
        fill='#FFFFFF'
    )

    # Lamp handle (arc)
    handle_bbox = [
        lamp_center_x - 40, lamp_center_y - 10,
        lamp_center_x - 20, lamp_center_y + 20
    ]
    draw.arc(handle_bbox, start=90, end=270, fill='#FFFFFF', width=5)

    # Magic sparkles (stars)
    star_positions = [
        (lamp_center_x + 50, lamp_center_y - 50),
        (lamp_center_x + 70, lamp_center_y - 30),
        (lamp_center_x + 60, lamp_center_y - 65)
    ]

    for star_x, star_y in star_positions:
        # Draw simple plus-shaped star
        star_size = 8
        draw.line(
            [(star_x - star_size, star_y), (star_x + star_size, star_y)],
            fill=cyan, width=3
        )
        draw.line(
            [(star_x, star_y - star_size), (star_x, star_y + star_size)],
            fill=cyan, width=3
        )

    return img

def create_outline_icon():
    """Create 32x32 outline icon (white on transparent)"""
    size = 32
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Simple lamp outline in white
    lamp_center_x = size // 2
    lamp_center_y = size // 2 + 2

    # Lamp body outline
    lamp_points = [
        (lamp_center_x - 6, lamp_center_y + 6),
        (lamp_center_x + 6, lamp_center_y + 6),
        (lamp_center_x + 4, lamp_center_y - 4),
        (lamp_center_x - 4, lamp_center_y - 4),
    ]
    draw.polygon(lamp_points, outline='#FFFFFF', width=2)

    # Spout
    draw.rectangle(
        [lamp_center_x + 4, lamp_center_y - 8,
         lamp_center_x + 6, lamp_center_y - 4],
        outline='#FFFFFF', width=1
    )

    # Small sparkle
    star_x, star_y = lamp_center_x + 10, lamp_center_y - 8
    star_size = 3
    draw.line(
        [(star_x - star_size, star_y), (star_x + star_size, star_y)],
        fill='#FFFFFF', width=2
    )
    draw.line(
        [(star_x, star_y - star_size), (star_x, star_y + star_size)],
        fill='#FFFFFF', width=2
    )

    return img

if __name__ == "__main__":
    # Create appPackage directory if it doesn't exist
    os.makedirs('appPackage', exist_ok=True)

    print("🎨 Creating Teams app icons...")

    # Create and save color icon
    color_icon = create_color_icon()
    color_path = 'appPackage/color.png'
    color_icon.save(color_path, 'PNG')
    print(f"✅ Created {color_path} (192x192)")

    # Create and save outline icon
    outline_icon = create_outline_icon()
    outline_path = 'appPackage/outline.png'
    outline_icon.save(outline_path, 'PNG')
    print(f"✅ Created {outline_path} (32x32)")

    print("\n🎉 Icons created successfully!")
    print("\nPreview:")
    print(f"  Color icon:   {os.path.abspath(color_path)}")
    print(f"  Outline icon: {os.path.abspath(outline_path)}")
