from PIL import Image
import numpy as np
import svgwrite
import os

# Multi-layer angled-line halftone (blinds-style) pattern for stencil generation

def add_blind_lines(drawing, cx, cy, size, angle_deg, density_factor):
    """Draws fewer, more distinct angled lines based on brightness level."""
    # Consolidate density into 4 buckets
    bucket = int(density_factor * 5)
    if bucket == 0:
        return  # skip very bright blocks

    spacing = 2 + (4 - bucket) * 1.5  # range: 2mm to 6.5mm
    line_count = bucket + 1  # 1 to 5 lines max

    length = size * 1.5  # line length to cover cell
    angle = np.radians(angle_deg)
    sin_a = np.sin(angle)
    cos_a = np.cos(angle)

    total_span = spacing * (line_count - 1)
    offset_start = -total_span / 2

    for i in range(line_count):
        dx = offset_start + i * spacing
        x1 = cx + dx * cos_a - length * sin_a / 2
        y1 = cy + dx * sin_a + length * cos_a / 2
        x2 = cx + dx * cos_a + length * sin_a / 2
        y2 = cy + dx * sin_a - length * cos_a / 2
        drawing.add(drawing.line(start=(x1, y1), end=(x2, y2), stroke="black", stroke_width=0.4))


def multi_layer_blindlines(image_path, out_dir="output_blinds", block_size=10, num_layers=5):

    DOT_AREA_WIDTH = 127
    DOT_AREA_HEIGHT = 178
    MARGIN = 5

    MM_WIDTH = DOT_AREA_WIDTH + 2 * MARGIN
    MM_HEIGHT = DOT_AREA_HEIGHT + 2 * MARGIN

    OFFSET_X = MARGIN
    OFFSET_Y = MARGIN

    os.makedirs(out_dir, exist_ok=True)
    img = Image.open(image_path).convert("L")
    img_small = img.resize((img.width // block_size, img.height // block_size), Image.Resampling.LANCZOS)
    data = np.array(img_small)

    height, width = data.shape
    layer_ranges = np.linspace(0, 256, num_layers + 1, dtype=int)
    layer_angles = [0, 45, 90, 135]  # Could customize these or rotate randomly

    usable_width = MM_WIDTH - 2 * MARGIN
    usable_height = MM_HEIGHT - 2 * MARGIN
    scale_x = usable_width / width
    scale_y = usable_height / height
    scale = min(scale_x, scale_y)

    drawings = [
        svgwrite.Drawing(
            filename=os.path.join(out_dir, f"blinds_layer_{i+1}.svg"),
            size=(f"{MM_WIDTH}mm", f"{MM_HEIGHT}mm"),
            viewBox=f"0 0 {MM_WIDTH} {MM_HEIGHT}"
        )
        for i in range(num_layers)
    ]

    for y in range(height):
        for x in range(width):
            brightness = data[y, x]
            inverted = 255 - brightness  # Darker = more lines

            cx = OFFSET_X + x * scale + scale / 2
            cy = OFFSET_Y + y * scale + scale / 2

            for i in range(num_layers):
                low, high = layer_ranges[i], layer_ranges[i+1]
                if low <= brightness < high:
                    density_factor = inverted / 255
                    add_blind_lines(drawings[i], cx, cy, scale, layer_angles[i], density_factor)
                    break

    for drawing in drawings:
        drawing.add(drawing.rect(
            insert=(0, 0),
            size=(MM_WIDTH, MM_HEIGHT),
            fill='none',
            stroke='black',
            stroke_width=0.2
        ))
        drawing.save()

    print(f"Saved {num_layers} angled-blinds layers to {out_dir}/")


if __name__ == "__main__":
    multi_layer_blindlines("images/hitw.png", out_dir="output", block_size=12, num_layers=4)
