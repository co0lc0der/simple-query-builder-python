import unittest
from querybuilder import *

# test run
# python .\qb_views_unittest.py -v


class QBViewsTestCase(unittest.TestCase):
    def setUp(self):
        self.qb = QueryBuilder(DataBase(), ":memory:")
        self.maxDiff = None

    def test_create_view_empty_view_name(self):
        result = self.qb.create_view('')

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), True)
        self.assertEqual(result.get_error_message(), "Empty view_name in create_view method")

    def test_create_view_no_select(self):
        result = self.qb.delete('comments').where([['user_id', 10]]).create_view('users_no_email')

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), True)
        self.assertEqual(result.get_error_message(), "No select found in create_view method")

    def test_create_view_exists(self):
        result = self.qb.select('users').is_null('email').create_view('users_no_email')

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "CREATE VIEW IF NOT EXISTS `users_no_email` AS SELECT * FROM `users` WHERE (`email` IS NULL)")
        self.assertEqual(self.qb.get_params(), ())

    def test_create_view_no_exists(self):
        result = self.qb.select('users').is_null('email').create_view('users_no_email', False)

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "CREATE VIEW `users_no_email` AS SELECT * FROM `users` WHERE (`email` IS NULL)")
        self.assertEqual(self.qb.get_params(), ())

    def test_create_view(self):
        result = self.qb.select('users').where([['email', 'is null'], 'or', ['email', '']])\
               .create_view('users_no_email')

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "CREATE VIEW IF NOT EXISTS `users_no_email` AS SELECT * FROM `users` WHERE (`email` IS NULL) OR (`email` = '')")
        self.assertEqual(self.qb.get_params(), ('', ))

    def test_drop_view_no_exists(self):
        result = self.qb.drop_view('users_no_email', False)

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "DROP VIEW `users_no_email`")
        self.assertEqual(self.qb.get_params(), ())

    def test_drop_view_exists(self):
        result = self.qb.drop_view('users_no_email')

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "DROP VIEW IF EXISTS `users_no_email`")
        self.assertEqual(self.qb.get_params(), ())

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
