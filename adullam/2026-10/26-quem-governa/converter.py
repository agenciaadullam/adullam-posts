# Converte os artboards do canvas (.dc.html) em slides HTML locais para render.
import re, sys, pathlib
src = pathlib.Path(sys.argv[1]); out = pathlib.Path(__file__).parent
files = ['Main','Slide02','Slide03','Slide04','Slide05','Slide06','Slide07']
fotos = {'photo-1695638720523':'trono.jpg','photo-1563165877':'rosto.jpg','photo-1723173330015':'loja.jpg'}
S = '../../../_sistema/'
for i,f in enumerate(files,1):
    h = (src/f'{f}.dc.html').read_text()
    body = re.search(r'</helmet>(.*)</x-dc>', h, re.S).group(1)
    body = body.replace('/_blob/005371112a37b3c893a39dd4d5eecd37', S+'logos/adullam-clara.png')
    body = body.replace('/_blob/a577382890a27a62183c054a1a465b13', S+'logos/adullam-escura.png')
    def rep(m):
        for k,v in fotos.items():
            if k in m.group(0): return 'src="'+S+'unsplash/'+v+'"'
        return m.group(0)
    body = re.sub(r'src="https://images\.unsplash\.com/[^"]+"', rep, body)
    html = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><link rel="stylesheet" href="{S}base.css"><style>body{{margin:0}}</style></head><body>{body}</body></html>'
    (out/f'slide-{i:02d}.html').write_text(html)
    print('ok', i)
