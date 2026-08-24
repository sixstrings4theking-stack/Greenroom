# Patreon tier-card badges at Patreon's recommended 460x200. Designed and
# rendered at 2x (920x400), then LANCZOS-downscaled, so text and rings stay
# crisp. Writes the tier*/oneshot src HTMLs and their PNGs in one run:
#   python _gen_tiercards.py
# Digit optical-centering offsets carry over from the 1024 squares, scaled.
import math, os, time, io
os.chdir(os.path.dirname(os.path.abspath(__file__)))

W, H = 920, 400  # 2x canvas; final PNGs are 460x200

HEAD = f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
  html, body {{ margin:0; padding:0; background:transparent; }}
  body {{ width:{W}px; height:{H}px; overflow:hidden; }}
  svg {{ display:block; }}
  .word {{ font-family:'Segoe UI','Segoe UI Variable',-apple-system,Roboto,Helvetica,Arial,sans-serif; font-weight:800; }}
  .tier {{ font-family:'Segoe UI','Segoe UI Variable',-apple-system,Roboto,Helvetica,Arial,sans-serif; font-weight:800; letter-spacing:12px; }}
  .num  {{ font-family:'Segoe UI','Segoe UI Variable',-apple-system,Roboto,Helvetica,Arial,sans-serif; font-weight:800; }}
</style></head>
<body>
'''
DEFS = '''  <defs>
    <radialGradient id="bg" cx="32%%" cy="38%%" r="95%%">
      <stop offset="0" stop-color="#222835"/>
      <stop offset="1" stop-color="#12151b"/>
    </radialGradient>
    <linearGradient id="amber" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#f2b85a"/>
      <stop offset="1" stop-color="#e8a13f"/>
    </linearGradient>
    <filter id="glow" x="-30%%" y="-30%%" width="160%%" height="160%%">
      <feGaussianBlur stdDeviation="%s" result="b"/>
      <feColorMatrix in="b" type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 %s 0" result="g"/>
      <feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
'''

def write(name, body, glow=('9', '.45')):
    html = (HEAD + f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n'
            + (DEFS % glow) + body + '</svg></body></html>')
    open(name, 'w', encoding='utf-8').write(html)

# Full-bleed background (Patreon rounds its own card corners) + inset stroke.
BG = f'''  <rect x="0" y="0" width="{W}" height="{H}" fill="url(#bg)"/>
  <rect x="3" y="3" width="{W-6}" height="{H-6}" fill="none" stroke="#2e3440" stroke-width="6"/>
'''

TEXT_X = 605  # center of the text block, right of the ring

def tier_body(digit, dx, dy, label, sub='Patreon Supporter'):
    # dx/dy are the 1024-square optical offsets at font-size 300, scaled to 156.
    k = 156 / 300
    return BG + f'''  <g filter="url(#glow)">
    <circle cx="190" cy="200" r="120" fill="none" stroke="url(#amber)" stroke-width="17"/>
    <text x="{190 + dx*k:.1f}" y="200" text-anchor="middle" dominant-baseline="central" dy="{dy*k:.1f}"
          class="num" font-size="156" fill="url(#amber)">{digit}</text>
  </g>
  <text x="{TEXT_X}" y="203" text-anchor="middle" class="tier" font-size="78" fill="#e7e9ee">{label}</text>
  <text x="{TEXT_X}" y="272" text-anchor="middle" class="word" font-size="33">
    <tspan fill="#8b93a3" font-weight="600">{sub} · </tspan><tspan fill="#e7e9ee">Chart</tspan><tspan fill="#e8a13f">Bench</tspan>
  </text>
