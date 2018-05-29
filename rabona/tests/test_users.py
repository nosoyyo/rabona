import pickle
import unittest

from models import RabonaUser


class TestUser(unittest.TestCase):

    def test_init(self):
        print('\nTestUser | test_init \n')
        with open('tests/TeleUser', 'rb') as f:
            tele_user = pickle.load(f)
        ru = RabonaUser(tele_user)

        attrs = ['tele_id', 'first_name', 'last_name', 'username']
        for attr in attrs:
            self.assertIn(attr, ru.__dict__)
        self.assertEqual(ru.tele_id, 547562504)
        self.assertEqual(ru.first_name, 'Paul')
        self.assertEqual(ru.last_name, 'Carino')
        self.assertEqual(ru.username, 'paulcarino')

    def test_save(self):
        print('\nTestUser | test_save \n')
        with open('tests/TeleUser', 'rb') as f:
            tele_user = pickle.load(f)
        ru = RabonaUser(tele_user)
        ru.some_new_attr = 'Super cool user.'
        ru.save()  # False
        self.assertIsNotNone(ru.load(ru.tele_id, 'users'))
        doc_r = ru.load(ru.tele_id, 'users')
        self.assertIn('some_new_attr', doc_r.keys())
        self.assertEqual('Super cool user.', doc_r['some_new_attr'])
        del ru

        ru = RabonaUser(tele_user)
        self.assertIn('ObjectId', ru.__dict__)
        r_n = 'ObjectId' in ru.__dict__
        print('"ObjectId" in ru.__dict__: {}'.format(r_n))
        print('"ObjectId": {}'.format(ru.ObjectId))
        self.assertIsNotNone(ru.m.ls(ru.ObjectId, 'users'))
        self.assertEqual(ru.m.ls(ru.ObjectId, 'users'), ru.__dict__)
        self.assertIn('some_new_attr', ru.__dict__)
        self.assertEqual(ru.some_new_attr, 'Super cool user.')
