#!/bin/sh
# Gera o PDF "7 dias para sair do improviso" com o botão de WhatsApp clicável.
set -e
cd "$(dirname "$0")"
python3 gerar.py
NODE_PATH=$(npm root -g) node -e "
const {chromium}=require('playwright');const fs=require('fs');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1440}});await p.goto('file://'+process.cwd()+'/guia.html');await p.evaluate(()=>document.fonts.ready);const els=await p.\$\$('.slide');for(let i=0;i<els.length;i++){await els[i].screenshot({path:'p'+String(i+1).padStart(2,'0')+'.jpg',type:'jpeg',quality:90});}
const box=await p.evaluate(()=>{const s=[...document.querySelectorAll('.slide')].pop().getBoundingClientRect();const r=document.getElementById('wa').getBoundingClientRect();return {x:r.left-s.left,y:r.top-s.top,w:r.width,h:r.height}});fs.writeFileSync('wa.json',JSON.stringify(box));await b.close();})()"
python3 - <<'EOF'
from PIL import Image; import glob, json
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, DictionaryObject, TextStringObject, ArrayObject, FloatObject, NumberObject
fs = sorted(glob.glob('p??.jpg')); ims = [Image.open(f).convert('RGB') for f in fs]
ims[0].save('tmp.pdf', save_all=True, append_images=ims[1:], resolution=72)
b = json.load(open('wa.json'))
r = PdfReader('tmp.pdf'); w = PdfWriter()
for pg in r.pages: w.add_page(pg)
H = float(w.pages[-1].mediabox.height); sx = float(w.pages[-1].mediabox.width) / 1080
url = "https://wa.me/5591993235567?text=Oi%2C%20Breno!%20Quero%20a%20An%C3%A1lise%20%2B%20Planejamento%20de%2030%20dias%20(R%24%20297)%20pro%20Instagram%20da%20minha%20empresa."
ann = DictionaryObject({NameObject("/Type"): NameObject("/Annot"), NameObject("/Subtype"): NameObject("/Link"),
  NameObject("/Rect"): ArrayObject([FloatObject(b['x']*sx), FloatObject(H-(b['y']+b['h'])*sx), FloatObject((b['x']+b['w'])*sx), FloatObject(H-b['y']*sx)]),
  NameObject("/Border"): ArrayObject([NumberObject(0)]*3),
  NameObject("/A"): DictionaryObject({NameObject("/S"): NameObject("/URI"), NameObject("/URI"): TextStringObject(url)})})
w.add_annotation(page_number=len(w.pages)-1, annotation=ann)
w.write('7-dias-para-sair-do-improviso.pdf')
ims[-1].save('preview-cta.jpg', quality=80)
EOF
rm -f tmp.pdf p??.jpg wa.json
