import unittest

from sqlalchemy import create_engine,Select
from sqlalchemy.orm import Session
from app.database.db_manager import managedb
from app.database import configuration
from app.database.models import Earthquake

from app.analytics.remove_dublication import remove_dublicate_records
class TestRemoveDuplication(unittest.TestCase):

    def setUp(self):

        self.engine = create_engine("postgresql+psycopg://earthquakes_user:1234@localhost:5432/test_db_earthquakes")
        test_session = Session(self.engine)
        self.session = test_session
        configuration.session = test_session
        managedb.session = test_session
        Earthquake.metadata.create_all(self.engine)

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
        self.session.close()
        Earthquake.metadata.drop_all(self.engine)
        self.engine.dispose()
