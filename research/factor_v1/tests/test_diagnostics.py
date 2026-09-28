import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parents[1]))
from diagnostics import (  # noqa: E402
    distribution_stats,
    factor_correlation_rows,
    horizon_returns,
    rank_autocorrelation_series,
    spread_stats,
)


class DiagnosticsTests(unittest.TestCase):
  def test_distribution_uses_daily_sample_statistics(self):
    result = distribution_stats([1.0, 2.0, 3.0])
    self.assertAlmostEqual(result["std"], 1.0)
    self.assertAlmostEqual(result["standard_error"], 1 / (3**0.5))
    self.assertAlmostEqual(result["t_stat"], 2 * (3**0.5))
    self.assertAlmostEqual(result["positive_ratio"], 1.0)
    self.assertAlmostEqual(result["negative_ratio"], 0.0)


  def test_rank_autocorrelation_aligns_instruments_not_rows(self):
    frame = pd.DataFrame({
        "datetime": pd.to_datetime(["2020-01-01"] * 3 + ["2020-01-02"] * 3),
        "instrument": ["A", "B", "C", "C", "A", "B"],
        "factor": [1.0, 2.0, 3.0, 30.0, 10.0, 20.0],
    })
    self.assertAlmostEqual(rank_autocorrelation_series(frame, "factor").iloc[0], 1.0)


  def test_daily_spread_statistics_are_not_aggregate_spread_statistics(self):
    frame = pd.DataFrame({
        "datetime": pd.to_datetime(["2020-01-01"] * 5 + ["2020-01-02"] * 5),
        "instrument": list("ABCDE") * 2,
        "factor": [1, 2, 3, 4, 5] * 2,
        "forward_return": [1, 1, 1, 1, 5, 2, 2, 2, 2, 4],
    })
    result = spread_stats(frame, "factor")
    self.assertAlmostEqual(result["spread_mean"], 3.0)
    self.assertAlmostEqual(result["spread_std"], 2**0.5)
    self.assertEqual(result["observation_days"], 2)


  def test_horizon_return_does_not_cross_split_boundary(self):
    frame = pd.DataFrame({
        "datetime": pd.to_datetime(["2020-01-01", "2020-01-02", "2020-01-03", "2020-01-04"]),
        "instrument": ["A"] * 4,
        "close": [10.0, 11.0, 12.0, 13.0],
        "factor": [1.0] * 4,
    })
    result = horizon_returns(frame, "2020-01-01", "2020-01-03", 1)
    self.assertEqual(result["datetime"].dt.strftime("%Y-%m-%d").tolist(), ["2020-01-01"])
    self.assertAlmostEqual(result["forward_return_h"].iloc[0], 12 / 11 - 1)


  def test_factor_correlation_is_long_format_with_diagonal(self):
    frame = pd.DataFrame({
        "datetime": pd.to_datetime(["2020-01-01"] * 3 + ["2020-01-02"] * 3),
        "A": [1, 2, 3, 2, 4, 6],
        "B": [3, 2, 1, 6, 4, 2],
    })
    result = pd.DataFrame(factor_correlation_rows(frame, ["A", "B"], "train"))
    self.assertEqual(len(result), 8)
    self.assertTrue((result[result.factor_a == result.factor_b].mean_correlation == 1.0).all())


if __name__ == "__main__":
    unittest.main()
