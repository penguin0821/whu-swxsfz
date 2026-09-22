# -*- coding: utf-8 -*-
# One-shot batch patch for demo6_template.html:
#  (1) natural scroll (remove pinned stage), (2) about lead de-AI + type balance,
#  (3) direction keywords, (4) advisor modal content + photo, (5) taste-skill pass.
import io, sys

P = 'demo6_template.html'
s = io.open(P, encoding='utf-8').read()
orig = s

R = []  # (old, new, label)

# ---------- (5) taste: clean <title> version label ----------
R.append((u'<title>涉外刑事风险治理与合规中心 · Demo v4</title>',
          u'<title>涉外刑事风险治理与合规中心 · 武汉大学涉外法治学院</title>', 'title'))

# ---------- (5) taste: no pure #fff on selection ----------
R.append((u'::selection{background:var(--green);color:#fff}',
          u'::selection{background:var(--green);color:var(--paper-2)}', 'selection'))

# ---------- (2) type-weight rebalance: kicker up, h2 down ----------
R.append((u'.kicker{font-size:12.5px;letter-spacing:.1em;color:var(--green)}',
          u'.kicker{font-size:13.5px;letter-spacing:.08em;color:var(--green)}', 'kicker'))
R.append((u'h2{font-size:clamp(26px,3.2vw,40px);line-height:1.25;margin:14px 0 10px;font-weight:600}',
          u'h2{font-size:clamp(24px,2.7vw,34px);line-height:1.3;margin:12px 0 10px;font-weight:600}', 'h2'))

# ---------- (5) taste: remove fixed corner HUD (numbered section eyebrow) ----------
R.append((u"""#hud{position:fixed;left:26px;top:50%;transform:translateY(-50%);z-index:40;display:flex;align-items:center;gap:10px;color:rgba(243,237,226,.55);font-size:11px;letter-spacing:.08em;pointer-events:none;transition:color .4s}
#hud .hud-lines{display:flex;flex-direction:column;gap:3px}
#hud .hud-lines i{display:block;height:1px;background:currentColor;opacity:.55}
#hud .hud-lines i:nth-child(1){width:26px}
#hud .hud-lines i:nth-child(2){width:17px}
#hud .hud-lines i:nth-child(3){width:9px}
#hud .hud-no{font-family:var(--serif);font-size:13.5px;color:var(--pink)}
#hud .hud-sl{opacity:.5}
#hud.on-paper{color:rgba(34,29,21,.5)}
#hud.on-paper .hud-no{color:var(--ink)}
""", u'', 'hud-css'))

# ---------- (1) remove pinned-stage CSS ----------
R.append((u"""/* pinned opening stage: hero holds the viewport while a short scroll choreography plays */
#homeStage{position:relative;height:178vh}
#home{position:sticky;top:0;height:100vh}
""", u'', 'pinned-css'))

# ---------- (5) taste: stats trio -> one editorial line ----------
R.append((u""".stats{display:flex;gap:46px;margin-top:42px;justify-content:flex-start}
.stats .n{font-family:var(--serif);font-size:32px;color:var(--green-deep);font-weight:600}
.stats .l{font-size:12.5px;color:var(--ink-mut);letter-spacing:.04em;margin-top:4px}""",
          u'.stats{margin-top:38px;font-size:14.5px;line-height:1.9;color:var(--ink-mut);max-width:34em}', 'stats-css'))

