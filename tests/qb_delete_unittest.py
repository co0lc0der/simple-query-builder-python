import unittest
from querybuilder import *

# test run
# python .\qb_delete_unittest.py -v


class QBDeleteTestCase(unittest.TestCase):
    def setUp(self):
        self.qb = QueryBuilder(DataBase(), ":memory:")
        self.maxDiff = None

    def test_delete_empty_table(self):
        result = self.qb.delete('')

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), True)
        self.assertEqual(result.get_error_message(), "Empty table in delete method")

    def test_delete_table_as_str(self):
        result = self.qb.delete('comments')

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "DELETE FROM `comments`")
        self.assertEqual(result.get_params(), ())

    def test_delete_table_as_dict(self):
        result = self.qb.delete({'g': 'groups'})

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "DELETE FROM `groups` AS `g`")
        self.assertEqual(result.get_params(), ())

    def test_delete_where_eq(self):
        result = self.qb.delete('comments').where([['user_id', '=', 10]])

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "DELETE FROM `comments` WHERE (`user_id` = 10)")
        self.assertEqual(result.get_params(), (10, ))

    def test_delete_where_no_eq(self):
        result = self.qb.delete('comments').where([['user_id', 10]])

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "DELETE FROM `comments` WHERE (`user_id` = 10)")
        self.assertEqual(result.get_params(), (10, ))

    def test_delete_limit_eq(self):
        result = self.qb.delete('users').where([['name', '=', 'John']]).limit()

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        if self.qb.get_driver() == 'sqlite':
            self.assertEqual(result.get_sql(), "DELETE FROM `users` WHERE (`name` = 'John')")
        else:
            self.assertEqual(result.get_sql(), "DELETE FROM `users` WHERE (`name` = 'John') LIMIT 1")
        self.assertEqual(result.get_params(), ('John',))

    def test_delete_limit_no_eq(self):
        result = self.qb.delete('users').where([['name', 'John']]).limit()

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        if self.qb.get_driver() == 'sqlite':
            self.assertEqual(result.get_sql(), "DELETE FROM `users` WHERE (`name` = 'John')")
        else:
            self.assertEqual(result.get_sql(), "DELETE FROM `users` WHERE (`name` = 'John') LIMIT 1")
        self.assertEqual(result.get_params(), ('John',))

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
