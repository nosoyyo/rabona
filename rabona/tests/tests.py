import pickle
import unittest
from bson.objectid import ObjectId
from telegram.user import User as TeleUser

from models.ru import RabonaUser
from models.rm import RabonaMatch
from models.base import RabonaModel
from utils.pipeline import MongoDBPipeline


class TestModel(unittest.TestCase):

    def test_init(self):
        print('\nTestModel | test_init \n')
        rm = RabonaModel(test_attr='test')
        self.assertEqual(rm.test_attr, 'test')
        rm.test_extra_attr = 'extra'
        self.assertTrue(bool(rm.save()))

        self.assertIsInstance(rm.ObjectId, ObjectId)
        rm.some_more_extra_attr = 'supra'
        self.assertTrue(bool(rm.save()))

        doc = rm.load()
        doc.pop('_id')
        self.assertEqual(rm.__dict__, doc)

        self.assertTrue(rm.m.rm(rm.ObjectId))


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


class TestPipeline(unittest.TestCase):
    '''
    All the collection param here should implicitly be `m.col`
    '''

    def test_init(self):
        print('\nTestPipeline | test_init \n')
        m = MongoDBPipeline()

        self.assertEqual(m.auth, True)

    def test_CRUD(self):
        m = MongoDBPipeline()

        print('\nTestPipeline | test_create \n')
        doc = {'as a test doc': 'i perform well'}
        oid = m.insert(doc)
        self.assertIsInstance(oid, ObjectId)

        print('\nTestPipeline | test_retrieve \n')
        doc_r = m.ls(oid)
        self.assertEqual(doc_r, doc)

        print('\nTestPipeline | test_update \n')
        extra = {'memento': 'mori'}
        test_doc = {'as a test doc': 'i perform well', 'memento': 'mori'}
        self.assertTrue(m.update(oid, extra))
        doc_r = m.ls(oid)
        doc_r.pop('_id')
        self.assertEqual(doc_r, test_doc)

        print('\nTestPipeline | test_delete \n')
        m.rm(oid)
        self.assertIsNone(m.ls(oid))


if __name__ == '__main__':
    unittest.main()
