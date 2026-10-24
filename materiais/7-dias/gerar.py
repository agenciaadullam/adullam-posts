# Gera o PDF "7 dias para sair do improviso" (lead magnet da Adullam).
import os
HERE = os.path.dirname(os.path.abspath(__file__))
SYS = "../../_sistema"
LILAS, ROXO, ROXO2, PRETO, VERM, MARCA = "#F3EEFF", "#26039B", "#5423CB", "#121212", "#FF3B5C", "#E2D6FF"

def grain(n, dark):
    if dark:
        return f'<svg class="grain" width="1080" height="1440" style="opacity:.14;mix-blend-mode:overlay"><filter id="g{n}"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch"/></filter><rect width="1080" height="1440" filter="url(#g{n})"/></svg>'
    return f'<svg class="grain" width="1080" height="1440" style="opacity:.2;mix-blend-mode:multiply"><filter id="g{n}"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter><rect width="1080" height="1440" filter="url(#g{n})"/></svg>'

def head(dark, label):
    logo = "adullam-escura.png" if dark else "adullam-clara.png"
    c = LILAS if dark else PRETO
    return f'<div class="head"><img src="{SYS}/logos/{logo}" alt="Adullam"><span class="count" style="color:{c}">{label}</span></div>'

def foot(dark, n):
    c = LILAS if dark else PRETO
    return f'<div class="foot"><span class="handle" style="color:{c}">7 dias para sair do improviso</span><span class="handle" style="color:{c}">@agenciaadullam · {n:02d}</span></div>'

def checklist(items, dark=False):
    box = "rgba(243,238,255,.9)" if dark else ROXO2
    rows = "".join(
        f'<li style="display:flex;gap:26px;align-items:flex-start;padding:22px 0;border-bottom:1px solid {"rgba(243,238,255,.25)" if dark else "rgba(18,18,18,.12)"}">'
        f'<span style="flex:none;width:34px;height:34px;margin-top:4px;border:3px solid {box};border-radius:8px"></span>'
        f'<span style="font-size:34px;font-weight:500;line-height:1.38">{t}</span></li>' for t in items)
    return f'<ul style="list-style:none;margin:40px 0 0;padding:0">{rows}</ul>'

pages = []

# Capa
pages.append(f'''<div class="slide" style="background:{ROXO};color:{LILAS}">
<div style="position:absolute;inset:0;background:radial-gradient(circle at 85% 10%,rgba(84,35,203,.95),rgba(38,3,155,1) 55%,rgba(18,18,18,.95) 100%)"></div>
<div aria-hidden="true" class="pf" style="position:absolute;right:-70px;top:90px;font-style:italic;font-weight:800;font-size:820px;line-height:1;color:rgba(243,238,255,.08)">7</div>
{grain(0, True)}{head(True, "CHECKLIST GRÁTIS")}
<div style="position:absolute;left:80px;right:80px;bottom:300px">
  <span class="tag">Guia prático para o seu Instagram</span>
  <p style="margin:36px 0 0;font-size:96px;font-weight:800;line-height:1;letter-spacing:-.03em">7 dias para</p>
  <p class="pf" style="margin:10px 0 0;font-style:italic;font-weight:700;font-size:150px;line-height:1;letter-spacing:-.02em;text-decoration:underline;text-decoration-color:{VERM};text-decoration-thickness:8px;text-underline-offset:22px">sair do improviso.</p>
  <p style="margin:64px 0 0;max-width:820px;font-size:38px;font-weight:500;line-height:1.4">Uma tarefa por dia, de 20 a 30 minutos, para o seu perfil parar de postar por postar e começar a trazer cliente.</p>
</div>
<div class="foot"><span class="handle" style="color:{LILAS}">Agência Adullam · Ulianópolis/PA</span><span class="handle" style="color:{LILAS}">@agenciaadullam</span></div>
</div>''')

# Como usar
pages.append(f'''<div class="slide" style="background:{LILAS};color:{PRETO}">{grain(1, False)}{head(False, "ANTES DE COMEÇAR")}

<div style="position:absolute;left:80px;right:110px;top:260px">
  <span class="tag" style="color:{ROXO2}">Como usar este guia</span>
  <p style="margin:40px 0 0;font-size:68px;font-weight:800;line-height:1.1;letter-spacing:-.025em;text-wrap:balance">Não precisa fazer tudo hoje. <span class="pf" style="font-style:italic;font-weight:400;color:{ROXO2}">(é só um dia de cada vez)</span></p>
  <div style="width:120px;height:4px;background:{ROXO};margin-top:56px"></div>
  {checklist(["Separe 20 a 30 minutos por dia, de preferência no mesmo horário.",
              "Faça a tarefa do dia e marque o quadradinho.",
              "Anote o que descobrir: isso vira o seu plano.",
              "No dia 7, compare o antes e o depois do seu perfil."])}
</div>{foot(False, 2)}</div>''')

