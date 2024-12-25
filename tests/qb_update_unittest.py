import unittest
from querybuilder import *

# test run
# python .\qb_update_unittest.py -v


class QBUpdateTestCase(unittest.TestCase):
    def setUp(self):
        self.qb = QueryBuilder(DataBase(), ":memory:")

    def test_sql_update(self):
        sql = self.qb.update('posts', {'status': 'published'})\
                    .where([['YEAR(`updated_at`)', '>', 2020]]).get_sql()
        self.assertEqual(sql, "UPDATE `posts` SET `status` = 'published' WHERE (YEAR(`updated_at`) > 2020)")
        self.assertEqual(self.qb.get_params(), ('published', 2020))

    def test_sql_update_limit_eq(self):
        sql = self.qb.update('users', {'username': 'John Doe', 'status': 'new status'})\
                    .where([['id', '=', 7]]).limit().get_sql()
        self.assertEqual(sql, "UPDATE `users` SET `username` = 'John Doe', `status` = 'new status' WHERE (`id` = 7) LIMIT 1")
        self.assertEqual(self.qb.get_params(), ('John Doe', 'new status', 7))

    def test_sql_update_limit_no_eq(self):
        sql = self.qb.update('users', {'username': 'John Doe', 'status': 'new status'})\
                    .where([['id', 7]]).limit().get_sql()
        self.assertEqual(sql, "UPDATE `users` SET `username` = 'John Doe', `status` = 'new status' WHERE (`id` = 7) LIMIT 1")
        self.assertEqual(self.qb.get_params(), ('John Doe', 'new status', 7))


if __name__ == "__main__":
    unittest.main()
