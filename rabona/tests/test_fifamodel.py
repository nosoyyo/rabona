import unittest
from bson.objectid import ObjectId

from models import FIFAModel


class TestFIFAModel(unittest.TestCase):

    fm = FIFAModel(test_attr='test')

    def test_init(self):
        print('\nTestModel | test_init \n')

    def test_create(self):
        # fm = FIFAModel(test_attr='test')
        self.assertEqual(self.fm.test_attr, 'test')

    def test_add_attr(self):
        # fm = FIFAModel(test_attr='test')
        self.fm.test_extra_attr = 'extra'
        self.assertTrue(bool(self.fm.save()))

    def test_oid(self):
        # fm = FIFAModel(test_attr='test')
        self.assertIsInstance(self.fm.ObjectId, ObjectId)
        self.fm.some_more_extra_attr = 'supra'
        self.assertTrue(bool(self.fm.save()))

    def test_load(self):
        # fm = FIFAModel(test_attr='test')
        doc = self.fm.load()
        doc['ObjectId'] = doc['_id']
        doc.pop('_id')
        self.assertEqual(self.fm.__dict__, doc)

    def test_rm(self):
        # fm = FIFAModel(test_attr='test')
        self.assertTrue(self.fm.m.rm(self.fm.ObjectId))


if __name__ == '__main__':
    unittest.main()
