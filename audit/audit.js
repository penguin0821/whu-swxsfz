(function(){
  function parseC(s){
    if(!s) return null;
    var m = s.match(/rgba?\(([^)]+)\)/);
    if(m){ var p = m[1].split(',').map(parseFloat); return {r:p[0],g:p[1],b:p[2],a:p.length>3?p[3]:1}; }
    m = s.match(/#([0-9a-f]{6}|[0-9a-f]{3})/i);
    if(m){ var h=m[1]; if(h.length===3) h=h.split('').map(function(c){return c+c;}).join('');
      return {r:parseInt(h.substr(0,2),16),g:parseInt(h.substr(2,2),16),b:parseInt(h.substr(4,2),16),a:1}; }
    return null;
  }
  function lum(c){ function f(v){ v/=255; return v<=0.03928? v/12.92 : Math.pow((v+0.055)/1.055,2.4); }
    return 0.2126*f(c.r)+0.7152*f(c.g)+0.0722*f(c.b); }
  function ratio(a,b){ var l1=lum(a),l2=lum(b); return (Math.max(l1,l2)+0.05)/(Math.min(l1,l2)+0.05); }
  function mix(a,b,t){ return {r:a.r+(b.r-a.r)*t, g:a.g+(b.g-a.g)*t, b:a.b+(b.b-a.b)*t, a:a.a+(b.a-a.a)*t}; }
  /* Sample a gradient at the position where the text actually sits.
     Chrome drops the default "to bottom" keyword from computed linear-gradients,
     so a missing direction must be treated as vertical-to-bottom (NOT first stop).
     Radial gradients are sampled at their centre (t=0.5) because text/initials sit
     mid-shape, not on the top-left highlight. */
  function sampleGrad(grad, el, node){
    var stops=[], re=/(rgba?\([^)]*\)|#[0-9a-f]{3,6})\s*([\d.]+%)?/gi, m;
    while((m=re.exec(grad))) { var c=parseC(m[1]); if(c) stops.push({c:c, p:m[2]?parseFloat(m[2])/100:null}); }
    if(!stops.length) return null;
    if(stops[0].p==null) stops[0].p=0;
    if(stops[stops.length-1].p==null) stops[stops.length-1].p=1;
    for(var i=1;i<stops.length-1;i++){
      if(stops[i].p==null){
        var j=i; while(j<stops.length && stops[j].p==null) j++;
        var a=stops[i-1].p, b=stops[j].p, n=j-i+1;
        for(var k=i;k<j;k++) stops[k].p=a+(b-a)*(k-i+1)/n;
      }
    }
    var radial=/radial-gradient/i.test(grad);
    var verticalUp=/to\s+top|(^|[^0-9])0deg/i.test(grad);
    var horizontal=/to\s+right|(^|[^0-9])90deg/i.test(grad);
    var horizontalL=/to\s+left|270deg/i.test(grad);
    var t;
    if(radial){ t=0.5; }
    else{
      var r1=node.getBoundingClientRect(), r2=el.getBoundingClientRect();
      var fy=(r2.top+r2.height/2-r1.top)/Math.max(1,r1.height);
      var fx=(r2.left+r2.width/2-r1.left)/Math.max(1,r1.width);
      if(verticalUp) t=1-fy;
      else if(horizontal) t=fx;
      else if(horizontalL) t=1-fx;
      else t=fy; /* to bottom / 180deg / default */
    }
    t=Math.max(0,Math.min(1,t));
    for(i=0;i<stops.length-1;i++){
      if(t>=stops[i].p && t<=stops[i+1].p){
        var span=stops[i+1].p-stops[i].p;
        return mix(stops[i].c, stops[i+1].c, span>0?(t-stops[i].p)/span:0);
      }
    }
    return stops[stops.length-1].c;
  }
  /* backdropNode: what is painted behind a fixed root (resolved via elementFromPoint),
     used in place of the DOM parent once we walk past the fixed root boundary. */
  function bgOf(el, node, fr, backdropNode){
    node = node || el;
    var n=node;
    while(n && n!==document.documentElement){
      var cs=getComputedStyle(n);
      var under = (n===fr && backdropNode) ? function(){return bgOf(el, backdropNode);} :
                  function(){return bgOf(el, n.parentElement||document.body, fr, backdropNode);};
      var grad=cs.backgroundImage;
      if(grad && grad!=='none'){
        var gc=sampleGrad(grad, el, n);
        if(gc){
          if(gc.a>=0.9) return gc;
          if(gc.a>0){
            var u=under();
            return {r:gc.r*gc.a+u.r*(1-gc.a), g:gc.g*gc.a+u.g*(1-gc.a), b:gc.b*gc.a+u.b*(1-gc.a), a:1};
          }
        }
      }
      var bc=parseC(cs.backgroundColor);
      if(bc){
        if(bc.a>=0.9) return bc;
        if(bc.a>0){
          var p=under();
          return {r:bc.r*bc.a+p.r*(1-bc.a), g:bc.g*bc.a+p.g*(1-bc.a), b:bc.b*bc.a+p.b*(1-bc.a), a:1};
        }
      }
      n = (n===fr && backdropNode) ? backdropNode : n.parentElement;
      if(n===backdropNode){ fr=null; backdropNode=null; }
    }
    return {r:243,g:237,b:226,a:1};
  }
  /* fixed-position chrome floats over whatever is scrolled behind it; resolve that
     real backdrop with elementFromPoint instead of its (dark) DOM ancestor body. */
  function fixedRoot(el){
    var n=el;
    while(n && n!==document.body){ if(getComputedStyle(n).position==='fixed') return n; n=n.parentElement; }
    return null;
  }
  function backdropOfFixed(fr){
    var r=fr.getBoundingClientRect(), cx=r.left+r.width/2, cy=r.top+r.height/2;
    cx=Math.max(1,Math.min(innerWidth-1,cx)); cy=Math.max(1,Math.min(innerHeight-1,cy));
    var prev=fr.style.display; fr.style.display='none';
    var behind=document.elementFromPoint(cx,cy);
    fr.style.display=prev;
    return behind;
  }
  function bgFor(el){
    var fr=fixedRoot(el);
    if(fr){
      var bd=backdropOfFixed(fr);
      if(bd) return bgOf(el, el, fr, bd);
    }
    return bgOf(el);
  }
  var bad=[];
  document.querySelectorAll('body *').forEach(function(el){
    if(!el.textContent || !el.textContent.trim()) return;
    var hasText=[].some.call(el.childNodes,function(n){return n.nodeType===3 && n.textContent.trim();});
    if(el.children.length && !hasText) return;
    var cs=getComputedStyle(el);
    if(cs.visibility==='hidden'||cs.display==='none'||+cs.opacity===0) return;
    var fg=parseC(cs.color); if(!fg) return;
    var bg=bgFor(el);
    var size=parseFloat(cs.fontSize);
    var weight=parseInt(cs.fontWeight)||400;
    var need=(size<18 && weight<700)?4.5:3.0;
    var r=ratio(fg,bg);
    if(r<need) bad.push({t:el.textContent.trim().slice(0,18), tag:el.tagName, cls:(el.className+'').slice(0,26), r:+r.toFixed(2), need:need, size:size});
  });
  window.__audit={count:bad.length, bad:bad.slice(0,30)};
  return window.__audit;
})();
