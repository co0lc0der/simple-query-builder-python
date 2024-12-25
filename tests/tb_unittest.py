import unittest
from simple_query_builder.querybuilder import *

# test run
# python .\tb_unittest.py -v
# python -m unittest .\tb_unittest.py


class TBTestCase(unittest.TestCase):
    def setUp(self):
        self.qb = QueryBuilder(DataBase(), ":memory:")

    def test_sql_drop_table_no_exists(self):
        sql = self.qb.drop('temporary', False).get_sql()
        self.assertEqual(sql, "DROP TABLE `temporary`")

    def test_sql_drop_table_exists(self):
        sql = self.qb.drop('temporary').get_sql()
        self.assertEqual(sql, "DROP TABLE IF EXISTS `temporary`")

    def test_sql_truncate_table(self):
        sql = self.qb.truncate('users').get_sql()
        self.assertEqual(sql, "TRUNCATE TABLE `users`")


if __name__ == "__main__":
    unittest.main()
