from unittest.mock import patch  # allows us to sim whether db is ready or not

from django.core.management import call_command  # call command in source
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""

        # Patch will mock the behaviour of the assigned task
        # we mock this function by returning trye, which simulates the
        # return value of the assigned task. We can also use this to monitor
        # how often this command is called
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # patch has the ability to raise 'sideeffects' which are
            # side effects to the function that we are mocking
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
