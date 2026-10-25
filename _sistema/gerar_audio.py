# Gera as falas (edge-tts, voz neural pt-BR) e baixa efeitos sonoros.
# Uso: python _sistema/gerar_audio.py audio/<pasta>
import asyncio, sys, pathlib, urllib.request
import edge_tts
pasta = pathlib.Path(sys.argv[1])
cfg = {}
for l in (pasta / 'voz.txt').read_text().splitlines():
    if '=' in l: k, v = l.split('=', 1); cfg[k.strip()] = v.strip()
VOZ = cfg.get('voz', 'pt-BR-AntonioNeural'); RATE = cfg.get('rate', '+0%'); PITCH = cfg.get('pitch', '+0Hz')
async def main():
    for linha in (pasta / 'falas.txt').read_text().splitlines():
        if '|' not in linha: continue
        fid, texto = linha.split('|', 1)
        out = pasta / f'{fid.strip()}.mp3'
        await edge_tts.Communicate(texto.strip(), VOZ, rate=RATE, pitch=PITCH).save(str(out))
        print('voz', out)
asyncio.run(main())
sfx = pasta.parent / 'sfx'; sfx.mkdir(exist_ok=True)
for linha in (pasta.parent / 'sfx.txt').read_text().splitlines():
    if not linha.strip(): continue
    nome, url = linha.split()
    dest = sfx / nome
    if dest.exists(): continue
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        dest.write_bytes(urllib.request.urlopen(req, timeout=30).read()); print('sfx', nome)
    except Exception as e:
        print('falhou', nome, e)
