#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v4 asset pipeline: flood-key near-white bg from border seeds -> feather -> trim -> webp -> base64. Pure PIL."""
import base64, io
from PIL import Image, ImageDraw, ImageFilter, ImageChops

MAG = (255, 0, 255)

def key(path, out_png, thresh=70, feather=1.4):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    seeds = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1),
             (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2),
             (w // 4, 0), (3 * w // 4, 0), (0, h // 4), (w - 1, 3 * h // 4)]
    for s in seeds:
        if im.getpixel(s) != MAG:
            ImageDraw.floodfill(im, s, MAG, thresh=thresh)
    r, g, b = im.split()
    mr = r.point(lambda v: 255 if v == 255 else 0)
    mg = g.point(lambda v: 255 if v == 0 else 0)
    mb = b.point(lambda v: 255 if v == 255 else 0)
    mask = ImageChops.multiply(ImageChops.multiply(mr, mg), mb)
    alpha = ImageChops.invert(mask).filter(ImageFilter.GaussianBlur(feather))
    rgba = Image.open(path).convert("RGBA")
    rgba.putalpha(alpha)
    bbox = alpha.point(lambda v: 255 if v > 8 else 0).getbbox()
    rgba = rgba.crop(bbox)
    rgba.save(out_png)
    return rgba.size

def b64webp(png_path, q=82):
    im = Image.open(png_path)
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=q, method=6)
    data = buf.getvalue()
    return base64.b64encode(data).decode(), len(data)

if __name__ == "__main__":
    jobs = [
        ("vibe_images/island_a_mossrock_1789637413.png", "v4_island_a.png", "v4_island_a.b64.txt"),
        ("vibe_images/island_b_diorama_1789637428.png", "v4_island_b.png", "v4_island_b.b64.txt"),
        ("vibe_images/fg_branch_moss_1789637445.png", "v4_branch.png", "v4_branch.b64.txt"),
    ]
    for src, png, b64 in jobs:
        size = key(src, png)
        code, nbytes = b64webp(png)
        with open(b64, "w") as f:
            f.write(code)
        print(f"{src} -> {png} {size} webp={nbytes/1024:.0f}KB b64={len(code)/1024:.0f}KB")
