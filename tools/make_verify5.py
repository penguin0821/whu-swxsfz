import re, pathlib
src = pathlib.Path("outputs/课题组网站Demo-v5/index.html").read_text(encoding="utf-8")
probe = """<style>
#home{min-height:100vh!important}
#about,#members,#pubs,#news{min-height:0!important}
header{position:absolute!important}
#hud{display:none!important}
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
    window.__freeze=true; /* stop rAF so headless captures settle */
    (function keep(){requestAnimationFrame(keep);})(); /* noop frames: headless compositor drops idle canvas layers */
    document.querySelectorAll('.lm>i').forEach(function(e){e.style.transition='none';});
    var hide=new URLSearchParams(location.search).get('hide');
    if(hide){hide.split(',').forEach(function(id){var s=document.getElementById(id.trim());if(s)s.style.display='none';});}
  },120);
});
</script>
</body>"""
assert "</body>" in src
out = src.replace("</body>", probe, 1)
pathlib.Path("outputs/verify5.html").write_text(out, encoding="utf-8")
print("verify5.html written", len(out)//1024, "KB")
