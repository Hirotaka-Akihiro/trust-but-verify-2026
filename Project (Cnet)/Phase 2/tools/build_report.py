"""Build the Times New Roman report and cited architecture adaptation."""
from pathlib import Path
from html import escape
import math
import re
from PIL import Image as PILImage, ImageDraw, ImageFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
    Spacer, PageBreak, NextPageTemplate, Table, TableStyle, Image)

ROOT=Path(__file__).resolve().parents[1]
FONTS=Path('C:/Windows/Fonts')
for name,file in [('TNR','times.ttf'),('TNR-Bold','timesbd.ttf'),
                  ('TNR-Italic','timesi.ttf'),('TNR-BoldItalic','timesbi.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(FONTS/file)))
pdfmetrics.registerFontFamily('TNR',normal='TNR',bold='TNR-Bold',italic='TNR-Italic',boldItalic='TNR-BoldItalic')


def diagram():
    w,h=1800,1260
    im=PILImage.new('RGB',(w,h),'white'); d=ImageDraw.Draw(im)
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',
         '<title id="title">Traffic-policy experiment adapted from ToolGuards Figure 1</title>',
         '<desc id="desc">Offline policy mapping and classifier training feed an agent. Identical proposals are replayed without a gate and with a deterministic gate. Simulator state is scored independently.</desc>',
         '<defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="#333"/></marker></defs><rect width="1800" height="1260" fill="white"/>']

    def text(x,y,s,size=28,bold=False):
        font=ImageFont.truetype(str(FONTS/('timesbd.ttf' if bold else 'times.ttf')),size)
        d.text((x,y),s,font=font,fill='#111')
        svg.append(f'<text x="{x}" y="{y+size*.88}" font-family="Times New Roman,Times,serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="#111">{escape(s)}</text>')

    def rect(x,y,bw,bh,lines,fill='#fff',dashed=False):
        d.rectangle((x,y,x+bw,y+bh),fill=fill,outline='#555',width=2)
        svg.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" fill="{fill}" stroke="#555" stroke-width="2"'+(' stroke-dasharray="8 6"' if dashed else '')+'/>')
        for i,s in enumerate(lines):
            size=36
            while size>22:
                font=ImageFont.truetype(str(FONTS/('timesbd.ttf' if i==0 else 'times.ttf')),size)
                if d.textlength(s,font=font)<=bw-30:break
                size-=1
            text(x+15,y+15+43*i,s,size,bold=(i==0))

    def arrow(points,dashed=False):
        if dashed:
            for (x1,y1),(x2,y2) in zip(points,points[1:]):
                length=math.hypot(x2-x1,y2-y1)
                for a in range(0,int(length),14):
                    t=a/length;u=min(a+8,length)/length
                    d.line((x1+(x2-x1)*t,y1+(y2-y1)*t,x1+(x2-x1)*u,y1+(y2-y1)*u),fill='#444',width=3)
        else:d.line(points,fill='#333',width=3)
        (x1,y1),(x2,y2)=points[-2:];a=math.atan2(y2-y1,x2-x1)
        d.polygon([(x2,y2),(x2-14*math.cos(a-.45),y2-14*math.sin(a-.45)),(x2-14*math.cos(a+.45),y2-14*math.sin(a+.45))],fill='#333')
        svg.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in points)+'" fill="none" stroke="#333" stroke-width="3" marker-end="url(#a)"'+(' stroke-dasharray="8 6"' if dashed else '')+'/>')

    text(60,25,'Network traffic policy: simplified research pipeline',42,True)
    text(60,105,'1. Prepare the traffic classifier',36,True)
    rect(70,180,420,120,['ISCXVPN2016','Flow-feature CSVs'])
    rect(650,180,480,120,['Preprocess and split','Clean data; separate test flows'])
    rect(1280,180,450,120,['Selected application classifier','Choose DT or RF; predict test flows'])
    arrow([(490,240),(650,240)])
    arrow([(1130,240),(1280,240)])

    text(60,355,'2. Generate one action per scenario',36,True)
    rect(70,430,420,120,['Operator request','Policy included in prompt'])
    rect(650,430,480,120,['Small local LLM','Request + predicted traffic type'])
    rect(1280,430,450,120,['100 cached proposals','Same calls used in every condition'])
    arrow([(490,490),(650,490)])
    arrow([(1130,490),(1280,490)])
    arrow([(1505,300),(1505,330),(890,330),(890,430)])

    text(60,605,'3. Compare outcomes with and without the gate',36,True)
    arrow([(1505,550),(1505,680),(400,680),(400,900)])
    arrow([(1505,680),(1390,680),(1390,740)])
    rect(650,740,400,120,['Gate inputs','Written rules + trusted prediction'],'#f3f3f3')
    rect(1140,740,500,120,['Deterministic policy gate','Accept action or reject and hold'],'#eeeeee')
    arrow([(1050,800),(1140,800)])
    rect(150,900,500,120,['B0: Ungated simulator','Execute recognized proposals'])
    rect(1140,900,500,120,['M: Gated simulator','Execute accepted; keep rejects held'])
    arrow([(1390,860),(1390,900)])
    arrow([(400,1020),(400,1070),(900,1070),(900,1120)])
    arrow([(1390,1020),(1390,1070),(900,1070)])
    rect(70,1120,430,100,['Independent reference','True labels + expected outcomes'])
    rect(650,1120,990,100,['Independent evaluation','Policy violations, task completion, rejection and latency'])
    arrow([(500,1170),(650,1170)])
    text(60,1230,'Adapted from Zwerdling et al., EMNLP 2025, Figure 1 (p. 597); mapped to this project.',24)
    svg.append('</svg>')
    (ROOT/'architecture.svg').write_text('\n'.join(svg),encoding='utf-8',newline='\n')
    im.save(ROOT/'architecture.png')


