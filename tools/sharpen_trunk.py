"""Selectively enhance trunk/aerial-root clarity of the banyan tree image.

Mask = warm brown pixels (R-G>10 and R-B>20): trunk, pillar roots, hanging
thread roots. Green canopy (G>R) and neutral gray background are excluded,
so canopy pixels stay bit-identical ("树冠不要动").

Enhancement inside mask (feathered):
  - fine unsharp  (radius 1.8, amount 1.1)  -> crisp bark/leaf-tip detail
  - clarity       (radius 14,  amount 0.45) -> mid-tone local contrast
  - gentle contrast lift (1.06 around mid-gray)
All math in 32-bit float ('F') channels to avoid 8-bit clipping artifacts.
"""
from PIL import Image, ImageChops, ImageFilter, ImageMath

SRC = "/Users/zhw/.qoderwork/workspace/mtmqoy4hwvnd8s3g/vibe_images/banyan-tree-natural-dense_1788948378.png"
DST = "/Users/zhw/.qoderwork/workspace/mtmqoy4hwvnd8s3g/outputs/banyan-tree-final.png"

img = Image.open(SRC).convert("RGB")
r, g, b = img.split()

# --- brown mask -------------------------------------------------------------
d_rg = ImageChops.subtract(r, g)           # R-G clipped at 0
d_rb = ImageChops.subtract(r, b)           # R-B clipped at 0
m1 = d_rg.point(lambda v: 255 if v > 10 else 0)
m2 = d_rb.point(lambda v: 255 if v > 20 else 0)
mask = ImageChops.multiply(m1, m2)         # 255 where both true
mask = mask.filter(ImageFilter.GaussianBlur(3))   # feather edges
mf = mask.convert("F")

FINE_R, FINE_A = 1.8, 1.1
BIG_R, BIG_A = 14.0, 0.45
CONTRAST = 1.06

out_chans = []
for ch in (r, g, b):
    cf = ch.convert("F")
    bf = ch.filter(ImageFilter.GaussianBlur(FINE_R)).convert("F")
    gf = ch.filter(ImageFilter.GaussianBlur(BIG_R)).convert("F")
    enh = ImageMath.lambda_eval(
        lambda a: (a["c"] - a["b"]) * FINE_A + a["c"] + (a["c"] - a["g"]) * BIG_A,
        c=cf, b=bf, g=gf,
    )
    enh = enh.point(lambda v: (v - 128.0) * CONTRAST + 128.0)
    enh_l = enh.convert("L")   # F->L conversion clips to 0..255
    out_chans.append(Image.composite(enh_l, ch, mask))

out = Image.merge("RGB", out_chans)
out.save(DST)

# report how much of the image was touched (sanity check: canopy untouched)
hist = mask.histogram()
touched = sum(hist[128:]) / (img.width * img.height)
print(f"saved {DST}; mask coverage (>50% strength): {touched:.1%}")