# ---------- (5) taste: remove hero search pill + scroll cue ----------
R.append((u""".hint{display:inline-flex;align-items:center;gap:9px;margin-top:40px;font-size:12.5px;letter-spacing:.02em;color:#4E4A40;border:1px dashed rgba(34,29,21,.32);border-radius:999px;padding:8px 16px;background:rgba(251,247,239,.42);transition:all .2s}
.hint:hover{color:var(--ink);border-color:rgba(34,29,21,.55);background:rgba(251,247,239,.7)}
""", u'', 'hint-css'))
R.append((u""".scroll-hint{position:absolute;left:34px;bottom:26px;z-index:6;font-size:11px;letter-spacing:.1em;color:var(--pink-mut);display:flex;align-items:center;gap:10px}
.scroll-hint i{display:block;width:1px;height:36px;background:linear-gradient(var(--green),transparent);animation:drip 2.4s ease-in-out infinite}
@keyframes drip{0%{transform:scaleY(0);transform-origin:top}45%{transform:scaleY(1);transform-origin:top}55%{transform:scaleY(1);transform-origin:bottom}100%{transform:scaleY(0);transform-origin:bottom}}
""", u'', 'scrollhint-css'))

# ---------- (5) taste: break 3-equal-card grid into a staggered cascade; unify radius ----------
R.append((u'.dirs{display:grid;grid-template-columns:1.15fr 1fr 1fr;gap:20px;margin-top:52px}',
          u""".dirs{display:grid;grid-template-columns:1.18fr 1fr 1fr;gap:20px;margin-top:52px;align-items:start}
.dir:nth-child(2){margin-top:30px}
.dir:nth-child(3){margin-top:60px}""", 'dirs-grid'))
R.append((u'.dir{position:relative;background:rgba(243,237,226,.035);border:1px solid var(--line-d);border-radius:16px;padding:30px 28px 34px;transition:border-color .3s,transform .3s,background .3s}',
          u'.dir{position:relative;background:rgba(243,237,226,.035);border:1px solid var(--line-d);border-radius:18px;padding:30px 28px 34px;transition:border-color .3s,transform .3s,background .3s}', 'dir-radius'))
R.append((u'.dir .ix{font-family:var(--serif);font-size:12.5px;letter-spacing:.12em;color:var(--green)}\n', u'', 'dir-ix-css'))
R.append((u'@media(max-width:900px){.dirs{grid-template-columns:1fr}}',
          u'@media(max-width:900px){.dirs{grid-template-columns:1fr}.dir:nth-child(2),.dir:nth-child(3){margin-top:0}}', 'dirs-mobile'))
R.append((u'border:1px solid var(--line-d);cursor:pointer;transition:transform .3s,box-shadow .3s}',
          u'border:1px solid var(--line-d);cursor:pointer;transition:transform .3s,box-shadow .3s}', 'sup-noop'))  # placeholder, replaced below
R.pop()  # drop noop
R.append((u'gap:44px;background:linear-gradient(135deg,var(--stage-2),var(--stage-3));border-radius:20px;',
          u'gap:44px;background:linear-gradient(135deg,var(--stage-2),var(--stage-3));border-radius:18px;', 'sup-radius'))

# ---------- (4) photo avatar support ----------
R.append((u'.dlg .ava.b{background:radial-gradient(circle at 34% 30%,#C08552,var(--brown-deep) 74%)}',
          u""".dlg .ava.b{background:radial-gradient(circle at 34% 30%,#C08552,var(--brown-deep) 74%)}
.ava.photo{background:none;font-size:0;overflow:hidden}
.ava.photo img{width:100%;height:100%;object-fit:cover;object-position:50% 35%;display:block}""", 'ava-photo-css'))

# ---------- (1) mobile + RM: drop homeStage overrides ----------
R.append((u"""  #homeStage{height:auto}
  #home{position:relative;top:auto;height:auto;flex-direction:column;align-items:stretch;justify-content:flex-start;min-height:auto;padding-top:78px}""",
          u'  #home{flex-direction:column;align-items:stretch;justify-content:flex-start;min-height:auto;padding-top:78px}', 'home-mobile'))
R.append((u'  .stats{gap:22px;flex-wrap:wrap;justify-content:center;margin-top:30px}',
          u'  .stats{margin-top:26px;text-align:center}', 'stats-mobile'))
