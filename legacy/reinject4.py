assets={}
for line in open('demo_assets_b64.txt'):
    line=line.strip()
    if not line or '=' not in line: continue
    k,v=line.split('=',1)
    assets[k.strip()]=v.strip()
island=open('v4_island_a.b64.txt').read().strip()
branch=open('v4_branch_mul.b64.txt').read().strip()
tpl=open('demo4_template.html').read()
tpl=tpl.replace('{{LOGO_B64}}',assets['LOGO']).replace('{{ISLAND_B64}}',island).replace('{{BRANCH_B64}}',branch)
assert '{{' not in tpl
open('outputs/课题组网站Demo-v4/index.html','w').write(tpl)
print('injected v4', len(tpl)//1024, 'KB')
