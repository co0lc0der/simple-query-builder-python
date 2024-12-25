import unittest
from querybuilder import *

# test run
# python .\qb_delete_unittest.py -v


class QBDeleteTestCase(unittest.TestCase):
    def setUp(self):
        self.qb = QueryBuilder(DataBase(), ":memory:")

    def test_sql_delete_eq(self):
        sql = self.qb.delete('comments').where([['user_id', '=', 10]]).get_sql()
        self.assertEqual(sql, "DELETE FROM `comments` WHERE (`user_id` = 10)")
        self.assertEqual(self.qb.get_params(), (10, ))

    def test_sql_delete_no_eq(self):
        sql = self.qb.delete('comments').where([['user_id', 10]]).get_sql()
        self.assertEqual(sql, "DELETE FROM `comments` WHERE (`user_id` = 10)")
        self.assertEqual(self.qb.get_params(), (10, ))

    # def test_sql_delete_limit_eq(self):
    #     sql = self.qb.delete('users').where([['name', '=', 'John']]).limit().get_sql()
    #     self.assertEqual(sql, "DELETE FROM `users` WHERE (`name` = 'John') LIMIT 1")
    #     self.assertEqual(self.qb.get_params(), ('John',))
    #
    # def test_sql_delete_limit_no_eq(self):
    #     sql = self.qb.delete('users').where([['name', 'John']]).limit().get_sql()
    #     self.assertEqual(sql, "DELETE FROM `users` WHERE (`name` = 'John') LIMIT 1")
    #     self.assertEqual(self.qb.get_params(), ('John',))


if __name__ == "__main__":
    unittest.main()
