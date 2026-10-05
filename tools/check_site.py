"""Verificador técnico del sitio: JSON-LD válido, enlaces/imágenes internos, alt en <img>, un solo H1."""
import re,json,os,glob,sys
import os
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pages=[f for f in glob.glob(root+'/**/*.html',recursive=True) if not any(x in f for x in ('/tools/','/brag-output/','/marketing/','/docs/'))]
def exists(url):
    u=url.split('#')[0].split('?')[0]
    if u=='' : return True
    if u.endswith('/'): u+='index.html'
    return os.path.exists(root+u)
bad=0
for f in pages:
    t=open(f,encoding='utf-8').read()
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>',t,re.S):
        json.loads(m.group(1))
    for h in re.findall(r'(?:href|src)="(/[^"]*)"',t):
        if not exists(h): print('MISSING',f.replace(root,''),h); bad+=1
    for h in re.findall(r'srcset="([^"]*)"',t):
        for part in h.split(','):
            u=part.strip().split(' ')[0]
            if not exists(u): print('MISSING srcset',u); bad+=1
    imgs=re.findall(r'<img[^>]*>',t)
    for i in imgs:
        if 'alt=' not in i: print('NOALT',f,i[:80]); bad+=1
    n=len(re.findall(r'<h1',t))
    if n!=1: print('H1 count',f,n)
print('pages',len(pages),'problems',bad)
sys.exit(1 if bad else 0)
