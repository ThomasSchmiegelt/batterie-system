#!/usr/bin/env python3
"""Erzeugt wissensnetz.html (eigenständig, offline) aus wissensnetz.json.
KI-generiert (Claude Opus/Sonnet). Nur Standardbibliothek."""
import json, os, datetime

HIER = os.path.dirname(os.path.abspath(__file__))
QUELLE = os.path.join(HIER, "wissensnetz.json")
ZIEL = os.path.join(HIER, "wissensnetz.html")

d = json.load(open(QUELLE, encoding="utf-8"))
stand = datetime.datetime.fromtimestamp(os.path.getmtime(QUELLE)).strftime("%Y-%m-%d %H:%M")
daten = json.dumps(d, ensure_ascii=False).replace("</", "<\\/")

HTML = r"""<!doctype html>
<html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Wissensnetz Batteriesystem</title>
<style>
:root{--fg:#1d232a;--bg:#f6f7f9;--card:#fff;--line:#c9d0d8;--rot:#c62828;--gruen:#a5d6a7;--gelb:#ffe082;--grau:#d9dde2;--blau:#1565c0}
*{box-sizing:border-box}
body{margin:0;font:14px/1.45 system-ui,Segoe UI,Arial,sans-serif;color:var(--fg);background:var(--bg)}
header{background:var(--card);border-bottom:1px solid var(--line);padding:10px 16px}
.titel{display:inline-block;border:2px solid var(--fg);padding:6px 12px;font-weight:700;font-size:18px}
.meta{margin:8px 0 0;color:#3a444e}
.meta span{margin-right:16px;white-space:nowrap}
.warn{margin:8px 0 0;padding:8px 12px;border:2px solid var(--rot);background:#fdecea;color:#7f1d1d}
.filter{display:flex;flex-wrap:wrap;gap:12px;align-items:center;padding:8px 16px;background:var(--card);border-bottom:1px solid var(--line)}
.filter label{display:flex;gap:6px;align-items:center}
select,input[type=search]{font:inherit;padding:3px 6px;max-width:260px}
button{font:inherit;padding:3px 10px;cursor:pointer}
main{display:flex;align-items:flex-start}
#netz{flex:1 1 auto;min-width:0;overflow:auto;padding:8px;max-height:calc(100vh - 180px);min-height:300px}
#seite{flex:0 0 380px;max-height:calc(100vh - 180px);overflow:auto;background:var(--card);border-left:1px solid var(--line);padding:12px 16px}
#seite h2{margin:0 0 4px;font-size:17px}
#seite h3{margin:14px 0 4px;font-size:13px;text-transform:uppercase;letter-spacing:.04em;color:#4a5560;border-bottom:1px solid var(--line)}
#seite ul{margin:0;padding-left:18px}
#seite table{border-collapse:collapse}
#seite td{padding:1px 10px 1px 0;vertical-align:top}
a{color:var(--blau)}
.ok{color:#2e7d32;font-weight:700}.nein{color:var(--rot);font-weight:700}
.leg{display:flex;flex-wrap:wrap;gap:14px;padding:6px 16px;font-size:13px;background:var(--card);border-top:1px solid var(--line)}
.leg i{display:inline-block;width:22px;height:13px;vertical-align:-2px;margin-right:4px;border:1.5px solid #555}
footer{padding:10px 16px;color:#4a5560;font-size:13px;border-top:1px solid var(--line);background:var(--card)}
.knoten{cursor:pointer}
.knoten rect{stroke-width:1.5}
.knoten.dim{opacity:.18}
.knoten.sel rect{stroke-width:4;stroke:var(--blau)!important}
.knoten.treffer rect{stroke-width:3.5;stroke:#6a1b9a!important}
.kante{fill:none;stroke:#7b8591;stroke-width:1.2}
.kante.kr{stroke:var(--rot);stroke-width:2}
.kante.dim{opacity:.12}
text{font-family:inherit}
@media(max-width:900px){main{flex-direction:column}#seite{flex:none;width:100%;border-left:0;border-top:1px solid var(--line);max-height:none}#netz{max-height:none;width:100%}}
</style></head><body>
<header>
<div class="titel">Wissensnetz Batteriesystem – KI-generiert</div>
<p class="meta" id="meta"></p>
<div id="warn"></div>
</header>
<div class="filter">
<label>Anforderung <select id="fReq"></select></label>
<label>Bauteil <select id="fBt"></select></label>
<label>Software <select id="fSw"></select></label>
<label>Stücklisten-Position <select id="fTl"></select></label>
<label>Suche <input type="search" id="fQ" placeholder="Name oder ID"></label>
<button id="fReset">Zurücksetzen</button>
<span id="fInfo"></span>
</div>
<div class="leg" id="leg"></div>
<main>
<div id="netz"></div>
<aside id="seite"><p>Knoten anklicken, um Einzelheiten zu sehen.</p></aside>
</main>
<footer>KI-generiert (Claude Opus/Sonnet). Erzeugt aus pm/plan/wissensnetz.json.</footer>
<script id="daten" type="application/json">__DATEN__</script>
<script>
const D=JSON.parse(document.getElementById('daten').textContent);
const STAND="__STAND__";
const N=D.knoten, byId={}; N.forEach(k=>byId[k.id]=k);
const FARBE={'fertig':'#a5d6a7','teilweise':'#ffe082','offen':'#d9dde2','ohne Nachweis':'#ffffff'};
const NS='http://www.w3.org/2000/svg';
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const link=p=>'<a href="../../'+esc(p)+'" target="_blank">'+esc(p)+'</a>';

// Kopf
const cnt={};N.forEach(k=>cnt[k.status]=(cnt[k.status]||0)+1);
document.getElementById('meta').innerHTML=
 '<span>Stand: '+STAND+'</span><span>Projektdauer: '+D.projektdauer_AT+' Arbeitstage</span>'+
 '<span>Knoten: '+N.length+'</span>'+
 ['fertig','teilweise','offen','ohne Nachweis'].map(s=>'<span>'+s+': '+(cnt[s]||0)+'</span>').join('')+
 '<span><b>Dauern sind Annahmen.</b></span>';
let w='';
if((D.pruef_fehler||[]).length) w+='<div class="warn"><b>Prüffehler:</b><ul>'+D.pruef_fehler.map(e=>'<li>'+esc(typeof e==='string'?e:JSON.stringify(e))+'</li>').join('')+'</ul></div>';
if((D.anforderungen_ohne_vorgang||[]).length) w+='<div class="warn"><b>Anforderungen ohne Vorgang:</b> '+D.anforderungen_ohne_vorgang.map(e=>esc(typeof e==='string'?e:JSON.stringify(e))).join(', ')+'</div>';
document.getElementById('warn').innerHTML=w;

// Legende
document.getElementById('leg').innerHTML=
 [['fertig','#a5d6a7','#555',''],['teilweise','#ffe082','#555',''],['offen','#d9dde2','#555',''],['ohne Nachweis','#fff','#555','dashed']]
 .map(a=>'<span><i style="background:'+a[1]+';border-style:'+(a[3]||'solid')+'"></i>'+a[0]+'</span>').join('')+
 '<span><i style="background:#fff;border-color:#c62828;border-width:2.5px"></i>kritischer Pfad (rot, auch Pfeile)</span>'+
 '<span><i style="background:#fff;border-color:#1565c0;border-width:3px"></i>gewählt</span>'+
 '<span><i style="background:#fff;border-color:#6a1b9a;border-width:3px"></i>Filter-/Suchtreffer</span>'+
 '<span>x-Position = frühester Start (Arbeitstage)</span>';

// Layout
const PX=40, BH=46, GAP=10, X0=20, Y0=40, MINW=76;
const lay={};
const sorted=[...N].sort((a,b)=>a.es-b.es||b.dauer-a.dauer||a.id.localeCompare(b.id));
const laneEnd=[];
sorted.forEach(k=>{
  const x=X0+k.es*PX, w=Math.max(k.dauer*PX,MINW);
  let l=laneEnd.findIndex(e=>e+8<=x);
  if(l<0){l=laneEnd.length;laneEnd.push(0);}
  laneEnd[l]=x+w;
  lay[k.id]={x,w,y:Y0+l*(BH+GAP),l};
});
const maxX=Math.max(...Object.values(lay).map(o=>o.x+o.w))+30;
const H=Y0+laneEnd.length*(BH+GAP)+10;
const svg=document.createElementNS(NS,'svg');
svg.setAttribute('width',maxX);svg.setAttribute('height',H);svg.setAttribute('viewBox','0 0 '+maxX+' '+H);
function el(t,a,p){const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);(p||svg).appendChild(e);return e;}
const defs=el('defs',{});
['g:#7b8591','r:#c62828'].forEach(s=>{const[i,c]=s.split(':');
 const m=el('marker',{id:'pf'+i,viewBox:'0 0 10 10',refX:9,refY:5,markerWidth:7,markerHeight:7,orient:'auto'},defs);
 el('path',{d:'M0,0L10,5L0,10z',fill:c},m);});
// Achse
const maxT=Math.ceil(D.projektdauer_AT)+1;
for(let t=0;t<=maxT;t++){
  const x=X0+t*PX, major=t%5===0;
  el('line',{x1:x,x2:x,y1:major?24:30,y2:H,stroke:major?'#c9d0d8':'#e6e9ed','stroke-width':1});
  if(major){const tx=el('text',{x:x,y:18,'text-anchor':'middle','font-size':12,fill:'#4a5560'});tx.textContent=t;}
}
const at=el('text',{x:X0+maxT*PX,y:12,'text-anchor':'end','font-size':11,fill:'#4a5560'});at.textContent='Arbeitstage (Tagesteilung = 1 AT)';
// Kanten
const kanten=[];
N.forEach(k=>(k.nachfolger||[]).forEach(n=>{
  if(!lay[n])return;
  const a=lay[k.id],b=lay[n];
  const x1=a.x+a.w, y1=a.y+BH/2, x2=b.x, y2=b.y+BH/2;
  const kr=k.kritisch&&byId[n].kritisch;
  const dx=Math.max(24,Math.abs(x2-x1)/2);
  const p=el('path',{d:'M'+x1+','+y1+' C'+(x1+dx)+','+y1+' '+(x2-dx)+','+y2+' '+x2+','+y2,
    class:'kante'+(kr?' kr':''),'marker-end':'url(#pf'+(kr?'r':'g')+')'});
  kanten.push({p,a:k.id,b:n});
}));
// Knoten
const gm={};
N.forEach(k=>{
  const o=lay[k.id];
  const g=el('g',{class:'knoten',transform:'translate('+o.x+','+o.y+')'});
  const t=el('title',{},g);
  t.textContent=k.id+': '+k.name+' ('+k.dauer+' AT, ES '+k.es+', Status: '+k.status+')';
  el('rect',{width:o.w,height:BH,rx:4,fill:FARBE[k.status]||'#fff',
    stroke:k.kritisch?'#c62828':'#555','stroke-dasharray':k.status==='ohne Nachweis'?'5 3':'none'},g)
   .style.strokeWidth=k.kritisch?'2.5':'1.5';
  const t1=el('text',{x:5,y:16,'font-size':12,'font-weight':700},g);t1.textContent=k.id;
  const cap=Math.floor((o.w-12)/6.3);
  const lines=wrap(k.name,cap,2);
  const t2=el('text',{x:5,y:29,'font-size':10.5},g);
  lines.forEach((ln,i)=>{const s=el('tspan',{x:5,dy:i?11:0},t2);s.textContent=ln;});
  g.addEventListener('click',()=>waehle(k.id,true));
  gm[k.id]=g;
});
function wrap(s,cap,max){
  const out=[];let cur='';
  for(const wd of s.split(' ')){
    if((cur+' '+wd).trim().length<=cap)cur=(cur+' '+wd).trim();
    else{if(cur)out.push(cur);cur=wd;}
  }
  if(cur)out.push(cur);
  if(out.length>max){const r=out.slice(0,max);let l=r[max-1];
    r[max-1]=(l.length>cap-1?l.slice(0,cap-1):l)+'…';return r;}
  return out.map(l=>l.length>cap?l.slice(0,cap-1)+'…':l);
}
document.getElementById('netz').appendChild(svg);

// Filter
const reqs={},bts={},sws={};
N.forEach(k=>{k.req.forEach(r=>reqs[r.id]=r.text);k.bt.forEach(b=>bts[b.id]=b.name);(k.software||[]).forEach(s=>sws[s.name]=s.status);});
const fR=document.getElementById('fReq'),fB=document.getElementById('fBt'),fQ=document.getElementById('fQ'),fS=document.getElementById('fSw'),fT=document.getElementById('fTl');
fS.innerHTML='<option value="">– alle –</option>'+Object.keys(sws).sort().map(i=>'<option value="'+esc(i)+'">'+esc(i)+'</option>').join('');
fT.innerHTML='<option value="">– alle –</option>'+(D.stueckliste||[]).map(t=>'<option value="'+esc(t.pos)+'">'+esc(t.pos)+' '+esc(t.benennung.slice(0,45))+'</option>').join('');
fR.innerHTML='<option value="">– alle –</option>'+Object.keys(reqs).sort().map(i=>'<option value="'+esc(i)+'">'+esc(i)+' '+esc(reqs[i].slice(0,50))+'</option>').join('');
fB.innerHTML='<option value="">– alle –</option>'+Object.keys(bts).sort().map(i=>'<option value="'+esc(i)+'">'+esc(i)+' '+esc(bts[i])+'</option>').join('');
let sel=null;
function filter(){
  const r=fR.value,b=fB.value,sw=fS.value,tl=fT.value,q=fQ.value.trim().toLowerCase();
  const aktiv=!!(r||b||sw||tl||q);
  const hit=new Set();
  N.forEach(k=>{
    let ok=true;
    if(r&&!k.req.some(x=>x.id===r))ok=false;
    if(b&&!k.bt.some(x=>x.id===b))ok=false;
    if(sw&&!(k.software||[]).some(x=>x.name===sw))ok=false;
    if(tl&&!(k.teile||[]).some(x=>x.pos===tl))ok=false;
    if(q&&!(k.id+' '+k.name).toLowerCase().includes(q))ok=false;
    if(ok)hit.add(k.id);
  });
  N.forEach(k=>{
    const g=gm[k.id];
    g.classList.toggle('dim',aktiv&&!hit.has(k.id));
    g.classList.toggle('treffer',aktiv&&hit.has(k.id));
  });
  kanten.forEach(e=>e.p.classList.toggle('dim',aktiv&&!(hit.has(e.a)&&hit.has(e.b))));
  document.getElementById('fInfo').textContent=aktiv?hit.size+' von '+N.length+' Knoten':'';
}
[fR,fB,fS,fT].forEach(e=>e.addEventListener('change',filter));fQ.addEventListener('input',filter);
document.getElementById('fReset').onclick=()=>{fR.value='';fB.value='';fS.value='';fT.value='';fQ.value='';filter();};

// Seitenleiste
function waehle(id,scroll){
  const k=byId[id];if(!k)return;
  if(sel&&gm[sel])gm[sel].classList.remove('sel');
  sel=id;gm[id].classList.add('sel');
  try{history.replaceState(null,'','?knoten='+encodeURIComponent(id));}catch(e){}
  const li=(a,f)=>a&&a.length?'<ul>'+a.map(f).join('')+'</ul>':'<p>–</p>';
  let h='<h2>'+esc(k.id)+': '+esc(k.name)+'</h2>'+
   '<table><tr><td>Status</td><td>'+esc(k.status)+(k.kritisch?' (kritischer Pfad)':'')+'</td></tr>'+
   '<tr><td>Dauer</td><td>'+k.dauer+' AT (Annahme)</td></tr>'+
   '<tr><td>ES / EF</td><td>'+k.es+' / '+k.ef+'</td></tr>'+
   '<tr><td>Puffer</td><td>'+k.puffer+' AT</td></tr>'+
   '<tr><td>Ressourcen</td><td>'+esc((k.ressourcen||[]).join(', ')||'–')+'</td></tr>'+
   '<tr><td>Vorgänger</td><td>'+esc((k.vorgaenger||[]).join(', ')||'–')+'</td></tr>'+
   '<tr><td>Nachfolger</td><td>'+esc((k.nachfolger||[]).join(', ')||'–')+'</td></tr>'+
   '<tr><td>Notiz</td><td>'+esc(k.notiz||'–')+'</td></tr></table>';
  h+='<h3>Anforderungen</h3>'+li(k.req,r=>'<li><b>'+esc(r.id)+'</b> '+esc(r.text)+'</li>');
  h+='<h3>Bauteile</h3>'+li(k.bt,b=>'<li><b>'+esc(b.id)+'</b> '+esc(b.name)+'</li>');
  h+='<h3>Wissen</h3>'+li(k.wissen,x=>'<li><b>'+esc(x.id)+'</b> – '+esc(x.status)+
    (x.pruefung?'<br><small>Prüfung: '+esc(x.pruefung)+'</small>':'')+(x.datei?'<br>'+link(x.datei):'')+'</li>');
  h+='<h3>Software</h3>'+li(k.software,x=>'<li><b>'+esc(x.name)+'</b> – '+(/nicht installiert/.test(x.status)?'<span class="nein">'+esc(x.status)+'</span>':esc(x.status))+'</li>');
  const tt=k.teile||[],ART={K:'Kauf',E:'Eigen',S:'Schnittst.'};
  const trow=t=>'<tr><td><b>'+esc(t.pos)+'</b></td><td>'+esc(t.benennung)+'</td><td>'+esc(t.menge)+'</td><td>'+esc(ART[t.art]||t.art)+'</td></tr>';
  h+='<h3>Stückliste ('+tt.length+')</h3>';
  if(!tt.length)h+='<p>–</p>';
  else{h+='<table><tr><td><i>Pos.</i></td><td><i>Benennung</i></td><td><i>Menge</i></td><td><i>Art</i></td></tr>'+tt.slice(0,10).map(trow).join('')+'</table>';
    if(tt.length>10)h+='<details><summary>… und '+(tt.length-10)+' weitere</summary><table>'+tt.slice(10).map(trow).join('')+'</table></details>';}
  h+='<p>'+link('docs/13_stueckliste.md')+'</p>';
  h+='<h3>Dokumente</h3>'+li(k.doc,p=>'<li>'+link(p)+'</li>');
  h+='<h3>Ergebnisse</h3>'+li(k.aus,x=>'<li><span class="'+(x.vorhanden?'ok':'nein')+'">'+(x.vorhanden?'✓':'✗')+'</span> '+esc(x.glob)+'</li>');
  h+='<h3>Befunde</h3>'+li(k.befunde,b=>'<li><b>'+esc(b.id)+'</b> '+esc(b.titel.replace(b.id,'').trim())+'</li>');
  h+='<h3>Entscheidungen</h3>'+li(k.entscheidungen,e=>'<li><b>'+esc(e.id)+'</b> '+esc(e.titel)+' ('+esc(e.status)+')'+(e.datei?'<br>'+link(e.datei):'')+'</li>');
  document.getElementById('seite').innerHTML=h;
  if(scroll){const n=document.getElementById('netz'),o=lay[id];
    n.scrollLeft=Math.max(0,o.x-n.clientWidth/3);}
}
const pm=new URLSearchParams(location.search).get('knoten');
if(pm&&byId[pm])waehle(pm,true);
</script></body></html>
"""
open(ZIEL, "w", encoding="utf-8").write(HTML.replace("__DATEN__", daten).replace("__STAND__", stand))
print("geschrieben:", ZIEL)
