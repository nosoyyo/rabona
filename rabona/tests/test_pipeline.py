import unittest
from bson.objectid import ObjectId

from utils.pipeline import MongoDBPipeline


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
