#!/usr/bin/env python3
"""Render three review-only Open Graph motion directions; no app runtime imports.

Usage: python render.py [--stills]
Requires Pillow and ffmpeg/ffprobe. All fonts and the rasterized brand mark are local.
The PNG mark is a raster export of the existing brand asset, not a new logo.
"""
import argparse
import functools
import html
import json
import math
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
W, H, FPS, DURATION = 1200, 630, 24, 6
C = json.loads((ROOT / 'config.json').read_text())
BG, INK, ACCENT, MUTED = C['background'], C['ink'], C['accent'], C['muted']
LOGO = Image.open(ROOT / 'assets/mark.png').convert('RGBA')


@functools.lru_cache(maxsize=128)
def font(size, weight='regular'):
    return ImageFont.truetype(str(ROOT / f'fonts/{weight}.ttf'), size)


def rgb(color):
    return tuple(bytes.fromhex(color.lstrip('#')))


def mix(a, b, t):
    return tuple(round(x * (1-t) + y*t) for x,y in zip(rgb(a),rgb(b)))


def text(draw, xy, value, size=26, color=None, weight='regular', max_width=None):
    face = font(size, weight)
    if max_width:
        while draw.textlength(value, font=face) > max_width and size > 12:
            size -= 1
            face = font(size, weight)
    draw.text(xy, value, font=face, fill=color or INK, anchor='lt')


def lines(draw, xy, values, size=72, color=None, weight='bold', gap=10, max_width=700):
    for i,value in enumerate(values):
        text(draw,(xy[0],xy[1]+i*(size+gap)),value,size,color,weight,max_width)


def box(draw, xy, fill, radius=24, outline=None, width=1):
    draw.rounded_rectangle(tuple(round(v) for v in xy),radius,fill,outline,width)


@functools.lru_cache(maxsize=128)
def mark(size):
    image = LOGO.copy()
    image.thumbnail((size,size),Image.Resampling.LANCZOS)
    return image


def logo(im,x,y,size):
    asset=mark(size)
    im.paste(asset,(round(x+(size-asset.width)/2),round(y+(size-asset.height)/2)),asset)


def header(im,draw):
    logo(im,56,38,48)
    text(draw,(120,47),C['name'],28,weight='bold')
    text(draw,(875,53),C['domain'],20,MUTED,max_width=265)


def footer(draw,label):
    draw.line((56,555,1144,555),fill=mix(BG,INK,.16),width=1)
    text(draw,(56,579),label,20,MUTED,max_width=900)
    draw.ellipse((1128,584,1140,596),fill=ACCENT)


def check(draw,x,y,color=INK):
    draw.line([(x,y+9),(x+8,y+17),(x+24,y)],fill=color,width=4)


def icon(draw,x,y,kind,color):
    if kind=='chat':
        box(draw,(x,y,x+52,y+38),None,10,color,3)
        draw.line((x+10,y+38,x+10,y+49,x+23,y+38),fill=color,width=3)
        for i in range(3):draw.ellipse((x+12+i*12,y+16,x+16+i*12,y+20),fill=color)
    elif kind=='terminal':
        box(draw,(x,y,x+54,y+45),None,8,color,3)
        draw.line((x+12,y+15,x+21,y+23,x+12,y+31),fill=color,width=3)
        draw.line((x+29,y+31,x+41,y+31),fill=color,width=3)
    elif kind=='file':
        box(draw,(x+7,y-3,x+45,y+48),None,6,color,3)
        for i in range(3):draw.line((x+16,y+13+i*10,x+35,y+13+i*10),fill=color,width=3)
    elif kind=='check':
        box(draw,(x+3,y,x+49,y+46),None,12,color,3)
        check(draw,x+14,y+13,color)
    elif kind=='video':
        box(draw,(x,y+3,x+38,y+38),None,7,color,3)
        draw.polygon([(x+39,y+14),(x+54,y+5),(x+54,y+37),(x+39,y+28)],outline=color,width=3)
    else:
        for dx,dy in [(0,0),(29,0),(0,29),(29,29)]:box(draw,(x+dx,y+dy,x+dx+20,y+dy+20),None,5,color,3)


def brand(im,draw,t):
    # A restrained continuous orbit. The first frame is already a full card.
    phase=2*math.pi*t/DURATION
    cx,cy=933,307
    for r in (157,208,262):
        draw.ellipse((cx-r,cy-r,cx+r,cy+r),outline=mix(BG,INK,.10),width=2)
    for i in range(3):
        a=phase+i*2*math.pi/3
        x=cx+208*math.cos(a); y=cy+208*math.sin(a)
        draw.ellipse((x-8,y-8,x+8,y+8),fill=ACCENT)
    side=250+round(10*math.sin(phase))
    if C['key'] in ('bloom','doozy'):
        box(draw,(cx-148,cy-148,cx+148,cy+148),C['panel'],44)
    logo(im,cx-side/2,cy-side/2,side)
    text(draw,(58,167),C['eyebrow'].upper(),18,ACCENT,weight='bold',max_width=625)
    lines(draw,(52,216),C['headline'],size=C.get('headline_size',78),max_width=660)
    text(draw,(58,455),C['subline'],25,MUTED,max_width=650)
    footer(draw,C['footer'])


