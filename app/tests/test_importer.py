import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from app.database.importer import import_one_file
from app.database import configuration
from app.database.models import Earthquake


class TestEarthquakeImporter(unittest.TestCase):

    def setUp(self):

        self.engine = create_engine(
            "postgresql+psycopg://earthquakes_user:1234@localhost:5432/test_db_earthquakes"
        )

        self.session = Session(self.engine)

        configuration.engine = self.engine

        Earthquake.metadata.create_all(self.engine)


        self.temp_dir = tempfile.TemporaryDirectory()

        self.test_csv_path = (
            Path(self.temp_dir.name) / "test_earthquake.csv"
        )


        data = pd.DataFrame({
            "time": [
                "2025-09-15T12:45:30.123Z",
                "2025-09-16T08:22:05.456Z",
                "Sep 17, 2025, 14:10:05"
            ],
            "latitude": [
                38.322,
                36.2048,
                43.0618
            ],
            "longitude": [
                142.369,
                138.2529,
                141.3545
            ],
            "depth": [
                35.0,
                43.0,
                10.2
            ],
            "mag": [
                5.1,
                2.3,
                4.8
            ],
            "place": [
                "off east coast of Honshu, Japan",
                "near Nagano, Japan",
                "Hokkaido, Japan region"
            ],
            "notes": [
                None,
                "Minor shock",
                None
            ]
        })


        data.to_csv(
            self.test_csv_path,
            index=False
        )

    @patch("app.database.importer.detect_source")
    @patch("app.database.importer.MAPPINGS")
    def test_import_one_file(self,mock_mappings, mock_detect_source):
        mock_detect_source.return_value = "irsc"

        mock_mappings.get.return_value = {
            "time": "time",
            "latitude": "latitude",
            "longitude": "longitude",
            "depth": "depth",
            "mag": "magnitude",
            "place": "place",
            "notes": "notes",
        }

        imported_rows = import_one_file(
            self.test_csv_path
        )


        self.assertEqual(
            imported_rows,
            3
        )


        result = self.session.execute(
            text("SELECT COUNT(*) FROM earthquakes")
        )

        count = result.scalar_one()


        self.assertEqual(
            count,
            3
        )


    def tearDown(self):

        self.session.close()

        Earthquake.metadata.drop_all(
            self.engine
        )

        self.engine.dispose()

        self.temp_dir.cleanup()



if __name__ == "__main__":
    unittest.main()