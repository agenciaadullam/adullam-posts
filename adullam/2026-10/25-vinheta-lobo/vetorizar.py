# Uso: python3 vetorizar.py
# Vetoriza _sistema/logos/adullam-escura.png (potracer) e grava logo-vetor.js:
# lobo (corpo e mandíbula separados), as 7 letras de "adullam" e o "AGÊNCIA DE MARKETING".
import json, os
import numpy as np
from PIL import Image, ImageDraw
import potrace

AQUI = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(AQUI, '../../../_sistema/logos/adullam-escura.png')
K = 4  # traça em 4x para curvas lisas; as coordenadas voltam à escala do PNG (801x208)

src = Image.open(LOGO).convert('RGBA')
W, H = src.size
alpha = np.array(src.getchannel('A').resize((W * K, H * K), Image.BICUBIC)) >= 128
yy, xx = np.mgrid[0:H * K, 0:W * K]

# Distintivo: círculo em (103,103), raio 99.5
CX, CY, R = 103.0, 103.0, 99.5
dist = np.hypot(xx / K - CX, yy / K - CY)
lobo = (~alpha) & (dist <= R - 0.8)
# Prolonga o pescoço para baixo do círculo, para não abrir fresta quando a cabeça gira
base = lobo[int((CY + R - 6) * K)]
lobo[int((CY + R - 6) * K):int((CY + R + 60) * K)] |= base

# Mandíbula: tudo do lobo abaixo do corte que passa pelo meio da boca aberta
# (a mandíbula sobrepõe o corpo em ~1 px para não aparecer fio na emenda)
corte = Image.new('L', (W * K, H * K), 0)
poli = [(p[0] * K, p[1] * K) for p in [(137, 96), (195, 85), (195, 128), (128, 128), (128, 108)]]
ImageDraw.Draw(corte).polygon(poli, fill=255, outline=255, width=2 * K)
mandibula = lobo & (np.array(corte) > 0)
corte = Image.new('L', (W * K, H * K), 0)
ImageDraw.Draw(corte).polygon(poli, fill=255)
corpo = lobo & ~(np.array(corte) > 0)

def tracar(mask):
    bm = potrace.Bitmap(~mask)  # o potracer preenche os pixels False
    plist = bm.trace(turdsize=8, alphamax=1.0, opticurve=True, opttolerance=0.2)
    f = lambda p: f'{p.x / K:.2f} {p.y / K:.2f}'
    d = []
    for c in plist:
        d.append('M' + f(c.start_point))
        for s in c.segments:
            if s.is_corner:
                d.append('L' + f(s.c) + 'L' + f(s.end_point))
            else:
                d.append('C' + f(s.c1) + ' ' + f(s.c2) + ' ' + f(s.end_point))
        d.append('Z')
    return ''.join(d)

def faixa(x0, x1, y0, y1):
    m = np.zeros_like(alpha)
    m[y0 * K:y1 * K, x0 * K:x1 * K] = alpha[y0 * K:y1 * K, x0 * K:x1 * K]
    return m

LETRAS = [(234, 320), (328, 414), (423, 500), (509, 529), (539, 559), (566, 652), (663, 796)]
out = {
    'size': [W, H],
    'badge': {'cx': CX, 'cy': CY, 'r': R},
    'jawPivot': [135, 99],
    'neckPivot': [96, 196],
    'body': tracar(corpo),
    'jaw': tracar(mandibula),
    'letters': [{'x0': a, 'x1': b, 'd': tracar(faixa(a - 3, b + 4, 10, 146))} for a, b in LETRAS],
    'tagline': tracar(faixa(295, 735, 160, 196)),
}
with open(os.path.join(AQUI, 'logo-vetor.js'), 'w') as fh:
    fh.write('// Gerado por vetorizar.py a partir de _sistema/logos/adullam-escura.png\n')
    fh.write('const LOGO = ' + json.dumps(out) + ';\n')
print('ok logo-vetor.js', {k: len(v) for k, v in out.items() if isinstance(v, str)})
