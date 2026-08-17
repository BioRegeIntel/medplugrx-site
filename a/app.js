
const nav=document.getElementById('nav'),prog=document.getElementById('prog'),cur=document.getElementById('cursor');
addEventListener('scroll',()=>{const h=document.documentElement;
if(prog)prog.style.width=(h.scrollTop/(h.scrollHeight-h.clientHeight)*100)+'%';
if(nav)nav.classList.toggle('on',h.scrollTop>60);},{passive:true});
addEventListener('mousemove',e=>{if(!cur)return;cur.style.opacity='1';
cur.style.transform='translate('+e.clientX+'px,'+e.clientY+'px)';},{passive:true});
const bg=document.getElementById('burger'),ul=document.getElementById('menu');
if(bg)bg.onclick=()=>ul.classList.toggle('open');

const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:0.02,rootMargin:'0px 0px -6% 0px'});
document.querySelectorAll('.rv,.lit,.cin,.plugsec').forEach(el=>io.observe(el));
/* clip-path can zero out an element's intersection rect in Chromium, so IO may
   never fire for .cin — this guarantees the reveal by scroll position. */
function sweep(){document.querySelectorAll('.rv:not(.in),.lit:not(.in),.cin:not(.in),.plugsec:not(.in),.stag:not(.in)').forEach(e=>{
 const r=e.getBoundingClientRect();if(r.top<innerHeight*0.96&&r.bottom>-40)e.classList.add('in');});}
addEventListener('scroll',sweep,{passive:true});addEventListener('resize',sweep);
sweep();setTimeout(sweep,600);setTimeout(sweep,3600);

document.querySelectorAll('h2.serif,h1.serif').forEach(h=>{
 const kids=[...h.childNodes];
 h.innerHTML=kids.map(n=>{
   if(n.nodeType===3) return n.textContent.split(/(\s+)/).map(word=>{
     if(word==='')return '';
     if(/^\s+$/.test(word))return ' ';
     return '<span class="w">'+[...word].map(c=>'<span>'+c+'</span>').join('')+'</span>';
   }).join('');
   if(n.nodeName==='BR') return '<br>';
   return '<span class="w"><span>'+n.outerHTML+'</span></span>';
 }).join('');
 h.classList.add('stag');
 [...h.querySelectorAll('.w>span')].forEach((sp,i)=>sp.style.transitionDelay=(i*0.020)+'s');
 io.observe(h);
});

const cio=new IntersectionObserver(es=>es.forEach(e=>{if(!e.isIntersecting)return;cio.unobserve(e.target);
const el=e.target,to=+el.dataset.to;let t0=null;el.textContent='0';
const st=t=>{if(!t0)t0=t;const p=Math.min((t-t0)/1700,1);
el.textContent=Math.floor((1-Math.pow(1-p,3))*to);if(p<1)requestAnimationFrame(st)};
requestAnimationFrame(st)}),{threshold:.5});
document.querySelectorAll('.cnt').forEach(el=>cio.observe(el));

const scz=[...document.querySelectorAll('.bg')];
addEventListener('scroll',()=>{scz.forEach(el=>{
 const host=el.parentElement.getBoundingClientRect();
 if(host.bottom<0||host.top>innerHeight)return;
 const t=(host.top+host.height/2-innerHeight/2)/innerHeight;
 el.style.transform='translateY('+(t*-64)+'px) scale('+(1.06+Math.abs(t)*0.11)+')';
});},{passive:true});

document.querySelectorAll('.tilt').forEach(c=>{
c.addEventListener('mousemove',e=>{const r=c.getBoundingClientRect();
const x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;
c.style.transform='rotateY('+(x*7)+'deg) rotateX('+(-y*7)+'deg) translateY(-7px)';});
c.addEventListener('mouseleave',()=>{c.style.transform=''});});

