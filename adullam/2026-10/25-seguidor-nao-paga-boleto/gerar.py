# Carrossel "Seguidor não paga boleto" — linha visual: EXTRATO
# (papel térmico, código de barras, tipografia monoespaçada de caixa registradora)
import pathlib
OUT = pathlib.Path(__file__).parent
S = '../../../_sistema/'
TOTAL = 8
INK, ROXO, PROF, PRETO, NEVOA, LILAS, BRANCO, VERM = '#121212', '#5423CB', '#26039B', '#121212', '#F3EEFF', '#E2D6FF', '#FFFFFF', '#FF3B5C'
MONO = "font-family:'Space Mono',monospace"
PF = "font-family:'Playfair Display',Georgia,serif;font-style:italic"

def grain(dark):
    blend = 'overlay' if dark else 'multiply'
    op = '0.16' if dark else '0.2'
    return f'<svg aria-hidden="true" width="1080" height="1440" style="position:absolute;inset:0;opacity:{op};mix-blend-mode:{blend};pointer-events:none"><filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter><rect width="1080" height="1440" filter="url(#g)"/></svg>'

def head(n, dark, logo=True):
    c = NEVOA if dark else INK
    lg = f'<img src="{S}logos/adullam-{"escura" if dark else "clara"}.png" style="height:54px;display:block">' if logo else f'<span style="font-size:22px;font-weight:500;color:{c}">@agenciaadullam</span>'
    return f'<div style="position:absolute;top:72px;left:80px;right:80px;display:flex;align-items:center;justify-content:space-between;z-index:5">{lg}<span style="{MONO};font-size:22px;font-weight:700;letter-spacing:.08em;color:{c}">{n:02d}/{TOTAL:02d}</span></div>'

def foot(dark, swipe=True):
    c = NEVOA if dark else INK
    sw = f'<div style="display:flex;align-items:center;gap:14px"><span style="font-size:24px;font-weight:600;letter-spacing:.04em;color:{c}">Arrasta</span><svg width="40" height="40" viewBox="0 0 44 44" fill="none" stroke="{c}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="22" cy="22" r="20"/><path d="M19 14l8 8-8 8"/></svg></div>' if swipe else '<span></span>'
    return f'<div style="position:absolute;left:80px;right:80px;bottom:96px;display:flex;align-items:center;justify-content:space-between;z-index:5">{sw}<span style="font-size:22px;font-weight:500;color:{c}">@agenciaadullam</span></div>'

def barcode(w, h, color, seed=7):
    import random
    r = random.Random(seed); x = 0; bars = []
    while x < w:
        bw = r.choice([2, 2, 3, 4, 6]); gap = r.choice([2, 3, 4])
        if x + bw > w: break
        bars.append(f'<rect x="{x}" y="0" width="{bw}" height="{h}"/>'); x += bw + gap
    return f'<svg width="{w}" height="{h}" fill="{color}" style="display:block">{"".join(bars)}</svg>'

def zig(w, color, flip=False, size=18):
    pts = []
    n = int(w / size)
    for i in range(n + 1):
        pts.append(f'{i*size},{0 if i % 2 == 0 else size}')
    d = ' '.join(pts)
    poly = f'0,{size} {d} {w},{size}' if not flip else f'0,0 {d} {w},0'
    return f'<svg width="{w}" height="{size}" viewBox="0 0 {w} {size}" preserveAspectRatio="none" style="display:block{";transform:scaleY(-1)" if flip else ""}"><polygon points="{poly}" fill="{color}"/></svg>'

def page(bg, inner):
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><link rel="stylesheet" href="{S}base.css"><style>body{{margin:0}}*{{box-sizing:border-box}}</style></head><body><div style="position:relative;width:1080px;height:1440px;overflow:hidden;background:{bg};font-family:Montserrat,sans-serif">{inner}</div></body></html>'

slides = []

