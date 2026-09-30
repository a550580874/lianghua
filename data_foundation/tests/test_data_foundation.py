import json
import os
import unittest
from data_foundation.probe_tushare import run_probe
try:
    import pandas as pd
    from data_foundation.validate_data import duplicate_keys, ohlc_violations
except ModuleNotFoundError:
    pd = None

class DataFoundationTests(unittest.TestCase):
    def test_missing_token_and_no_secret(self):
        old = os.environ.pop("TUSHARE_TOKEN", None)
        try:
            result = run_probe()
            self.assertEqual(result["status"], "BLOCKED_CREDENTIAL")
            self.assertNotIn("[REDACTED]", json.dumps(result))
        finally:
            if old is not None: os.environ["TUSHARE_TOKEN"] = old

    def test_schema_quality(self):
        if pd is None: self.skipTest("pandas is required for local data checks")
        frame = pd.DataFrame({"instrument": ["A", "A"], "trade_date": ["2024-01-02", "2024-01-03"], "open": [1, 2], "high": [2, 3], "low": [1, 2], "close": [2, 3], "volume": [1, 2], "amount": [1, 2]})
        self.assertEqual(duplicate_keys(frame), 0)
        self.assertEqual(ohlc_violations(frame), 0)

    def test_invalid_rows_detected(self):
        if pd is None: self.skipTest("pandas is required for local data checks")
        frame = pd.DataFrame({"instrument": ["A", "A"], "trade_date": ["2024-01-02", "2024-01-02"], "open": [1, 1], "high": [0, 1], "low": [2, 1], "close": [2, 1], "volume": [1, -1], "amount": [1, 1]})
        self.assertEqual(duplicate_keys(frame), 1)
        self.assertEqual(ohlc_violations(frame), 2)

if __name__ == "__main__": unittest.main()
