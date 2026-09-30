import os
os.makedirs('cache',exist_ok=True)
import json,time,urllib.request,urllib.parse,os,re,sys
from terms import TERMS
LAST=['conteo de calorías','ayuno intermitente','rutina de gimnasio','embarazo semanas','seguimiento de hábitos','tareas escolares','examen de admisión','vocabulario inglés','cuidado de mascotas','lista de compras','recetas de cocina','verificación vehicular','hoy no circula']
PRIO=sorted(TERMS,key=lambda gt:(gt[1] in LAST))
TERMS=PRIO
H={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) research-script'}
def slug(s): return re.sub(r'[^a-z0-9]+','_',s.lower())
done=0
for g,t in TERMS:
    f=f'cache/s_{slug(t)}.json'
    if os.path.exists(f): continue
    url='https://itunes.apple.com/search?'+urllib.parse.urlencode({'term':t,'country':'mx','entity':'software','limit':30,'lang':'es_mx'})
    for k in range(5):
        try:
            r=urllib.request.urlopen(urllib.request.Request(url,headers=H),timeout=30).read()
            d=json.loads(r);json.dump(d,open(f,'w'),ensure_ascii=False);break
        except Exception as e:
            print('retry',t,e,flush=True);time.sleep(25)
    done+=1;print(done,t,flush=True)
    time.sleep(11.0)
print('FIN',flush=True)
