from PIL import Image
import numpy as np
import svgwrite

def halftone_svg(image_path, output_path="halftone.svg", block_size=10, max_radius=5):
    img = Image.open(image_path).convert("L")
    img = img.resize((img.width // block_size, img.height // block_size), Image.Resampling.LANCZOS)
    data = np.array(img)

    dwg = svgwrite.Drawing(output_path, size=(img.width * block_size, img.height * block_size))

    for y in range(data.shape[0]):
        for x in range(data.shape[1]):
            brightness = 255 - data[y, x]  # invert: darker → bigger
            # radius = (brightness / 255) * max_radius

            radius = max((brightness / 255) * (max_radius), 0.5)



            if radius > 0:
                cx = x * block_size + block_size / 2
                cy = y * block_size + block_size / 2
                dwg.add(dwg.circle(center=(cx, cy), r=radius, fill="black"))

    dwg.save()

halftone_svg("images/hitw.png", "output/output.svg", block_size=12, max_radius=6)
