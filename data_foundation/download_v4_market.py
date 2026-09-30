"""Checkpointed per-instrument market downloader using BaoStockSessionManager."""
import json, os, tempfile
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
import baostock as bs
from data_foundation.baostock_session import BaoStockSessionManager
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'data_foundation/output'; CACHE=ROOT/'data_foundation/cache/baostock'; START,END='2017-07-01','2024-03-31'; FIELDS='date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST'
def atomic(frame,path):
 path.parent.mkdir(parents=True,exist_ok=True); fd,tmp=tempfile.mkstemp(dir=path.parent,suffix='.tmp'); os.close(fd)
 try: frame.to_parquet(tmp,index=False); pd.read_parquet(tmp); os.replace(tmp,path)
 finally:
  if os.path.exists(tmp): os.unlink(tmp)
def main():
 hist=pd.read_csv(OUT/'csi300_snapshot_history.csv'); instruments=sorted(hist.code.astype(str).unique()); (OUT/'research_universe_instruments.txt').write_text('\n'.join(instruments)+'\n'); cp=CACHE/'checkpoint.json'; state=json.loads(cp.read_text()) if cp.exists() else {}; CACHE.mkdir(parents=True,exist_ok=True); m=BaoStockSessionManager(bs)
 try: m.login()
 except Exception: raise SystemExit('BLOCKED_DOWNLOAD')
 try:
  for n,code in enumerate(instruments,1):
   e=state.setdefault(code,{})
   for flag,label in [('3','raw'),('2','adjusted')]:
    dest=CACHE/label/(code.replace('.','').upper()+'.parquet')
    if e.get(label,{}).get('status')=='COMPLETE' and dest.exists(): continue
    try:
     r=m.request(bs.query_history_k_data_plus,code,FIELDS,start_date=START,end_date=END,frequency='d',adjustflag=flag)
     if m.classify(r)!='OK': raise RuntimeError(m.classify(r))
     atomic(r.get_data(),dest); e[label]={'status':'COMPLETE','row_count':len(r.get_data()),'completed_at':datetime.now(timezone.utc).isoformat(),'error_type':None}
    except Exception as exc: e[label]={'status':'RETRYABLE_FAILED','row_count':0,'completed_at':None,'error_type':type(exc).__name__}
   cp.write_text(json.dumps(state,indent=2)); print(f'completed={n}/{len(instruments)}')
 finally: m.logout()
if __name__=='__main__': main()