def workflow(im,draw,t):
    text(draw,(58,138),C['workflow_title'],48,weight='bold',max_width=1080)
    phase=t/DURATION
    progress=[.5+.5*math.sin(2*math.pi*phase-i*.85) for i in range(3)]
    scene=C['scene']
    if scene=='chat':
        box(draw,(58,219,1142,521),C['panel'],28)
        for i,(msg,p) in enumerate(zip(C['rows'],progress)):
            x=93 if i%2==0 else 398
            y=245+i*81+4*math.sin(2*math.pi*phase+i)
            box(draw,(x,y,x+650,y+62),C['surface'] if i%2==0 else ACCENT,20)
            text(draw,(x+24,y+18),msg,25,C['panel_ink'],max_width=590)
        for i in range(3):
            y=473+5*math.sin(2*math.pi*phase+i)
            draw.ellipse((1044+i*21,y,1054+i*21,y+10),fill=INK)
    elif scene=='terminals':
        for i,(title,row,p) in enumerate(zip(C['features'],C['rows'],progress)):
            x=58+i*366
            box(draw,(x,223,x+352,518),C['panel'],18,mix(BG,INK,.19))
            for j in range(3):draw.ellipse((x+20+j*17,242,x+27+j*17,249),fill=mix(C['panel'],INK,.4))
            text(draw,(x+21,279),title,27,C['panel_ink'],weight='bold',max_width=310)
            text(draw,(x+21,329),row,20,MUTED,weight='mono',max_width=310)
            for j in range(3):
                yy=383+j*24
                box(draw,(x+22,yy,x+55+round((230-j*37)*(.55+.45*p)),yy+7),mix(C['panel'],ACCENT,.25+j*.2),3)
            text(draw,(x+22,472),'Working on its own branch',16,MUTED,max_width=310)
    elif scene=='tasks':
        box(draw,(58,224,416,520),C['panel'],25)
        logo(im,153,247,167)
        text(draw,(102,443),'Your next steps',25,C['panel_ink'],weight='bold',max_width=280)
        for i,(row,p) in enumerate(zip(C['rows'],progress)):
            y=224+i*103
            box(draw,(445,y,1142,y+90),C['surface'],18,mix(BG,INK,.2))
            box(draw,(469,y+28,503,y+62),ACCENT,9)
            if p>.35:check(draw,474,y+34,C['panel_ink'])
            text(draw,(525,y+30),row,26,INK,max_width=580)
    elif scene=='files':
        box(draw,(58,224,440,520),C['panel'],24)
        text(draw,(83,252),'Your agent makes it',27,C['panel_ink'],weight='bold',max_width=330)
        for i,row in enumerate(C['rows']):
            y=325+i*55
            icon(draw,85,y-3,'file',ACCENT)
            text(draw,(154,y+5),row,23,C['panel_ink'],weight='mono',max_width=260)
        box(draw,(477,224,1142,520),C['surface'],24,mix(BG,INK,.2))
        text(draw,(503,248),'A link your team can open',26,INK,weight='bold',max_width=605)
        box(draw,(505,307,1113,487),C['panel'],14)
        text(draw,(531,332),'Team dashboard',28,C['panel_ink'],weight='bold')
        for i,p in enumerate(progress):
            x=539+i*170
            box(draw,(x,437-round(52*p),x+119,461),ACCENT,9)
    else:
        for i,(title,row,p) in enumerate(zip(C['features'],C['rows'],progress)):
            x=58+i*366
            box(draw,(x,227,x+352,516),C['surface'],22)
            icon(draw,x+27,259,C['icons'][i],C['panel_ink'])
            text(draw,(x+27,332),title,28,C['panel_ink'],weight='bold',max_width=300)
            text(draw,(x+27,379),row,23,C['panel_ink'],max_width=300)
            box(draw,(x+27,451,x+102,482),ACCENT,16)
            draw.ellipse((x+30+round(p*39),455,x+53+round(p*39),478),fill=C['panel'])
    footer(draw,C['workflow_footer'])


def features(im,draw,t):
    phase=2*math.pi*t/DURATION
    lines(draw,(58,154),C['feature_headline'],size=65,max_width=480)
    text(draw,(60,418),C['feature_subline'],24,MUTED,max_width=480)
    centers=[(758,250),(1013,250),(758,438),(1013,438)]
    for i,(x,y) in enumerate(centers):
        offset=7*math.sin(phase+i*math.pi/2)
        y+=offset
        box(draw,(x-116,y-78,x+116,y+78),C['surface'],24,mix(BG,INK,.13))
        icon(draw,x-26,y-49,C['icons'][i],C['tile_ink'])
        text(draw,(x-94,y+23),C['features'][i],23,C['tile_ink'],weight='bold',max_width=195)
    # A traveling signal through the four tiles; muted enough to keep copy primary.
    draw.line((758,350,1013,350),fill=mix(BG,INK,.25),width=2)
    signal=885+120*math.sin(phase)
    draw.ellipse((signal-6,344,signal+6,356),fill=ACCENT)
    footer(draw,C['feature_footer'])


