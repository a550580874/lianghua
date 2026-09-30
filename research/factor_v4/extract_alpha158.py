from pathlib import Path
import json,qlib
from qlib.config import REG_CN
from qlib.contrib.data.handler import Alpha158
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'research/factor_v4/output'; PROVIDER=ROOT/'data_foundation/output/alpha158_full/qlib_bin'
def main():
 OUT.mkdir(parents=True,exist_ok=True); qlib.init(provider_uri=str(PROVIDER),region=REG_CN); meta=json.loads((ROOT/'data_foundation/output/alpha158_full_build_metadata.json').read_text()); h=Alpha158(instruments='all',start_time='2018-01-01',end_time='2024-03-31'); f=h.fetch(col_set='feature'); f.to_parquet(OUT/'alpha158_features.parquet'); f.notna().sum().to_csv(OUT/'alpha158_coverage.csv'); f.isna().sum().to_csv(OUT/'alpha158_sanity.csv'); (OUT/'alpha158_metadata.json').write_text(json.dumps({**meta,'feature_count':len(f.columns),'rows':len(f),'volume_semantics':'VOLUME_SEMANTICS_PARTIAL'},indent=2))
if __name__=='__main__': main()
