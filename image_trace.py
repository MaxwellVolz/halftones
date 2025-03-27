import cv2
import numpy as np
import svgwrite
from PIL import Image
import os

def trace_stencil_layers(image_path, out_dir="output", num_layers=5, canvas_size=(126, 175), margin=0, min_area=500):

    os.makedirs(out_dir, exist_ok=True)

    # Load and convert
    img = Image.open(image_path).convert("L")
    data = np.array(img)

    # Define thresholds
    ranges = np.linspace(0, 256, num_layers + 1, dtype=np.uint8)

    for i in range(num_layers):
        low, high = int(ranges[i]), int(ranges[i + 1])
        
        mask = cv2.inRange(data, low, high - 1)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        dwg = svgwrite.Drawing(
            filename=os.path.join(out_dir, f"trace_sketch_{i+1}.svg"),
            size=(f"{canvas_size[0]}mm", f"{canvas_size[1]}mm"),
            viewBox=f"0 0 {canvas_size[0]} {canvas_size[1]}"
        )

        scale_x = (canvas_size[0] - 2 * margin) / img.width
        scale_y = (canvas_size[1] - 2 * margin) / img.height

        for contour in contours:
            area = cv2.contourArea(contour)
            if area < min_area:
                continue

            points = [
                (
                    margin + pt[0][0] * scale_x,
                    margin + pt[0][1] * scale_y
                ) for pt in contour
            ]
            if len(points) > 2:
                dwg.add(dwg.polygon(points, fill='black'))

        dwg.save()

    print(f"Saved {num_layers} traced stencil layers to {out_dir}/")


if __name__ == "__main__":
    trace_stencil_layers("images/hitw.png", out_dir="output")
