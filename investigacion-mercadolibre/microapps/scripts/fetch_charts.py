import os
os.makedirs('cache',exist_ok=True)
import json,time,urllib.request,os
H={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64)'}
GEN={6000:'Negocios',6015:'Finanzas',6007:'Productividad',6002:'Utilidades',6012:'Estilo de vida',6013:'Salud y forma física',6017:'Educación',6024:'Compras',6023:'Comida y bebida',6020:'Medicina',6006:'Referencia',6003:'Viajes',6010:'Navegación',6008:'Foto y video'}
JOBS=[('topgrossingapplications',g) for g in GEN]+[('topfreeapplications',g) for g in (6000,6015,6007,6002,6012,6013)]
def get(url):
    for k in range(5):
        try: return urllib.request.urlopen(urllib.request.Request(url,headers=H),timeout=40).read()
        except Exception as e:
            print('retry',url[-60:],e,flush=True);time.sleep(25)
    return None
for kind,g in JOBS:
    f=f'cache/c_{kind}_{g}.json'
    if os.path.exists(f): continue
    r=get(f'https://itunes.apple.com/mx/rss/{kind}/limit=100/genre={g}/json')
    if r:
        d=json.loads(r);ents=d['feed'].get('entry',[])
        ids=[int(e['id']['attributes']['im:id']) for e in ents]
        json.dump(ids,open(f,'w'));print(kind,GEN[g],len(ids),flush=True)
    time.sleep(12)
# lookup
ids=set()
for f in os.listdir('cache'):
    if f.startswith('c_'): ids|=set(json.load(open('cache/'+f)))
ids=sorted(ids);print('ids únicos',len(ids),flush=True)
out={}
if os.path.exists('cache/lookup.json'): out=json.load(open('cache/lookup.json'))
todo=[i for i in ids if str(i) not in out]
for i in range(0,len(todo),100):
    chunk=todo[i:i+100]
    r=get('https://itunes.apple.com/lookup?country=mx&id='+','.join(map(str,chunk)))
    if r:
        for a in json.loads(r).get('results',[]): out[str(a['trackId'])]={k:a.get(k) for k in ('trackId','trackName','sellerName','primaryGenreName','averageUserRating','userRatingCount','price','formattedPrice','currentVersionReleaseDate','releaseDate','trackViewUrl','description','languageCodesISO2A')}
        json.dump(out,open('cache/lookup.json','w'),ensure_ascii=False);print('lookup',len(out),flush=True)
    time.sleep(12)
print('FIN',flush=True)
