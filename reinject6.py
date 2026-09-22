#!/usr/bin/env python3
"""v6 build: font self-sync + asset injection.

Why this file exists: the SHS woff2 subsets only carry the glyphs listed in
fonts/charset_live.txt. Any new CJK character added to demo6_template.html
used to fall back to a system face silently (visibly off-baseline glyphs).
Every build now:
  1. extracts CJK from the template,
  2. unions it into the monotonic fonts/charset_live.txt (chars never drop),
  3. diffs that against the current woff2 cmap and re-subsets BOTH weights
     automatically if anything is missing, then re-base64s them,
  4. injects the binary assets, and finally
  5. asserts the shipped index.html contains no glyph absent from the font,
     so a broken font can never ship quietly again.

Edit demo6_template.html, then just run:  python3 reinject6.py
Output: ./index.html  (this is also the file GitHub Pages serves at repo root).

------------------------------------------------------------------------
FONT SOURCE FILES (not committed to keep the repo light)
------------------------------------------------------------------------
Re-subsetting needs the two full Source Han Serif CN OTFs (~11.6 MB each):
    fonts/SourceHanSerifCN-Regular.otf
    fonts/SourceHanSerifCN-SemiBold.otf
Download them (SIL Open Font License) from Adobe's official release:
    https://github.com/adobe-fonts/source-han-serif/releases
  -> pick "09_SourceHanSerifCN.zip" (Simplified Chinese), unpack the
     Regular and SemiBold OTFs into fonts/ with the exact names above.

If the OTFs are ABSENT, the build still runs: it reuses the committed
woff2 subsets and only WARNS about characters it cannot verify/add.
That is enough for text-only edits that reuse existing glyphs. As soon as
you introduce a NEW CJK character, drop the OTFs in and re-run so the
subset is recast and the hard glyph guard re-engages.
------------------------------------------------------------------------
Requires: python3, fontTools  (pip install fonttools brotli)
"""
import base64, os, subprocess, sys

RANGES = ((0x2000, 0x9FFF), (0xFF00, 0xFFEF), (0x3000, 0x303F))
LIVE = 'fonts/charset_live.txt'
WEIGHTS = (('fonts/SourceHanSerifCN-Regular.otf', 'fonts/SHS-Regular.woff2', 'fonts/v5_font_reg.b64.txt'),
           ('fonts/SourceHanSerifCN-SemiBold.otf', 'fonts/SHS-SemiBold.woff2', 'fonts/v5_font_sb.b64.txt'))
OTF_AVAILABLE = all(os.path.exists(w[0]) for w in WEIGHTS)

# Icon/UI glyphs that Source Han Serif does not provide on purpose; they are
# rendered by system fallback and must NOT be treated as missing-glyph errors.
# (When the OTF is present this set is derived automatically as want - src;
#  it is only hardcoded here for the OTF-absent warning path.)
ICON_FALLBACK = set('⌕⌘⏎←→↑↓✓·')


def cjk(s):
    return {ch for ch in s if any(a <= ord(ch) <= b for a, b in RANGES)}


def cmap(path):
    from fontTools.ttLib import TTFont
    return {chr(k) for k in TTFont(path).getBestCmap()}


