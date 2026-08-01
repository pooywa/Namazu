import unittest
from unittest.mock import patch, ANY

from app.analytics.combine_region_and_category import grouping, main

class TestCombineRegionAndCategory(unittest.TestCase):

    @patch("app.analytics.combine_region_and_category.managedb")
    def test_grouping(self, mock_managedb):
       
        expected = [
            ("08", "city", "Strong", 7, 6.1, 18.2),  #tof to alzaimer name city benevis
            ("08", "city", "Moderate", 3, 4.8, 15.0), # bala ro bekhon
        ]
        mock_managedb.read.return_value = expected

        result = grouping()
        # Ignore the exact SQL query (first argument); only verify that "all_row"
        # is passed as the second argument.
        self.assertEqual(result, expected)
        mock_managedb.read.assert_called_once_with(ANY, "all_row")

    @patch("app.analytics.combine_region_and_category.grouping")
    @patch("builtins.print")
    def test_main(self, mock_print, mock_grouping):
        mock_grouping.return_value = [
            ("08", "x", "Strong", 7, 6.1, 18.2),  # x mishe name city
        ]

        main()


        self.assertTrue(mock_print.called)
        # mock_print.assert_called_once()
        # self.assertIn("month, category, region, earthquake_count", mock_print.call_args[0][0])

    @patch("app.analytics.combine_region_and_category.grouping")
    def test_main_raises_on_key_error(self, mock_grouping):
        mock_grouping.side_effect = KeyError("all_row")
        with self.assertRaises(KeyError):
            main()

if __name__ == "__main__":
    unittest.main()
