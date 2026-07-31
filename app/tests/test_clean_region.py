import unittest
from app.database.clean_region import extract_region


class TestCleanRegion(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(extract_region("  tokyo  "), "Tokyo")
        self.assertEqual(extract_region("Near Osaka"), "Osaka")
        self.assertEqual(extract_region("Fukushima, Japan"), "Fukushima")
        self.assertEqual(extract_region("Chiba Prefecture"), "Chiba")
        self.assertEqual(extract_region("osaka"), "Osaka")


if __name__ == "__main__":
    unittest.main()
