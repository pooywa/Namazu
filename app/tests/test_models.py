import unittest
from app.database.models import Earthquake


EXPECTED_COLUMNS = {"id", "time", "latitude", "longitude", "depth", "magnitude", "source", "place"}


class TestEarthquakeModel(unittest.TestCase):

    @classmethod
    def test_table_columns(self):
        cols = {c.name for c in Earthquake.__table__.columns}
        self.assertEqual(cols, EXPECTED_COLUMNS)

    def test_numeric_types(self):
        cols = {c.name: str(c.type) for c in Earthquake.__table__.columns}
        self.assertIn("FLOAT", cols["depth"])
        self.assertIn("FLOAT", cols["magnitude"])
        self.assertIn("DATETIME", cols["time"])


if __name__ == "__main__":
    unittest.main()
