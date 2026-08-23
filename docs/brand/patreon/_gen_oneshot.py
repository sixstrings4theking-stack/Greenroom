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

write('oneshot-src.html', 1024, 1024, '''
  <rect x="0" y="0" width="1024" height="1024" rx="190" ry="190" fill="url(#bg)"/>
  <rect x="3" y="3" width="1018" height="1018" rx="188" ry="188" fill="none" stroke="#2e3440" stroke-width="6"/>
  <g filter="url(#glow)">
    <circle cx="512" cy="430" r="230" fill="none" stroke="url(#amber)" stroke-width="30"/>
    <g stroke="#edaa45" stroke-width="20" stroke-linecap="round">
      <line x1="512" y1="128" x2="512" y2="180"/>
      <line x1="512" y1="680" x2="512" y2="732"/>
      <line x1="210" y1="430" x2="262" y2="430"/>
      <line x1="762" y1="430" x2="814" y2="430"/>
    </g>
    <text x="502" y="430" text-anchor="middle" dominant-baseline="central" dy="-16.5"
          class="num" font-size="300" fill="url(#amber)">1</text>
  </g>
  <text x="512" y="812" text-anchor="middle" class="tier" font-size="86" fill="#e7e9ee">ONE SHOT</text>
  <text x="512" y="920" text-anchor="middle" class="word" font-size="56">
    <tspan fill="#8b93a3" style="font-weight:600;">One-Time Supporter · </tspan><tspan fill="#e7e9ee">Chart</tspan><tspan fill="#e8a13f">Bench</tspan>
  </text>
''', ('18','.5'))

write('sticker-round-src.html', 1100, 1100, '''
  <circle cx="550" cy="550" r="530" fill="#f4f2ec"/>
  <circle cx="550" cy="550" r="490" fill="url(#bg)"/>
  <defs>
    <path id="arcTop" d="M 550,550 m -400,0 a 400,400 0 0 1 800,0" fill="none"/>
    <path id="arcBot" d="M 550,550 m -400,0 a 400,400 0 0 0 800,0" fill="none"/>
  </defs>
  <text class="tier" font-size="92" fill="#e7e9ee" letter-spacing="26"><textPath href="#arcTop" startOffset="50%" text-anchor="middle">CHARTBENCH</textPath></text>
  <text class="word" font-size="54" fill="#8b93a3" letter-spacing="6" font-weight="600"><textPath href="#arcBot" startOffset="50%" text-anchor="middle">thechartbench.com</textPath></text>
  <g filter="url(#glow)">
    <circle cx="550" cy="560" r="205" fill="none" stroke="url(#amber)" stroke-width="28"/>
    <text x="541" y="560" text-anchor="middle" dominant-baseline="central" dy="-15"
          class="num" font-size="270" fill="url(#amber)">1</text>
  </g>
''', ('16','.45'))

write('sticker-pick-src.html', 1000, 1150, '''
  <path d="M 455,1000 C 280,860 90,650 90,390 C 90,160 270,52 500,52 C 730,52 910,160 910,390 C 910,650 720,860 545,1000 Q 500,1046 455,1000 Z" fill="#f4f2ec"/>
  <path d="M 462,952 C 308,825 128,640 128,392 C 128,182 292,90 500,90 C 708,90 872,182 872,392 C 872,640 692,825 538,952 Q 500,990 462,952 Z" fill="url(#bg)"/>
  <g filter="url(#glow)">
    <circle cx="500" cy="420" r="195" fill="none" stroke="url(#amber)" stroke-width="26"/>
    <text x="491" y="420" text-anchor="middle" dominant-baseline="central" dy="-14"
          class="num" font-size="255" fill="url(#amber)">1</text>
  </g>
  <text x="500" y="740" text-anchor="middle" class="word" font-size="84" letter-spacing="-3">
    <tspan fill="#e7e9ee">Chart</tspan><tspan fill="#e8a13f">Bench</tspan>
  </text>
''')

write('sticker-145-src.html', 1400, 560, '''
  <rect x="10" y="10" width="1380" height="540" rx="120" fill="#f4f2ec"/>
  <rect x="42" y="42" width="1316" height="476" rx="92" fill="url(#bg)"/>
  <g filter="url(#glow)">
    <circle cx="330" cy="240" r="115" fill="none" stroke="url(#amber)" stroke-width="18"/>
    <text x="325" y="240" text-anchor="middle" dominant-baseline="central" dy="-8" class="num" font-size="150" fill="url(#amber)">1</text>
    <circle cx="700" cy="240" r="115" fill="none" stroke="url(#amber)" stroke-width="18"/>
    <text x="698" y="240" text-anchor="middle" dominant-baseline="central" dy="-8" class="num" font-size="150" fill="url(#amber)">4</text>
    <circle cx="1070" cy="240" r="115" fill="none" stroke="url(#amber)" stroke-width="18"/>
    <text x="1070" y="240" text-anchor="middle" dominant-baseline="central" dy="-8" class="num" font-size="150" fill="url(#amber)">5</text>
  </g>
  <text x="700" y="455" text-anchor="middle" class="word" font-size="54">
    <tspan fill="#8b93a3" font-weight="600">Know these three, play anything. · </tspan><tspan fill="#e7e9ee">Chart</tspan><tspan fill="#e8a13f">Bench</tspan>
  </text>
''', ('10','.4'))

write('sticker-slogan-src.html', 1400, 640, '''
  <rect x="10" y="10" width="1380" height="620" rx="110" fill="#f4f2ec"/>
  <rect x="42" y="42" width="1316" height="556" rx="82" fill="url(#bg)"/>
  <text x="700" y="250" text-anchor="middle" class="word" font-size="150" letter-spacing="-4">
    <tspan fill="#e7e9ee">Play by </tspan><tspan fill="url(#amber)">numbers.</tspan>
  </text>
  <line x1="380" y1="352" x2="1020" y2="352" stroke="#edaa45" stroke-width="10" stroke-linecap="round"/>
  <text x="700" y="490" text-anchor="middle" class="word" font-size="76" letter-spacing="-2">
    <tspan fill="#e7e9ee">Chart</tspan><tspan fill="#e8a13f">Bench</tspan><tspan fill="#8b93a3" font-size="56" font-weight="600"> · thechartbench.com</tspan>
  </text>
''', ('10','.4'))
print('written')
