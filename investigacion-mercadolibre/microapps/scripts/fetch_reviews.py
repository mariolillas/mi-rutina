import os
os.makedirs('cache',exist_ok=True)
import json,time,urllib.request,os,sys
H={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64)'}
def fetch(app_id,pages=5):
    f=f'cache/r_{app_id}.json'
    if os.path.exists(f): return json.load(open(f))
    out=[]
    for p in range(1,pages+1):
        url=f'https://itunes.apple.com/mx/rss/customerreviews/page={p}/id={app_id}/sortby=mostrecent/json'
        ok=False
        for k in range(3):
            try:
                d=json.loads(urllib.request.urlopen(urllib.request.Request(url,headers=H),timeout=30).read())
                ok=True;break
            except Exception as e:
                time.sleep(6)
        if not ok: break
        ents=d.get('feed',{}).get('entry',[])
        if isinstance(ents,dict): ents=[ents]
        got=0
        for e in ents:
            if 'im:rating' not in e: continue
            out.append({'r':int(e['im:rating']['label']),'t':e.get('title',{}).get('label',''),'c':e.get('content',{}).get('label',''),'v':e.get('im:version',{}).get('label',''),'d':e.get('updated',{}).get('label','')[:10]})
            got+=1
        if got==0: break
        time.sleep(1.5)
    json.dump(out,open(f,'w'),ensure_ascii=False)
    return out
if __name__=='__main__':
    sl=json.load(open(sys.argv[1]))
    for niche in sl:
        for a in niche['apps']:
            r=fetch(a['id']);print(niche['term'],a['name'],len(r),flush=True)
    print('FIN',flush=True)
