import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parents[1]))
from adapter import aligned_inputs  # noqa: E402


class ExactTimingTests(unittest.TestCase):
    def test_weekend_and_horizon_entry_mapping(self):
        dates = pd.to_datetime(["2020-01-03", "2020-01-06", "2020-01-07", "2020-01-08", "2020-01-09", "2020-01-10", "2020-01-13"])
        frame = pd.DataFrame({"datetime": dates, "instrument": "A", "ROC20": range(7), "close": range(100, 107)})
        _, _, signal = aligned_inputs(frame, "ROC20", "2020-01-03", "2020-01-13", 5)
        row = signal.loc[signal.datetime == pd.Timestamp("2020-01-03")].iloc[0]
        self.assertEqual(row.entry_date, pd.Timestamp("2020-01-06"))
        self.assertEqual(row.exit_date, pd.Timestamp("2020-01-13"))
        self.assertNotEqual(row.entry_date, pd.Timestamp("2020-01-04"))

    def test_signal_value_survives_timestamp_shift(self):
        dates = pd.to_datetime(["2020-01-03", "2020-01-06", "2020-01-07", "2020-01-08"])
        frame = pd.DataFrame({"datetime": dates, "instrument": "A", "ROC20": [11, 22, 33, 44], "close": [10, 11, 12, 13]})
        _, _, signal = aligned_inputs(frame, "ROC20", "2020-01-03", "2020-01-08", 1)
        self.assertEqual(signal.loc[signal.datetime == pd.Timestamp("2020-01-03"), "ROC20"].iloc[0], 11)


if __name__ == "__main__":
    unittest.main()
