import pathlib, json
src = pathlib.Path("outputs/课题组网站Demo-v5/index.html").read_text(encoding="utf-8")
probe = """<pre id="ixout" style="display:none"></pre>
<script>
window.addEventListener('load',function(){
  setTimeout(function(){
    var pills=document.querySelectorAll('#gate .gpills button');
    if(pills[0]) pills[0].click();
    var g=document.getElementById('gate'); if(g) g.style.display='none';
    document.querySelectorAll('.rv').forEach(function(e){e.classList.add('in');e.style.transition='none';});
    var ht=document.getElementById('heroTitle'); if(ht) ht.classList.add('on');
    window.__freeze=true; /* stop the rAF loop so the synchronous probes aren't starved */
  },120);
  setTimeout(function(){
    var out={};
    out.gateGone = getComputedStyle(document.getElementById('gate')).display==='none';
    /* 1) Cmd+K opens search overlay */
    window.dispatchEvent(new KeyboardEvent('keydown',{key:'k',metaKey:true,bubbles:true}));
    out.cmdk = document.getElementById('sov').classList.contains('open');
    document.getElementById('sov').classList.remove('open');
    /* 2) member card opens modal */
    var mc=document.querySelector('.mcard');
    if(mc){ mc.click(); }
    out.modal = document.getElementById('mov').classList.contains('open');
    document.getElementById('mov').classList.remove('open');
    /* 3) logo click opens zoom lightbox */
    var lb=document.getElementById('logoBtn');
    if(lb){ lb.click(); }
    out.logoZoom = document.getElementById('logoZoom').classList.contains('on');
    /* 4) canvases sized */
    out.cv = document.getElementById('partCv').width>0;
    document.getElementById('ixout').textContent='IXJSON '+JSON.stringify(out);
  },900);
});
</script>
</body>"""
assert "</body>" in src
out = src.replace("</body>", probe, 1)
pathlib.Path("outputs/interact5.html").write_text(out, encoding="utf-8")
print("interact5.html written", len(out)//1024, "KB")
