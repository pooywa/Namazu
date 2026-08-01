import unittest

from sqlalchemy import create_engine,Select,text
from sqlalchemy.orm import Session
from app.database.db_manager import managedb
from app.database import configuration
from app.database.models import Earthquake

from app.analytics.convert_column_type import conver_to_float,convert_table_type
class TestRemoveDuplication(unittest.TestCase):

    def setUp(self):

        self.engine = create_engine("postgresql+psycopg://earthquakes_user:1234@localhost:5432/test_db_earthquakes")
        test_session = Session(self.engine)
        self.session = test_session
        configuration.session = test_session
        managedb.session = test_session
        Earthquake.metadata.create_all(self.engine)

    def test_convert_to_float(self):
        mod1 = Earthquake(
            time="2026-07-30 22:50:30",
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
            time="2026-07-14 11:37:32.2",
            latitude="32.600",
            longitude="130.700",
            depth="10.0",
            magnitude="3.0",
            place="KYUSHU, JAPAN",
            source="USGS"
        )
        managedb.create(mod1)

        convert_table_type()

        result = self.session.execute(text("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name='earthquakes'
        AND column_name='depth';
        """))

        self.assertEqual(result.first()[1],"double precision")




    def tearDown(self):
        self.session.close()
        Earthquake.metadata.drop_all(self.engine)
        self.engine.dispose()