/* hero video carousel */
const hv=[...document.querySelectorAll('.hstack video')],dots=[...document.querySelectorAll('.hdots i')];
if(hv.length){let k=0;hv[0].classList.add('on');if(dots[0])dots[0].classList.add('on');
setInterval(()=>{hv[k].classList.remove('on');if(dots[k])dots[k].classList.remove('on');
k=(k+1)%hv.length;hv[k].classList.add('on');if(dots[k])dots[k].classList.add('on');
hv[k].currentTime=0;hv[k].play().catch(()=>{});},7000);}

const heroEl=document.querySelector('.hero');
if(heroEl){heroEl.addEventListener('mousemove',e=>{
 const x=(e.clientX/innerWidth-.5),y=(e.clientY/innerHeight-.5);
 const inner=heroEl.querySelector('.hero-in');if(inner)inner.style.transform='translate('+(x*13)+'px,'+(y*10)+'px)';});
heroEl.addEventListener('mouseleave',()=>{const inner=heroEl.querySelector('.hero-in');if(inner)inner.style.transform='';});}

const pre=document.getElementById('pre');
if(pre){document.body.style.overflow='hidden';
setTimeout(()=>{pre.classList.add('done');document.body.style.overflow='';
window.scrollTo(0,0);},3200);
setTimeout(()=>pre.remove(),4600);}

/* real vesicles, cut from the source imagery, drifting independently.
   drawn additively so their black surround disappears completely. */
const SPR=[];let SPRN=0;
for(let i=0;i<8;i++){const im=new Image();im.src='a/ves'+i+'.jpg';
 im.onload=()=>{SPRN++};SPR.push(im);}

function field(cv,opt){
 const cx=cv.getContext('2d');let V=[],D=[],W=0,H=0,mx=0,my=0;
 const CFG=Object.assign({den:20,min:26,max:58,rmin:26,rmax:120,clear:1,dust:1},opt||{});
 function size(){W=cv.offsetWidth;H=cv.offsetHeight;
  cv.width=Math.round(W*devicePixelRatio);cv.height=Math.round(H*devicePixelRatio);
  cx.setTransform(devicePixelRatio,0,0,devicePixelRatio,0,0);}
 function R(a,b){return a+Math.random()*(b-a)}
 function init(){
  const n=CFG.max===0?0:Math.round(Math.min(CFG.max,Math.max(CFG.min,W/CFG.den)));
  V=[];for(let i=0;i<n;i++){const z=Math.pow(Math.random(),1.45);
   V.push({s:(Math.random()*8)|0,x:R(-.08,1.08)*W,y:R(-.08,1.08)*H,z:z,
    r:CFG.rmin+z*(CFG.rmax-CFG.rmin),
    vx:R(-.10,.10)*(.30+z),vy:-R(.02,.16)*(.30+z),
    rot:R(0,6.283),vr:R(-.00016,.00016),
    ph:R(0,6.283),sw:R(.00035,.0011),am:R(3,13)*(.3+z),
    a:.30+z*.62});}
  D=[];const m=Math.round(Math.min(120,W/9)*CFG.dust);
  for(let i=0;i<m;i++)D.push({x:Math.random()*W,y:Math.random()*H,r:R(.3,1.3),
    vx:R(-.05,.05),vy:-R(.015,.08),a:R(.08,.34),ph:R(0,6.283)});
 }
 function clear(x,y){ if(!CFG.clear) return 1;
  const dx=(x-W/2)/(W*.34),dy=(y-H*.52)/(H*.30);
  const d=Math.sqrt(dx*dx+dy*dy);
  return .22+.78*Math.min(1,Math.max(0,(d-.55)/.75));
 }
 function draw(t){
  cx.clearRect(0,0,W,H);
  if(SPRN===0){requestAnimationFrame(draw);return;}
  cx.globalCompositeOperation='lighter';
  for(const d of D){d.x+=d.vx;d.y+=d.vy;
   if(d.y<-6)d.y=H+6;if(d.x<-6)d.x=W+6;if(d.x>W+6)d.x=-6;
   cx.globalAlpha=d.a*(.55+.45*Math.sin(t*.0015+d.ph))*clear(d.x,d.y);
   cx.fillStyle='#F5E9C4';cx.beginPath();
   cx.arc(d.x+mx*8,d.y+my*6,d.r,0,6.2832);cx.fill();}
  V.sort((a,b)=>a.z-b.z);
  for(const p of V){
   p.x+=p.vx;p.y+=p.vy;p.rot+=p.vr;
   const m=p.r*1.4;
   if(p.y<-m)p.y=H+m;if(p.y>H+m)p.y=-m;
   if(p.x<-m)p.x=W+m;if(p.x>W+m)p.x=-m;
   const x=p.x+Math.sin(t*p.sw+p.ph)*p.am+mx*p.z*24;
   const y=p.y+Math.cos(t*p.sw*.8+p.ph)*p.am*.6+my*p.z*17;
   const sc=p.r*(.93+.07*Math.sin(t*.0009+p.ph));
   const al=p.a*clear(x,y);
   if(al<.02)continue;
   const img=SPR[p.s];if(!img.complete||!img.naturalWidth)continue;
   cx.globalAlpha=al;
   cx.save();cx.translate(x,y);cx.rotate(p.rot);
   cx.drawImage(img,-sc,-sc,sc*2,sc*2);
   cx.restore();
  }
  cx.globalAlpha=1;cx.globalCompositeOperation='source-over';
  requestAnimationFrame(draw);
 }
 size();init();requestAnimationFrame(draw);
 addEventListener('resize',()=>{size();init()});
 addEventListener('mousemove',e=>{mx=(e.clientX/innerWidth-.5);my=(e.clientY/innerHeight-.5);},{passive:true});
}
const cv=document.getElementById('field');
const HOME=/(?:^|\/)(?:index\.html)?$/.test(location.pathname.replace(/\/+$/,'/'))
        || /index\.html$/.test(location.pathname);
