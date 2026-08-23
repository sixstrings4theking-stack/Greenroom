import math
HEAD = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
  html, body { margin:0; padding:0; background:transparent; }
  body { width:%dpx; height:%dpx; overflow:hidden; }
  svg { display:block; }
  .word { font-family:'Segoe UI','Segoe UI Variable',-apple-system,Roboto,Helvetica,Arial,sans-serif; font-weight:800; }
  .tier { font-family:'Segoe UI','Segoe UI Variable',-apple-system,Roboto,Helvetica,Arial,sans-serif; font-weight:800; letter-spacing:10px; }
  .num  { font-family:'Segoe UI','Segoe UI Variable',-apple-system,Roboto,Helvetica,Arial,sans-serif; font-weight:800; }
</style></head>
<body>
'''
DEFS = '''  <defs>
    <radialGradient id="bg" cx="50%%" cy="38%%" r="75%%">
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
def write(name, w, h, body, glow=('14','.45')):
    html = HEAD % (w,h) + f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n' + (DEFS % glow) + body + '</svg></body></html>'
    open(name, 'w', encoding='utf-8').write(html)

def cb(x, y, size):
    ls = -22/600*size; dy = -38/600*size
    return (f'<g filter="url(#glow)">\n'
            f'    <text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="central" dy="{dy:.0f}" class="num" style="letter-spacing:{ls:.0f}px" font-size="{size}">\n'
            f'      <tspan fill="#e7e9ee">C</tspan><tspan fill="url(#amber)">B</tspan>\n'
            f'    </text>\n  </g>')

def lugs(cx, cy, r0, r1, n=8, w=16):
    out=[]
    for i in range(n):
        a = math.pi*2*i/n - math.pi/2
        out.append(f'<line x1="{cx+r0*math.cos(a):.0f}" y1="{cy+r0*math.sin(a):.0f}" x2="{cx+r1*math.cos(a):.0f}" y2="{cy+r1*math.sin(a):.0f}"/>')
    return f'<g stroke="#edaa45" stroke-width="{w}" stroke-linecap="round">' + ''.join(out) + '</g>'

def stick(cx, cy, angle_deg, length, w=24, color="#d9d2c4"):
    a = math.radians(angle_deg)
    x0,y0 = cx - length*.5*math.cos(a), cy - length*.5*math.sin(a)
    x1,y1 = cx + length*.5*math.cos(a), cy + length*.5*math.sin(a)
    return (f'<line x1="{x0:.0f}" y1="{y0:.0f}" x2="{x1:.0f}" y2="{y1:.0f}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<circle cx="{x1:.0f}" cy="{y1:.0f}" r="{w*0.85:.0f}" fill="{color}"/>')

oneshot_body = f'''
  <rect x="0" y="0" width="1024" height="1024" rx="190" ry="190" fill="url(#bg)"/>
  <rect x="3" y="3" width="1018" height="1018" rx="188" ry="188" fill="none" stroke="#2e3440" stroke-width="6"/>
  <g opacity="0.95">
    {stick(512, 560, -40, 490, 26)}
    {stick(512, 560, 220, 490, 26)}
  </g>
  <g filter="url(#glow)">
    <circle cx="512" cy="400" r="205" fill="#161a22"/>
    <circle cx="512" cy="400" r="205" fill="none" stroke="url(#amber)" stroke-width="28"/>
    {lugs(512, 400, 224, 254)}
    <text x="503" y="400" text-anchor="middle" dominant-baseline="central" dy="-14" class="num" font-size="260" fill="url(#amber)">1</text>
  </g>
  <g stroke="#f2b85a" stroke-width="14" stroke-linecap="round">
    <line x1="712" y1="230" x2="756" y2="196"/>
    <line x1="742" y1="292" x2="796" y2="272"/>
    <line x1="664" y1="180" x2="690" y2="130"/>
  </g>
  <text x="512" y="812" text-anchor="middle" class="tier" font-size="86" fill="#e7e9ee">ONE SHOT</text>
  <text x="512" y="920" text-anchor="middle" class="word" font-size="56">
    <tspan fill="#8b93a3" style="font-weight:600;">One-Time Supporter · </tspan><tspan fill="#e7e9ee">Chart</tspan><tspan fill="#e8a13f">Bench</tspan>
  </text>
'''
write('oneshot-src.html', 1024, 1024, oneshot_body, ('18','.5'))