R.append((u'  #homeStage{height:auto}#home{position:relative;top:auto;height:auto}.hero-grid{opacity:1!important;transform:none!important}}',
          u'  .hero-grid{opacity:1!important;transform:none!important}}', 'home-rm'))

# ---------- (5) taste: remove giant outlined section numerals ----------
R.append((u""".shd::before{content:attr(data-no);position:absolute;right:0;top:-.42em;z-index:0;
  font-family:var(--serif);font-weight:600;font-size:clamp(80px,13vw,200px);line-height:1;
  color:transparent;-webkit-text-stroke:1px rgba(127,160,90,.30);pointer-events:none;user-select:none}
.on-paper .shd::before{-webkit-text-stroke:1px rgba(20,28,18,.15)}
""", u'', 'shd-numeral-css'))

# ---------- markup: HUD element ----------
R.append((u'<div id="hud" aria-hidden="true"><span class="hud-lines"><i></i><i></i><i></i></span><span class="hud-no" id="hudNo">00</span><span class="hud-sl">/</span><span class="hud-name" id="hudName"></span></div>\n',
          u'', 'hud-el'))

# ---------- markup: homeStage wrapper ----------
R.append((u'<main>\n<div id="homeStage">\n<section id="home">', u'<main>\n<section id="home">', 'stage-open'))
R.append((u'</section>\n</div>\n\n<section id="about">', u'</section>\n\n<section id="about">', 'stage-close'))

# ---------- markup: hero pill + scroll cue + epi1 ----------
R.append((u'        <button class="hint rv" style="--d:.54s" id="hintBtn"><span>⌕</span><span id="hintTxt"></span></button>\n', u'', 'hint-el'))
R.append((u'  <div class="scroll-hint"><i></i><span id="scrollTxt"></span></div>\n', u'', 'scrollhint-el'))
R.append((u'    <div class="epi rv" style="--d:.18s" id="epi1"></div>\n', u'', 'epi1-el'))

# ---------- markup: data-no attrs ----------
for n in (u'01', u'02', u'03', u'04'):
    R.append((u'<div class="shd" data-no="%s">' % n, u'<div class="shd">', 'shd-attr-' + n))

# ---------- footer version label ----------
R.append((u'<div class="ftbot"><span id="ftDisc"></span><span>© 2026 · Demo v4</span></div>',
          u'<div class="ftbot"><span id="ftDisc"></span><span>© 2026</span></div>', 'footer'))

# ---------- UI strings zh ----------
R.append((u'  stats:[["研究人员",20,"+"],["研究方向",3,""],["代表性成果",13,""]],',
          u'  statsLine:"二十余位研究者，三个研究方向，十三项代表性成果。",', 'stats-zh'))
R.append((u'  hint:"按 ⌘K 搜索成员、成果与新闻",scroll:"向下滚动",\n', u'', 'hintscroll-zh'))
R.append((u'  aboutSub:"从教义学根基到网络空间、再到涉外场域，三个方向共用一套问题意识：技术时代的刑法如何既不缺席、也不越位。",',
          u'  aboutSub:"在信息网络时代，刑法需要解决“法益侵害社会化”和“刑事归责个别化”的冲突。",', 'aboutsub-zh'))
R.append((u'  epi1:"法益侵害社会化和刑事归责个别化",\n', u'', 'epi1-zh'))
R.append((u'sup:"副教授 · 导师",', u'sup:"副教授 · 博士生导师",', 'sup-zh'))

# ---------- UI strings en ----------
R.append((u'  stats:[["Researchers",20,"+"],["Directions",3,""],["Selected outputs",13,""]],',
          u'  statsLine:"Twenty-odd researchers, three directions, thirteen selected outputs.",', 'stats-en'))
R.append((u'  hint:"Press ⌘K to search people, outputs & news",scroll:"Scroll",\n', u'', 'hintscroll-en'))
R.append((u'  aboutSub:"From doctrinal foundations to cyberspace to foreign-related arenas, one question runs through: how should criminal law respond to technology without overreaching?",',
          u'  aboutSub:"In the information-network era, criminal law must reconcile the socialization of harm to legal interests with the individualization of criminal imputation.",', 'aboutsub-en'))
