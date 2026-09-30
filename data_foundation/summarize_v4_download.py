import json
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]; CACHE=ROOT/'data_foundation/cache/baostock'; OUT=ROOT/'research/factor_v4/output'
def main():
 state=json.loads((CACHE/'checkpoint.json').read_text()) if (CACHE/'checkpoint.json').exists() else {}; rows=[]
 for instrument,e in state.items():
  raw=e.get('raw',{}); adj=e.get('adjusted',{}); rows.append({'instrument':instrument,'raw_status':raw.get('status','MISSING'),'raw_rows':raw.get('row_count',0),'adjusted_status':adj.get('status','MISSING'),'adjusted_rows':adj.get('row_count',0),'retry_count':int(raw.get('status')!='COMPLETE')+int(adj.get('status')!='COMPLETE'),'last_error_type':raw.get('error_type') or adj.get('error_type')})
 pd.DataFrame(rows).to_csv(OUT/'market_download_summary.csv',index=False)
 print(len(rows),sum(r['raw_status']=='COMPLETE' and r['adjusted_status']=='COMPLETE' for r in rows))
if __name__=='__main__': main()