round_body = f'''
  <circle cx="550" cy="550" r="530" fill="#f4f2ec"/>
  <circle cx="550" cy="550" r="490" fill="url(#bg)"/>
  <defs>
    <path id="arcTop" d="M 550,550 m -400,0 a 400,400 0 0 1 800,0" fill="none"/>
    <path id="arcBot" d="M 550,550 m -400,0 a 400,400 0 0 0 800,0" fill="none"/>
  </defs>
  <text class="tier" font-size="92" fill="#e7e9ee" letter-spacing="26"><textPath href="#arcTop" startOffset="50%" text-anchor="middle">CHARTBENCH</textPath></text>
  <text class="word" font-size="50" fill="#8b93a3" letter-spacing="6" font-weight="600"><textPath href="#arcBot" startOffset="50%" text-anchor="middle">thechartbench.com</textPath></text>
  <g filter="url(#glow)">
    <circle cx="550" cy="560" r="230" fill="none" stroke="url(#amber)" stroke-width="22"/>
  </g>
  {cb(546, 568, 300)}
'''
write('sticker-round-src.html', 1100, 1100, round_body, ('16','.45'))

pick_body = f'''
  <path d="M 455,1000 C 280,860 90,650 90,390 C 90,160 270,52 500,52 C 730,52 910,160 910,390 C 910,650 720,860 545,1000 Q 500,1046 455,1000 Z" fill="#f4f2ec"/>
  <path d="M 462,952 C 308,825 128,640 128,392 C 128,182 292,90 500,90 C 708,90 872,182 872,392 C 872,640 692,825 538,952 Q 500,990 462,952 Z" fill="url(#bg)"/>
  {cb(496, 400, 380)}
  <text x="500" y="700" text-anchor="middle" class="word" font-size="80" letter-spacing="-3">
    <tspan fill="#e7e9ee">Chart</tspan><tspan fill="#e8a13f">Bench</tspan>
  </text>
  <text x="500" y="780" text-anchor="middle" class="word" font-size="38" font-weight="600" fill="#8b93a3">thechartbench.com</text>
'''
write('sticker-pick-src.html', 1000, 1150, pick_body)

tile_body = f'''
  <rect x="10" y="10" width="1080" height="1080" rx="240" fill="#f4f2ec"/>
  <rect x="48" y="48" width="1004" height="1004" rx="205" fill="url(#bg)"/>
  <rect x="51" y="51" width="998" height="998" rx="203" fill="none" stroke="#2e3440" stroke-width="6"/>
  {cb(546, 500, 560)}
  <text x="550" y="900" text-anchor="middle" class="word" font-size="72" letter-spacing="-2">
    <tspan fill="#e7e9ee">Chart</tspan><tspan fill="#e8a13f">Bench</tspan>
  </text>
  <text x="550" y="970" text-anchor="middle" class="word" font-size="36" font-weight="600" fill="#8b93a3">thechartbench.com</text>
'''
write('sticker-tile-src.html', 1100, 1100, tile_body, ('16','.45'))

strip_body = '''
  <rect x="10" y="10" width="1380" height="540" rx="120" fill="#f4f2ec"/>
  <rect x="42" y="42" width="1316" height="476" rx="92" fill="url(#bg)"/>
  <g filter="url(#glow)">
    <circle cx="330" cy="230" r="112" fill="none" stroke="url(#amber)" stroke-width="18"/>
    <text x="325" y="230" text-anchor="middle" dominant-baseline="central" dy="-8" class="num" font-size="146" fill="url(#amber)">1</text>
    <circle cx="700" cy="230" r="112" fill="none" stroke="url(#amber)" stroke-width="18"/>
    <text x="698" y="230" text-anchor="middle" dominant-baseline="central" dy="-8" class="num" font-size="146" fill="url(#amber)">4</text>
    <circle cx="1070" cy="230" r="112" fill="none" stroke="url(#amber)" stroke-width="18"/>
    <text x="1070" y="230" text-anchor="middle" dominant-baseline="central" dy="-8" class="num" font-size="146" fill="url(#amber)">5</text>
  </g>
  <text x="700" y="443" text-anchor="middle" class="word" font-size="62" letter-spacing="-2">
    <tspan fill="#e7e9ee">Chart</tspan><tspan fill="#e8a13f">Bench</tspan><tspan fill="#8b93a3" font-size="44" font-weight="600"> · thechartbench.com</tspan>
  </text>
'''
write('sticker-145-src.html', 1400, 560, strip_body, ('10','.4'))
print('written v2')
