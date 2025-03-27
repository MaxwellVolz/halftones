import svgwrite
import os

def generate_circle_test(out_path="output/test_print.svg", canvas_size=(150, 20), margin=10, min_radius=0.5, max_radius=5.0, count=10):


    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    dwg = svgwrite.Drawing(out_path, size=(f"{canvas_size[0]}mm", f"{canvas_size[1]}mm"), viewBox=f"0 0 {canvas_size[0]} {canvas_size[1]}")
    
    spacing = (canvas_size[0] - 2 * margin) / (count - 1)
    center_y = canvas_size[1] / 2

    for i in range(count):
        radius = min_radius + i * (max_radius - min_radius) / (count - 1)
        cx = margin + i * spacing
        dwg.add(dwg.circle(center=(cx, center_y), r=radius, fill='black'))

    # Optional frame

    dwg.save()
    print(f"Test print saved to {out_path}")


generate_circle_test()