# 01 — CAPA clara: boleto
slides.append(page(BRANCO, grain(False) + head(1, False) + f'''
<div style="position:absolute;left:80px;top:196px;{MONO};font-size:22px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:{ROXO}">Métricas que importam ›</div>
<p style="position:absolute;left:72px;right:60px;top:240px;margin:0;font-size:150px;font-weight:800;line-height:.86;letter-spacing:-.06em;text-transform:uppercase;color:{INK}">Seguidor<br>não paga<br><span style="color:{ROXO}">boleto.</span></p>
<div style="position:absolute;left:150px;top:840px;width:820px;background:{NEVOA};border:2px solid {INK};transform:rotate(-3deg);box-shadow:16px 16px 0 {PROF}">
  <div style="display:flex;border-bottom:2px solid {INK}">
    <div style="padding:18px 24px;border-right:2px solid {INK};{MONO};font-size:22px;font-weight:700">ADULLAM | 001-9</div>
    <div style="padding:18px 24px;{MONO};font-size:20px;color:rgba(18,18,18,.65);flex:1;text-align:right">Vencimento: todo mês</div>
  </div>
  <div style="display:flex;border-bottom:2px solid {INK}">
    <div style="flex:1;padding:16px 24px;border-right:2px solid {INK}"><div style="{MONO};font-size:16px;color:rgba(18,18,18,.6)">PAGADOR</div><div style="font-size:30px;font-weight:800;margin-top:4px">Seus seguidores</div></div>
    <div style="width:250px;padding:16px 24px"><div style="{MONO};font-size:16px;color:rgba(18,18,18,.6)">VALOR PAGO</div><div style="{MONO};font-size:34px;font-weight:700;margin-top:2px">R$ 0,00</div></div>
  </div>
  <div style="padding:22px 24px 20px">{barcode(770, 74, INK)}</div>
  <div style="position:absolute;right:-46px;top:-92px;transform:rotate(-10deg);background:{BRANCO};border:5px solid {VERM};color:{VERM};{MONO};font-weight:700;font-size:40px;letter-spacing:.1em;padding:6px 20px;border-radius:10px;opacity:.92">NÃO PAGO</div>
</div>
''' + foot(False)))

# 02 — preto + foto celular
slides.append(page(PRETO, f'''
<div style="position:absolute;right:0;top:0;width:560px;height:1440px;overflow:hidden">
  <img src="{S}unsplash/celular.jpg" style="width:560px;height:1440px;object-fit:cover;object-position:50% 50%;filter:grayscale(1) contrast(1.25) brightness(1.35);display:block">
  <div style="position:absolute;inset:0;background:linear-gradient(90deg,{PRETO} 0%,rgba(18,18,18,.4) 40%,rgba(18,18,18,0) 70%)"></div>
  <div style="position:absolute;inset:0;background:rgba(84,35,203,.35);mix-blend-mode:multiply"></div>
</div>''' + grain(True) + head(2, True) + f'''
<div style="position:absolute;left:80px;top:250px;width:640px">
  <div style="{MONO};font-size:22px;font-weight:700;letter-spacing:.12em;color:{LILAS}">&gt; SALDO DO PERFIL</div>
  <p style="margin:34px 0 0;font-size:84px;font-weight:800;line-height:.98;letter-spacing:-.045em;color:{NEVOA}">Tem perfil com muito seguidor e caixa vazio.</p>
  <p style="margin:40px 0 0;{PF};font-size:58px;line-height:1.1;color:{LILAS}">E perfil pequeno com a agenda cheia.</p>
  <div style="margin-top:70px;display:inline-block;background:{NEVOA};color:{INK};{MONO};font-size:28px;font-weight:700;padding:14px 22px">A diferença está no que você mede.</div>
</div>''' + foot(True)))

# 03 — roxo: vaidade x caixa (duas colunas de cupom)
def cupom(titulo, itens, risca, w, rot, bg, ink):
    lis = ''.join(
        f'<div style="display:flex;justify-content:space-between;align-items:baseline;gap:10px;padding:14px 0;border-bottom:2px dashed {ink}33"><span style="font-size:30px;font-weight:{500 if risca else 700};{"text-decoration:line-through;text-decoration-color:"+VERM+";text-decoration-thickness:4px;color:"+ink+"99" if risca else ""}">{t}</span><span style="{MONO};font-size:22px;color:{ink}99">{"—" if risca else "✓"}</span></div>' for t in itens)
    return f'''<div style="width:{w}px;transform:rotate({rot}deg);filter:drop-shadow(0 22px 30px rgba(0,0,0,.35))">{zig(w, bg)}<div style="background:{bg};color:{ink};padding:26px 34px 30px"><div style="{MONO};font-size:20px;font-weight:700;letter-spacing:.14em;text-align:center">{titulo}</div><div style="height:2px;background:{ink};margin:18px 0 6px"></div>{lis}</div>{zig(w, bg, flip=True)}</div>'''