days = [
  (True, PRETO, "Dia 1", "Defina pra que serve", "seu Instagram.", [
     "Escreva em uma frase o que o Instagram precisa trazer: <b>vendas, agendamentos ou gente na loja</b>.",
     "Descreva o seu cliente ideal: idade, bairro, o que ele procura e o que faz ele comprar.",
     "Liste as 3 perguntas que mais chegam no seu WhatsApp ou balcão.",
     "Escolha <b>uma ação</b> que você quer que a pessoa faça: chamar no WhatsApp, agendar, visitar."],
   "Sem objetivo, todo post vira sorte."),
  (False, LILAS, "Dia 2", "Arrume a sua", "vitrine.", [
     "<b>Nome</b> com palavra de busca: \"Sua Marca | O que você faz em Sua Cidade\".",
     "<b>Bio</b> em 4 linhas: o que faz, pra quem, onde fica, e o que a pessoa deve fazer.",
     "<b>Link</b> direto para o WhatsApp (wa.me/55DDDNÚMERO).",
     "<b>Foto de perfil</b> legível no círculo pequeno: logo simples ou o seu rosto.",
     "Endereço, horário e categoria certos no perfil."],
   "Quem chega no perfil decide em 3 segundos se fica."),
  (True, ROXO, "Dia 3", "Organize os", "destaques.", [
     "Crie de 4 a 5 destaques com capas no mesmo estilo e nas cores da marca.",
     "Sugestão: <b>Serviços ou Cardápio · Como chegar · Clientes · Bastidores · Contato</b>.",
     "Apague destaques antigos, vazios ou que não ajudam a vender.",
     "Coloque o mais importante primeiro: é o que aparece sem arrastar."],
   "Destaque é o seu catálogo que nunca some."),
  (False, "#FFFFFF", "Dia 4", "Escolha os seus", "pilares.", [
     "Defina 3 temas que você vai repetir sempre. Ex.: <b>Produto · Dica · Bastidores</b>.",
     "Para cada tema, escreva 3 ideias de post (são 9 ideias na mão).",
     "Pense nas perguntas do Dia 1: cada uma vira um post.",
     "Corte qualquer ideia que não tenha a ver com o seu cliente ideal."],
   "Quem sabe sobre o que fala, nunca fica sem post."),
  (True, PRETO, "Dia 5", "Monte a semana", "no calendário.", [
     "Escolha 3 dias fixos de feed (ex.: segunda, quarta e sexta).",
     "Distribua: 1 carrossel, 1 post de foto e 1 Reels.",
     "Para cada post, escreva o <b>objetivo</b> e o <b>pedido no final</b> (salvar, comentar, chamar no WhatsApp).",
     "Planeje stories todos os dias: bom dia, bastidor, produto, enquete, convite."],
   "Post com data marcada sai. Post \"quando der\" não sai."),
  (False, LILAS, "Dia 6", "Produza tudo", "de uma vez.", [
     "Reserve 1 hora para fotografar e gravar o conteúdo da semana inteira.",
     "Use <b>fotos reais</b>: você, a equipe, o produto, o lugar. Luz de janela ajuda muito.",
     "Grave vídeos curtos na vertical, de 3 a 5 segundos por cena.",
     "Deixe as legendas prontas: gancho na primeira linha, chamada no final."],
   "Gravar um pouco por dia cansa. Em lote, rende."),
  (True, ROXO, "Dia 7", "Olhe os", "números.", [
     "Abra o painel profissional do Instagram e anote: <b>alcance, visitas ao perfil, cliques no link e mensagens</b>.",
     "Veja qual post foi mais salvo e mais compartilhado: faça mais daquilo.",
     "Veja em que dia e horário o seu público está mais ativo.",
     "Repita o ciclo na próxima semana, ajustando o que não funcionou."],
   "O que não é medido vira achismo."),
]

