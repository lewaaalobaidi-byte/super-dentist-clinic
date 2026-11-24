"""Original SVG illustrations for the 7 service cards (400 x 250)."""
import os
OUT = os.path.join(os.path.dirname(__file__), 'site', 'services')
os.makedirs(OUT, exist_ok=True)

TOOTH = ("M -38,-48 C -55,-48 -62,-30 -58,-12 C -54,6 -48,16 -46,34 C -44,52 -40,66 -30,66 "
         "C -20,66 -18,50 -14,38 C -10,26 -6,22 0,22 C 6,22 10,26 14,38 C 18,50 20,66 30,66 "
         "C 40,66 44,52 46,34 C 48,16 54,6 58,-12 C 62,-30 55,-48 38,-48 C 26,-48 14,-40 0,-40 "
         "C -14,-40 -26,-48 -38,-48 Z")
CROWN = ("M -38,-48 C -55,-48 -62,-30 -58,-12 C -55,2 -50,10 -48,16 L 48,16 C 50,10 55,2 58,-12 "
         "C 62,-30 55,-48 38,-48 C 26,-48 14,-40 0,-40 C -14,-40 -26,-48 -38,-48 Z")


def defs(c1, c2):
    return f'''<defs>
  <radialGradient id="bg" cx="20%" cy="0%" r="130%"><stop offset="0" stop-color="{c2}"/><stop offset=".75" stop-color="{c1}"/></radialGradient>
  <linearGradient id="enamel" x1="0" y1="0" x2="0.4" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".55" stop-color="#f1f7ff"/><stop offset="1" stop-color="#cfe0f5"/></linearGradient>
  <linearGradient id="glass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity=".08"/></linearGradient>
  <linearGradient id="metal" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a97a8"/><stop offset=".35" stop-color="#eef2f7"/><stop offset=".6" stop-color="#b9c4d2"/><stop offset="1" stop-color="#6f7c8e"/></linearGradient>
  <linearGradient id="pulp" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fb7185"/><stop offset="1" stop-color="#e11d48"/></linearGradient>
  <filter id="shadow" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="10" stdDeviation="10" flood-color="#0b1d3a" flood-opacity=".35"/></filter>
  <filter id="soft"><feGaussianBlur stdDeviation="6"/></filter>
</defs>'''


