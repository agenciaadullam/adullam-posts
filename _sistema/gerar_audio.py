# Gera as falas (edge-tts, voz neural pt-BR) com tempo de cada palavra, e baixa efeitos sonoros.
# Uso: python _sistema/gerar_audio.py audio/<pasta>
import asyncio, sys, json, pathlib, urllib.request
import edge_tts
pasta = pathlib.Path(sys.argv[1])
cfg = {}
for l in (pasta / 'voz.txt').read_text().splitlines():
    if '=' in l: k, v = l.split('=', 1); cfg[k.strip()] = v.strip()
VOZ = cfg.get('voz', 'pt-BR-AntonioNeural'); RATE = cfg.get('rate', '+0%'); PITCH = cfg.get('pitch', '+0Hz')
async def uma(fid, texto):
    com = edge_tts.Communicate(texto, VOZ, rate=RATE, pitch=PITCH, boundary='WordBoundary')
    audio = bytearray(); palavras = []
    async for ch in com.stream():
        if ch['type'] == 'audio': audio.extend(ch['data'])
        elif ch['type'] == 'WordBoundary':
            palavras.append({'w': ch['text'], 's': ch['offset'] / 1e7, 'd': ch['duration'] / 1e7})
    (pasta / f'{fid}.mp3').write_bytes(bytes(audio))
    (pasta / f'{fid}.json').write_text(json.dumps(palavras, ensure_ascii=False))
    print('voz', fid, len(palavras))
async def main():
    for linha in (pasta / 'falas.txt').read_text().splitlines():
        if '|' not in linha: continue
        fid, texto = linha.split('|', 1)
        await uma(fid.strip(), texto.strip())
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
