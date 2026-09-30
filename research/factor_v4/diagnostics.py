import pandas as pd
def coverage(frame): return pd.DataFrame({'valid_observations':frame.notna().sum(),'missing_observations':frame.isna().sum(),'coverage_ratio':frame.notna().mean()})
def sanity(frame): return pd.DataFrame({'finite_ratio':frame.apply(lambda s: pd.to_numeric(s,errors='coerce').replace([float('inf'),float('-inf')],pd.NA).notna().mean()),'unique_count':frame.nunique(dropna=True)})
