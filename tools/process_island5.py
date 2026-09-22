"""Process the regenerated floating-island render into the v5 inline asset.

- global chroma-key: drop neutral & bright background pixels (keeps pale trunks,
  eats the paper-white backdrop and inter-leaf pockets)
- erode 1px + feather to kill fringe
- mild unsharp so the island stays crisp at Retina display size
- upscale 1024 -> 1600 wide (display box is ~620 CSS px = ~1240 device px)
- WebP q84 with alpha -> base64 into v4_island_a.b64.txt
"""
import base64
import io

from PIL import Image, ImageFilter

WS = "/Users/zhw/.qoderwork/workspace/mtmqoy4hwvnd8s3g"
SRC = f"{WS}/vibe_images/island_v5_hi_1789893989.png"

img = Image.open(SRC).convert("RGB")
w, h = img.size
px = img.load()

# background statistics from the border ring
bs = [px[x, y] for x in range(0, w, 7) for y in (0, 1, h - 2, h - 1)]
bs += [px[x, y] for y in range(0, h, 7) for x in (0, 1, w - 2, w - 1)]
bmin = min(min(c) for c in bs)
bmax = max(max(c) for c in bs)
print("border rgb min/max:", bmin, bmax)
lo = bmin - 10          # anything this bright AND neutral is backdrop
spread = 12             # max channel spread considered neutral

alpha = Image.new("L", (w, h), 0)
ap = alpha.load()
kept = 0
for y in range(h):
    for x in range(w):
        r, g, b = px[x, y]
        mx, mn = max(r, g, b), min(r, g, b)
        if mn >= lo and (mx - mn) <= spread:
            continue
        ap[x, y] = 255
        kept += 1
print(f"kept {kept}/{w*h} = {kept/(w*h):.2%}")

alpha = alpha.filter(ImageFilter.MinFilter(3))       # eat halo fringe
alpha = alpha.filter(ImageFilter.GaussianBlur(0.9))  # feather
img = img.filter(ImageFilter.UnsharpMask(radius=1.6, percent=118, threshold=2))
img.putalpha(alpha)

nw = 1600
nh = round(h * nw / w)
img = img.resize((nw, nh), Image.LANCZOS)
buf = io.BytesIO()
img.save(buf, "WEBP", quality=84, method=6)
b64 = base64.b64encode(buf.getvalue()).decode()
print(f"island webp: {len(buf.getvalue())/1024:.0f} KB -> b64 {len(b64)/1024:.0f} KB, {nw}x{nh}")

with open(f"{WS}/v4_island_a.b64.txt", "w") as f:
    f.write(b64)
print("written v4_island_a.b64.txt")
