import unittest
from app.database.models import Earthquake




class TestEarthquakeModel(unittest.TestCase):

    def test_table_columns(self):

        cols = {c.name for c in Earthquake.__table__.columns}
        EXPECTED_COLUMNS = {'id', 'category', 'region', 'source', 'latitude', 'time', 'notes', 'longitude', 'magnitude', 'depth', 'month', 'place'}
        self.assertEqual(cols,EXPECTED_COLUMNS)

    # def test_numeric_types(self):
    #     cols = {c.name: str(c.type) for c in Earthquake.__table__.columns}
    #     self.assertIn("FLOAT", cols["depth"])
    #     self.assertIn("FLOAT", cols["magnitude"])
    #     self.assertIn("DATETIME", cols["time"])


if __name__ == "__main__":
    unittest.main()
