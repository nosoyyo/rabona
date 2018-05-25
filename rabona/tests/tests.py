import pickle
import unittest
from bson.objectid import ObjectId
from telegram.user import User as TeleUser

from models.ru import RabonaUser
from models.base import RabonaModel
from utils.pipeline import MongoDBPipeline


class TestModel(unittest.TestCase):

    def test_init(self):
        rm = RabonaModel(test_attr='test')
        self.assertEqual(rm.test_attr, 'test')
        rm.test_extra_attr = 'extra'
        rm.save()
        self.assertIsInstance(rm.ObjectId, ObjectId)
        rm.some_more_extra_attr = 'supra'
        self.assertEqual(rm.save(), True)

        doc = rm.load()
        doc.pop('_id')
        self.assertEqual(rm.__dict__, doc)


if __name__ == '__main__':
    unittest.main()


class TestUser(unittest.TestCase):

    def test_init(self):
        with open('tests/TeleUser', 'rb') as f:
            tele_user = pickle.load(f)
        ru = RabonaUser(tele_user)

        attrs = ['tele_id', 'is_new', 'first_name', 'last_name', 'username']
        for attr in attrs:
            self.assertIn(attr, ru.__dict__)
        self.assertEqual(ru.tele_id, 547562504)
        self.assertEqual(ru.is_new, False)
        self.assertEqual(ru.first_name, 'Paul')
        self.assertEqual(ru.last_name, 'Carino')
        self.assertEqual(ru.username, 'paulcarino')

    def test_save(self):
        with open('tests/TeleUser', 'rb') as f:
            tele_user = pickle.load(f)
        ru = RabonaUser(tele_user)
        ru.some_new_attr = 'Super cool user.'
        ru.save()
        del ru
        ru = RabonaUser(tele_user)
        self.assertIn('some_new_attr', ru.__dict__)
        self.assertEqual(ru.some_new_attr, 'Super cool user.')


class TestPipeline(unittest.TestCase):
    '''
    All the collection param here should implicitly be `self.m.col`
    '''

    def test_init(self):
        self.m = MongoDBPipeline()
        self.doc = {'as a test doc': 'i perform well'}
        self.extra = {'memento': 'mori'}
        self.test_doc = {'as a test doc': 'i perform well', 'memento': 'mori'}
        self.assertEqual(self.m.auth, True)

    def create(self):
        self.oid = self.m.insert(self.doc)
        self.assertIsInstance(self.oid, ObjectId)

    def retrieve(self):
        doc_r = self.m.ls(self.oid)
        self.assertEqual(doc_r, self.doc)

    def update(self):
        self.assertEqual(self.m.update(self.oid, self.extra))
        self.assertEqual(self.m.ls(self.oid), self.test_doc)

    def delete(self):
        self.m.rm(self.oid)
        self.assertListEqual(self.m.ls(self.oid), [])
