import unittest

from sqlalchemy import create_engine,Select,text
from sqlalchemy.orm import Session
from app.database.db_manager import managedb
from app.database import configuration
from app.database.models import Earthquake

from app.analytics.handel_null_invalid import handel_date_format,not_be_nigative,remove_dublications_and_invalid_data
class TestRemoveDuplication(unittest.TestCase):

    def setUp(self):

        self.engine = create_engine("postgresql+psycopg://earthquakes_user:1234@localhost:5432/test_db_earthquakes")
        test_session = Session(self.engine)
        self.session = test_session
        configuration.session = test_session
        managedb.session = test_session
        Earthquake.metadata.create_all(self.engine)

    def test_handel_date_format(self):
        mod1 = Earthquake(
            time="2026-07-30 17:17:39 18 hr 15 min ago",
            latitude="32.600",
            longitude="130.700",
            depth="10",
            magnitude="3",
            place="KYUSHU, JAPAN",
            source="USGS"
        )
        managedb.create(mod1)

        handel_date_format()

        stmt = Select(Earthquake)
        earthquakes = managedb.read(stmt,"one")

        self.assertEqual(earthquakes.time,"2026-07-30 20:47:39+03:30")

    def test_not_be_nigative(self):
        mod1 = Earthquake(
            time="2026-07-14 11:37:32.2",
            latitude="32.600",
            longitude="130.700",
            depth="-10",
            magnitude="3.0",
            place="KYUSHU, JAPAN",
            source="USGS"
        )
        managedb.create(mod1)

        not_be_nigative()

        stmt = Select(Earthquake)
        earthquakes = managedb.read(stmt,"one")

        self.assertEqual(earthquakes.depth,"10")

    def test_remove_duplication_with_nots(self):
        mod1 = Earthquake(
            time="2026-07-14 11:37:32.2",
            latitude="32.600",
            longitude="130.700",
            depth="-10",
            magnitude="3.0",
            place="KYUSHU, JAPAN",
            source="USGS",
            notes="DUPLICATE"

        )
        managedb.create(mod1)

        mod2 = Earthquake(
            time="2026-07-14 11:37:32.2",
            latitude="32.600",
            longitude="130.700",
            depth="-10",
            magnitude="3.0",
            place="KYUSHU, JAPAN",
            source="USGS",
            notes="Possible Duplicate"

        )
        managedb.create(mod2)

        mod3 = Earthquake(
            time="2026-07-14 11:37:32.2",
            latitude="32.600",
            longitude="130.700",
            depth="-10",
            magnitude="3.0",
            place="KYUSHU, JAPAN",
            source="USGS"
        )
        managedb.create(mod3)

        remove_dublications_and_invalid_data()

        stmt = Select(Earthquake)
        earthquakes = managedb.read(stmt,"all")

        self.assertEqual(len(earthquakes),1)



    def tearDown(self):
        self.session.close()
        Earthquake.metadata.drop_all(self.engine)
        self.engine.dispose()