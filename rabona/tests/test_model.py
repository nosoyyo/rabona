import unittest
from bson.objectid import ObjectId

from models import RabonaModel


class TestModel(unittest.TestCase):

    rm = RabonaModel(test_attr='test')

    def test_init(self):
        print('\nTestModel | test_init \n')

    def test_create(self):
        # rm = RabonaModel(test_attr='test')
        self.assertEqual(self.rm.test_attr, 'test')

    def test_add_attr(self):
        # rm = RabonaModel(test_attr='test')
        self.rm.test_extra_attr = 'extra'
        self.assertTrue(bool(self.rm.save()))

    def test_oid(self):
        # rm = RabonaModel(test_attr='test')
        self.assertIsInstance(self.rm.ObjectId, ObjectId)
        self.rm.some_more_extra_attr = 'supra'
        self.assertTrue(bool(self.rm.save()))

    def test_load(self):
        # rm = RabonaModel(test_attr='test')
        doc = self.rm.load()
        doc['ObjectId'] = doc['_id']
        doc.pop('_id')
        self.assertEqual(self.rm.__dict__, doc)

    def test_rm(self):
        # rm = RabonaModel(test_attr='test')
        self.assertTrue(self.rm.m.rm(self.rm.ObjectId))


if __name__ == '__main__':
    unittest.main()
