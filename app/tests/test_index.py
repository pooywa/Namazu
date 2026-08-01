import unittest

from sqlalchemy import text
from app.database.db_manager import managedb
from app.database.create_indexes import main
from app.database.models import Earthquake


class TestIndex(unittest.TestCase):

    
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        test_session = Session(engine)
        configuration.session = test_session
        managedb.session = test_session
        Earthquake.metadata.create_all(managedb.engine)

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