def sync_fonts(tpl_text):
    live = set(open(LIVE, encoding='utf-8').read()) if os.path.exists(LIVE) else set()
    want = live | cjk(tpl_text)
    if want != live or not os.path.exists(LIVE):
        open(LIVE, 'w', encoding='utf-8').write(''.join(sorted(want)))

    if not OTF_AVAILABLE:
        # No OTF source: cannot recast. Reuse committed woff2, warn on gaps.
        have = set()
        for _s, woff, _b in WEIGHTS:
            if os.path.exists(woff):
                have |= cmap(woff)
        gap = {c for c in (want - have) if c not in ICON_FALLBACK and cjk(c)}
        print('font sync: OTF source absent -> reusing committed woff2 subsets '
              '(%d chars in charset_live).' % len(want))
        if gap:
            print('  WARNING: %d char(s) in the template are NOT in the current '
                  'subset and will fall back to a system font: %s'
                  % (len(gap), ''.join(sorted(gap))))
            print('  To fix: download the Source Han Serif CN OTFs into fonts/ '
                  '(see header) and re-run so the subset is recast.')
        return

    src = cmap(WEIGHTS[0][0])           # what Source Han Serif can provide at all
    unsupported = want - src            # icon glyphs (⌕ ⌘ ⏎ …): intentional system fallback
    missing = (want & src) - cmap(WEIGHTS[0][1])
    if missing:
        for srcf, out, _b in WEIGHTS:
            subprocess.run([sys.executable, '-m', 'fontTools.subset', srcf,
                            '--text-file=' + LIVE, '--flavor=woff2', '--no-hinting',
                            '--output-file=' + out], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _s, woff, b64 in WEIGHTS:
            open(b64, 'w').write(base64.b64encode(open(woff, 'rb').read()).decode())
        print('font sync: +%d glyph(s) recast:' % len(missing), ''.join(sorted(missing)))
    else:
        print('font sync: in sync (%d chars, 0 missing)' % len(want))
    if unsupported:
        print('font sync: note, %d char(s) absent from Source Han Serif, left to system fallback:' % len(unsupported), ''.join(sorted(unsupported)))


tpl = open('demo6_template.html', encoding='utf-8').read()
sync_fonts(tpl)

assets = {}
for line in open('assets/demo_assets_b64.txt'):
    line = line.strip()
    if not line or '=' not in line: continue
    k, v = line.split('=', 1)
    assets[k.strip()] = v.strip()
island = open('assets/v6_island.b64.txt').read().strip()
branch = open('assets/v4_branch_mul.b64.txt').read().strip()
land = open('assets/_land_b64.txt').read().strip()
fontreg = open('fonts/v5_font_reg.b64.txt').read().strip()
fontsb = open('fonts/v5_font_sb.b64.txt').read().strip()
photo = open('assets/v6_photo.b64.txt').read().strip()
tpl = (tpl.replace('{{LOGO_B64}}', assets['LOGO'])
          .replace('{{ISLAND_B64}}', island)
          .replace('{{BRANCH_B64}}', branch)
          .replace('{{LAND_B64}}', land)
          .replace('{{FONT_REG_B64}}', fontreg)
          .replace('{{FONT_SB_B64}}', fontsb)
          .replace('{{PHOTO_B64}}', photo))
assert '{{' not in tpl, 'unreplaced placeholder remains in template'
out = 'index.html'
open(out, 'w', encoding='utf-8').write(tpl)
print('injected v6 ->', out, len(tpl) // 1024, 'KB', len(tpl), 'bytes')

# post-build glyph guard: the shipped file must not use any char the font lacks.
# Hard-fails when the OTF source is present (so a broken font can never ship);
# downgraded to a warning when it is not (see header note).
ship_all = cjk(open(out, encoding='utf-8').read())
if OTF_AVAILABLE:
    ship = ship_all & cmap(WEIGHTS[0][0])
    for _s, woff, _b in WEIGHTS:
        gap = ship - cmap(woff)
        assert not gap, 'shipped page uses glyphs missing from %s: %s' % (woff, ''.join(sorted(gap)))
    print('glyph guard: shipped CJK %d chars, covered by both weights' % len(ship))
else:
    have = set()
    for _s, woff, _b in WEIGHTS:
        if os.path.exists(woff):
            have |= cmap(woff)
    gap = ship_all - have - ICON_FALLBACK
    if gap:
        print('glyph guard (OTF absent, WARNING only): %d shipped char(s) not in subset: %s'
              % (len(gap), ''.join(sorted(gap))))
    else:
        print('glyph guard: shipped CJK %d chars, all covered by committed woff2' % len(ship_all))