slides.append(page(ROXO, grain(True) + head(3, True) + f'''
<p style="position:absolute;left:80px;right:80px;top:200px;margin:0;font-size:76px;font-weight:800;line-height:.98;letter-spacing:-.045em;color:{NEVOA}">Número bonito<br><span style="{PF};font-weight:400;letter-spacing:-.01em">não é número que vende.</span></p>
<div style="position:absolute;left:60px;top:520px">{cupom("MÉTRICA DE VAIDADE", ["Seguidores", "Curtidas", "Visualização solta"], True, 440, -4, NEVOA, INK)}</div>
<div style="position:absolute;right:56px;top:560px">{cupom("MÉTRICA DE CAIXA", ["Não seguidores", "Salvar + enviar", "Toque no WhatsApp", "Conversa que vende"], False, 470, 3, BRANCO, INK)}</div>
''' + foot(True)))

# 04 — lilás: alcance de não seguidores (diagrama de círculos)
slides.append(page(LILAS, grain(False) + head(4, False) + f'''
<div style="position:absolute;left:80px;top:190px;{MONO};font-size:200px;font-weight:700;line-height:1;color:{ROXO};letter-spacing:-.06em">01</div>
<p style="position:absolute;left:80px;right:80px;top:410px;margin:0;font-size:72px;font-weight:800;line-height:.98;letter-spacing:-.04em;color:{INK}">Alcance de<br>não seguidores</p>
<div style="position:absolute;left:560px;top:640px;width:420px;height:420px">
  <div style="position:absolute;inset:0;border-radius:50%;border:3px dashed {ROXO}"></div>
  <div style="position:absolute;inset:40px;border-radius:50%;background:{ROXO}22"></div>
  <div style="position:absolute;left:150px;top:150px;width:120px;height:120px;border-radius:50%;background:{INK};display:flex;align-items:center;justify-content:center;{MONO};font-size:15px;font-weight:700;color:{NEVOA};text-align:center;line-height:1.2">QUEM JÁ<br>TE SEGUE</div>
  <div style="position:absolute;right:-10px;top:30px;background:{VERM};color:#fff;{MONO};font-size:18px;font-weight:700;padding:8px 14px;transform:rotate(6deg)">GENTE NOVA</div>
</div>
<div style="position:absolute;left:80px;top:680px;width:440px">
  <p style="margin:0;font-size:34px;font-weight:500;line-height:1.38;color:{INK}">Mostra se <b style="font-weight:800">gente nova</b> está descobrindo o seu negócio.</p>
  <p style="margin:34px 0 0;{PF};font-size:42px;line-height:1.18;color:{PROF}">Se só seguidor vê, você fala sempre com as mesmas pessoas.</p>
</div>
''' + foot(False)))

# 05 — branco: salvar e compartilhar (3 fichas)
def ficha(icon, nome, sig, destaque, rot):
    bg = PROF if destaque else BRANCO; c = NEVOA if destaque else INK
    op = '1' if destaque else '.55'
    return f'<div style="width:270px;height:360px;background:{bg};border:2px solid {INK};transform:rotate({rot}deg);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:22px;opacity:{op}"><svg width="86" height="86" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{icon}</svg><div style="font-size:30px;font-weight:800;color:{c}">{nome}</div><div style="{MONO};font-size:20px;font-weight:700;letter-spacing:.06em;color:{c};text-transform:uppercase">= {sig}</div></div>'
