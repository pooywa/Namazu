import unittest


from app.analytics.analytics import (
    earthquakes_by_month,
    region_stats,
    top_10_recent,
    total_records
)

class TestAnalytics(unittest.TestCase):

    def test_earthquakes_by_month(self):
        rows = earthquakes_by_month()
        self.assertIsInstance(rows, list)
        
    def test_region_stats(self):
        rows = region_stats()
        self.assertIsInstance(rows, list)
    
    def test_top_10_recent(self):
        rows = top_10_recent()
        self.assertIsInstance(rows, list)
        self.assertLessEqual(len(rows), 10)
        
    def test_total_records(self):
        total = total_records()
        self.assertGreaterEqual(total, 0)

if __name__ == "__main__":
    unittest.main()
