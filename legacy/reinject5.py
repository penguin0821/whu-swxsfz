assets={}
for line in open('demo_assets_b64.txt'):
    line=line.strip()
    if not line or '=' not in line: continue
    k,v=line.split('=',1)
    assets[k.strip()]=v.strip()
island=open('v4_island_a.b64.txt').read().strip()
branch=open('v4_branch_mul.b64.txt').read().strip()
land=open('_land_b64.txt').read().strip()
fontreg=open('v5_font_reg.b64.txt').read().strip()
fontsb=open('v5_font_sb.b64.txt').read().strip()
tpl=open('demo5_template.html').read()
tpl=tpl.replace('{{LOGO_B64}}',assets['LOGO']).replace('{{ISLAND_B64}}',island).replace('{{BRANCH_B64}}',branch).replace('{{LAND_B64}}',land).replace('{{FONT_REG_B64}}',fontreg).replace('{{FONT_SB_B64}}',fontsb)
assert '{{' not in tpl
open('outputs/课题组网站Demo-v5/index.html','w').write(tpl)
print('injected v5', len(tpl)//1024, 'KB')
