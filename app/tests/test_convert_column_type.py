import unittest

from sqlalchemy import create_engine,Select,text
from sqlalchemy.orm import Session
from app.database.db_manager import managedb
from app.database import configuration
from app.database.models import Earthquake

from app.analytics.convert_column_type import conver_to_float,convert_table_type
class TestRemoveDuplication(unittest.TestCase):

    def setUp(self):

        engine = create_engine("sqlite:///:memory:")
        test_session = Session(engine)
        self.session = test_session
        configuration.session = test_session
        managedb.session = test_session
        Earthquake.metadata.create_all(engine)

    def test_convert_to_float(self):
        mod1 = Earthquake(
            time="2026-07-30 22:50:30 18 hr 15 min ago",
            latitude="32.600",
            longitude="130.700",
            depth="10",
            magnitude="3",
            place="KYUSHU, JAPAN",
            source="USGS"
        )
        managedb.create(mod1)

        conver_to_float()

        stmt = Select(Earthquake)
        earthquakes = managedb.read(stmt,"one")
        self.assertEqual(earthquakes.depth,"10.0")
        self.assertEqual(earthquakes.magnitude,"3.0")

    def test_change_column_type(self):
        mod1 = Earthquake(
            time="2026-07-30 22:50:30 18 hr 15 min ago",
            latitude="32.600",
            longitude="130.700",
            depth="10.0",
            magnitude="3.0",
            place="KYUSHU, JAPAN",
            source="USGS"
        )
        managedb.create(mod1)

        convert_table_type()

        result = self.session.execute(text("PRAGMA table_info(earthquakes)"))
        for s in result:
            print(s)

        # self.assertEqual(earthquakes.depth,"10.0")
        # self.assertEqual(earthquakes.magnitude,"3.0")




    def tearDown(self):
        return super().tearDown()
