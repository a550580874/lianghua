import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parents[1]))
from adapter import aligned_inputs  # noqa: E402


class AdapterTests(unittest.TestCase):
    def setUp(self):
        dates = pd.to_datetime(["2020-01-03", "2020-01-06", "2020-01-07", "2020-01-08", "2020-01-09"])
        self.frame = pd.DataFrame({
            "datetime": list(dates) * 2,
            "instrument": ["A"] * 5 + ["B"] * 5,
            "ROC20": list(range(5)) + list(range(10, 15)),
            "close": [10, 11, 12, 13, 14, 20, 21, 22, 23, 24],
        })

    def test_signal_maps_to_next_observed_trading_date(self):
        factor, prices, signal = aligned_inputs(self.frame, "ROC20", "2020-01-03", "2020-01-09", 1)
        self.assertIn(pd.Timestamp("2020-01-06"), factor.index.get_level_values("entry_date"))
        friday = signal[signal.datetime == pd.Timestamp("2020-01-03")]
        self.assertTrue((friday.entry_date == pd.Timestamp("2020-01-06")).all())
        self.assertNotIn(pd.Timestamp("2020-01-04"), factor.index.get_level_values("entry_date"))

    def test_horizon_uses_entry_plus_h_and_preserves_values(self):
        factor, _, signal = aligned_inputs(self.frame, "ROC20", "2020-01-03", "2020-01-09", 1)
        original = self.frame.set_index(["datetime", "instrument"])["ROC20"]
        mapped = signal.set_index(["datetime", "instrument"])["ROC20"]
        self.assertTrue(mapped.equals(original.loc[mapped.index]))
        self.assertTrue((signal.exit_date > signal.entry_date).all())
        self.assertEqual(factor.loc[(pd.Timestamp("2020-01-06"), "A")], 0)

    def test_split_boundary_excludes_signal_without_complete_exit(self):
        _, _, signal = aligned_inputs(self.frame, "ROC20", "2020-01-03", "2020-01-07", 1)
        self.assertNotIn(pd.Timestamp("2020-01-07"), signal.datetime.unique())


if __name__ == "__main__":
    unittest.main()
