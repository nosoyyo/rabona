import unittest
from bson.objectid import ObjectId

from models.ru import RabonaUser
from models.base import RabonaModel


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