if(cv)field(cv, HOME
  ? {den:26,min:18,max:34,rmin:26,rmax:112,clear:1,dust:1}   // the home hero
  : {den:40,min:0,max:0,rmin:0,rmax:0,clear:1,dust:1.4});    // interior: drift only
document.querySelectorAll('canvas.bfield').forEach(c=>{
 const dense=c.classList.contains('dense');
 field(c, dense
  ? {den:20,min:22,max:44,rmin:24,rmax:126,clear:1,dust:1}     // it IS the background
  : {den:34,min:12,max:26,rmin:20,rmax:78,clear:0,dust:.5});   // a layer over footage
});


/* liquid gold — flowing metal, generated live. no footage. */
function goldflow(cv){
 const cx=cv.getContext('2d');let W=0,H=0,mx=0,my=0;
 const N=9, bands=[];
 for(let i=0;i<N;i++)bands.push({
  o:(i+0.5)/N, k1:0.9+Math.random()*1.5, k2:2.1+Math.random()*2.4,
  a1:0.055+Math.random()*0.085, a2:0.018+Math.random()*0.036,
  w1:0.00013+Math.random()*0.00022, w2:0.00021+Math.random()*0.00030,
  p1:Math.random()*6.283, p2:Math.random()*6.283,
  th:0.020+Math.random()*0.055, al:0.30+Math.random()*0.55,
  hue:Math.random()});
 const dust=[];
 function size(){W=cv.offsetWidth;H=cv.offsetHeight;
  cv.width=Math.round(W*devicePixelRatio);cv.height=Math.round(H*devicePixelRatio);
  cx.setTransform(devicePixelRatio,0,0,devicePixelRatio,0,0);
  dust.length=0;const m=Math.round(Math.min(150,W/8));
  for(let i=0;i<m;i++)dust.push({x:Math.random(),y:Math.random(),
   r:0.3+Math.random()*1.5,v:0.00004+Math.random()*0.00013,
   a:0.10+Math.random()*0.40,ph:Math.random()*6.283});}
 function yAt(b,xr,t){
  return (b.o + b.a1*Math.sin(b.k1*xr*6.283 + b.w1*t + b.p1)
              + b.a2*Math.sin(b.k2*xr*6.283 - b.w2*t + b.p2)
              + my*0.05) * H;
 }
 function draw(t){
  cx.clearRect(0,0,W,H);
  cx.globalCompositeOperation='lighter';
  const STEP=Math.max(4,Math.round(W/220));
  for(const b of bands){
   const th=b.th*H*(0.75+0.25*Math.sin(t*0.00035+b.p1));
   // body
   cx.beginPath();
   for(let x=0;x<=W;x+=STEP){const xr=x/W; const y=yAt(b,xr,t);
    const w=th*(0.55+0.45*Math.sin(xr*9.4+t*0.0004+b.p2));
    if(x===0)cx.moveTo(x,y-w/2);else cx.lineTo(x,y-w/2);}
   for(let x=W;x>=0;x-=STEP){const xr=x/W; const y=yAt(b,xr,t);
    const w=th*(0.55+0.45*Math.sin(xr*9.4+t*0.0004+b.p2));
    cx.lineTo(x,y+w/2);}
   cx.closePath();
   const g=cx.createLinearGradient(0,0,W,0);
   const a=b.al;
   g.addColorStop(0,   'rgba(94,68,22,'+(a*0.16)+')');
   g.addColorStop(0.22,'rgba(176,138,64,'+(a*0.42)+')');
   g.addColorStop(0.44,'rgba(238,214,158,'+(a*0.78)+')');
   g.addColorStop(0.58,'rgba(252,238,205,'+(a*0.88)+')');
   g.addColorStop(0.78,'rgba(176,138,64,'+(a*0.40)+')');
   g.addColorStop(1,   'rgba(94,68,22,'+(a*0.14)+')');
   cx.fillStyle=g;cx.fill();
   // specular crest
   cx.beginPath();
   for(let x=0;x<=W;x+=STEP){const xr=x/W;const y=yAt(b,xr,t);
    const w=th*(0.55+0.45*Math.sin(xr*9.4+t*0.0004+b.p2));
    if(x===0)cx.moveTo(x,y-w*0.30);else cx.lineTo(x,y-w*0.30);}
   const g2=cx.createLinearGradient(0,0,W,0);
   g2.addColorStop(0,'rgba(255,252,242,0)');
   g2.addColorStop(0.5,'rgba(255,246,222,'+(a*0.50)+')');
   g2.addColorStop(1,'rgba(255,252,242,0)');
   cx.strokeStyle=g2;cx.lineWidth=Math.max(0.7,th*0.055);cx.stroke();
  }
  // motes riding the flow
  for(const d of dust){
   d.x+=d.v*16; if(d.x>1.05)d.x=-0.05;
   const b=bands[(d.ph*N|0)%N];
   const y=yAt(b,d.x,t)+Math.sin(d.ph+t*0.0006)*H*0.05;
   cx.globalAlpha=d.a*(0.5+0.5*Math.sin(t*0.0014+d.ph));
   cx.fillStyle='#F8F0DA';
   cx.beginPath();cx.arc(d.x*W+mx*10,y,d.r,0,6.2832);cx.fill();
  }
  cx.globalAlpha=1;cx.globalCompositeOperation='source-over';
  requestAnimationFrame(draw);
 }
 size();requestAnimationFrame(draw);
 addEventListener('resize',size);
 addEventListener('mousemove',e=>{mx=(e.clientX/innerWidth-.5);my=(e.clientY/innerHeight-.5);},{passive:true});
}
document.querySelectorAll('canvas.gflow').forEach(goldflow);
