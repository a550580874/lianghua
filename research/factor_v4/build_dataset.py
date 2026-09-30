from pathlib import Path
import hashlib,json,pandas as pd,baostock as bs
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'data_foundation/output'; CACHE=ROOT/'data_foundation/cache/baostock'; DATA=OUT/'alpha158_full/parquet'; START,END='2017-07-01','2024-03-31'
def fetch(r):
    if str(r.error_code)!='0': raise RuntimeError(r.error_msg)
    return r.get_data()
def main():
    DATA.mkdir(parents=True,exist_ok=True); CACHE.mkdir(parents=True,exist_ok=True); login=bs.login()
    if str(login.error_code)!='0': raise SystemExit('BLOCKED_DOWNLOAD')
    try:
        snaps=[]; members=set()
        for dt in pd.date_range('2017-12-31','2024-03-31',freq='ME'):
            try: f=fetch(bs.query_hs300_stocks(date=dt.strftime('%Y-%m-%d')))
            except Exception: continue
            f['requested_date']=dt.strftime('%Y-%m-%d'); f['constituent_hash']=hashlib.sha256('|'.join(sorted(f.code.astype(str))).encode()).hexdigest()[:16]; snaps.append(f); members.update(f.code.astype(str))
        if snaps:
            h=pd.concat(snaps,ignore_index=True); h.to_csv(OUT/'csi300_snapshot_history.csv',index=False); h[['code','updateDate','requested_date']].drop_duplicates().rename(columns={'code':'instrument','updateDate':'snapshot_source_date'}).to_csv(OUT/'csi300_snapshot_derived_membership.csv',index=False); (OUT/'csi300_snapshot_analysis.md').write_text('# CSI300 snapshot analysis\n\nStatus: `SNAPSHOT_BASED_CSI300_RESEARCH_UNIVERSE`; updateDate retained; effective intervals not inferred.\n',encoding='utf-8')
        raw=[]; adj=[]
        for code in sorted(members):
            key=code.replace('.','_'); rp=CACHE/f'{key}_{START}_{END}_3.csv'; ap=CACHE/f'{key}_{START}_{END}_2.csv'; r=pd.read_csv(rp) if rp.exists() else fetch(bs.query_history_k_data_plus(code,'date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST',start_date=START,end_date=END,frequency='d',adjustflag='3')); a=pd.read_csv(ap) if ap.exists() else fetch(bs.query_history_k_data_plus(code,'date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST',start_date=START,end_date=END,frequency='d',adjustflag='2')); r.to_csv(rp,index=False) if not rp.exists() else None; a.to_csv(ap,index=False) if not ap.exists() else None; raw.append(r); adj.append(a)
        if raw: pd.concat(raw,ignore_index=True).to_parquet(DATA/'daily_price_raw.parquet',index=False); pd.concat(adj,ignore_index=True).to_parquet(DATA/'daily_price_adjusted.parquet',index=False); pd.DataFrame({'instrument':sorted(members)}).to_parquet(DATA/'research_membership.parquet',index=False)
        (OUT/'alpha158_full_build_metadata.json').write_text(json.dumps({'start':START,'end':END,'instrument_count':len(members),'universe_status':'SNAPSHOT_BASED_CSI300_RESEARCH_UNIVERSE'},indent=2),encoding='utf-8')
    finally: bs.logout()
if __name__=='__main__': main()