for i, (dark, bg, label, t1, t2, items, quote) in enumerate(days, start=3):
    color = LILAS if dark else PRETO
    tagc = LILAS if dark else ROXO2
    deco = f'<div aria-hidden="true" class="pf" style="position:absolute;right:-50px;top:110px;font-style:italic;font-weight:800;font-size:560px;line-height:1;color:{"rgba(243,238,255,.07)" if dark else "rgba(84,35,203,.07)"}">{label[-1]}</div>'
    hl = f'background:linear-gradient(180deg,transparent 62%,{MARCA} 62%,{MARCA} 90%,transparent 90%);padding:0 10px' if not dark else f'text-decoration:underline;text-decoration-color:{VERM};text-decoration-thickness:6px;text-underline-offset:16px'
    pages.append(f'''<div class="slide" style="background:{bg};color:{color}">{deco}{grain(i, dark)}{head(dark, label.upper())}
<div style="position:absolute;left:80px;right:80px;top:230px">
  <span class="tag" style="color:{tagc}">{label} · checklist</span>
  <p style="margin:30px 0 0;font-size:72px;font-weight:800;line-height:1.02;letter-spacing:-.025em">{t1}</p>
  <p class="pf" style="margin:6px 0 0;font-style:italic;font-weight:700;font-size:108px;line-height:1.08;letter-spacing:-.015em;color:{LILAS if dark else ROXO}"><span style="{hl}">{t2}</span></p>
  {checklist(items, dark)}
  <p class="pf" style="margin:44px 0 0;font-style:italic;font-weight:400;font-size:40px;line-height:1.3;color:{LILAS if dark else ROXO}">({quote})</p>
</div>{foot(dark, i)}</div>''')

# CTA
pages.append(f'''<div class="slide" style="background:{ROXO};color:{LILAS}">
<div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 0%,rgba(84,35,203,.85),rgba(38,3,155,1) 60%)"></div>{grain(10, True)}
<div class="head"><span class="handle" style="color:{LILAS}">@agenciaadullam</span><span class="count" style="color:{LILAS}">PRÓXIMO PASSO</span></div>
<div style="position:absolute;left:80px;right:80px;top:160px;display:flex;flex-direction:column;align-items:center;text-align:center">
  <p class="pf" style="margin:0;font-style:italic;font-weight:400;font-size:62px;line-height:1">Sem tempo pra fazer sozinho?</p>
  <p style="margin:28px 0 0;max-width:900px;font-size:70px;font-weight:800;line-height:1.06;letter-spacing:-.025em;text-wrap:balance">A gente monta o plano do seu perfil.</p>
  <div style="margin-top:44px;width:100%;box-sizing:border-box;background:{LILAS};color:{PRETO};border-radius:24px;padding:40px 52px;text-align:left">
    <span class="tag" style="color:{ROXO2}">Análise + planejamento de 30 dias</span>
    <ul style="list-style:none;margin:24px 0 0;padding:0;font-size:31px;font-weight:500;line-height:1.35">
      <li style="padding:10px 0">✓&nbsp; Análise completa do seu perfil, com o que ajustar</li>
      <li style="padding:10px 0">✓&nbsp; Calendário de 30 dias de feed: carrosséis, posts e Reels</li>
      <li style="padding:10px 0">✓&nbsp; Roteiro de cada Reels e texto de cada carrossel</li>
      <li style="padding:10px 0">✓&nbsp; Cronograma de stories, fala por fala</li>
    </ul>
    <div style="display:flex;align-items:baseline;justify-content:space-between;margin-top:28px;padding-top:28px;border-top:1px solid rgba(18,18,18,.15)">
      <span style="font-size:30px;font-weight:600">Investimento</span>
      <span class="pf" style="font-style:italic;font-weight:700;font-size:84px;color:{ROXO}">R$ 297</span>
    </div>
  </div>
  <p style="margin:40px 0 0;font-size:34px;font-weight:600;line-height:1.45">Para agendar a sua call, manda <span style="display:inline-block;background:{ROXO2};font-weight:800;letter-spacing:.08em;border-radius:12px;padding:0 16px 4px">ANÁLISE</span><br>no direct do @agenciaadullam <span class="pf" style="font-style:italic;font-weight:400">e a gente marca um horário com você.</span></p>
</div>
<div style="position:absolute;left:0;right:0;bottom:80px;display:flex;justify-content:center"><img src="{SYS}/logos/adullam-escura.png" alt="Adullam" style="width:300px;height:auto"></div>
</div>''')

html = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><link rel="stylesheet" href="{SYS}/base.css">
<style>@page{{size:1080px 1440px;margin:0}} .slide{{page-break-after:always}} b{{font-weight:800}}</style></head><body>{"".join(pages)}</body></html>'''
with open(os.path.join(HERE, "guia.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("paginas:", len(pages))
