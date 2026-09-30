import json,glob,os,re,math,statistics,datetime as dt
from terms import TERMS
TODAY=dt.date(2026,9,30)
STOP=set("de la el en para y del los las con por un una al app apps mi tu".split())
def slug(s): return re.sub(r'[^a-z0-9]+','_',s.lower())
def clip(x,a=0,b=100): return max(a,min(b,x))
def toks(term): return [t for t in re.findall(r'[a-záéíóúñü]+',term.lower()) if t not in STOP and len(t)>3]
def relevant(app,term):
    tk=toks(term);text=(app.get('trackName','')+' '+app.get('description','')[:700]).lower()
    hits=sum(1 for t in tk if t[:max(4,len(t)-2)] in text)
    return hits>=max(1,math.ceil(len(tk)*0.6))
def months_since(iso):
    try:
        d=dt.date.fromisoformat(iso[:10]);return (TODAY-d).days/30.4
    except Exception: return None
def main():
    rows=[]
    for grupo,term in TERMS:
        f=f'cache/s_{slug(term)}.json'
        if not os.path.exists(f): continue
        d=json.load(open(f))
        apps=[a for a in d.get('results',[]) if a.get('kind')=='software']
        rel=[a for a in apps if relevant(a,term)]
        for a in rel: a['_m']=months_since(a.get('currentVersionReleaseDate',''))
        cnt=lambda a:a.get('userRatingCount',0) or 0
        top10=rel[:10]
        demand_sum=sum(cnt(a) for a in top10)
        big=[a for a in rel if cnt(a)>=300]
        tot=sum(cnt(a) for a in big)
        wr=(sum((a.get('averageUserRating') or 0)*cnt(a) for a in big)/tot) if tot else None
        stale=(sum(1 for a in big if (a['_m'] or 0)>12)/len(big)) if big else None
        n1k=sum(1 for a in rel if cnt(a)>=1000); n10k=sum(1 for a in rel if cnt(a)>=10000)
        def age_m(a):
            try: return (TODAY-dt.date.fromisoformat(a.get('releaseDate','')[:10])).days/30.4
            except Exception: return 999
        n_new=sum(1 for a in rel if age_m(a)<=12); n_new_tiny=sum(1 for a in rel if age_m(a)<=12 and cnt(a)<20)
        lead=sorted(rel,key=cnt,reverse=True)[:3]
        dem=clip(20*(math.log10(max(demand_sum,1))-2))
        weak=clip((4.6-wr)/(4.6-3.4)*100) if wr else 0
        sta=(stale or 0)*100
        neg=0.6*weak+0.4*sta
        comp=clip(0.7*clip(n1k/6*100)+0.3*clip(n_new/8*100))
        opp=round(0.40*dem+0.35*neg+0.25*(100-comp))
        rows.append(dict(grupo=grupo,term=term,n_api=len(apps),n_rel=len(rel),n1k=n1k,n10k=n10k,n_new=n_new,n_new_tiny=n_new_tiny,demand_sum=demand_sum,
            rating_w=round(wr,2) if wr else None,stale=round(stale,2) if stale is not None else None,
            dem=round(dem),neg=round(neg),comp=round(comp),opp=opp,
            leaders=[dict(id=a['trackId'],name=a['trackName'][:50],seller=a.get('sellerName',''),rating=round(a.get('averageUserRating') or 0,2),n=cnt(a),meses=round(a['_m']) if a.get('_m') is not None else None,price=a.get('formattedPrice'),url=a.get('trackViewUrl','').split('?')[0]) for a in lead]))
    rows.sort(key=lambda r:-r['opp'])
    json.dump(rows,open('niches.json','w'),ensure_ascii=False,indent=1)
    print(f"{'opp':>3} {'dem':>3} {'neg':>3} {'cmp':>3} {'rel':>3} {'1k':>3} {'new':>3} {'rat':>4} {'stl':>4} {'sumratings':>10}  nicho  | líder")
    for r in rows:
        l=r['leaders'][0] if r['leaders'] else {}
        print(f"{r['opp']:>3} {r['dem']:>3} {r['neg']:>3} {r['comp']:>3} {r['n_rel']:>3} {r['n1k']:>3} {r['n_new']:>3} {str(r['rating_w']):>4} {str(r['stale']):>4} {r['demand_sum']:>10}  {r['term']} | {l.get('name','')} ({l.get('n','')}, {l.get('rating','')}★)")


if __name__=='__main__':
    main()