def inline(s):
    s=escape(s)
    s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:f'<link href="{m[2]}" color="#222">{m[1]}</link>',s)
    s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<i>\1</i>',s)
    return re.sub(r'`([^`]+)`',r'\1',s)


def build_pdf():
    styles=getSampleStyleSheet()
    for name in ['Normal','BodyText','Title','Heading1','Heading2','Heading3']:
        styles[name].fontName='TNR'
    styles['BodyText'].fontSize=12;styles['BodyText'].leading=15;styles['BodyText'].spaceAfter=7
    for name,size in [('Heading1',18),('Heading2',14),('Heading3',12)]:
        styles[name].fontName='TNR-Bold';styles[name].fontSize=size;styles[name].leading=size+3
    styles.add(ParagraphStyle(name='Cell',fontName='TNR',fontSize=10,leading=12))
    styles.add(ParagraphStyle(name='WideCell',fontName='TNR',fontSize=9,leading=10.7))
    styles.add(ParagraphStyle(name='Cover',fontName='TNR-Bold',fontSize=28,leading=34,spaceAfter=20))
    p=lambda text,style='BodyText':Paragraph(inline(text),styles[style])
    story=[Spacer(1,70),p('Trust but Verify','Cover'),
           p('Deterministic Gating for LLM Agents Enforcing Network Traffic Policy','Heading1'),
           Spacer(1,20),p('Phase 2: Literature review and research methodology','Heading2'),
           p('M. Abdullah Aamir (23i-2538) · Haider Farooq Toor (23i-2542) · DS-A'),
           p('Computer Networks'),Spacer(1,22),
           p('1. Extended literature review\n2. Refined research gap\n3. Twelve-step methodology\n4. Research architecture'.replace('\n','<br/>')),
           Spacer(1,18),p('Research proposal; experiments remain future work.'),PageBreak()]
    # Paragraph markup in the cover is intentional.
    story[8]=Paragraph('1. Extended literature review<br/>2. Refined research gap<br/>3. Twelve-step methodology<br/>4. Research architecture',styles['BodyText'])
    for n in range(1,5):
        if n>1:story.append(PageBreak())
        lines=(ROOT/f'Deliverable{n}.md').read_text(encoding='utf-8').splitlines();i=0
        while i<len(lines):
            line=lines[i].strip()
            if not line:i+=1;continue
            if line.startswith('!['):
                story.extend([NextPageTemplate('landscape'),PageBreak(),
                              Image(str(ROOT/'architecture.png'),width=680,height=476)])
                i+=1
                while i<len(lines) and not lines[i].strip():i+=1
                if i<len(lines) and lines[i].strip().startswith('**Figure'):
                    story.append(p(lines[i].strip(),'Cell'));i+=1
                if any(v.strip() for v in lines[i:]):story.extend([NextPageTemplate('portrait'),PageBreak()])
                continue
            if line.startswith('|'):
                rows=[]
                while i<len(lines) and lines[i].strip().startswith('|'):
                    row=[v.strip() for v in lines[i].strip().strip('|').split('|')]
                    if not all(re.fullmatch(':?-+:?',v.replace(' ','')) for v in row):rows.append(row)
                    i+=1
                wide=len(rows[0])>=8
                if wide:story.extend([NextPageTemplate('landscape'),PageBreak(),p('Cross-paper comparison','Heading2')])
                widths=[24,120,32,70,80,82,65,85,220] if wide else [487/len(rows[0])]*len(rows[0])
                table=Table([[p(c,'WideCell' if wide else 'Cell') for c in row] for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
                table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8e8e8')),
                    ('GRID',(0,0),(-1,-1),.35,colors.grey),('VALIGN',(0,0),(-1,-1),'TOP'),
                    ('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),
                    ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
                story.extend([table,Spacer(1,8)])
                if wide:story.extend([NextPageTemplate('portrait'),PageBreak()])
                continue
            if line.startswith('#'):
                if n==4 and line=='## Architecture':i+=1;continue
                level=len(line)-len(line.lstrip('#'));story.append(p(line.lstrip('#').strip(),f'Heading{min(level,3)}'));i+=1;continue
            block=[line];i+=1
            if not re.match(r'^(\d+\.|-) ',line):
                while i<len(lines) and lines[i].strip() and not re.match(r'^(#|\||!\[|\d+\. |\- )',lines[i].strip()):
                    block.append(lines[i].strip());i+=1
            story.append(p(' '.join(block)))
    def footer(c,doc):
        w,h=c._pagesize;c.setFont('TNR',9);c.setFillColor(colors.HexColor('#555'))
        c.drawString(40,20,'Trust but Verify | Phase 2');c.drawRightString(w-40,20,str(doc.page))
    doc=BaseDocTemplate(str(ROOT/'23i-2538_23i-2542_Phase-2.pdf'),title='Trust but Verify: Phase 2',author='M. Abdullah Aamir; Haider Farooq Toor')
    doc.addPageTemplates([
        PageTemplate(id='portrait',pagesize=A4,frames=[Frame(54,45,487,A4[1]-90,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=footer),
        PageTemplate(id='landscape',pagesize=landscape(A4),frames=[Frame(32,32,landscape(A4)[0]-64,landscape(A4)[1]-64,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=footer)])
    doc.build(story)


if __name__=='__main__':
    diagram();build_pdf()
    print('Built Times New Roman PDF and architecture exports.')
