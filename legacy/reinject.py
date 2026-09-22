assets={}
for line in open('demo_assets_b64.txt'):
    line=line.strip()
    if not line or '=' not in line: continue
    k,v=line.split('=',1)
    assets[k.strip()]=v.strip()
assets['TREE']=open('tree_clean.b64').read().strip()
tpl=open('demo2_template.html').read()
tpl=tpl.replace('{{LOGO_B64}}',assets['LOGO']).replace('{{TREE_B64}}',assets['TREE'])
assert '{{' not in tpl
open('outputs/课题组网站Demo-v2/index.html','w').write(tpl)
print('injected', len(tpl))
