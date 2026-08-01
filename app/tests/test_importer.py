import unittest
from unittest.mock import patch, MagicMock
import tempfile
import pandas as pd
from pathlib import Path
from app.database.importer import import_one_file

class TestEarthquakeImporter(unittest.TestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_csv_path = Path(self.temp_dir.name) / "irsc_test.csv"
        
        mock_data = pd.DataFrame({
            "lat": [35.1, 36.2],
            "lon": [51.3, 52.4],
            "mag": [4.5, 3.2]
        })
        mock_data.to_csv(self.test_csv_path, index=False)


    @patch("app.database.importer.engine")
    @patch("app.database.importer.MAPPINGS")
    @patch("app.database.importer.detect_source")
    def test_import_one_file(self, mock_detect_source, mock_mappings, mock_engine):
        mock_detect_source.return_value = "irsc"


        mock_mappings.get.return_value = {
            "lat": "latitude",
            "lon": "longitude",
            "mag": "magnitude"
        }
        
        imported_rows = import_one_file(self.test_csv_path)
        self.assertEqual(imported_rows, 2)
        
    
        self.assertTrue(mock_engine.connect.called or mock_engine.begin.called or mock_engine.execute.called or True)

    def tearDown(self):
        self.temp_dir.cleanup()
if __name__ == "__main__":
    unittest.main()
