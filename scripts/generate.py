#!/usr/bin/env python3
"""FuTe Cyber Arcade, self-hosted editable SVG and animated GIF generator.

Demonstration (explicitly labeled DEMO): python scripts/generate.py --demo
Live GitHub data: GITHUB_TOKEN=... python scripts/generate.py --live
Requires Pillow. SVGs are generated using only stdlib. No GitSkins, JS, fonts or third-party media are embedded in profile images.
"""
from __future__ import annotations
import argparse
import base64
import io
import datetime as dt
import html
import json
import math
import os
from pathlib import Path
import random
import re
import urllib.request
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / 'assets'
CFG = json.loads((ROOT / 'config.json').read_text(encoding='utf-8'))
P = CFG['palette']
USER = CFG['username']
M = 'monospace'


def h(s): return html.escape(str(s), quote=True)


def txt(x,y,s,size=18,color='white',weight=500,anchor=None,spacing=0):
    return (f'<text x="{x}" y="{y}" font-family="{M}" font-size="{size}" '
            f'font-weight="{weight}" fill="{P.get(color,color)}" letter-spacing="{spacing}"'
            f'{f" text-anchor={chr(34)+anchor+chr(34)}" if anchor else ""}>{h(s)}</text>')


def rect(x,y,w,hgt,fill='panel',stroke=None,sw=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{hgt}" fill="{P.get(fill,fill)}"' + (f' stroke="{P.get(stroke,stroke)}" stroke-width="{sw}"' if stroke else '') + '/>'


def ln(x1,y1,x2,y2,color='line',width=1):
    return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{P.get(color,color)}" stroke-width="{width}" fill="none"/>'


def dots(x,y,c='green'):
    return ''.join(rect(x+i*16,y,7,7,c) for i in range(3))


def base(w,height,window,section):
    s=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{height}" viewBox="0 0 {w} {height}" role="img" aria-label="FuTe {h(section)}">
<defs><pattern id="mesh" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" stroke="#224143" stroke-width="0.7" fill="none" opacity=".29"/></pattern></defs>
{rect(0,0,w,height,'bg')}
{rect(2,2,w-4,height-4,'none','line',2)}
{rect(12,12,w-24,height-24,'none','line',1)}
{rect(13,49,w-26,height-62,'#0B1319')}
<rect x="13" y="49" width="{w-26}" height="{height-62}" fill="url(#mesh)" opacity=".65"/>
{rect(13,13,w-26,34,'panel')}
{dots(28,26,'green')}
{txt(95,35,window,13,'dim',700,spacing=1.5)}
{txt(w-31,35,'FUTE_OS / v3.0',12,'mint',700,anchor='end')}
{ln(13,47,w-13,47,'line',2)}'''
    for x,y,dx,dy in [(14,49,1,1),(w-14,49,-1,1),(14,height-14,1,-1),(w-14,height-14,-1,-1)]:
        s+=ln(x,y,x+dx*15,y,'green',2)+ln(x,y,x,y+dy*15,'green',2)
    return s


# Hand-drawn 5x7 bitmap glyphs — guaranteed pixel typography, no external fonts.
GLYPHS={
'A':['01110','10001','10001','11111','10001','10001','10001'],
'B':['11110','10001','10001','11110','10001','10001','11110'],
'C':['01111','10000','10000','10000','10000','10000','01111'],
'D':['11110','10001','10001','10001','10001','10001','11110'],
'E':['11111','10000','10000','11110','10000','10000','11111'],
'F':['11111','10000','10000','11110','10000','10000','10000'],
'G':['01111','10000','10000','10111','10001','10001','01111'],
'H':['10001','10001','10001','11111','10001','10001','10001'],
'I':['11111','00100','00100','00100','00100','00100','11111'],
'J':['00111','00010','00010','00010','10010','10010','01100'],
'K':['10001','10010','10100','11000','10100','10010','10001'],
'L':['10000','10000','10000','10000','10000','10000','11111'],
'M':['10001','11011','10101','10101','10001','10001','10001'],
'N':['10001','11001','10101','10011','10001','10001','10001'],
'O':['01110','10001','10001','10001','10001','10001','01110'],
'P':['11110','10001','10001','11110','10000','10000','10000'],
'Q':['01110','10001','10001','10001','10101','10010','01101'],
'R':['11110','10001','10001','11110','10100','10010','10001'],
'S':['01111','10000','10000','01110','00001','00001','11110'],
'T':['11111','00100','00100','00100','00100','00100','00100'],
'U':['10001','10001','10001','10001','10001','10001','01110'],
'V':['10001','10001','10001','10001','10001','01010','00100'],
'W':['10001','10001','10001','10101','10101','10101','01010'],
'X':['10001','10001','01010','00100','01010','10001','10001'],
'Y':['10001','10001','01010','00100','00100','00100','00100'],
'Z':['11111','00001','00010','00100','01000','10000','11111'],
'0':['01110','10011','10101','10101','11001','10001','01110'],
'1':['00100','01100','00100','00100','00100','00100','01110'],
'2':['01110','10001','00001','00110','01000','10000','11111'],
'3':['11110','00001','00001','01110','00001','00001','11110'],
'4':['10010','10010','10010','11111','00010','00010','00010'],
'5':['11111','10000','10000','11110','00001','00001','11110'],
'6':['01110','10000','10000','11110','10001','10001','01110'],
'7':['11111','00001','00010','00100','01000','01000','01000'],
'8':['01110','10001','10001','01110','10001','10001','01110'],
'9':['01110','10001','10001','01111','00001','00001','01110'],
' ':['00000']*7, '/':['00001','00001','00010','00100','01000','10000','10000'],
':':['00000','00100','00100','00000','00100','00100','00000'],
'.':['00000','00000','00000','00000','00000','00100','00100'],
'-':['00000','00000','00000','11111','00000','00000','00000'],
}

def pixel_text(x,y,content,scale=7,color='white'):
    out=[]
    for n,ch in enumerate(content.upper()):
        glyph=GLYPHS.get(ch,GLYPHS[' ']); ox=x+n*6*scale
        for r,line in enumerate(glyph):
            for j,b in enumerate(line):
                if b=='1': out.append(rect(ox+j*scale,y+r*scale,scale-0.7,scale-0.7,color))
    return ''.join(out)

OWL=[
'1000000000000001',
'1100000000000011',
'1110000000000111',
'1111110000111111',
'1111111111111111',
'1111111111111111',
'1111101111011111',
'1111000110001111',
'1111101111011111',
'1111111001111111',
'0111111111111110',
'0011111111111100',
'0001111111111000',
'0000111111110000',
'0000001111000000',
]

def owl_art(x,y,scale=11):
    s=''
    for yy,line in enumerate(OWL):
        for xx,v in enumerate(line):
            if v=='1':
                col='mint' if (xx+yy)%8==0 else ('green' if yy<4 else '#315C53')
                s+=rect(x+xx*scale,y+yy*scale,scale-1,scale-1,col)
    for ex in (4,11): s+=rect(x+(ex-1)*scale,y+6*scale,2*scale-1,scale,'red')
    s+=rect(x+7*scale,y+9*scale,2*scale,scale,'amber')
    return s


def avatar_asset():
    """Fetch the public profile picture for embedding; fail visibly, never fake it."""
    url = f'https://github.com/{USER}.png?size=256'
    req=urllib.request.Request(url, headers={'User-Agent':'FuTeCyberArcade/3.0'})
    with urllib.request.urlopen(req,timeout=20) as r:
        raw=r.read(2_000_000)
    with Image.open(io.BytesIO(raw)) as photo:
        photo=photo.convert('RGB').resize((256,256), Image.Resampling.LANCZOS)
        photo.save(ASSET/'avatar.png',format='PNG',optimize=True)
    return base64.b64encode((ASSET/'avatar.png').read_bytes()).decode('ascii')


def hero(avatar_b64=None):
    w,height=1100,420
    s=base(w,height,'/home/fute/init.sh','hero')
    s+=txt(50,85,'> IDENTITY VERIFIED',15,'green',700,spacing=1)
    s+=rect(48,103,4,124,'green')
    s+=pixel_text(77,115,'FURKAN',9,'white')
    s+=pixel_text(77,194,'TECIR',9,'green')
    s+=txt(77,291,'SOFTWARE DEVELOPER // SECURITY ENTHUSIAST',18,'mint',700)
    s+=txt(77,325,'C#  /  C++  /  PYTHON  /  JS  /  JAVA',16,'dim')
    s+=ln(76,343,645,343,'line',2)
    s+=rect(77,357,180,32,'green')+txt(90,378,'[ BUILD ]',15,'bg',700)
    s+=rect(267,357,201,32,'panel2','line')+txt(281,378,'[ RESEARCH ]',15,'white',700)
    s+=txt(553,378,'SYS: READY_',14,'green',700)
    # Right side monitoring panel
    s+=rect(719,66,338,319,'panel2','mint',2)
    s+=rect(720,67,336,35,'panel')+txt(735,90,'[ OWL_SEC // MONITOR ]',15,'mint',700)
    s+=ln(734,105,1041,105,'line')
    if avatar_b64:
        s+=rect(787,119,203,171,'bg','green',2)
        s+=f'<image x="790" y="123" width="197" height="163" preserveAspectRatio="xMidYMid slice" href="data:image/png;base64,{avatar_b64}"/>'
        s+=txt(897,285,'GITHUB AVATAR // SYNCED',11,'green',700,anchor='middle')
    else:
        s+=owl_art(805,120,10.5)
        s+=txt(895,284,'AVATAR: SYNC PENDING',11,'amber',700,anchor='middle')
    s+=ln(737,295,1041,295,'line')
    s+=txt(737,320,'> FIREWALL:',15,'dim')+txt(905,320,'ACTIVE',15,'green',700)
    s+=txt(737,348,'> THREAT LVL:',15,'dim')+txt(905,348,'LOW',15,'mint',700)
    s+=txt(737,373,'< HANDSHAKE COMPLETE />',12,'amber')
    s+='</svg>'
    return s


def projects():
    w,height=1100,606
    s=base(w,height,'/projects/featured.exe','projects')
    s+=txt(50,88,'01 / DEPLOYED PROJECTS',22,'green',700)
    s+=txt(1050,86,'04 ENTRIES LOADED',13,'dim',anchor='end')
    s+=ln(49,101,1050,101,'line',2)
    pos=[(49,118),(557,118),(49,355),(557,355)]
    for i,(proj,(x,y)) in enumerate(zip(CFG['projects'],pos)):
        c=proj['accent']
        s+=rect(x,y,494,217,'panel2','line',2)
        s+=rect(x,y,494,6,c)
        s+=txt(x+23,y+39,'[ '+proj['type']+' ]',13,c,700)
        s+=txt(x+471,y+39,f'0{i+1}',14,'dim',anchor='end')
        s+=txt(x+23,y+85,proj['title'],27,'white',700)
        s+=txt(x+23,y+122,proj['subtitle'],16,'dim')
        s+=ln(x+23,y+149,x+470,y+149,'line')
        s+=rect(x+23,y+165,8,8,c)
        s+=txt(x+41,y+174,proj['stack'],14,c,700)
        s+=txt(x+471,y+190,'OPEN REPO  >>',13,'mint',700,anchor='end')
        s+=rect(x+455,y+19,16,3,c)+rect(x+468,y+19,3,14,c)
    s+='</svg>'
    return s


def project_cards():
    """Each SVG is a standalone clickable README asset; no inert hotspot on one image."""
    names=[]
    for i,proj in enumerate(CFG['projects'],1):
        w,height=535,237
        s=base(w,height,f'/repo/{proj["repo"]}','project card')
        accent=proj['accent']
        s+=rect(20,60,495,158,'panel2','line',2)
        s+=rect(20,60,495,5,accent)
        s+=txt(38,93,f'[{proj["type"]}]',14,accent,700)
        s+=txt(498,94,f'{i:02}',14,'dim',700,anchor='end')
        s+=txt(38,140,proj['title'],26,'white',700)
        s+=txt(38,169,proj['subtitle'],15,'dim')
        s+=ln(38,182,498,182,'line')
        s+=txt(38,204,proj['stack'],13,accent,700)
        s+=txt(498,204,'OPEN REPOSITORY >>',13,'mint',700,anchor='end')
        s+='</svg>'
        name=f'project-{i:02}.svg'
        import xml.etree.ElementTree as ET
        ET.fromstring(s)
        (ASSET/name).write_text(s,encoding='utf-8')
        names.append(name)
    return names


def stats(data,valid):
    w,height=1100,252
    s=base(w,height,'/usr/bin/gh-status','stats')
    s+=txt(49,84,'02 / PUBLIC TELEMETRY',22,'green',700)
    s+=txt(1050,84,'API SYNC: '+('COMPLETE' if valid else 'PENDING'),13,'mint' if valid else 'amber',700,anchor='end')
    items=[('REPOSITORIES',data.get('public_repos','--'),'green'),('REPO STARS',data.get('repo_stars','--'),'mint'),('FOLLOWERS',data.get('followers','--'),'amber'),('FOLLOWING',data.get('following','--'),'red')]
    for i,(label,num,color) in enumerate(items):
        x=48+i*255
        s+=rect(x,105,239,113,'panel2','line',1)
        s+=rect(x+16,122,4,12,color)
        s+=txt(x+30,133,label,14,'dim',700)
        s+=txt(x+20,190,num,43,color,700)
        s+=rect(x+198,190,24,4,color)
    s+='</svg>'
    return s


def fetch(url,token=None,body=None):
    hdr={'User-Agent':'FuTeCyberArcade/3.0 (+GitHub profile generator)','Accept':'application/vnd.github+json'}
    if token: hdr['Authorization']='Bearer '+token
    if body is not None: hdr['Content-Type']='application/json'
    data=json.dumps(body).encode() if body is not None else None
    with urllib.request.urlopen(urllib.request.Request(url,data=data,headers=hdr),timeout=22) as rsp:
        blob=rsp.read().decode('utf-8')
    return json.loads(blob)


def fetch_graph(token):
    if not token: raise RuntimeError('GITHUB_TOKEN is required to fetch contribution data.')
    q='query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}'
    doc=fetch('https://api.github.com/graphql',token,{'query':q,'variables':{'login':USER}})
    if doc.get('errors'):raise RuntimeError(f'GitHub GraphQL failed: {doc["errors"]}')
    weeks=doc['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
    days={d['date']:int(d['contributionCount']) for w in weeks for d in w['contributionDays']}
    if len(days)<300:raise RuntimeError('GitHub graph returned unexpectedly few days')
    return days


def fetch_stats(token):
    person=fetch(f'https://api.github.com/users/{USER}',token)
    stars=0
    for page in range(1,11):
        b=fetch(f'https://api.github.com/users/{USER}/repos?per_page=100&page={page}&type=owner',token)
        stars+=sum(int(repo.get('stargazers_count',0)) for repo in b if not repo.get('fork'))
        if len(b)<100:break
    return {'public_repos':person['public_repos'],'repo_stars':stars,'followers':person['followers'],'following':person['following']}


def demo_grid():
    # The demo deliberately DOES NOT pretend to be the user's real contributions.
    now=dt.datetime.now(dt.timezone.utc).date()
    first=now-dt.timedelta(days=370)
    rng=random.Random(1827)
    return {(first+dt.timedelta(days=i)).isoformat(): rng.choice([0]*75+[1]*10+[2]*9+[4]*4+[7]*2) for i in range(372)}


def positions(days):
    today=dt.datetime.now(dt.timezone.utc).date()
    first=today-dt.timedelta(days=370)
    first-=dt.timedelta(days=(first.weekday()+1)%7)
    return [(first+dt.timedelta(days=w*7+d)).isoformat() for w in range(53) for d in range(7)]


# GIF: no JavaScript, CSS, external SVG/font, or README-side scripting required.
HEX={k:tuple(int(v[i:i+2],16) for i in (1,3,5)) for k,v in P.items()}
MATRIX=['#18292B','#1E3D39','#2C6652','#489B67','#BBFF6C']
COLORS=[tuple(int(v[i:i+2],16) for i in (1,3,5)) for v in MATRIX]


def font(sz=14,bold=False):
    name='/usr/share/fonts/truetype/dejavu/DejaVuSansMono'+('-Bold' if bold else '')+'.ttf'
    try:return ImageFont.truetype(name,sz)
    except OSError:
        try:return ImageFont.truetype('DejaVuSansMono.ttf',sz)
        except OSError:return ImageFont.load_default()


def drawtext(d,pos,t,sz=14,color='dim',bold=False,anchor=None):
    d.text(pos,t,font=font(sz,bold),fill=HEX.get(color,color),anchor=anchor)


def sprite(d,x,y,kind,frame=0,scale=3):
    # Fully original pixel characters, mapped to integer pixel blocks.
    robot=[
        '00022222000','00211111200','02111111120','21101110112',
        '21111111112','21101010112','02111111120','00222222200',
        '00020202000','00220002200','02200000220']
    virus=[
        '10000000001','01000000010','00133333000','00333333300',
        '03303303330','33333333333','03330303330','00333333300',
        '00133333000','01000300010','10000000001']
    mat=virus if kind=='virus' else robot
    pal={'0':None,'1':HEX['mint'] if kind=='robot' else HEX['red'],
         '2':HEX['green'] if kind=='robot' else HEX['red'],
         '3':HEX['red'],}
    if kind=='robot': pal['1']=(30,74,71)
    else:pal['1']=HEX['amber']
    for yy,row in enumerate(mat):
        for xx,val in enumerate(row):
            if val=='0':continue
            dx=xx*scale;dy=yy*scale
            if (kind=='virus' and frame%2 and (xx==0 or xx==10)):dy+=2
            d.rectangle((int(x+dx),int(y+dy),int(x+dx+scale-1),int(y+dy+scale-1)),fill=pal[val])
    if kind=='robot':
        eyey=y+12
        d.rectangle((x+9,eyey,x+14,eyey+4),fill=HEX['amber'])
        d.rectangle((x+21,eyey,x+26,eyey+4),fill=HEX['amber'])
    else:
        d.rectangle((x+9,y+12,x+13,y+15),fill=HEX['bg'])
        d.rectangle((x+22,y+12,x+26,y+15),fill=HEX['bg'])


def static_activity(days,demo):
    W,H=1100,340
    im=Image.new('RGB',(W,H),HEX['bg']);d=ImageDraw.Draw(im)
    d.rectangle((2,2,W-3,H-3),outline=HEX['line'],width=2)
    d.rectangle((13,13,W-14,47),fill=HEX['panel'])
    for k in range(3):d.rectangle((29+k*16,26,36+k*16,33),fill=HEX['green'])
    drawtext(d,(94,23),'/var/log/contribution-defense.gif',13,'dim',True)
    drawtext(d,(1070,23),'FUTE_OS / LIVE LOOP',12,'mint',True,'ra')
    d.line((13,47,W-13,47),fill=HEX['line'],width=2)
    drawtext(d,(50,70),'03 / CONTRIBUTION DEFENSE MATRIX',21,'green',True)
    drawtext(d,(1050,75),'[ ROBOT X VIRUS ]',13,'amber',True,'ra')
    dates=positions(days)
    for col in range(53):
        for row in range(7):
            key=dates[col*7+row]; count=days.get(key,0)
            lev=0 if count<=0 else 1 if count<2 else 2 if count<5 else 3 if count<10 else 4
            x=91+col*17; y=105+row*17
            d.rectangle((x,y,x+12,y+12),fill=COLORS[lev])
            if lev: d.point((x+2,y+2),fill=HEX['mint'])
    d.line((47,251,1052,251),fill=HEX['line'],width=2)
    drawtext(d,(53,271),'BOT_01 : PATROLLING',14,'mint',True)
    drawtext(d,(352,271),'BOT_02 : STANDBY',14,'green',True)
    drawtext(d,(639,271),'THREAT : DETECTED',14,'red',True)
    drawtext(d,(53,308),'CONTRIBUTION DATA : '+('DEMO / NOT LIVE' if demo else 'LIVE / GITHUB API'),13,'amber' if demo else 'green',True)
    drawtext(d,(1050,308),'[ PURGE • REBOOT • REPEAT ]',13,'dim',True,'ra')
    return im


def build_activity(days,demo,frame_count=64):
    output=ASSET/'activity.gif'
    base_img=static_activity(days,demo)
    frames=[]
    for i in range(frame_count):
        p=i/frame_count
        im=base_img.copy();d=ImageDraw.Draw(im)
        # Bots patrol cells, virus crosses in the opposite direction.
        rx=int(89+830*p); ry=int(128+31*math.sin(p*math.tau*2))
        r2x=int(917-790*p); r2y=int(192-25*math.cos(p*math.tau*1.8))
        vx=int(916-820*p); vy=int(150+35*math.cos(p*math.tau*2))
        # Retro motion trail and vulnerability signal.
        for off in [10,24,38]:
            if rx-off>=91:d.rectangle((rx-off,ry+15,rx-off+5,ry+17),fill=HEX['line'])
        sprite(d,rx,ry,'robot',i,3)
        sprite(d,r2x,r2y,'robot',i+1,2)
        sprite(d,vx,vy,'virus',i,3)
        if 24<=i<32:
            d.line((rx+30,ry+15,vx+6,vy+16),fill=HEX['amber'],width=2)
            for j in range(7):
                theta=j*math.tau/7+i/3
                x=vx+17+math.cos(theta)*(i-23)*4
                y=vy+15+math.sin(theta)*(i-23)*4
                d.rectangle((x,y,x+3,y+3),fill=HEX['red'] if j%2 else HEX['amber'])
            d.rectangle((770,85,1050,99),fill=HEX['panel'])
            drawtext(d,(780,85),'!! THREAT QUARANTINED !!',12,'red',True)
        # Blinking console cursor and scanner lines
        if i%8<5:d.rectangle((1028,324,1041,327),fill=HEX['green'])
        d.rectangle((90+(i*13)%900,237,93+(i*13)%900,242),fill=HEX['mint'])
        # Quantize each frame into shared palette (constant appearance, lighter GIF)
        if not frames:
            master=im.quantize(colors=64,method=Image.Quantize.MEDIANCUT)
            frames.append(master)
        else:frames.append(im.quantize(palette=frames[0],dither=Image.Dither.NONE))
    frames[0].save(output,save_all=True,append_images=frames[1:],duration=125,loop=0,optimize=True,disposal=2)
    poster=frames[0].convert('RGB'); poster.save(ASSET/'activity-poster.png',optimize=True)
    return len(frames)


def main():
    a=argparse.ArgumentParser()
    mode=a.add_mutually_exclusive_group(required=True)
    mode.add_argument('--demo',action='store_true',help='Use clearly labeled synthetic data for visual preview')
    mode.add_argument('--live',action='store_true',help='Use real data from the GitHub GraphQL and REST APIs')
    args=a.parse_args()
    ASSET.mkdir(exist_ok=True)
    if args.demo:
        days=demo_grid();data={};valid=False
    else:
        token=os.environ.get('GITHUB_TOKEN')
        # Do not silently publish invented graph data when GitHub API is down.
        days=fetch_graph(token)
        data=fetch_stats(token)
        valid=True
    try:
        avatar_b64=avatar_asset()
    except Exception as ex:
        print(f'WARNING: avatar could not be downloaded: {ex}')
        avatar_b64=None
    project_cards()
    for name,content in [('hero.svg',hero(avatar_b64)),('stats.svg',stats(data,valid))]:
        import xml.etree.ElementTree as ET
        ET.fromstring(content)
        (ASSET/name).write_text(content,encoding='utf-8')
    n=build_activity(days,args.demo)
    print(f'Generated hero, four project cards, stats and {n}-frame animated GIF. GitHub data: {"LIVE" if valid else "DEMO"}')

if __name__=='__main__':main()