R.append((u'  epi1:"The socialization of harm to legal interests, and the individualization of criminal imputation",\n', u'', 'epi1-en'))
R.append((u'sup:"Associate Professor · Supervisor",', u'sup:"Associate Professor · Doctoral Supervisor",', 'sup-en'))

# ---------- DIRS keywords (3) ----------
R.append((u'k:["行为不法","犯罪参与","预备犯"]},', u'k:["行为不法","犯罪参与","共犯理论","预备犯"]},', 'dirs0-zh'))
R.append((u'k:["Wrong-doing","Participation","Preparatory offences"]}},', u'k:["Wrong-doing","Participation","Complicity","Preparatory offences"]}},', 'dirs0-en'))
R.append((u'k:["跨境数据","电诈产业链","刑事合规"]},', u'k:["跨境网络犯罪","电诈犯罪产业链","《联合国打击网络犯罪公约》"]},', 'dirs2-zh'))
R.append((u'k:["Cross-border data","Fraud chains","Compliance"]}}', u'k:["Cross-border cybercrime","Telecom-fraud chains","UN Cybercrime Convention"]}}', 'dirs2-en'))

# ---------- SUP bio / contact / outputs (4) ----------
R.append((u' bio:{zh:"武汉大学法学院副教授。从事预防刑法、信息网络犯罪与数据合规研究。",',
          u' bio:{zh:"武汉大学法学院副教授、博士生导师。从事预防刑法、信息网络犯罪与数据合规研究。",', 'sup-bio'))
R.append((u""" contact:{zh:"武汉大学法学院 · 涉外法治学院（邮箱待补充）",en:"Law School / School of Foreign-Related Rule of Law, WHU (email TBA)"}};""",
          u""" contact:{zh:"武汉大学法学院 · 涉外法治学院 · jinglijia11@sina.cn",en:"Law School / School of Foreign-Related Rule of Law, WHU · jinglijia11@sina.cn"},
 out:{zh:["《论帮助信息网络犯罪活动罪的规范属性》，《法学家》2025 年第 2 期",
      "《个人信息保护合规的体系构建》，《法学研究》2022 年第 4 期",
      "《网络暴力法律规制的完善路径》（与胡隽合著），《中国人民公安大学学报（社会科学版）》2021 年第 5 期",
      "专著《犯罪参与行为的处罚边界：网络时代的新展开》，社会科学文献出版社 2023 年",
      "专著《信息网络犯罪规制的预防转向与限度》，社会科学文献出版社 2019 年",
      "创办“网络犯罪治理实务论坛”"],
  en:["“The Normative Attribute of the Crime of Assisting Information-Network Criminal Activity”, Jurists, 2025(2)",
      "“Systematic Construction of Personal-Information Protection Compliance”, Chinese Journal of Law, 2022(4)",
      "“The Perfect Path of Legal Regulation of Cyber Violence” (with Hu Jun), J. People's Public Security Univ. (Soc. Sci.), 2021(5)",
      "Monograph: The Boundaries of Punishment for Criminal Participation, SSAP, 2023",
      "Monograph: The Preventive Turn and Its Limits in the Regulation of Information-Network Crimes, SSAP, 2019",
      "Founder of the Practical Forum on Cybercrime Governance"]}};""", 'sup-contact-out'))

# ---------- TAGS unify to one accent family (5) ----------
R.append((u""" {zh:"调研考察",en:"Fieldwork",c:"#8A5A3B",bg:"rgba(169,113,75,.14)"},
 {zh:"合作交流",en:"Cooperation",c:"#5B4A8A",bg:"rgba(91,74,138,.12)"},""",
          u""" {zh:"调研考察",en:"Fieldwork",c:"#3E5B26",bg:"rgba(127,160,90,.12)"},
 {zh:"合作交流",en:"Cooperation",c:"#3E5B26",bg:"rgba(127,160,90,.12)},""", 'tags-unify'))