heart = '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1 1.1L12 21l7.8-7.6 1-1.1a5.5 5.5 0 0 0 0-7.7z"/>'
mark = '<path d="M6 3h12v18l-6-4-6 4z"/>'
send = '<path d="M22 2L11 13"/><path d="M22 2l-7 20-4-9-9-4z"/>'
slides.append(page(BRANCO, grain(False) + head(5, False) + f'''
<div style="position:absolute;left:80px;top:200px;display:flex;align-items:baseline;gap:26px"><span style="{MONO};font-size:44px;font-weight:700;color:{ROXO}">02</span><span style="font-size:68px;font-weight:800;letter-spacing:-.04em;color:{INK};line-height:1">Salvar e enviar</span></div>
<div style="position:absolute;left:80px;right:80px;top:330px;height:2px;background:{INK}"></div>
<div style="position:absolute;left:60px;right:60px;top:430px;display:flex;justify-content:center;gap:30px">
  {ficha(heart, "Curtir", "aplauso", False, -3)}
  {ficha(mark, "Salvar", "vou voltar", True, 0)}
  {ficha(send, "Enviar", "indicação", True, 3)}
</div>
<p style="position:absolute;left:80px;right:80px;top:900px;margin:0;font-size:40px;font-weight:500;line-height:1.35;color:{INK}">Curtida é educação. Quem <b style="font-weight:800;background:{LILAS};padding:0 8px">salva</b> quer voltar. Quem <b style="font-weight:800;background:{LILAS};padding:0 8px">envia</b> está te indicando de graça.</p>
<p style="position:absolute;left:80px;right:80px;top:1110px;margin:0;{PF};font-size:42px;color:{ROXO}">Conteúdo que é salvo vira cliente depois.</p>
''' + foot(False)))

# 06 — roxo profundo: toque no WhatsApp (botão gigante)
slides.append(page(PROF, grain(True) + head(6, True) + f'''
<div style="position:absolute;left:80px;top:200px;{MONO};font-size:24px;font-weight:700;letter-spacing:.1em;color:{LILAS}">03 / TOQUES NO BOTÃO E NO LINK</div>
<p style="position:absolute;left:80px;right:80px;top:260px;margin:0;font-size:96px;font-weight:800;line-height:.95;letter-spacing:-.05em;color:{NEVOA}">É o cliente<br>levantando<br>a mão.</p>
<div style="position:absolute;left:140px;top:720px;width:800px;height:150px;border-radius:24px;background:{NEVOA};display:flex;align-items:center;justify-content:center;gap:22px;box-shadow:0 14px 0 {INK}">
  <svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="{PROF}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 21l2.1-5.4A8.4 8.4 0 1 1 21 11.5z"/></svg>
  <span style="font-size:48px;font-weight:800;color:{PROF}">Enviar mensagem</span>
</div>
<svg width="200" height="200" viewBox="0 0 200 200" style="position:absolute;left:800px;top:810px" fill="none">
  <circle cx="70" cy="60" r="34" stroke="{VERM}" stroke-width="5"/><circle cx="70" cy="60" r="58" stroke="{VERM}" stroke-width="3" opacity=".55"/>
  <path d="M70 60l58 112 14-44 44-12z" fill="{INK}" stroke="{NEVOA}" stroke-width="5" stroke-linejoin="round"/>
</svg>
<p style="position:absolute;left:80px;right:80px;top:1040px;margin:0;font-size:36px;font-weight:500;line-height:1.38;color:{NEVOA}">Toque no WhatsApp, no link da bio, no “como chegar”. <b style="font-weight:800">Isso é intenção de compra.</b></p>
''' + foot(True)))

