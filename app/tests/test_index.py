import unittest

from sqlalchemy import text,create_engine
from sqlalchemy.orm import Session
from app.database.db_manager import managedb
from app.database import configuration
from app.analytics.add_index import main
from app.database.models import Earthquake


class TestIndex(unittest.TestCase):

    
    def setUp(self):
        # engine = create_engine("sqlite:///:memory:")
        # test_session = Session(engine)
        # configuration.session = test_session
        # managedb.session = test_session
        # Earthquake.metadata.create_all(engine)
        self.engine = create_engine("postgresql+psycopg://earthquakes_user:1234@localhost:5432/test_db_earthquakes")
        test_session = Session(self.engine)
        self.session = test_session
        configuration.session = test_session
        managedb.session = test_session
        Earthquake.metadata.create_all(self.engine)

    def test_indexes_created(self):

        earthquake = Earthquake(
            region="Japan",
            magnitude=5.5,
            time="2025-01-01 10:00:00",
            
        )

        managedb.create(earthquake)

        main()

        result = managedb.session.execute(
            text("""
                SELECT indexname
                FROM pg_indexes
                WHERE tablename = 'earthquakes';
            """)
        )

        indexes = [row.indexname for row in result]

        self.assertIn("idx_earthquakes_region", indexes)
        self.assertIn("idx_earthquakes_time", indexes)
        self.assertIn("idx_earthquakes_magnitude", indexes)

    def tearDown(self):
        self.session.close()
        Earthquake.metadata.drop_all(self.engine)
        self.engine.dispose()