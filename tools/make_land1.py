"""Rasterize Natural Earth 110m land to a 1deg (360x180) bitmask for the hero globe.

Scanline even-odd ray cast: per latitude row collect edge crossings (x at that lat
is constant per edge), then per cell count crossings to the right via bisect.
Writes base64 of the bitmask to _land_b64.txt (backup of the old 3deg mask kept
as _land3_b64.txt by the caller).
"""
import base64
import bisect
import json

WS = "/Users/zhw/.qoderwork/workspace/mtmqoy4hwvnd8s3g"
d = json.load(open(f"{WS}/_ne_land.geojson"))

rings = []
for f in d["features"]:
    g = f["geometry"]
    polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
    for poly in polys:
        rings.extend(poly)

edges = []
for ring in rings:
    for i in range(len(ring) - 1):
        x1, y1 = ring[i][0], ring[i][1]
        x2, y2 = ring[i + 1][0], ring[i + 1][1]
        if y1 == y2:
            continue
        edges.append((y1, y2, x1, x2))
print("rings", len(rings), "edges", len(edges))

ROWS, COLS = 180, 360
bits = bytearray(ROWS * COLS // 8)
land = 0
for r in range(ROWS):
    lat = 90 - 1 * (r + 0.5)
    xs = []
    for y1, y2, x1, x2 in edges:
        if (y1 > lat) != (y2 > lat):
            xs.append(x1 + (lat - y1) * (x2 - x1) / (y2 - y1))
    xs.sort()
    row = r * COLS
    for c in range(COLS):
        lon = -180 + 1 * (c + 0.5)
        cnt = len(xs) - bisect.bisect_left(xs, lon)
        if cnt & 1:
            idx = row + c
            bits[idx >> 3] |= 1 << (7 - (idx & 7))
            land += 1
print("land cells", land, "of", ROWS * COLS)
b64 = base64.b64encode(bytes(bits)).decode()
open(f"{WS}/_land_b64.txt", "w").write(b64)
print("b64 chars", len(b64))
