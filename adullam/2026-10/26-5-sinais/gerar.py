# Gera os slides HTML do carrossel "5 sinais de que sua empresa posta por postar".
import os
HERE = os.path.dirname(os.path.abspath(__file__))
SYS = "../../../_sistema"
TOTAL = 8
LILAS, ROXO, ROXO2, PRETO, VERM, MARCA = "#F3EEFF", "#26039B", "#5423CB", "#121212", "#FF3B5C", "#E2D6FF"

def grain(n, dark):
    if dark:
        return f'<svg class="grain" width="1080" height="1440" style="opacity:.14;mix-blend-mode:overlay"><filter id="g{n}"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch"/></filter><rect width="1080" height="1440" filter="url(#g{n})"/></svg>'
    return f'<svg class="grain" width="1080" height="1440" style="opacity:.2;mix-blend-mode:multiply"><filter id="g{n}"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter><rect width="1080" height="1440" filter="url(#g{n})"/></svg>'

def head(n, dark):
    logo = "adullam-escura.png" if dark else "adullam-clara.png"
    c = LILAS if dark else PRETO
    return f'<div class="head"><img src="{SYS}/logos/{logo}" alt="Adullam"><span class="count" style="color:{c}">{n:02d}/{TOTAL:02d}</span></div>'

def foot(dark):
    c = LILAS if dark else PRETO
    return (f'<div class="foot"><div class="swipe" style="color:{c}">Arrasta<svg width="40" height="40" viewBox="0 0 44 44" fill="none" stroke="{c}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="22" cy="22" r="20"/><path d="M19 14l8 8-8 8"/></svg></div>'
            f'<span class="handle" style="color:{c}">@agenciaadullam</span></div>')

def page(n, bg, dark, body, extra_bg=""):
    color = LILAS if dark else PRETO
    return f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><link rel="stylesheet" href="{SYS}/base.css"></head>
<body><div class="slide" style="background:{bg};color:{color}">{extra_bg}{grain(n, dark)}{head(n, dark)}{body}{foot(dark) if n < TOTAL else ""}</div></body></html>'''

slides = {}

# 01 Hook: escuro, degradê roxo, faixas
slides[1] = page(1, PRETO, True, extra_bg='<div aria-hidden="true" class="pf" style="position:absolute;right:-60px;top:120px;font-style:italic;font-weight:800;font-size:760px;line-height:1;color:rgba(84,35,203,.35)">5</div><div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(18,18,18,0) 0%,rgba(38,3,155,.55) 60%,rgba(18,18,18,.92) 100%)"></div>', body=f'''
<div style="position:absolute;left:80px;right:80px;bottom:236px;display:flex;flex-direction:column;align-items:flex-start">
  <span class="tag" style="margin-bottom:32px">Teste rápido</span>
  <span style="display:inline-block;background:{ROXO2};padding:6px 20px 10px;font-size:78px;font-weight:800;line-height:1;letter-spacing:-.025em">Sua empresa posta</span>
  <span style="display:inline-block;background:{ROXO2};padding:6px 20px 12px;margin-top:6px;font-size:78px;font-weight:800;line-height:1;letter-spacing:-.025em">todo dia e não vende?</span>
  <p class="pf" style="margin:40px 0 0;font-size:84px;font-weight:400;line-height:1.06;letter-spacing:-.015em">Talvez esteja postando<br><span style="font-style:italic;font-weight:700;text-decoration:underline;text-decoration-color:{VERM};text-decoration-thickness:6px;text-underline-offset:16px">por postar</span>.</p>
