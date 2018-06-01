import unittest

from models import dataminer, FIFAPlayer


class TestDataminer(unittest.TestCase):
    def test_player(self):
        player = dataminer.getPlayer('Gabriel Jesus')
        self.assertIsInstance(player, FIFAPlayer)
