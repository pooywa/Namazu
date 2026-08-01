import unittest

from sqlalchemy import create_engine,Select
from sqlalchemy.orm import Session
from app.database.db_manager import managedb
from app.database import configuration
from app.database.models import Earthquake

class TestRemoveDuplication(unittest.TestCase):

    def setUp(self):

        engine = create_engine("sqlite:///:memory:")
        test_session = Session(engine)
        configuration.session = test_session
        managedb.session = test_session
        Earthquake.metadata.create_all(engine)

    def test_remove_duplicatoin(self):
        print("config session",configuration.session)
        print("managedb sesison",managedb.session)

        mod1 = Earthquake(
            time="2026-07-30 22:50:30 18 hr 15 min ago",
            latitude="32.600",
            longitude="130.700",
            depth="10",
            magnitude="3.3",
            place="KYUSHU, JAPAN",
            source="USGS"
        )
        mod2 = Earthquake(
            time="2026-08-30 22:50:30 18 hr 15 min ago",
            latitude="31.600",
            longitude="10.00",
            depth="10.32",
            magnitude="11.3",
            place="kuni, JAPAN",
            source="USGS"
        )
        managedb.create(mod1)
        managedb.create(mod2)

        stmt = Select(Earthquake)
        earthquakes = managedb.read(stmt,"all")
        self.assertEqual(len(earthquakes),2)




    def tearDown(self):
        return super().tearDown()