</div>''')

# 02 Explicação: lilás, aparte em Playfair, palavra circulada
slides[2] = page(2, LILAS, False, f'''
<div aria-hidden="true" class="pf" style="position:absolute;right:-20px;bottom:-190px;font-style:italic;font-weight:800;font-size:700px;line-height:1;color:rgba(84,35,203,.07)">5</div>
<div style="position:absolute;left:80px;right:120px;top:300px;display:flex;flex-direction:column;align-items:flex-start">
  <span class="tag" style="color:{ROXO2}">Vamos falar a real</span>
  <p style="margin:48px 0 0;font-size:66px;font-weight:800;line-height:1.12;letter-spacing:-.025em;text-wrap:balance">Postar todo dia <span class="pf" style="font-style:italic;font-weight:400;letter-spacing:-.01em;color:{ROXO2}">(sem saber pra quê)</span> não faz ninguém comprar.</p>
  <div style="width:120px;height:4px;background:{ROXO};margin-top:64px"></div>
  <p class="pf" style="margin:56px 0 0;font-size:60px;font-weight:400;line-height:1.2;letter-spacing:-.01em;text-wrap:balance">Conta quantos destes 5 sinais você <span style="position:relative;display:inline-block;font-style:italic;font-weight:700;color:{ROXO}">reconhece<svg width="340" height="104" viewBox="0 0 420 120" preserveAspectRatio="none" fill="none" style="position:absolute;left:-26px;top:-12px"><path d="M215 9C110 4 12 22 9 60c-3 38 110 52 215 48 104-4 186-26 183-56-3-30-90-46-196-42" stroke="{VERM}" stroke-width="4" stroke-linecap="round"/></svg></span>.</p>
</div>''')

# 03 Sinal 1: caixa vazada à esquerda, escuro
slides[3] = page(3, ROXO, True, extra_bg='<div style="position:absolute;inset:0;background:radial-gradient(circle at 80% 15%,rgba(84,35,203,.9),rgba(18,18,18,.95) 70%)"></div>', body=f'''
<div style="position:absolute;left:-48px;top:380px;width:980px;box-sizing:border-box;padding:76px 80px 80px 128px;border:2px solid rgba(243,238,255,.85);border-radius:44px;display:flex;flex-direction:column;align-items:flex-start">
  <span class="tag">Sinal nº 1</span>
  <p style="margin:36px 0 0;font-size:84px;font-weight:800;line-height:1;letter-spacing:-.025em">Não sabe o</p>
  <p class="pf" style="margin:4px 0 0;font-style:italic;font-weight:700;font-size:100px;line-height:1.05;letter-spacing:-.015em">objetivo.</p>
  <p style="margin:40px 0 0;font-size:38px;font-weight:500;line-height:1.4;text-wrap:pretty">Todo post precisa de uma missão: vender, atrair ou gerar confiança. Sem isso, o resultado <span style="font-weight:800;background:{ROXO2};padding:0 10px">é sorte</span>.</p>
</div>''')

# 04 Sinal 2: centralizado branco, palavra gigante com marca-texto
slides[4] = page(4, "#FFFFFF", False, f'''
<div style="position:absolute;left:80px;right:80px;top:270px;display:flex;flex-direction:column;align-items:center;text-align:center">
  <div style="width:3px;height:190px;background:{ROXO2}"></div>
  <span class="tag" style="margin-top:56px;color:{ROXO2}">Sinal nº 2</span>
  <p style="margin:28px 0 0;font-size:64px;font-weight:800;line-height:1;letter-spacing:-.025em">Copia toda</p>
  <p class="pf" style="margin:8px 0 0;font-style:italic;font-weight:700;font-size:190px;line-height:1;letter-spacing:-.02em;color:{ROXO}"><span style="background:linear-gradient(180deg,transparent 64%,{MARCA} 64%,{MARCA} 90%,transparent 90%);padding:0 16px">trend.</span></p>
  <p style="margin:56px 0 0;max-width:820px;font-size:40px;font-weight:500;line-height:1.4;text-wrap:balance">Se a dancinha não tem nada a ver com o seu negócio, ela não traz cliente.</p>
