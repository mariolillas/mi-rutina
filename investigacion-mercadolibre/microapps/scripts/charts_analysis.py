import json,os,datetime as dt
GEN={6000:'Negocios',6015:'Finanzas',6007:'Productividad',6002:'Utilidades',6012:'Estilo de vida',6013:'Salud y forma física',6017:'Educación',6024:'Compras',6023:'Comida y bebida',6020:'Medicina',6006:'Referencia',6003:'Viajes',6010:'Navegación',6008:'Foto y video'}
TODAY=dt.date(2026,9,30)
lk=json.load(open('cache/lookup.json'))
def info(i):
    a=lk.get(str(i));return a
def row(rank,a):
    if not a: return f"  {rank:>3}. (sin datos)"
    m=(TODAY-dt.date.fromisoformat(a['currentVersionReleaseDate'][:10])).days//30 if a.get('currentVersionReleaseDate') else -1
    return f"  {rank:>3}. {a['trackName'][:40]:40} | {str(a.get('sellerName',''))[:24]:24} | {a.get('userRatingCount') or 0:>7} | {a.get('averageUserRating') or 0:.2f} | {a.get('formattedPrice')}"
def show(kind,top=12):
    for g,n in GEN.items():
        f=f'cache/c_{kind}_{g}.json'
        if not os.path.exists(f): continue
        ids=json.load(open(f));print(f'\n## {kind} · {n}')
        for k,i in enumerate(ids[:top],1): print(row(k,info(i)))
if __name__=='__main__':
    import sys
    show('topgrossingapplications',int(sys.argv[1]) if len(sys.argv)>1 else 12)
    print('\n\n=== POPULARES PERO MAL CALIFICADAS (≥1,500 calificaciones y ≤4.2★) ===')
    seen={}
    for f in os.listdir('cache'):
        if not f.startswith('c_'): continue
        kind,g=f[2:-5].rsplit('_',1)
        for k,i in enumerate(json.load(open('cache/'+f)),1):
            a=info(i)
            if a and (a.get('userRatingCount') or 0)>=1500 and (a.get('averageUserRating') or 5)<=4.2:
                seen.setdefault(i,[]).append(f"{kind.replace('applications','')}:{GEN.get(int(g),g)}#{k}")
    for i,w in sorted(seen.items(),key=lambda kv:-(info(kv[0]).get('userRatingCount') or 0)):
        a=info(i);print(f"{a['trackName'][:38]:38} | {str(a.get('sellerName',''))[:22]:22} | {a['userRatingCount']:>7} | {a['averageUserRating']:.2f} | {', '.join(w[:3])}")