def frame(c1, c2, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 250" preserveAspectRatio="xMidYMid slice">
{defs(c1, c2)}
<rect width="400" height="250" fill="url(#bg)"/>
<circle cx="345" cy="20" r="120" fill="#fff" fill-opacity=".14" stroke="#fff" stroke-opacity=".3"/>
<circle cx="30" cy="250" r="80" fill="#fff" fill-opacity=".10" stroke="#fff" stroke-opacity=".25"/>
<ellipse cx="200" cy="222" rx="90" ry="10" fill="#0b1d3a" fill-opacity=".22" filter="url(#soft)"/>
{body}
<rect width="400" height="250" fill="url(#glass)" opacity=".35"/>
</svg>'''


def sparkle(x, y, s=1, o=1):
    return (f'<path transform="translate({x},{y}) scale({s})" d="M0,-12 C1.5,-3 3,-1.5 12,0 C3,1.5 1.5,3 0,12 '
            f'C-1.5,3 -3,1.5 -12,0 C-3,-1.5 -1.5,-3 0,-12 Z" fill="#fff" fill-opacity="{o}"/>')


def tooth(x, y, s=1, extra=''):
    return (f'<g transform="translate({x},{y}) scale({s})" filter="url(#shadow)">'
            f'<path d="{TOOTH}" fill="url(#enamel)" stroke="#fff" stroke-width="2"/>'
            f'<path d="M -40,-38 C -44,-22 -42,-8 -36,4" stroke="#fff" stroke-width="7" stroke-linecap="round" fill="none" opacity=".9"/>'
            f'{extra}</g>')


ART = {}

# 1 Hollywood smile: a bright smile with sparkles
teeth = ''.join(
    f'<rect x="{-66 + i * 19}" y="-14" width="17" height="{30 - abs(i - 3.5) * 3}" rx="7" fill="url(#enamel)" stroke="#e2ecf8" stroke-width="1"/>'
    for i in range(8))
ART['hollywood-smile'] = ('#2563EB', '#7DD3FC', f'''
<g transform="translate(200,128)" filter="url(#shadow)">
  <path d="M -95,-22 C -60,-40 60,-40 95,-22 C 80,40 -80,40 -95,-22 Z" fill="#be123c"/>
  <path d="M -86,-18 C -50,-30 50,-30 86,-18 C 70,30 -70,30 -86,-18 Z" fill="#7f1d1d"/>
  <g clip-path="url(#mouth)">{teeth}</g>
  <clipPath id="mouth"><path d="M -86,-18 C -50,-30 50,-30 86,-18 C 70,30 -70,30 -86,-18 Z"/></clipPath>
  <path d="M -95,-22 C -60,-40 60,-40 95,-22" stroke="#fda4af" stroke-width="6" fill="none" stroke-linecap="round" opacity=".7"/>
</g>
{sparkle(300, 70, 1.6)}{sparkle(110, 62, 1.0, .9)}{sparkle(330, 160, .9, .8)}{sparkle(85, 170, .7, .7)}''')

# 2 Implant: crown + abutment + titanium screw
threads = ''.join(f'<path d="M -22,{y} L 22,{y + 6}" stroke="#64748b" stroke-width="3" stroke-linecap="round"/>' for y in range(34, 92, 10))
ART['dental-implants'] = ('#0E7490', '#5EEAD4', f'''
<g transform="translate(200,98) scale(.95)" filter="url(#shadow)">
  <path d="M -24,26 L 24,26 L 18,100 Q 0,116 -18,100 Z" fill="url(#metal)" stroke="#e2e8f0" stroke-width="1.5"/>
  {threads}
  <rect x="-15" y="12" width="30" height="18" rx="4" fill="url(#metal)"/>
  <path d="{CROWN}" fill="url(#enamel)" stroke="#fff" stroke-width="2"/>
  <path d="M -40,-38 C -44,-24 -42,-10 -36,0" stroke="#fff" stroke-width="7" stroke-linecap="round" fill="none"/>
</g>
{sparkle(285, 60, 1.2)}{sparkle(120, 80, .8, .8)}''')

# 3 Cosmetic: tooth with a magic wand and sparkles
ART['cosmetic-dentistry'] = ('#7C3AED', '#F0ABFC', f'''
{tooth(185, 120, 1.15)}
<g transform="translate(285,85) rotate(40)" filter="url(#shadow)">
  <rect x="-5" y="0" width="10" height="90" rx="5" fill="#1e1b4b"/>
  <rect x="-5" y="0" width="10" height="16" rx="5" fill="#fff"/>
</g>
{sparkle(272, 62, 1.8)}{sparkle(300, 40, .9)}{sparkle(250, 40, .7, .9)}{sparkle(110, 70, .9, .8)}{sparkle(120, 175, .6, .7)}''')

# 4 Orthodontics: row of teeth with brackets and wire
row = ''
for i in range(4):
    x = -96 + i * 64
    row += (f'<g transform="translate({x + 32},0) scale(.62)"><path d="{CROWN}" fill="url(#enamel)" stroke="#fff" stroke-width="3"/></g>'
            f'<rect x="{x + 20}" y="-14" width="24" height="18" rx="4" fill="url(#metal)" stroke="#94a3b8"/>')
ART['orthodontics'] = ('#1D4ED8', '#A5B4FC', f'''
<g transform="translate(200,120)" filter="url(#shadow)">
  {row}
  <path d="M -96,-5 C -40,-1 40,-1 96,-5" stroke="#cbd5e1" stroke-width="3.5" fill="none"/>
</g>
{sparkle(310, 60, 1.1)}{sparkle(95, 70, .8, .8)}''')

# 5 Root canal: tooth cross-section with canals
ART['root-canal'] = ('#0F766E', '#99F6E4', tooth(200, 112, 1.25, '''
  <path d="M -18,-22 C -20,-10 -18,4 -22,18 C -26,34 -30,48 -30,60 M 18,-22 C 20,-10 18,4 22,18 C 26,34 30,48 30,60"
        stroke="url(#pulp)" stroke-width="7" stroke-linecap="round" fill="none"/>
  <path d="M -22,-26 C -10,-34 10,-34 22,-26 C 18,-12 -18,-12 -22,-26 Z" fill="url(#pulp)"/>
  <circle cx="-30" cy="62" r="3" fill="#fbbf24"/><circle cx="30" cy="62" r="3" fill="#fbbf24"/>''') +
    sparkle(300, 70, 1.0) + sparkle(110, 80, .7, .8))

# 6 Pediatric: friendly tooth with a face and a toothbrush
ART['pediatric-dentistry'] = ('#EA580C', '#FDE68A', tooth(180, 118, 1.15, '''
  <circle cx="-17" cy="-14" r="5.5" fill="#1e293b"/><circle cx="17" cy="-14" r="5.5" fill="#1e293b"/>
  <circle cx="-15" cy="-16" r="1.8" fill="#fff"/><circle cx="19" cy="-16" r="1.8" fill="#fff"/>
  <path d="M -12,2 Q 0,14 12,2" stroke="#1e293b" stroke-width="3.5" fill="none" stroke-linecap="round"/>
  <ellipse cx="-30" cy="0" rx="7" ry="4" fill="#fb7185" opacity=".55"/><ellipse cx="30" cy="0" rx="7" ry="4" fill="#fb7185" opacity=".55"/>''') + '''
<g transform="translate(292,128) rotate(-35)" filter="url(#shadow)">
  <rect x="-6" y="-10" width="12" height="96" rx="6" fill="#38bdf8"/>
  <rect x="-11" y="-36" width="22" height="30" rx="6" fill="#fff"/>
  <g fill="#e0f2fe">''' + ''.join(f'<rect x="{-9 + i * 5}" y="-48" width="3" height="14" rx="1.5"/>' for i in range(4)) + '''</g>
</g>''' + sparkle(110, 70, 1.0) + sparkle(320, 55, .8, .9))

# 7 Laser whitening: light beams on a bright tooth + shade scale
beams = ''.join(f'<path d="M 60,10 L {200 + dx},{100 + dy}" stroke="#fff" stroke-opacity=".35" stroke-width="{w}" stroke-linecap="round"/>'
                for dx, dy, w in [(-20, -10, 10), (0, 0, 14), (20, 8, 8)])
shades = ''.join(f'<rect x="{278 + i * 18}" y="186" width="14" height="30" rx="5" fill="{c}" stroke="#fff" stroke-opacity=".7"/>'
                 for i, c in enumerate(['#e7d9b8', '#efe6cf', '#f6f1e4', '#ffffff']))
ART['laser-whitening'] = ('#0284C7', '#E0F2FE', f'''
{beams}
<circle cx="60" cy="10" r="26" fill="#fff" fill-opacity=".55" filter="url(#soft)"/>
{tooth(205, 112, 1.2)}
<g filter="url(#shadow)">{shades}</g>
{sparkle(265, 70, 1.6)}{sparkle(150, 60, .8, .9)}''')

for slug, (c1, c2, body) in ART.items():
    with open(os.path.join(OUT, slug + '.svg'), 'w') as f:
        f.write(frame(c1, c2, body))
print(sorted(os.listdir(OUT)))
