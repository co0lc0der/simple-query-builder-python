import unittest
from querybuilder import *

# test run
# python .\qb_views_unittest.py -v


class QBViewsTestCase(unittest.TestCase):
    def setUp(self):
        self.qb = QueryBuilder(DataBase(), ":memory:")

    def test_sql_create_view_exists(self):
        sql = self.qb.select('users').is_null('email').create_view('users_no_email').get_sql()
        self.assertEqual(sql, "CREATE VIEW IF NOT EXISTS `users_no_email` AS SELECT * FROM `users` WHERE (`email` IS NULL)")
        self.assertEqual(self.qb.get_params(), ())

    def test_sql_create_view_no_exists(self):
        sql = self.qb.select('users').is_null('email').create_view('users_no_email', False).get_sql()
        self.assertEqual(sql, "CREATE VIEW `users_no_email` AS SELECT * FROM `users` WHERE (`email` IS NULL)")
        self.assertEqual(self.qb.get_params(), ())

    def test_sql_create_view(self):
        sql = self.qb.select('users').where([['email', 'is null'], 'or', ['email', '']])\
               .create_view('users_no_email').get_sql()
        self.assertEqual(sql, "CREATE VIEW IF NOT EXISTS `users_no_email` AS SELECT * FROM `users` WHERE (`email` IS NULL) OR (`email` = '')")
        self.assertEqual(self.qb.get_params(), ('', ))
        # self.qb.go()

    def test_sql_drop_view_no_exists(self):
        sql = self.qb.drop_view('users_no_email', False).get_sql()
        self.assertEqual(sql, "DROP VIEW `users_no_email`")

    def test_sql_drop_view_exists(self):
        sql = self.qb.drop_view('users_no_email').get_sql()
        self.assertEqual(sql, "DROP VIEW IF EXISTS `users_no_email`")


if __name__ == "__main__":
    unittest.main()
