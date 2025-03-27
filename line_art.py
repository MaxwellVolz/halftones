import cv2
import numpy as np
import svgwrite
from PIL import Image
import os

def generate_line_art_svg(
    image_path,
    out_path="line_art.svg",
    canvas_size=(126, 175),
    margin=0,
    low_threshold=50,
    high_threshold=150,
    min_area=100
):
    # Load and grayscale
    img = Image.open(image_path).convert("L")
    data = np.array(img)

    # Edge detection using Canny
    edges = cv2.Canny(data, low_threshold, high_threshold)

    # Find contours from edges
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Prepare SVG
    dwg = svgwrite.Drawing(
        filename=out_path,
        size=(f"{canvas_size[0]}mm", f"{canvas_size[1]}mm"),
        viewBox=f"0 0 {canvas_size[0]} {canvas_size[1]}"
    )

    # Scaling factors
    scale_x = (canvas_size[0] - 2 * margin) / img.width
    scale_y = (canvas_size[1] - 2 * margin) / img.height

    # Draw lines for each contour
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

        if len(points) > 1:
            dwg.add(dwg.polyline(points=points, fill="none", stroke="black", stroke_width=0.2))

    dwg.save()
    print(f"Saved line art to {out_path}")


if __name__ == "__main__":
    generate_line_art_svg(
        "images/hitw.png",
        out_path="output/line_art.svg",
        canvas_size=(126, 175),
        margin=0,
        low_threshold=115,
        high_threshold=255,
        min_area=300
    )
