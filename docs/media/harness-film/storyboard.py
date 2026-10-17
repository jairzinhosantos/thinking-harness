"""Build three editable SVG keyframes and their review gallery. No video generation."""
from pathlib import Path
from html import escape

HERE = Path(__file__).resolve().parent
BG = '#0b1118'
INK = '#edf3f5'
SOFT = '#9cabb7'
CYAN = '#85d6d1'
AMBER = '#d7b789'


def text(x, y, value, size=24, color=INK, weight=400, anchor='start', mono=False, spacing=0):
    font = 'Courier New, monospace' if mono else 'Arial, Helvetica, sans-serif'
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="{font}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" letter-spacing="{spacing}">{escape(value)}</text>'


def line(x1, y1, x2, y2, color='#425362', width=1.5, dash=None):
    return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" stroke-width="{width}" fill="none"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'


def path(d, color=CYAN, arrow=False, dash=False, width=2):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"'+(' marker-end="url(#arrow)"' if arrow else '')+(' stroke-dasharray="6 7"' if dash else '')+'/>'


def rect(x,y,w,h,fill='#131e29',stroke='#344552',radius=4):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>'


def points(coords):
    return ' '.join(f'{x:.1f},{y:.1f}' for x,y in coords)


def box(cx,cy,u,v,w,d,z,h,accent=CYAN,top='#223746',scale=1):
    def p(a,b,c):return (cx+(a-b)*.866*scale,cy+((a+b)*.38-c)*scale)
    a,b,c,e=[p(*v) for v in [(u,v,z+h),(u+w,v,z+h),(u+w,v+d,z+h),(u,v+d,z+h)]]
    b0,c0,e0=[p(*v) for v in [(u+w,v,z),(u+w,v+d,z),(u,v+d,z)]]
    return (f'<polygon points="{points([e,c,c0,e0])}" fill="#111d27" stroke="#405363"/>'
            f'<polygon points="{points([b,c,c0,b0])}" fill="#192833" stroke="#405363"/>'
            f'<polygon points="{points([a,b,c,e])}" fill="{top}" stroke="{accent}" stroke-opacity=".6"/>'
            +line(*a,*b,accent,1.5))


def assembly(cx,cy,scale=1,explode=False,accent=CYAN):
    result=box(cx,cy,-270,-230,540,460,-35,25,accent,'#12212c',scale)
    for u,v,w,d in [(-238,-198,180,120),(58,-198,180,120),(-238,78,180,120),(58,78,180,120)]:
        z=75 if explode else 12
        if explode:
            x=cx+(u-v)*.866*scale;y=cy+(u+v)*.38*scale
            result+=line(x,y,x,y-z*scale,'#486071',1.2,'4 7')
        result+=box(cx,cy,u,v,w,d,z,32,accent,'#263d49',scale)
        result+=box(cx,cy,u+14,v+14,w-28,d-28,z+32,3,accent,'#1c303d',scale)
    result+=box(cx,cy,-76,-70,152,140,28,87,'#c5d3de','#344857',scale)
    result+=box(cx,cy,-56,-50,112,100,115,6,'#c5d3de','#415866',scale)
    return result


def label(x,y,name,sub,anchor='start'):
    return text(x,y,name,20,CYAN,500,anchor,True,1.5)+text(x,y+29,sub,19,SOFT,400,anchor)


def base(number,time,title_lines,description,art):
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">
<title>Thinking Harness: storyboard frame {number}</title>
<desc>{escape(' '.join(title_lines)+' '+description)}</desc>
<defs>
 <radialGradient id="haze"><stop stop-color="#203541" stop-opacity=".48"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></radialGradient>
 <pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse"><path d="M48 0H0V48" fill="none" stroke="#a9c4cf" stroke-opacity=".035"/></pattern>
 <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1L9 5L0 9" fill="none" stroke="{CYAN}" stroke-width="1.4"/></marker>
</defs>
<rect width="1920" height="1080" fill="{BG}"/>
<ellipse cx="1280" cy="520" rx="780" ry="570" fill="url(#haze)"/>
<rect x="720" y="150" width="1120" height="720" fill="url(#grid)"/>
'''
    svg+=text(88,77,'THINKING HARNESS',24,INK,500,spacing=4)+text(1832,77,'RESEARCH FILM / STORYBOARD',17,SOFT,400,'end',True,1)
    svg+=line(88,110,1832,110,'#30404d')
    svg+=text(88,202,f'{number:02d} / '+['ASSEMBLY','SELECTION','RECURSION'][number-1],18,CYAN,400,mono=True,spacing=2)
    for i,s in enumerate(title_lines):svg+=text(82,310+i*90,s,76,INK,500,spacing=-2.5)
    for i,s in enumerate(description.split('|')):svg+=text(88,660+i*35,s,23,SOFT)
    svg+=text(88,842,time,17,SOFT,mono=True,spacing=2)
    svg+=art
    svg+=line(88,932,1832,932,'#30404d')
    svg+=text(88,981,'FIXED',15,SOFT,mono=True,spacing=1.5)
    svg+=text(170,981,'Model  /  Objective  /  External evaluator',20,INK)
    svg+=text(960,981,'MUTABLE',15,CYAN,mono=True,spacing=1.5)+text(1070,981,'Harness components',20,INK)
    svg+=text(1832,1040,'CONCEPTUAL SEQUENCE / NOT MEASURED RESULTS',15,SOFT,400,'end',True,1)
    return svg+'</svg>'


def first():
    art='<ellipse cx="1260" cy="707" rx="470" ry="116" fill="#050b11" opacity=".65"/>'
    art+=assembly(1260,650,1.02,True)
    art+=text(1260,321,'H₀',54,INK,400,'middle')
    art+=text(1260,354,'INITIAL ASSEMBLY',16,SOFT,400,'middle',True,2)
    art+=path('M1065 452 L985 397 H833','#49616f')+label(815,351,'POLICY','Instructions and constraints')
    art+=path('M1438 455 L1512 397 H1760','#49616f')+label(1770,351,'CONTEXT','Relevant task information','end')
    art+=path('M1002 628 H844 V691','#49616f')+label(815,738,'TOOLS','Available actions')
    art+=path('M1505 635 H1703 V691','#49616f')+label(1770,738,'CONTROL','Execution and retries','end')
    art+=text(1260,548,'MODEL',18,INK,500,'middle',True,1)
    art+=text(1260,907,'Separate parts. One executable system.',22,SOFT,400,'middle')
    return base(1,'KEYFRAME 00:08',['A system','around','the model.'],'The harness connects instructions,|context, tools and execution.|Its parts can be studied and changed.',art)


def second():
    art=text(968,235,'CANDIDATE ASSEMBLIES',16,SOFT,400,'middle',True,2)
    for y,name,accent in [(374,'H₁-A',AMBER),(574,'H₁-B','#697782'),(774,'H₁-C',CYAN)]:
        art+=assembly(957,y,.35,False,accent)
        art+=box(957,y,-238,-198,180,120,75,25,accent,'#304549',.35)
        art+=text(795,y-5,name,22,accent,500,'middle',True)
        state='RETAIN' if name=='H₁-C' else 'REJECT'
        art+=text(795,y+21,state,12,accent,400,'middle',True)
    art+=path('M1124 365 H1190 V535 H1240',AMBER,False,True)
    art+=path('M1124 565 H1240','#697782',False,True)
    art+=path('M1124 765 H1190 V595 H1240',CYAN,True)
    art+=rect(1240,458,240,214,'#101b25','#65818b')
    art+=text(1360,501,'EVALUATE',21,INK,500,'middle',True,1)
    art+=line(1265,521,1455,521,'#374d5a')
    for i,label_ in enumerate(['Task outcome','Constraint checks','Bounded cost']):art+=text(1265,558+i*34,label_,20,SOFT)
    art+=path('M1480 565 H1560',CYAN,True)
    art+=assembly(1695,604,.30,False,CYAN)
    art+=text(1695,444,'H₁',48,CYAN,400,'middle')
    art+=text(1695,476,'RETAINED',16,CYAN,400,'middle',True,1)
    art+=text(1695,720,'Illustrative selection',18,SOFT,400,'middle')
    art+=text(958,900,'Variants can be rejected.',21,SOFT,400,'middle')
    return base(2,'KEYFRAME 00:25',['Propose.','Evaluate.','Retain.'],'Candidate parts are tested against|a fixed objective. A change is kept|only when it meets the criteria.',art)


def third():
    art=text(1000,283,'SELECTED HARNESS',16,CYAN,400,'middle',True,2)+text(1000,339,'H₁',54,CYAN,400,'middle')
    art+=text(1590,283,'SUCCESSOR CANDIDATE',16,AMBER,400,'middle',True,2)+text(1590,339,'H₂',54,AMBER,400,'middle')
    art+=assembly(1000,555,.52,False,CYAN)
    art+=assembly(1590,555,.52,True,AMBER)
    art+=path('M1210 505 H1360',CYAN,True)
    art+=text(1285,457,'CONSTRUCTS',15,CYAN,400,'middle',True,1)
    art+=text(1000,713,'The current harness participates',19,INK,400,'middle')
    art+=text(1000,741,'in building the next version.',19,SOFT,400,'middle')
    art+=path('M1590 662 V777',AMBER,False,True)
    art+=rect(1440,777,300,76,'#111d26','#627a86')
    art+=text(1590,823,'EXTERNAL EVALUATION',18,INK,400,'middle',True)
    art+=path('M1440 815 H1280 V868 H1000 V777',CYAN,True,True)
    art+=text(1240,900,'PROMOTE H₂ ONLY IF ACCEPTED',15,SOFT,400,'middle',True,1)
    return base(3,'KEYFRAME 00:38',['Improve how','the next system','is built.'],'The selected harness helps construct|its successor. The evaluator stays|outside the changing system.',art)


def main():
    frames=[('01-assembly',first()),('02-selection',second()),('03-recursion',third())]
    for name,svg in frames:(HERE/(name+'.svg')).write_text(svg)
    cards=''.join(f'<figure><img src="{name}.svg" alt="{name}"/><figcaption>{name.replace("-", " ")}</figcaption></figure>' for name,_ in frames)
    (HERE/'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Thinking Harness | Storyboard</title><style>body{margin:0;background:#080d13;color:#dfe8eb;font-family:Arial,sans-serif}header,main{max-width:1440px;margin:auto;padding:32px}h1{font-size:30px;font-weight:500}p{color:#9cabb7;line-height:1.6}figure{margin:0 0 40px}img{display:block;width:100%;border:1px solid #273844}figcaption{font:14px monospace;color:#9cabb7;margin:12px 0}a{color:#85d6d1}</style><header><h1>Thinking Harness / Research film</h1><p>Three keyframes for a conceptual sequence. The visuals illustrate a research direction, not results from the current pilot.</p><a href="storyboard.md">Read the script</a></header><main>'''+cards+'</main></html>')


if __name__=='__main__':main()
