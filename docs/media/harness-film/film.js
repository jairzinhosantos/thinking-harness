/* Deterministic motion design. The sequence is conceptual, not experiment output. */
'use strict';
const canvas = document.querySelector('#film');
const ctx = canvas.getContext('2d');
const C = {bg:'#0b1118', ink:'#edf3f5', soft:'#9cabb7', line:'#405765', cyan:'#85d6d1', amber:'#d7b789'};
const clamp = x => Math.max(0, Math.min(1, x));
const ease = x => { x=clamp(x); return x*x*(3-2*x); };
const phase = (t,a,b) => ease((t-a)/(b-a));
const mix = (a,b,p) => a+(b-a)*p;
function alpha(a, fn) { ctx.save(); ctx.globalAlpha*=clamp(a); fn(); ctx.restore(); }
function text(x,y,s,size=24,color=C.ink,align='left',mono=false) {
  ctx.fillStyle=color; ctx.font=`${size}px ${mono?'"Courier New", monospace':'Arial, sans-serif'}`;
  ctx.textAlign=align; ctx.fillText(s,x,y);
}
function stroke(points,color=C.line,width=1.5,dash=[]) {
  ctx.beginPath(); points.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));
  ctx.strokeStyle=color; ctx.lineWidth=width; ctx.setLineDash(dash); ctx.stroke(); ctx.setLineDash([]);
}
function route(points,p=1,color=C.cyan,width=2.3) {
  const lengths=points.slice(1).map((v,i)=>Math.hypot(v[0]-points[i][0],v[1]-points[i][1]));
  let remaining=lengths.reduce((a,b)=>a+b,0)*clamp(p), path=[points[0]];
  for(let i=0;i<lengths.length && remaining>0;i++) {
    const f=Math.min(1,remaining/lengths[i]);
    path.push([mix(points[i][0],points[i+1][0],f),mix(points[i][1],points[i+1][1],f)]);
    remaining-=lengths[i];
  }
  if(path.length>1) {
    stroke(path,color,width);
    const [x,y]=path[path.length-1]; ctx.fillStyle=color;ctx.beginPath();ctx.arc(x,y,3.5,0,Math.PI*2);ctx.fill();
  }
}
function polygon(points,fill,line=C.line) {
  ctx.beginPath(); points.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.closePath();
  ctx.fillStyle=fill;ctx.fill();ctx.strokeStyle=line;ctx.lineWidth=1;ctx.stroke();
}
function panel(x,y,w,h) {
  ctx.fillStyle='#101c26';ctx.fillRect(x,y,w,h);ctx.strokeStyle='#54717f';ctx.lineWidth=1;ctx.strokeRect(x,y,w,h);
}
function project(cx,cy,s,u,v,z) { return [cx+(u-v)*.866*s,cy+((u+v)*.38-z)*s]; }
function box(cx,cy,s,u,v,w,d,z,h,color=C.cyan,fill='#253d48') {
  const p=(a,b,c)=>project(cx,cy,s,a,b,c);
  const a=p(u,v,z+h),b=p(u+w,v,z+h),c=p(u+w,v+d,z+h),e=p(u,v+d,z+h);
  polygon([e,c,p(u+w,v+d,z),p(u,v+d,z)],'#111e28');
  polygon([b,c,p(u+w,v+d,z),p(u+w,v,z)],'#1a2b36');
  polygon([a,b,c,e],fill,color); stroke([a,b],color,1.8);
}
const slots=[[-238,-198],[58,-198],[-238,78],[58,78]];
function modulePart(cx,cy,s,u,v,z,variant=0,color=C.cyan) {
  box(cx,cy,s,u,v,180,120,z,26,color);
  if(variant===0) {
    box(cx,cy,s,u+12,v+12,156,96,z+26,4,color,'#1b303b');
    const p=(a,b)=>project(cx,cy,s,u+a,v+b,z+31);
    stroke([p(36,32),p(140,32)],color,1.2);
    stroke([p(36,48),p(100,48)],'#617f8a',1.2);
  } else {
    // Split, routed subcomponents make a replacement visibly different from the seed.
    const n=Math.min(4,variant+1);
    for(let i=0;i<n;i++) box(cx,cy,s,u+12+i*(156/n),v+14,156/n-8,64,z+26,7,color,'#304b55');
    const p=(a,b)=>project(cx,cy,s,u+a,v+b,z+28);
    stroke([p(25,92),p(150,92),p(150,78)],color,1.7);
    for(let i=0;i<n;i++) stroke([p(30+i*(156/n),78),p(30+i*(156/n),92)],color,1.7);
  }
}
function assembly(cx,cy,s,{drop=[0,0,0,0],variant=0,control=0,policyColor=C.cyan,visible=[1,1,1,1],core=1}={}) {
  alpha(.5,()=>{ctx.fillStyle='#040a10';ctx.beginPath();ctx.ellipse(cx,cy+65*s,460*s,110*s,0,0,Math.PI*2);ctx.fill();});
  box(cx,cy,s,-270,-230,540,460,-35,25,'#537784','#12212c');
  // Back components, central fixed model, front components: stable depth order.
  for(const i of [0,1,2]) alpha(visible[i],()=>modulePart(cx,cy,s,...slots[i],12+drop[i],i===0?variant:0,i===0?policyColor:C.cyan));
  alpha(core,()=>{
    box(cx,cy,s,-76,-70,152,140,28,87,'#bdced8','#344957');
    box(cx,cy,s,-56,-50,112,100,115,6,'#bdced8','#415967');
    if(s>.65) text(cx,cy-97*s,'MODEL',17,C.ink,'center',true);
  });
  alpha(visible[3],()=>modulePart(cx,cy,s,...slots[3],12+drop[3],control,C.cyan));
}
function backdrop(t) {
  ctx.fillStyle=C.bg;ctx.fillRect(0,0,1920,1080);
  const haze=ctx.createRadialGradient(1280,520,20,1280,520,760);
  haze.addColorStop(0,'#172b36');haze.addColorStop(1,C.bg);ctx.fillStyle=haze;ctx.fillRect(640,130,1280,790);
  alpha(.055,()=>{for(let x=720;x<1840;x+=48)stroke([[x,150],[x,900]],'#a9c4cf',.7);for(let y=150;y<900;y+=48)stroke([[720,y],[1840,y]],'#a9c4cf',.7);});
  text(88,77,'T H I N K I N G   H A R N E S S',24);text(1832,77,'RESEARCH FILM',17,C.soft,'right',true);
  stroke([[88,110],[1832,110]],'#30404d');stroke([[88,932],[1832,932]],'#30404d');
  text(88,981,'FIXED',15,C.soft,'left',true);text(170,981,'Model / Objective / External evaluator',20);
  text(990,981,'MUTABLE',15,C.cyan,'left',true);text(1100,981,'Harness components',20);
  text(1832,1040,'CONCEPTUAL SEQUENCE / NOT MEASURED RESULTS',15,C.soft,'right',true);
  stroke([[88,1064],[1832,1064]],'#21313b',2);stroke([[88,1064],[88+1744*clamp(t/45),1064]],C.cyan,2);
}
function heading(n,tag,lines,body) {
  text(88,202,`${n} / ${tag}`,18,C.cyan,'left',true);
  lines.forEach((s,i)=>text(82,310+i*90,s,76));body.forEach((s,i)=>text(88,660+i*35,s,23,C.soft));
}
function caption(s,color=C.soft) { text(1270,899,s,22,color,'center'); }
function sceneAssembly(t) {
  heading('01','ASSEMBLY',['A system','around','the model.'],['Instructions, context, tools and control.','Separate parts form an executable system.']);
  const ready=phase(t,1,2.4);
  const drop=slots.map((_,i)=>120*(1-phase(t,2.1+i*.9,5.6+i*.9)));
  // A visible extraction starts the transition from the initial system to candidate parts.
  drop[0]+=110*phase(t,11.7,13.2);
  alpha(ready,()=>assembly(1260,650,1.0,{drop,visible:slots.map((_,i)=>phase(t,1.8+i*.65,3+i*.65))}));
  alpha(phase(t,2,3),()=>{
    text(1260,278,'H₀',50,C.ink,'center');text(1260,312,'INITIAL ASSEMBLY',16,C.soft,'center',true);
  });
  const labels=[['POLICY',815,400,[[1070,460],[990,435],[835,435]]],['CONTEXT',1750,400,[[1440,460],[1510,435],[1750,435]]],['TOOLS',815,770,[[1000,640],[840,640],[840,725]]],['CONTROL',1750,770,[[1510,640],[1720,640],[1720,725]]]];
  labels.forEach(([s,x,y,p],i)=>alpha(phase(t,4.3+i*.65,5.1+i*.65),()=>{text(x,y,s,19,C.cyan,i%2?'right':'left',true);stroke(p,'#537180');}));
  caption(t<10.8?'Assemble the harness.': 'Lift one component. Keep the rest fixed.',t<10.8?C.soft:C.amber);
  alpha(phase(t,11.7,12.5),()=>text(1260,350,'POLICY: OPEN FOR REVISION',16,C.amber,'center',true));
}
function sceneSelection(t) {
  heading('02','SELECTION',['Propose.','Evaluate.','Retain.'],['Replace one component.','Compare against the same criteria.','Keep a change only if it qualifies.']);
  const starts=[15.2,16.2,17.2], tests=[19,21.2,23.4], ys=[365,565,765];
  text(955,235,'CANDIDATE ASSEMBLIES',16,C.soft,'center',true);
  for(let i=0;i<3;i++) {
    const a=phase(t,starts[i]-.8,starts[i]);
    const tested=phase(t,tests[i]+.9,tests[i]+1.3);
    const rejected=i<2;
    alpha(a*(rejected?mix(1,.28,tested):1),()=>{
      assembly(955,ys[i],.35,{drop:[145*(1-phase(t,starts[i],starts[i]+1.4)),0,0,0],variant:i+1,policyColor:i===2&&tested?C.cyan:C.amber});
      text(790,ys[i]-10,['A','B','C'][i],23,i===2&&tested?C.cyan:C.amber,'center',true);
    });
    alpha(a,()=>{
      route([[1120,ys[i]],[1190,ys[i]],[1190,535+i*30],[1240,535+i*30]],phase(t,tests[i],tests[i]+.9),i===2?C.cyan:C.amber);
      alpha(tested,()=>text(790,ys[i]+19,rejected?'REJECT':'RETAIN',13,rejected?C.soft:C.cyan,'center',true));
    });
  }
  panel(1240,458,240,214);text(1360,500,'EVALUATE',21,C.ink,'center',true);stroke([[1265,521],[1455,521]]);
  ['Task behavior','Constraints','Bounded cost'].forEach((s,i)=>text(1260,558+i*34,s,20,C.soft));
  const selected=phase(t,24.7,25.4);
  route([[1480,565],[1560,565]],selected);
  alpha(selected,()=>{
    assembly(1695,604,.30,{variant:3,drop:[70*(1-phase(t,25.2,26.3)),0,0,0]});
    text(1695,444,'H₁',48,C.cyan,'center');text(1695,478,'RETAINED',16,C.cyan,'center',true);
    text(1695,730,'Updated policy',20,C.cyan,'center');
  });
  caption(t<19?'Different parts. The same fixed model.':t<24.7?'Evaluate each candidate before selection.':'Retain the qualifying configuration.');
}
function sceneRecursion(t) {
  heading('03','RECURSION',['Improve how','the next system','is built.'],['The selected harness participates','in constructing its successor.','Evaluation remains external.']);
  const construction=phase(t,29.2,31), accepted=phase(t,36.3,36.9), promotion=phase(t,37.7,39.1);
  const predecessor=1-phase(t,37.1,37.7);
  const successorX=mix(1590,1000,promotion), successorY=mix(555,555,promotion);
  alpha(predecessor,()=>{
    assembly(1000,555,.52,{variant:3});
    text(1000,283,'SELECTED HARNESS',16,C.cyan,'center',true);text(1000,339,'H₁',54,C.cyan,'center');
  });
  alpha(predecessor,()=>{
    route([[1210,505],[1360,505]],construction);
    text(1285,457,'CONSTRUCTS',15,C.cyan,'center',true);
  });
  const appear=phase(t,30.4,31.2);
  alpha(appear,()=>{
    const drops=slots.map((_,i)=>140*(1-phase(t,31+i*.45,32.5+i*.45)));
    assembly(successorX,successorY,.52,{variant:3,control:2,drop:drops,visible:slots.map((_,i)=>phase(t,30.8+i*.35,31.5+i*.35)),policyColor:accepted?C.cyan:C.amber});
    text(successorX,283,accepted?'SELECTED HARNESS':'SUCCESSOR CANDIDATE',16,accepted?C.cyan:C.amber,'center',true);
    text(successorX,339,'H₂',54,accepted?C.cyan:C.amber,'center');
  });
  alpha(predecessor,()=>{
    text(1000,718,'Constructs a changed configuration',19,C.soft,'center');
    alpha(appear,()=>text(1590,718,'Policy retained. Control revised.',19,C.amber,'center'));
    route([[1590,665],[1590,777]],phase(t,34,34.9),C.amber);
  });
  panel(1440,777,300,76);text(1590,822,'EXTERNAL EVALUATION',18,C.ink,'center',true);
  route([[1440,815],[1280,815],[1280,868],[1000,868],[1000,777]],phase(t,35.2,37));
  alpha(accepted*(1-promotion),()=>text(1590,749,'ACCEPTED',16,C.cyan,'center',true));
  alpha(phase(t,38.7,39.3),()=>{
    text(1000,718,'Now participates in the next construction',19,C.cyan,'center');
    route([[1210,505],[1360,505]],phase(t,38.6,39.6));
    text(1285,457,'CONSTRUCTS',15,C.cyan,'center',true);
    alpha(phase(t,38.7,39.8)*.45,()=>assembly(1590,555,.52,{variant:3,control:3,drop:[60,80,60,100]}));
    text(1590,283,'NEXT CANDIDATE',16,C.soft,'center',true);text(1590,339,'H₃',54,C.soft,'center');
  });
  caption(t<35?'Change the harness. Preserve the evaluator.':t<37.3?'Promote only after external evaluation.':'The accepted version takes the construction role.',t>=35?C.cyan:C.soft);
}
function endcard(t) {
  alpha(.2,()=>{
    assembly(1040,635,.61,{variant:3});assembly(1630,635,.61,{variant:3,control:2});
    route([[1290,590],[1390,590]],1);
  });
  text(100,330,'THINKING HARNESS',67);
  text(100,454,'Can a harness improve',58);
  text(100,528,'how it improves?',58);
  text(104,655,'Applied research on agent harnesses.',24,C.soft);
  text(104,702,'Assemble. Evaluate. Iterate.',23,C.cyan);
  text(104,840,'github.com/jairzinhosantos/thinking-harness',22,C.soft,'left',true);
}
function blend(t,a,b,prev,next) {
  // Fade through the shared surface so successive headings never overlap.
  const span=b-a;
  alpha(1-phase(t,a,a+span*.45),()=>prev(t));
  alpha(phase(t,a+span*.5,b),()=>next(t));
}
window.drawFrame = function(t) {
  t=Math.max(0,Math.min(45,t));ctx.globalAlpha=1;backdrop(t);
  if(t<14) alpha(phase(t,0,.8),()=>sceneAssembly(t));
  else if(t<15) blend(t,14,15,sceneAssembly,sceneSelection);
  else if(t<27) sceneSelection(t);
  else if(t<28) blend(t,27,28,sceneSelection,sceneRecursion);
  else if(t<40) sceneRecursion(t);
  else if(t<41) blend(t,40,41,sceneRecursion,endcard);
  else endcard(t);
  document.querySelector('#timeline').value=t;
  document.querySelector('#time').textContent=`00:${Math.floor(t).toString().padStart(2,'0')} / 00:45`;
};
let playing=false, offset=0, start=0;
const play=document.querySelector('#play');
play.onclick=()=>{
  playing=!playing;play.textContent=playing?'Pause':'Play';
  if(playing){if(offset>=45)offset=0;start=performance.now();requestAnimationFrame(tick);}
  else offset=Number(document.querySelector('#timeline').value);
};
function tick(now) {
  if(!playing)return;
  const t=offset+(now-start)/1000;window.drawFrame(t);
  if(t>=45){playing=false;offset=45;play.textContent='Replay';return;}
  requestAnimationFrame(tick);
}
document.querySelector('#timeline').oninput=e=>{
  playing=false;play.textContent='Play';offset=Number(e.target.value);window.drawFrame(offset);
};
window.drawFrame(0);