R.append((u' {zh:"荣誉获奖",en:"Honors",c:"#8A5A3B",bg:"rgba(169,113,75,.16)"}];',
          u' {zh:"荣誉获奖",en:"Honors",c:"#3E5B26",bg:"rgba(127,160,90,.20)"}];', 'tags-honors'))

# ---------- renderStatic ----------
R.append((u'  document.getElementById("hintTxt").textContent = t().hint.replace(/按 |Press /,"");\n', u'', 'hinttxt'))
R.append((u'  document.getElementById("scrollTxt").textContent = t().scroll;\n', u'', 'scrolltxt'))
R.append((u"""  document.getElementById("stats").innerHTML = t().stats.map(s=>
    `<div><div class="n"><span data-cnt="${s[1]}">0</span>${s[2]}</div><div class="l">${s[0]}</div></div>`).join("");
  const stEl=document.getElementById("stats"); if(stEl.classList.contains("in")) countUp(stEl);""",
          u'  document.getElementById("stats").textContent = t().statsLine;', 'stats-render'))
R.append((u'  document.getElementById("epi1").innerHTML = "<b>"+words(t().epi1)+"</b>";\n', u'', 'epi1-render'))

# ---------- renderDirs: drop numeral ----------
R.append((u'    <div class="dir rv" style="--d:${i*0.08}s"><div class="ix">0${i+1}</div>\n',
          u'    <div class="dir rv" style="--d:${i*0.08}s">\n', 'dir-ix-render'))

# ---------- photo URI constant + modal data (4) ----------
R.append((u'function personModalData(p,isSup){',
          u'const PHOTO_URI="data:image/webp;base64,{{PHOTO_B64}}";\nfunction personModalData(p,isSup){', 'photo-uri'))
R.append((u"""    contact:isSup?pick(p.contact):t().ftMail,
    pubs:isSup?PUBS.papers.slice(0,3).map(x=>pick(x)):null};""",
          u"""    contact:isSup?pick(p.contact):t().ftMail,
    photo:isSup?PHOTO_URI:null,
    pubs:isSup?pick(p.out):null};""", 'modal-data'))
R.append((u'    <div class="top"><div class="ava ${cls||"g"}">${d.ini}</div>',
          u'    <div class="top">${d.photo?`<div class="ava photo"><img src="${d.photo}" alt="${d.name}"></div>`:`<div class="ava ${cls||"g"}">${d.ini}</div>`}', 'modal-ava'))
R.append((u'    <div class="ava">${LANG==="zh"?"敬":"J"}</div>',
          u'    <div class="ava photo"><img src="${PHOTO_URI}" alt="${pick(s)}"></div>', 'supcard-ava'))

# ---------- onScroll: drop HUD, drop ci ----------
R.append((u"""  const SECS=["home","about","members","pubs","news"];
  let ci=0;
  document.querySelectorAll("nav a[data-sec]").forEach(a=>{
    const sec=document.getElementById(a.dataset.sec);if(!sec)return;
    const r=sec.getBoundingClientRect();
    const act=r.top<=vh*0.4&&r.bottom>vh*0.4;
    a.classList.toggle("on",act);
    if(act)ci=SECS.indexOf(a.dataset.sec);});
  if(ci<0)ci=0;
  if(ci!==hudIdx){
    hudIdx=ci;
    const hud=document.getElementById("hud");
    if(hud){
      document.getElementById("hudNo").textContent=String(ci).padStart(2,"0");
      document.getElementById("hudName").textContent=t().nav[ci]||"";
      const sec=document.getElementById(SECS[ci]);
      hud.classList.toggle("on-paper",!!(sec&&(sec.classList.contains("on-paper")||sec.id==="home")));
    }
  }
}""",
          u"""  document.querySelectorAll("nav a[data-sec]").forEach(a=>{
    const sec=document.getElementById(a.dataset.sec);if(!sec)return;
    const r=sec.getBoundingClientRect();
    const act=r.top<=vh*0.4&&r.bottom>vh*0.4;
    a.classList.toggle("on",act);});
}""", 'onscroll-hud'))
R.append((u'let hudIdx=-1;\n', u'', 'hudidx-decl'))
R.append((u'  hudIdx=-1;\n', u'', 'hudidx-reset'))

