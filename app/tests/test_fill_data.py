import unittest
from unittest.mock import patch, MagicMock
from app.analytics.fill_data_to_earthquakes import add_label_of_category, add_rigion_finder
from app.database import configuration
from app.database.db_manager import managedb
from sqlalchemy import create_engine,Select
from sqlalchemy.orm import Session
from app.database.models import Earthquake

class TestFillDataToEarthkes(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("postgresql+psycopg://earthquakes_user:1234@localhost:5432/test_db_earthquakes")
        test_session = Session(self.engine)
        print("test_session",test_session)
        self.session = test_session
        configuration.session = test_session
        managedb.session = test_session
        Earthquake.metadata.create_all(self.engine)

    # @patch("app.analytics.fill_data_to_earthquakes.managedb")
    def test_add_label_of_category(self):
        # mock_eq1 = MagicMock(magnitude=5.12) #weak
        # mock_eq2 = MagicMock(magnitude=8.10) #moderate
        # mock_eq3 = MagicMock(magnitude=3.5) #strong
        # mock_eq1.category = "Weak"
        # mock_eq2.category = "Moderate"
        # mock_eq3.category = "Strong"

        #call read to return fake list
        # mock_managedb.read.return_value = [mock_eq1, mock_eq2, mock_eq3]
        
        # add_label_of_category()
        
        #check result

        # self.assertEqual(mock_eq1.category, "Weak")
        # self.assertEqual(mock_eq2.category, "Moderate")
        # self.assertEqual(mock_eq3.category, "Strong")
        
        # self.assertEqual(mock_managedb.update.call_count, 3)
        mod1 = Earthquake(
            time="2026-07-30 22:50:30 18 hr 15 min ago",
            latitude="32.600",
            longitude="130.700",
            depth="10",
            magnitude=6.3, #strong
            place="KYUSHU, JAPAN",
            source="USGS"
        )
        mod2 = Earthquake(
            time="2026-07-30 22:50:30 18 hr 15 min ago",
            latitude="32.600",
            longitude="130.700",
            depth="10",
            magnitude=5.3, #moderate
            place="KYUSHU, JAPAN",
            source="USGS"
        )
        managedb.create(mod1)
        managedb.create(mod2)

        mod3 = Earthquake(
            time="2026-07-30 22:50:30 18 hr 15 min ago",
            latitude="32.600",
            longitude="130.700",
            depth="10",
            magnitude=3.3, #weak
            place="KYUSHU, JAPAN",
            source="USGS"
        )
        managedb.create(mod3)

        add_label_of_category()

        stmt = Select(Earthquake).where(Earthquake.magnitude == "3.3")
        earth_weak = managedb.read(stmt,"one")

        stmt = Select(Earthquake).where(Earthquake.magnitude == "5.3")
        earth_moderate = managedb.read(stmt,"one")

        stmt = Select(Earthquake).where(Earthquake.magnitude == "6.3")
        earth_strong = managedb.read(stmt,"one")

        self.assertEqual(earth_weak.category,"Weak")
        self.assertEqual(earth_moderate.category,"Moderate")
        self.assertEqual(earth_strong.category,"Strong")
        
    def test_add_rigion_finder_with_comma(self):

        mod1 = Earthquake(
            time="2026-07-30 22:50:30 18 hr 15 min ago",
            latitude="32.600",
            longitude="130.700",
            depth="10",
            magnitude=6.3, #strong
            place="KYUSHU, JAPAN",
            source="USGS"
        )
        
        managedb.create(mod1)

        add_rigion_finder()

        stmt = Select(Earthquake)
        earth_place = managedb.read(stmt,"one")

        self.assertEqual(earth_place.region, "kyushu") #check


    def tearDown(self):
        self.session.close()
        Earthquake.metadata.drop_all(self.engine)
        self.engine.dispose()
        
if __name__ == "__main__":
    unittest.main()