import unittest

from models import databuilder, FIFAClub, FIFAPlayer


class TestDataBuilder(unittest.TestCase):

    def test_magic(self):
        print('\nTestDataBuilder | test_magic \n')
        phrase = '1T9e6¥8ˆk'
        self.assertEqual(phrase, databuilder.readMagic(
            databuilder.magic(phrase)))

    def test_player(self):
        print('\nTestDataBuilder | test_player \n')
        player = databuilder.getPlayer('Gabriel Jesus')
        self.assertIsInstance(player, FIFAPlayer)

    def test_getClubs(self):
        print('\nTestDataBuilder | test_getClubs \n')
        clubs = databuilder.getClubs('LaLiga Santander')
        self.assertEqual(20, len(clubs))
        for club in clubs:
            self.assertEqual(club['league'], 'LaLiga Santander')

    def test_getPlayers(self):
        print('\nTestDataBuilder | test_getPlayers \n')
        players = databuilder.getPlayers('Atlético Madrid')
        self.assertIsInstance(players, list)
        self.assertEqual(18, len(list(set(players))))
        AM = FIFAClub(name='Atlético Madrid')
        for player in players:
            self.assertIn(player, AM.players)

    def test_getPlayer(self):
        print('\nTestDataBuilder | test_getPlayer \n')
        gb = databuilder.getPlayer('Gareth Bale')
        self.assertIsInstance(gb, FIFAPlayer)
        self.assertIn('common_name', gb.__dict__)
        self.assertIn('dob', gb.__dict__)
        self.assertIn('foot', gb.__dict__)
        self.assertIn('full_name', gb.__dict__)
        self.assertIn('height', gb.__dict__)
        self.assertIn('intl_rep', gb.__dict__)
        self.assertIn('origin', gb.__dict__)
        self.assertIn('photo', gb.__dict__)
        self.assertIn('position', gb.__dict__)
        self.assertIn('weight', gb.__dict__)

        self.assertEqual(gb.common_name, 'Gareth Bale')
        self.assertEqual(gb.dob, '16-07-1989')
        self.assertEqual(gb.foot, 'Left')
        self.assertEqual(gb.full_name, 'Gareth Bale')
        self.assertEqual(gb.height, '183')
        self.assertEqual(gb.intl_rep, '4')
        self.assertEqual(gb.position, 'RW')
        self.assertEqual(gb.weight, '74')