'''

write('tier1-the-one-src.html',  tier_body('1', -3, -16.5, 'THE ONE'))
write('tier2-the-four-src.html', tier_body('4', -4, -19.0, 'THE FOUR'))
write('tier3-the-five-src.html', tier_body('5', +1, -21.0, 'THE FIVE'))

# OneShot: the drum badge, same left-emblem/right-text layout. Geometry is
# the 1024 square's, scaled by 105/205 and re-centered on (190, 200).
def lugs(cx, cy, r0, r1, n=8, w=8):
    out = []
    for i in range(n):
        a = math.pi*2*i/n - math.pi/2
        out.append(f'<line x1="{cx+r0*math.cos(a):.0f}" y1="{cy+r0*math.sin(a):.0f}" x2="{cx+r1*math.cos(a):.0f}" y2="{cy+r1*math.sin(a):.0f}"/>')
    return f'<g stroke="#edaa45" stroke-width="{w}" stroke-linecap="round">' + ''.join(out) + '</g>'

def stick(cx, cy, angle_deg, length, w=13, color="#d9d2c4"):
    a = math.radians(angle_deg)
    x0, y0 = cx - length*.5*math.cos(a), cy - length*.5*math.sin(a)
    x1, y1 = cx + length*.5*math.cos(a), cy + length*.5*math.sin(a)
    return (f'<line x1="{x0:.0f}" y1="{y0:.0f}" x2="{x1:.0f}" y2="{y1:.0f}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<circle cx="{x1:.0f}" cy="{y1:.0f}" r="{w*0.85:.0f}" fill="{color}"/>')

oneshot_body = BG + f'''  <g opacity="0.95">
    {stick(190, 282, -40, 250)}
    {stick(190, 282, 220, 250)}
  </g>
  <g filter="url(#glow)">
    <circle cx="190" cy="200" r="105" fill="#161a22"/>
    <circle cx="190" cy="200" r="105" fill="none" stroke="url(#amber)" stroke-width="14"/>
    {lugs(190, 200, 115, 130)}
    <text x="185.4" y="200" text-anchor="middle" dominant-baseline="central" dy="-7" class="num" font-size="133" fill="url(#amber)">1</text>
  </g>
  <g stroke="#f2b85a" stroke-width="7" stroke-linecap="round">
    <line x1="292" y1="113" x2="315" y2="96"/>
    <line x1="308" y1="145" x2="336" y2="135"/>
    <line x1="268" y1="88" x2="281" y2="62"/>
  </g>
  <text x="{TEXT_X}" y="203" text-anchor="middle" class="tier" font-size="78" fill="#e7e9ee">ONE SHOT</text>
  <text x="{TEXT_X}" y="272" text-anchor="middle" class="word" font-size="33">
    <tspan fill="#8b93a3" font-weight="600">One-Time Supporter · </tspan><tspan fill="#e7e9ee">Chart</tspan><tspan fill="#e8a13f">Bench</tspan>
  </text>
'''
write('oneshot-src.html', oneshot_body, ('11', '.5'))
print('src HTMLs written')

# ---- render: headless Chrome screenshot at 920x400, downscale to 460x200 ----
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image

JOBS = [
    ('tier1-the-one-src.html',  'chartbench-patreon-tier1-the-one.png'),
    ('tier2-the-four-src.html', 'chartbench-patreon-tier2-the-four.png'),
    ('tier3-the-five-src.html', 'chartbench-patreon-tier3-the-five.png'),
    ('oneshot-src.html',        'chartbench-oneshot.png'),
]
import base64
opts = Options()
opts.add_argument('--headless=new')
opts.add_argument(f'--window-size={W},{H+120}')
opts.add_argument('--hide-scrollbars')
d = webdriver.Chrome(options=opts)
# Pin the viewport exactly — Windows display scaling otherwise shrinks it
# below the requested window size and the capture crops.
d.execute_cdp_cmd('Emulation.setDeviceMetricsOverride',
                  {'width': W, 'height': H, 'deviceScaleFactor': 1, 'mobile': False})
for src, png in JOBS:
    d.get('file:///' + os.path.abspath(src).replace('\\', '/'))
    time.sleep(0.6)
    shot = d.execute_cdp_cmd('Page.captureScreenshot', {'format': 'png'})
    img = Image.open(io.BytesIO(base64.b64decode(shot['data']))).convert('RGB')
    assert img.size == (W, H), img.size
    img = img.resize((460, 200), Image.LANCZOS)
    img.save(png)
    print(png, img.size)
d.quit()
print('done')