</div>''')

# 05 Sinal 3: caixa à direita, roxo
slides[5] = page(5, ROXO, True, f'''
<div aria-hidden="true" class="pf" style="position:absolute;left:-40px;top:150px;font-style:italic;font-weight:800;font-size:520px;line-height:1;color:rgba(243,238,255,.06)">♡</div>
<div style="position:absolute;left:148px;right:-48px;bottom:280px;box-sizing:border-box;padding:76px 128px 80px 76px;border-radius:44px;background:rgba(18,18,18,.28);border:2px solid rgba(243,238,255,.7);display:flex;flex-direction:column;align-items:flex-start">
  <span class="tag">Sinal nº 3</span>
  <p style="margin:36px 0 0;font-size:80px;font-weight:800;line-height:1.02;letter-spacing:-.025em">Só a <span class="pf" style="font-style:italic;font-weight:700;font-size:96px;letter-spacing:-.015em">família</span> curte.</p>
  <p style="margin:28px 0 0;font-size:38px;font-weight:500;line-height:1.4">E ninguém pergunta o preço.</p>
  <p class="pf" style="margin:36px 0 0;padding-top:32px;border-top:1px solid rgba(243,238,255,.4);font-style:italic;font-weight:400;font-size:44px;line-height:1.25;text-wrap:balance">(o post fala com todo mundo, ou seja, com ninguém)</p>
</div>''')

# 06 Sinal 4: elemento digital (seleção de texto), lilás
slides[6] = page(6, LILAS, False, f'''
<div style="position:absolute;left:80px;right:80px;top:280px;display:flex;flex-direction:column;align-items:flex-start">
  <span class="tag" style="color:{ROXO2}">Sinal nº 4</span>
  <p style="margin:36px 0 0;max-width:900px;font-size:72px;font-weight:800;line-height:1.08;letter-spacing:-.025em;text-wrap:balance">O post termina e não pede nada.</p>
  <div style="width:3px;height:110px;background:{PRETO};margin:44px 0 0 4px"></div>
  <p style="margin:40px 0 0;font-size:52px;font-weight:500;line-height:1.1">Faltou um simples</p>
  <div style="position:relative;margin-top:150px">
    <div style="position:absolute;left:0;top:-108px;display:flex;align-items:center;background:{PRETO};border-radius:14px;padding:0 8px;box-shadow:0 10px 30px rgba(18,18,18,.22)">
      <span style="padding:16px 20px;font-size:22px;font-weight:500;color:{LILAS}">Copiar</span><span style="width:1px;height:28px;background:rgba(243,238,255,.35)"></span>
      <span style="padding:16px 20px;font-size:22px;font-weight:500;color:{LILAS}">Colar</span><span style="width:1px;height:28px;background:rgba(243,238,255,.35)"></span>
      <span style="padding:16px 20px;font-size:22px;font-weight:500;color:{LILAS}">Compartilhar</span>
    </div>
    <p class="pf" style="margin:0;font-style:italic;font-weight:700;font-size:96px;line-height:1.12;letter-spacing:-.015em;color:{ROXO};background:rgba(84,35,203,.18);padding:0 12px;white-space:nowrap">chama no direct.</p>
    <div style="position:absolute;left:-3px;top:-6px;width:4px;height:122px;background:{ROXO2}"></div>
    <div style="position:absolute;left:-11px;top:-22px;width:20px;height:20px;border-radius:50%;background:{ROXO2}"></div>
    <div style="position:absolute;right:-3px;bottom:-6px;width:4px;height:122px;background:{ROXO2}"></div>
    <div style="position:absolute;right:-11px;bottom:-22px;width:20px;height:20px;border-radius:50%;background:{ROXO2}"></div>
  </div>