# 07 — foto balcão: conversa que vira venda
tally = ''.join(f'<span style="display:inline-block;width:6px;height:64px;background:{INK};margin-right:12px;transform:rotate({(-1)**i*3}deg)"></span>' for i in range(4)) + f'<span style="display:inline-block;width:6px;height:90px;background:{VERM};transform:rotate(62deg);margin-left:-70px"></span>'
slides.append(page(PRETO, f'''
<div style="position:absolute;left:0;top:0;width:1080px;height:760px;overflow:hidden">
  <img src="{S}unsplash/balcao.jpg" style="width:1080px;height:760px;object-fit:cover;object-position:50% 40%;filter:grayscale(1) contrast(1.15);display:block">
  <div style="position:absolute;inset:0;background:rgba(84,35,203,.45);mix-blend-mode:multiply"></div>
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(18,18,18,.55) 0%,rgba(18,18,18,0) 30%,rgba(18,18,18,0) 70%,{PRETO} 100%)"></div>
</div>''' + grain(True) + head(7, True) + f'''
<div style="position:absolute;left:80px;top:690px;{MONO};font-size:24px;font-weight:700;letter-spacing:.1em;color:{LILAS}">04 / A MAIS IMPORTANTE</div>
<p style="position:absolute;left:80px;right:80px;top:740px;margin:0;font-size:88px;font-weight:800;line-height:.95;letter-spacing:-.05em;color:{NEVOA}">Conversa que<br>vira venda.</p>
<div style="position:absolute;left:80px;top:990px;width:470px"><p style="margin:0;font-size:32px;font-weight:500;line-height:1.4;color:{NEVOA}">Nenhum aplicativo conta essa por você. <b style="font-weight:800">Anote no caderno</b> quantas conversas do direct viraram cliente.</p></div>
<div style="position:absolute;right:80px;top:960px;width:380px;transform:rotate(3deg)">{zig(380, NEVOA)}<div style="background:{NEVOA};padding:20px 28px 26px;color:{INK}"><div style="{MONO};font-size:18px;font-weight:700;letter-spacing:.1em">VENDAS PELO DIRECT</div><div style="margin-top:22px;height:96px;display:flex;align-items:center;padding-left:8px">{tally}</div></div>{zig(380, NEVOA, flip=True)}</div>
''' + foot(True)))

# 08 — CTA: extrato do mês (cupom longo)
linhas = [("01", "Alcance de não seguidores"), ("02", "Salvamentos + envios"), ("03", "Toques no WhatsApp e link"), ("04", "Conversas que viraram venda")]
ls = ''.join(f'<div style="display:flex;align-items:flex-end;gap:14px;padding:16px 0"><span style="{MONO};font-size:24px;font-weight:700;color:{ROXO}">{a}</span><span style="font-size:30px;font-weight:700;white-space:nowrap">{b}</span><span style="flex:1;border-bottom:3px dotted {INK}66;margin-bottom:8px"></span><span style="{MONO};font-size:24px;color:{INK}88">____</span></div>' for a, b in linhas)
slides.append(page(NEVOA, grain(False) + head(8, False, logo=False) + f'''
<div style="position:absolute;left:150px;top:170px;width:780px;filter:drop-shadow(0 26px 34px rgba(38,3,155,.22))">
  {zig(780, BRANCO)}
  <div style="background:{BRANCO};padding:34px 50px 40px;color:{INK}">
    <div style="text-align:center;{MONO};font-size:22px;font-weight:700;letter-spacing:.18em">*** EXTRATO DO SEU INSTAGRAM ***</div>
    <div style="text-align:center;{MONO};font-size:18px;color:{INK}99;margin-top:8px">Painel profissional › Insights › 30 dias</div>
    <div style="height:2px;background:{INK};margin:26px 0 10px"></div>
    {ls}
    <div style="height:2px;background:{INK};margin:14px 0 22px"></div>
    <div style="display:flex;justify-content:space-between;{MONO};font-size:22px;font-weight:700"><span>SEGUIDORES</span><span style="text-decoration:line-through;text-decoration-color:{VERM};text-decoration-thickness:3px">NÃO ENTRA NA CONTA</span></div>
    <div style="margin-top:30px;display:flex;justify-content:center">{barcode(560, 60, INK, seed=3)}</div>
  </div>
  {zig(780, BRANCO, flip=True)}
</div>
<p style="position:absolute;left:80px;right:80px;top:1010px;margin:0;text-align:center;font-size:120px;font-weight:800;line-height:.9;letter-spacing:-.06em;color:{ROXO}">SALVA.</p>
<p style="position:absolute;left:80px;right:80px;top:1135px;margin:0;text-align:center;{PF};font-size:44px;color:{INK}">e confere os seus números todo mês.</p>
<div style="position:absolute;left:0;right:0;bottom:90px;display:flex;justify-content:center"><img src="{S}logos/adullam-clara.png" style="width:260px;display:block"></div>
'''))

for i, h in enumerate(slides, 1):
    (OUT / f'slide-{i:02d}.html').write_text(h)
print('ok', len(slides))
