from PIL import Image
import numpy as np
import svgwrite
import os

# Multi-layer halftone pattern for making 5x7 postcard stencils

def multi_layer_halftone(image_path, out_dir="output", block_size=10, max_radius=5, num_layers=3):

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

    usable_width = MM_WIDTH - 2 * MARGIN
    usable_height = MM_HEIGHT - 2 * MARGIN
    scale_x = usable_width / width
    scale_y = usable_height / height
    scale = min(scale_x, scale_y)  # uniform scaling

    drawings = [
        svgwrite.Drawing(
            filename=os.path.join(out_dir, f"halftone_layer_{i+1}.svg"),
            size=(f"{MM_WIDTH}mm", f"{MM_HEIGHT}mm"),
            viewBox=f"0 0 {MM_WIDTH} {MM_HEIGHT}"
        )
        for i in range(num_layers)
    ]

    for y in range(height):
        for x in range(width):
            brightness = data[y, x]
            inverted = 255 - brightness
            cx = OFFSET_X + x * scale + scale / 2
            cy = OFFSET_Y + y * scale + scale / 2

            for i in range(num_layers):
                low, high = layer_ranges[i], layer_ranges[i+1]
                if low <= brightness < high:
                    radius = (inverted / 255) * (max_radius * scale / block_size)

                    if radius > 0:
                        drawings[i].add(drawings[i].circle(center=(cx, cy), r=radius, fill="black"))
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

    print(f"Saved {num_layers} halftone layers to {out_dir}/")



if __name__ == "__main__":
    multi_layer_halftone("images/hitw.png", out_dir="output", block_size=12, max_radius=6, num_layers=3)
