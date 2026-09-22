"""Prepare demo assets: transparent-background banyan tree + compressed logo.

- Tree: chroma-key out the neutral warm-gray background (low-saturation pixels),
  feather alpha 1px, resize to 1100px wide, export WebP with alpha.
- Logo: resize to 360px wide, export WebP.
Both printed as base64 size estimates so we know the inline cost.
"""
import base64
import io
from PIL import Image, ImageFilter

WS = "/Users/zhw/.qoderwork/workspace/mtmqoy4hwvnd8s3g"
TREE_SRC = f"{WS}/vibe_images/banyan-tree-natural-dense_1788948378.png"  # pre-sharpen source
TREE_SHARP = f"{WS}/outputs/banyan-tree-final.png"                        # sharpened final
LOGO_SRC = f"{WS}/outputs/center-logo.jpg"

# --- tree: use sharpened final, knock out gray background -------------------
img = Image.open(TREE_SHARP).convert("RGB")
w, h = img.size
px = img.load()
alpha = Image.new("L", (w, h), 0)
ap = alpha.load()
for y in range(h):
    for x in range(w):
        r, g, b = px[x, y]
        mx, mn = max(r, g, b), min(r, g, b)
        # keep greens and warm browns; drop neutral gray background
        if (g - r) > 6 or (r - g) > 8 or (mx - mn) > 20:
            ap[x, y] = 255
alpha = alpha.filter(ImageFilter.MinFilter(3))          # eat halo fringe
alpha = alpha.filter(ImageFilter.GaussianBlur(1.2))     # feather edge
tree = img.convert("RGB")
tree.putalpha(alpha)
# resize to 1100 wide
nw = 1100
nh = round(h * nw / w)
tree = tree.resize((nw, nh), Image.LANCZOS)
buf = io.BytesIO()
tree.save(buf, "WEBP", quality=82, method=6)
tree_b64 = base64.b64encode(buf.getvalue()).decode()
print(f"tree webp: {len(buf.getvalue())/1024:.0f} KB -> b64 {len(tree_b64)/1024:.0f} KB, {nw}x{nh}")

# --- logo --------------------------------------------------------------------
logo = Image.open(LOGO_SRC).convert("RGB")
lw = 360
lh = round(logo.height * lw / logo.width)
logo = logo.resize((lw, lh), Image.LANCZOS)
buf2 = io.BytesIO()
logo.save(buf2, "WEBP", quality=88, method=6)
logo_b64 = base64.b64encode(buf2.getvalue()).decode()
print(f"logo webp: {len(buf2.getvalue())/1024:.0f} KB -> b64 {len(logo_b64)/1024:.0f} KB, {lw}x{lh}")

with open(f"{WS}/demo_assets_b64.txt", "w") as f:
    f.write("TREE=" + tree_b64 + "\nLOGO=" + logo_b64 + "\n")
print("written demo_assets_b64.txt")
