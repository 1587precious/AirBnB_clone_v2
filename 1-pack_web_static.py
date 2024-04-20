import unittest
import MySQLdb
from models import storage
from models.state import State
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch

class TestMySQLStorage(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Set up MySQL connection and create necessary tables."""
        cls.connection = MySQLdb.connect(host='localhost',
                                          user='hbnb_test',
                                          passwd='hbnb_test_pwd',
                                          db='hbnb_test_db',
                                          charset='utf8')
        cls.cursor = cls.connection.cursor()
        cls.cursor.execute("DROP TABLE IF EXISTS states")
        cls.cursor.execute("CREATE TABLE states (id VARCHAR(60) NOT NULL, name VARCHAR(128), PRIMARY KEY (id))")
        cls.connection.commit()
        cls.connection.close()

    @classmethod
    def tearDownClass(cls):
        """Close MySQL connection."""
        cls.connection.close()

    def setUp(self):
        """Set up a clean database before each test."""
        self.connection = MySQLdb.connect(host='localhost',
                                           user='hbnb_test',
                                           passwd='hbnb_test_pwd',
                                           db='hbnb_test_db',
                                           charset='utf8')
        self.cursor = self.connection.cursor()
        self.cursor.execute("DELETE FROM states")
        self.connection.commit()

    def tearDown(self):
        """Close MySQL connection after each test."""
        self.connection.close()

    def test_create_state_command(self):
        """Test if the create State command adds a new record in the states table."""
        # Get initial count of records in the states table
        initial_count = self._get_record_count()

        # Execute the console command
        with patch('sys.stdout', new=StringIO()) as fake_out:
            HBNBCommand().onecmd("create State name=\"California\"")

        # Get count of records in the states table after executing the command
        final_count = self._get_record_count()

        # Check if the difference is +1
        self.assertEqual(final_count - initial_count, 1)

    def _get_record_count(self):
        """Helper method to get the number of records in the states table."""
        self.cursor.execute("SELECT COUNT(*) FROM states")
        count = self.cursor.fetchone()[0]
        return count

if __name__ == '__main__':
    unittest.main()

