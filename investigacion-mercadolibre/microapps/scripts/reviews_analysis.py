import json,re,collections,sys,os,datetime as dt
BUCKETS={
 'anuncios':r'anuncio|publicidad|propaganda',
 'cobros y suscripción':r'suscripci|cobr|caro|pagar|de pago|premium|cancelar|precio|dólares|dolares',
 'fallas':r'no funciona|falla|error|se cierra|cierra sola|\bbug|lento|traba|no abre|no carga|se congela|deja de funcionar|no sirve',
 'pierde datos o no sincroniza':r'perd[ií]|respaldo|backup|sincroniz|se borr|borr[oó]|desapare|recuper',
 'falta una función':r'falta|no tiene|no permite|no deja|no puedo|sería bueno|seria bueno|agreguen|agregar|añadir|necesito|quisiera|me gustaría|me gustaria|ojalá|ojala|debería|deberia|exportar|excel|pdf|whatsapp',
 'soporte':r'soporte|atenci[oó]n al cliente|no responden|nadie responde|no contestan|sin respuesta',
 'cuenta o registro':r'iniciar sesi|registro|contraseña|verificaci|cuenta|correo|login|no me deja entrar',
 'complicada':r'complica|confus|dif[ií]cil|no entiendo|no se entiende|poco intuitiv',
 'solo en inglés o dólares':r'ingl[eé]s|d[oó]lares|traducci|español|en otro idioma',
}
STOP=set("de la el en y a que los las un una es no me mi se con por para lo al del su muy mas más pero como ya si le te mis tu está esta esto este son fue ser hay sin sus han son nos les qué q yo app aplicación aplicacion".split())
def words(t): return [w for w in re.findall(r"[a-záéíóúñü]+",t.lower())]
def analyze(revs):
    low=[x for x in revs if x['r']<=3]
    n=len(revs);nl=len(low)
    res={'n':n,'n_bajas':nl,'pct_bajas':round(100*nl/n) if n else 0,'rating':round(sum(x['r'] for x in revs)/n,2) if n else None,'buckets':{},'frases':[],'citas':{}}
    for b,rx in BUCKETS.items():
        hit=[x for x in low if re.search(rx,(x['t']+' '+x['c']).lower())]
        res['buckets'][b]=round(100*len(hit)/nl) if nl else 0
        ex=[x for x in hit if 40<=len(x['c'])<=220]
        ex.sort(key=lambda x:-len(x['c']))
        res['citas'][b]=[dict(r=x['r'],t=x['c'].replace('\n',' ').strip(),d=x['d']) for x in ex[:2]]
    # frases de 2 palabras en reseñas bajas
    bi=collections.Counter()
    for x in low:
        w=[t for t in words(x['t']+' '+x['c'])]
        for i in range(len(w)-1):
            a,b=w[i],w[i+1]
            if a in STOP or b in STOP or len(a)<3 or len(b)<3: continue
            bi[a+' '+b]+=1
    res['frases']=[k for k,v in bi.most_common(14) if v>=3]
    return res
if __name__=='__main__':
    niches=json.load(open(sys.argv[1]))
    out={}
    for nn in niches:
        allr=[];per=[]
        for a in nn['apps']:
            f=f"cache/r_{a['id']}.json"
            if not os.path.exists(f): continue
            r=json.load(open(f));allr+=r;per.append(dict(id=a['id'],name=a['name'],**{k:v for k,v in analyze(r).items() if k in('n','pct_bajas','rating')}))
        out[nn['term']]=dict(apps=per,**analyze(allr))
    json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False,indent=1)
    for t,o in out.items():
        print('\n##',t,o['n'],'reseñas |',o['pct_bajas'],'% de 1-3★ | rating',o['rating'])
        print('  quejas %:',{k:v for k,v in sorted(o['buckets'].items(),key=lambda kv:-kv[1]) if v})
        print('  frases:',', '.join(o['frases'][:10]))