# ---------- loop: natural scroll (1) + poll onScroll in rAF (5) ----------
R.append((u"""    /* pinned-stage progress: the 78vh of #homeStage past the first viewport */
    const stg=wide?Math.max(0,Math.min(1,sy/(innerHeight*0.78))):0;
""", u'', 'stg-decl'))
R.append((u"""      if(tw)tw.style.transform=
        `translate3d(${(lx*-7).toFixed(1)}px,${(sy*0.04+ly*-5-stg*34).toFixed(1)}px,0) scale(${(1+br+stg*0.09).toFixed(4)})`;""",
          u"""      if(tw)tw.style.transform=
        `translate3d(${(lx*-7).toFixed(1)}px,${(sy*0.04+ly*-5).toFixed(1)}px,0) scale(${(1+br).toFixed(4)})`;""", 'treewrap-stg'))
R.append((u"""    const hg=document.querySelector(".hero-grid");
    if(hg){
      const op=wide?(1-0.94*stg).toFixed(3):Math.max(0,1-sy/(innerHeight*0.9)).toFixed(3);
      const tf=wide?`translateY(${(-62*stg).toFixed(1)}px)`:"";
      if(hg.style.opacity!==op)hg.style.opacity=op;
      if(hg.style.transform!==tf)hg.style.transform=tf;
    }
    requestAnimationFrame(loop);""",
          u"""    if(syT!==lastNavSy){lastNavSy=syT;onScroll();}
    requestAnimationFrame(loop);""", 'herogrid-block'))
R.append((u'    const still=()=>{if(window.__freeze)return;drawParts();drawGlobe();drawBirds();drawRoots();drawFgRoots();requestAnimationFrame(still);};',
          u'    const still=()=>{if(window.__freeze)return;drawParts();drawGlobe();drawBirds();drawRoots();drawFgRoots();if(syT!==lastNavSy){lastNavSy=syT;onScroll();}requestAnimationFrame(still);};', 'still-poll'))
R.append((u'let parts=[],leaves=[],birds=[],mouse={x:-9999,y:-9999},px=0,py=0,syT=0,sy=0;',
          u'let parts=[],leaves=[],birds=[],mouse={x:-9999,y:-9999},px=0,py=0,syT=0,sy=0,lastNavSy=-1;', 'lastnavsy-decl'))
R.append((u'  addEventListener("scroll",()=>{if(RM)onScroll();else onScroll();},{passive:true});\n', u'', 'scroll-listener'))
R.append((u'  size();addEventListener("resize",()=>{size();buildSpine();});',
          u'  size();addEventListener("resize",()=>{size();buildSpine();onScroll();});', 'resize-onscroll'))

# ---------- hintBtn listener ----------
R.append((u'document.getElementById("hintBtn").addEventListener("click",openSearch);\n', u'', 'hintbtn-listener'))

# ---------- apply ----------
fails = []
for old, new, label in R:
    c = s.count(old)
    if c != 1:
        fails.append((label, c))
        continue
    s = s.replace(old, new)
if fails:
    for label, c in fails:
        sys.stderr.write(u'ANCHOR FAIL %s count=%d\n' % (label, c))
    sys.exit(1)
io.open(P, 'w', encoding='utf-8').write(s)
print('patched ok:', len(R), 'replacements;', len(orig), '->', len(s), 'bytes')
