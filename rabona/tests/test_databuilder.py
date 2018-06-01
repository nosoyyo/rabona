import unittest

from models import databuilder, FIFAPlayer


class TestDataBuilder(unittest.TestCase):
    def test_player(self):
        player = databuilder.getPlayer('Gabriel Jesus')
        self.assertIsInstance(player, FIFAPlayer)
