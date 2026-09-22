import pathlib, json
aud = pathlib.Path("outputs/audit.js").read_text(encoding="utf-8")
src = pathlib.Path("outputs/课题组网站Demo-v5/index.html").read_text(encoding="utf-8")
# settle probe ONLY (no layout-neutralizing CSS) so the audit's fixed-header
# backdrop resolution (elementFromPoint) sees the real hero behind the nav.
probe = """<style>
*{transition:none!important;animation:none!important}
</style>
<script>
window.addEventListener('load',function(){
  setTimeout(function(){
    var lang=new URLSearchParams(location.search).get('lang')||'zh';
    var pills=document.querySelectorAll('#gate .gpills button');
    var b=(lang==='en'&&pills[1])?pills[1]:pills[0]; if(b) b.click();
    var g=document.getElementById('gate'); if(g) g.style.display='none';
    document.querySelectorAll('.rv').forEach(function(e){e.classList.add('in');e.style.transition='none';});
    var ht=document.getElementById('heroTitle'); if(ht) ht.classList.add('on');
    document.querySelectorAll('.lm>i').forEach(function(e){e.style.transition='none';});
    window.__freeze=true; /* stop the rAF loop so the synchronous audit walk isn't starved */
  },120);
});
</script>
<pre id="auditout" style="display:none"></pre>
<script>
window.addEventListener('load',function(){
  setTimeout(function(){
    var res;
    try{ res = eval(%s); }catch(e){ res={count:-1,bad:[{t:'ERR:'+e.message}]}; }
    document.getElementById('auditout').textContent = 'AUDITJSON '+JSON.stringify(res);
  },900);
});
</script>
</body>""" % json.dumps(aud)
assert "</body>" in src
out = src.replace("</body>", probe, 1)
pathlib.Path("outputs/audit5.html").write_text(out, encoding="utf-8")
print("audit5.html written", len(out)//1024, "KB")
