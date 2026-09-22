import pathlib
src = pathlib.Path("outputs/课题组网站Demo-v5/index.html").read_text(encoding="utf-8")
probe = """<script>
window.addEventListener('load',function(){
  setTimeout(function(){
    var lang=new URLSearchParams(location.search).get('lang')||'zh';
    var pills=document.querySelectorAll('#gate .gpills button');
    var b=(lang==='en'&&pills[1])?pills[1]:pills[0]; if(b) b.click();
    var g=document.getElementById('gate'); if(g) g.style.display='none';
    var sec=new URLSearchParams(location.search).get('sec')||'members';
    var s=document.getElementById(sec);
    window.scrollTo(0, s.offsetTop+60);
    setTimeout(function(){window.__freeze=true;},400);
  },150);
});
</script>
</body>"""
assert "</body>" in src
out = src.replace("</body>", probe, 1)
pathlib.Path("outputs/_hdr5.html").write_text(out, encoding="utf-8")
print("hdr5 written", len(out)//1024, "KB")
