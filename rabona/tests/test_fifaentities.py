import unittest
from bson.objectid import ObjectId

from models import FIFALeague, FIFAClub, FIFAPlayer


class TestFIFALeague(unittest.TestCase):
    def test_init(self):
        print('\nTestFIFALeague | test_init \n')
        liga = FIFALeague(name='laliga santa')
        self.assertIsInstance(liga, FIFALeague)
        self.assertEqual(liga.league_name, 'LaLiga Santander')
        self.assertEqual(20, len(liga.clubs))


class TestFIFAClub(unittest.TestCase):
    def test_init(self):
        print('\nTestFIFAClub | test_init \n')
        club = FIFAClub(name='manchest utd')
        self.assertIsInstance(club, FIFAClub)
        self.assertIn('club_name', club.__dict__)
        self.assertIn('club_url', club.__dict__)
        self.assertIn('club_logo', club.__dict__)
        self.assertIn('league', club.__dict__)
        self.assertIn('ObjectId', club.__dict__)
        self.assertIn('players', club.__dict__)

        self.assertEqual(len(club.players), 37)
        self.assertIsInstance(club.ObjectId, ObjectId)


class TestFIFAPlayer(unittest.TestCase):

    def test_init(self):
        print('\nTestFIFAPlayer | test_init \n')
        gj = FIFAPlayer(common_name='Gabriel Jesus')
        self.assertIsInstance(gj, FIFAPlayer)
        self.assertIn('height', gj.__dict__)
        self.assertIn('intl_rep', gj.__dict__)
        self.assertIn('position', gj.__dict__)
        self.assertIn('dob', gj.__dict__)
        self.assertIn('common_name', gj.__dict__)
        self.assertIn('weight', gj.__dict__)
        self.assertIn('full_name', gj.__dict__)
        self.assertIn('foot', gj.__dict__)
        self.assertIn('nation', gj.__dict__)
