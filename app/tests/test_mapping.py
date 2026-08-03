import unittest

from app.database.mapping import (
    map_row,
    detect_source,
    normalize_columns
)

import pandas as pd

class TestMapping(unittest.TestCase):

    def test_detect_source_usgs(self):
        self.assertEqual(
            detect_source("usgs-earthquakes.csv"),
            "USGS"
        )

    def test_detect_source_emsc(self):
        self.assertEqual(
            detect_source("emsc_data.csv"),
            "EMSC"
        )

    def test_detect_source_geofon(self):
        self.assertEqual(
            detect_source("GEOFON-raw.csv"),
            "GEOFON"
        )

    def test_detect_source_messy(self):
        self.assertEqual(
            detect_source("messy_dataset.csv"),
            "MESSY"
        )

    def test_detect_source_invalid(self):
        with self.assertRaises(ValueError):
            detect_source("unknown_file.csv")

    def test_normalize_columns(self):

        df = pd.DataFrame(
            [
                {
                    "DateTime": "2024-01-01",
                    "Latitude": "35.6",
                    "Longitude": "139.7",
                    "Magnitude": "4.5",
                    "Region": "Tokyo"
                }
            ]
        )

        result = normalize_columns(df)

        self.assertIn(
            "time",
            result.columns
        )

        self.assertIn(
            "latitude",
            result.columns
        )

        self.assertIn(
            "longitude",
            result.columns
        )

        self.assertIn(
            "mag",
            result.columns
        )

        self.assertIn(
            "place",
            result.columns
        )
    def test_map_row_success(self):

        row = {
            "time": "2024-01-01T00:00:00",
            "latitude": "35.6",
            "longitude": "139.7",
            "depth": "10",
            "mag": "4.5",
            "place": "Tokyo",
            "notes": ""
        }


        result = map_row(
            row,
            source="USGS",
            filename="usgs.csv"
        )


        self.assertEqual(
            result["time"],
            "2024-01-01T00:00:00"
        )

        self.assertEqual(
            result["latitude"],
            "35.6"
        )

        self.assertEqual(
            result["longitude"],
            "139.7"
        )

        self.assertEqual(
            result["depth"],
            "10"
        )

        self.assertEqual(
            result["magnitude"],
            "4.5"
        )

        self.assertEqual(
            result["place"],
            "Tokyo"
        )

        self.assertEqual(
            result["source"],
            "USGS"
        )


    def test_map_row_missing_column(self):

        row = {
            "time": "2024-01-01",
            "latitude": "35.6",
            "depth": "10",
            "mag": "4.5",
            "place": "Tokyo",
            "notes": ""
        }


        with self.assertRaises(ValueError) as error:

            map_row(
                row,
                source="USGS",
                filename="usgs.csv"
            )


        self.assertIn(
            "missing required column",
            str(error.exception)
        )


def test_map_row_unknown_source(self):

    row = {
        "DateTime": "2024",
        "Latitude": "35",
        "Longitude": "139",
        "Depth(km)": "10",
        "Magnitude": "4",
        "Notes": "",
        "Region": "Tokyo"
    }

    result = map_row(
        row,
        source="UNKNOWN",
        filename="unknown.csv"
    )

    self.assertEqual(
        result["source"],
        "UNKNOWN"
    )

    self.assertEqual(
        result["place"],
        "Tokyo"
    )
if __name__ == "__main__":
    unittest.main()
