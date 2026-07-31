import unittest
from app.database.mapping import map_row, detect_source, TARGET_COLUMNS


class TestMapping(unittest.TestCase):

    def test_detect_source_usgs(self):
        self.assertEqual(detect_source("usgs-earthquakes.csv"), "USGS")

    def test_detect_source_emsc(self):
        self.assertEqual(detect_source("emsc_data.csv"), "EMSC")

    def test_detect_source_geofon(self):
        self.assertEqual(detect_source("GEOFON-raw.csv"), "GEOFON")

    def test_detect_source_messy(self):
        self.assertEqual(detect_source("messy_dataset.csv"), "MESSY")

    def test_detect_source_invalid(self):
        with self.assertRaises(ValueError):
            detect_source("unknown.csv")

    def test_map_row_ok(self):
        row = {
            "DateTime": "2024-01-01T00:00:00",
            "Latitude": "35.6",
            "Longitude": "139.7",
            "Depth(km)": "10.0",
            "Magnitude": "4.5",
            "Notes": "",
            "Region": "Tokyo",
        }
        mapped = map_row(row, source="USGS", filename="usgs.csv")

        self.assertEqual(mapped["time"], "2024-01-01T00:00:00")
        self.assertEqual(mapped["latitude"], "35.6")
        self.assertEqual(mapped["magnitude"], "4.5")
        self.assertEqual(mapped["place"], "Tokyo")
        self.assertEqual(mapped["source"], "USGS")

    def test_map_row_missing_column(self):
        row = {
            "DateTime": "2024-01-01T00:00:00",
            "Latitude": "35.6",
            # Longitude missing
            "Depth(km)": "10.0",
            "Magnitude": "4.5",
            "Notes": "",
            "Region": "Tokyo",
        }
        with self.assertRaises(ValueError) as cm:
            map_row(row, source="USGS", filename="usgs.csv")

        self.assertIn("missing required column", str(cm.exception))
        self.assertIn("Longitude", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
