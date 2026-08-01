import unittest

from sqlalchemy import create_engine,Select
from sqlalchemy.orm import Session
from app.database.db_manager import managedb
from app.database import configuration
from app.database.models import Earthquake

from app.analytics.remove_dublication import remove_dublicate_records
class TestRemoveDuplication(unittest.TestCase):

    def setUp(self):

        engine = create_engine("sqlite:///:memory:")
        test_session = Session(engine)
        configuration.session = test_session
        managedb.session = test_session
        Earthquake.metadata.create_all(engine)

    def test_remove_duplicatoin(self):
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
            time="2026-07-30 22:50:30 18 hr 15 min ago",
            latitude="32.600",
            longitude="130.700",
            depth="10",
            magnitude="3.3",
            place="KYUSHU, JAPAN",
            source="USGS"
        )
        managedb.create(mod1)
        managedb.create(mod2)

        remove_dublicate_records()

        stmt = Select(Earthquake)
        earthquakes = managedb.read(stmt,"all")
        self.assertEqual(len(earthquakes),1)




    def tearDown(self):
        return super().tearDown()
