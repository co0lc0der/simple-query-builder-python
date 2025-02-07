import unittest
from simple_query_builder.querybuilder import *

# test run
# python .\tb_unittest.py -v


class TBTestCase(unittest.TestCase):
    def setUp(self):
        self.qb = QueryBuilder(DataBase(), ":memory:")

    def test_drop_table_empty_name(self):
        result = self.qb.drop('')

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), True)
        self.assertEqual(result.get_error_message(), "Empty table in drop method")

    def test_drop_table_no_exists(self):
        result = self.qb.drop('temporary', False)

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "DROP TABLE `temporary`")
        self.assertEqual(result.get_params(), ())

    def test_drop_table_exists(self):
        result = self.qb.drop('temporary')

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "DROP TABLE IF EXISTS `temporary`")
        self.assertEqual(result.get_params(), ())

    def test_truncate_table_empty_name(self):
        result = self.qb.truncate('')

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), True)
        self.assertEqual(result.get_error_message(), "Empty table in truncate method")

    def test_truncate_table(self):
        result = self.qb.truncate('users')

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "TRUNCATE TABLE `users`")
        self.assertEqual(result.get_params(), ())


if __name__ == "__main__":
    unittest.main()
