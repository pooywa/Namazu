import unittest
from unittest.mock import patch, MagicMock
from app.analytics.fill_data_to_earthquakes import add_label_of_category, add_rigion_finder

class TestFillDataToEarthkes(unittest.TestCase):
    @patch("app.analytics.fill_data_to_earthquakes.managedb")
    def test_add_label_of_category(self,mock_managedb):
        mock_eq1 = MagicMock(magnitude=3.5) #weak
        mock_eq2 = MagicMock(magniyude=5.0) #moderate
        mock_eq3 = MagicMock(magnitude=6.5) #strong
        
        #call read to return fake list
        mock_managedb.read.return_value = [mock_eq1, mock_eq2, mock_eq3]
        
        add_label_of_category()
        
        #check result
        self.assertEqual(mock_eq1.category, "Weak")
        self.assertEqual(mock_eq2.category, "Moderate")
        self.assertEqual(mock_eq3.category, "Strong")
        
        self.assertEqual(mock_managedb.update.call_count, 3)
        
    @patch("app.analytics.fill_data_to_earthquakes.managedb")
    def test_add_rigion_finder_with_comma(self, mock_managedb):
        
        mock_eq = MagicMock(place="10 km NNE of x, Japen") # ino check konin data
        mock_managedb.read.return_value = [mock_eq]
        self.assertEqual(mock_eq.region, "name of city") #check
        mock_managedb.update.assert_called_once_with(mock_eq)


        add_rigion_finder()
        
if __name__ == "__main__":
    unittest.main()