</div>''')

# 07 Sinal 5: preto, "notificação" de métricas
slides[7] = page(7, PRETO, True, f'''
<div aria-hidden="true" class="pf" style="position:absolute;right:-40px;bottom:-120px;font-style:italic;font-weight:800;font-size:640px;line-height:1;color:rgba(84,35,203,.16)">%</div>
<div style="position:absolute;left:80px;right:80px;top:300px;display:flex;flex-direction:column;align-items:flex-start">
  <span class="tag">Sinal nº 5</span>
  <p style="margin:36px 0 0;font-size:84px;font-weight:800;line-height:1;letter-spacing:-.025em">Nunca olha os</p>
  <p class="pf" style="margin:4px 0 0;font-style:italic;font-weight:700;font-size:110px;line-height:1.05;letter-spacing:-.015em;text-decoration:underline;text-decoration-color:{VERM};text-decoration-thickness:6px;text-underline-offset:18px">números.</p>
  <div style="margin-top:64px;width:760px;box-sizing:border-box;background:rgba(243,238,255,.08);border:1px solid rgba(243,238,255,.25);border-radius:28px;padding:32px 36px">
    <div style="display:flex;justify-content:space-between;font-size:22px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:rgba(243,238,255,.7)"><span>Insights da semana</span><span>?</span></div>
    <div style="display:flex;gap:40px;margin-top:22px;font-size:30px;font-weight:600">
      <span>Alcance <b class="pf" style="font-style:italic;font-weight:700;font-size:44px">??</b></span>
      <span>Salvos <b class="pf" style="font-style:italic;font-weight:700;font-size:44px">??</b></span>
      <span>Mensagens <b class="pf" style="font-style:italic;font-weight:700;font-size:44px">??</b></span>
    </div>
  </div>
  <p style="margin:48px 0 0;max-width:860px;font-size:38px;font-weight:500;line-height:1.4;text-wrap:pretty">Postou e esqueceu? Sem olhar o resultado, você repete o que não funciona.</p>
</div>''')

# 08 CTA: roxo, cartão lilás, logo grande
slides[8] = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><link rel="stylesheet" href="{SYS}/base.css"></head>
<body><div class="slide" style="background:{ROXO};color:{LILAS}">
<div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 0%,rgba(84,35,203,.85),rgba(38,3,155,1) 60%)"></div>
{grain(8, True)}
<div class="head"><span class="handle" style="color:{LILAS}">@agenciaadullam</span><span class="count" style="color:{LILAS}">08/08</span></div>
<div style="position:absolute;left:80px;right:80px;top:210px;display:flex;flex-direction:column;align-items:center;text-align:center">
  <p class="pf" style="margin:0;font-style:italic;font-weight:400;font-size:72px;line-height:1;letter-spacing:-.01em">Marcou 2 ou mais?</p>
  <p style="margin:32px 0 0;max-width:880px;font-size:76px;font-weight:800;line-height:1.06;letter-spacing:-.025em;text-wrap:balance">Sua empresa está no improviso.</p>
  <div style="margin-top:64px;width:100%;box-sizing:border-box;background:{LILAS};border-radius:24px;padding:56px 64px;display:flex;flex-direction:column;align-items:center">
    <p style="margin:0;font-size:42px;font-weight:600;line-height:1.3;color:{PRETO}">Comenta <span style="display:inline-block;background:{ROXO2};color:{LILAS};font-weight:800;letter-spacing:.08em;border-radius:12px;padding:2px 20px 6px">PLANO</span> aqui embaixo</p>
    <p class="pf" style="margin:20px 0 0;max-width:760px;font-style:italic;font-weight:400;font-size:40px;line-height:1.3;color:{ROXO};text-wrap:balance">que eu te mando o checklist grátis <b>7 dias pra sair do improviso</b>.</p>
  </div>
  <div style="margin-top:48px;display:flex;gap:56px;justify-content:center">
    <div style="display:flex;align-items:center;gap:14px"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="{LILAS}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h12v18l-6-4-6 4z"/></svg><span style="font-size:26px;font-weight:600">Salva pra não esquecer</span></div>
    <div style="display:flex;align-items:center;gap:14px"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="{LILAS}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 2L11 13"/><path d="M22 2l-7 20-4-9-9-4z"/></svg><span style="font-size:26px;font-weight:600">Manda pra quem precisa ler</span></div>
  </div>
</div>
<div style="position:absolute;left:0;right:0;bottom:96px;display:flex;justify-content:center"><img src="{SYS}/logos/adullam-escura.png" alt="Adullam" style="width:380px;height:auto;display:block"></div>
</div></body></html>'''

for n, html in slides.items():
    with open(os.path.join(HERE, f"slide-{n:02d}.html"), "w", encoding="utf-8") as f:
        f.write(html)
print("slides:", len(slides))
