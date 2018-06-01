import time
import unittest
import numpy as np

from screen import Screen
from ri import RabonaImage
from models import FIFAClub, FIFAPlayer
from parsers import RabonaParserA, RabonaParserE


class TestRI(unittest.TestCase):

    def test_init(self):
        t0 = time.time()
        print('\nTestRI | test_init starts at {}\n'.format(t0))
        f = 'src/test.jpg'
        ri = RabonaImage(f)
        t1 = time.time()
        print('time usage: {:.3f}s'.format(t1-t0))

        self.assertIsInstance(ri, RabonaImage)
        self.assertEqual(ri.filename, 'src/test')
        self.assertEqual(ri.suffix, '.jpg')

    def test_screen(self):
        t0 = time.time()
        print('\nTestRI | test_screen starts at {}\n'.format(t0))
        f = 'src/test.jpg'
        ri = RabonaImage(f)
        t1 = time.time()
        print('time usage: {:.3f}s'.format(t1-t0))

        self.assertIn('screen', ri.__dict__)
        self.assertIsInstance(ri.screen, Screen)
        self.assertIsInstance(ri.screen._raw, np.ndarray)
        self.assertEqual(len(ri.screen._raw[0]), 1080)
        self.assertEqual(len(ri.screen._raw), 561)
        self.assertEqual(len(ri.screen._raw[0]), ri.screen._raw_w)
        self.assertEqual(len(ri.screen._raw), ri.screen._raw_h)
        self.assertEqual(len(ri.screen.faces), 2)
        self.assertIsInstance(ri.screen.A, np.ndarray)
        self.assertIsInstance(ri.screen.E, np.ndarray)

    def test_parser_A(self):
        t0 = time.time()
        print('\nTestRI | test_parser starts at {}\n'.format(t0))
        f = 'src/test.jpg'
        ri = RabonaImage(f)
        t1 = time.time()
        print('time usage: {:.3f}s'.format(t1-t0))

        self.assertIn('A_parsed', ri.__dict__)
        self.assertIsInstance(ri.A_parsed, RabonaParserA)
        self.assertIn('_raw', ri.A_parsed.__dict__)
        self.assertIn('home', ri.A_parsed.__dict__)
        self.assertIn('away', ri.A_parsed.__dict__)
        self.assertIn('home_score', ri.A_parsed.__dict__)
        self.assertIn('away_score', ri.A_parsed.__dict__)
        self.assertIn('match_score', ri.A_parsed.__dict__)
        self.assertIn('match_result', ri.A_parsed.__dict__)

        self.assertIsInstance(ri.A_parsed.home, FIFAClub)
        self.assertEqual(ri.A_parsed.home.club_name, 'Real Madrid')
        self.assertEqual(ri.A_parsed.home.league, 'LaLiga Santander')
        self.assertIsInstance(ri.A_parsed.away, FIFAClub)
        self.assertEqual(ri.A_parsed.away.club_name, 'Liverpool')
        self.assertEqual(ri.A_parsed.away.league, 'Premier League')
        self.assertEqual(ri.A_parsed.home_score, '7')
        self.assertEqual(ri.A_parsed.away_score, '0')
        self.assertEqual(ri.A_parsed.match_score, '7 : 0')
        self.assertEqual(ri.A_parsed.match_result,
                         'Real Madrid 7 : 0 Liverpool')

    def test_parser_E(self):
        t0 = time.time()
        print('\nTestRI | test_parser starts at {}\n'.format(t0))
        f = 'src/test.jpg'
        ri = RabonaImage(f)
        t1 = time.time()
        print('time usage: {:.3f}s'.format(t1-t0))

        self.assertIn('E_parsed', ri.__dict__)
        self.assertIsInstance(ri.E_parsed, RabonaParserE)
        self.assertLessEqual(ri.E_parsed.state, 2)
        self.assertIn('_raw', ri.E_parsed.__dict__)
        self.assertIn('motm', ri.E_parsed.__dict__)
        self.assertTrue(ri.E_parsed.user_is_home)

        gb = FIFAPlayer(common_name='Gareth Bale')
        self.assertDictEqual(ri.E_parsed.motm.__dict__, gb.__dict__)