def frame(option,t):
    im=Image.new('RGB',(W,H),BG)
    draw=ImageDraw.Draw(im)
    header(im,draw)
    [brand,workflow,features][option](im,draw,t)
    return im


def encode(option,path):
    proc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24',
        '-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264',
        '-preset','medium','-crf','22','-pix_fmt','yuv420p','-movflags','+faststart',
        '-threads','2',str(path)],stdin=subprocess.PIPE)
    try:
        for n in range(FPS*DURATION):proc.stdin.write(frame(option,n/FPS).tobytes())
    finally:
        proc.stdin.close()
    if proc.wait()!=0:raise RuntimeError(f'ffmpeg failed: {path}')


def review(out):
    cards=[]
    for i,option in enumerate(C['options']):
        key=chr(97+i)
        cards.append(f'''<article><header><b>{key.upper()}</b><div><h2>{html.escape(option['name'])}</h2><p>{html.escape(option['description'])}</p></div></header><video controls muted loop playsinline preload="none" poster="{key}.png"><source src="{key}.mp4" type="video/mp4"></video><p><a href="{key}.mp4" download>Download MP4</a> · <a href="{key}.png">Static poster</a></p></article>''')
    document=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>{html.escape(C['name'])} · motion options</title><style>*{{box-sizing:border-box}}body{{margin:0;background:#f5f4f0;color:#202326;font:16px system-ui,sans-serif}}main{{max-width:1060px;margin:auto;padding:48px 24px}}h1{{font-size:clamp(32px,5vw,56px);letter-spacing:-2px;margin:16px 0}}.intro{{max-width:720px;color:#53605b;line-height:1.6}}article{{background:white;border:1px solid #ddd;border-radius:24px;padding:22px;margin:28px 0}}header{{display:flex;gap:20px;align-items:center;margin-bottom:20px}}header b{{font-size:40px;color:#65786c}}h2{{margin:0 0 6px;font-size:25px}}p{{margin:8px 0;line-height:1.5}}video{{width:100%;aspect-ratio:1200/630;border-radius:12px;background:#202326}}a{{color:#215d51}}button{{font:inherit;padding:12px 18px;border:1px solid #ccc;background:white;border-radius:9px;cursor:pointer}}</style><main><small>OPEN GRAPH / DESIGN REVIEW</small><h1>{html.escape(C['name'])}, in motion.</h1><p class="intro">Three directions for your link previews. Each is a 6-second silent loop, with a static poster. Choose A, B or C; production metadata is unchanged in this draft. Workflow drawings are illustrative, not recordings of the live app.</p>{''.join(cards)}<p class="intro">Video playback in social previews depends on the receiving app. The chosen implementation will retain existing page-specific image fallbacks, titles and descriptions. Preview concepts use DejaVu type; final typesetting should use the site's brand fonts.</p></main></html>'''
    (out/'index.html').write_text(document)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--stills',action='store_true')
    args=parser.parse_args()
    out=ROOT/'previews';out.mkdir(exist_ok=True)
    contact=Image.new('RGB',(1200,1110),'#f5f4f0')
    cd=ImageDraw.Draw(contact)
    for i,option in enumerate(C['options']):
        key=chr(97+i)
        still=frame(i,0)
        still.save(out/f'{key}.png',optimize=True)
        small=still.resize((600,315),Image.Resampling.LANCZOS)
        contact.paste(small,(568,i*370+28))
        text(cd,(32,i*370+50),f'{key.upper()} / {option["name"]}',30,'#202326','bold',500)
        for j,line in enumerate(option['caption']):text(cd,(32,i*370+110+j*34),line,23,'#53605b',max_width=490)
        if not args.stills:
            encode(i,out/f'{key}.mp4')
            print(f'Rendered {C["name"]} {key.upper()}',flush=True)
    contact.save(out/'comparison.png',optimize=True)
    review(out)
    if not args.stills:
        # Convenience exports derive from exactly the same frames and media.
        frames=[]
        for n in range(36):
            overview=Image.new('RGB',(600,1080),'#f5f4f0')
            draw=ImageDraw.Draw(overview)
            for i,option in enumerate(C['options']):
                text(draw,(16,360*i+12),chr(65+i)+' / '+option['name'],20,'#202326','bold',568)
                preview=frame(i,n/6).resize((600,315),Image.Resampling.LANCZOS)
                overview.paste(preview,(0,360*i+42))
            frames.append(overview)
        palette=frames[0].quantize(colors=128)
        frames=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
        frames[0].save(out/'comparison.gif',save_all=True,append_images=frames[1:],
            duration=167,loop=0,optimize=True,disposal=1)



if __name__=='__main__':main()
