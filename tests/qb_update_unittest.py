import unittest
from querybuilder import *

# test run
# python .\qb_update_unittest.py -v


class QBUpdateTestCase(unittest.TestCase):
    def setUp(self):
        self.qb = QueryBuilder(DataBase(), ":memory:")
        self.maxDiff = None

    def test_update_empty_table(self):
        result = self.qb.update('', {'param': 'new_value'})

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), True)
        self.assertEqual(result.get_error_message(), "Empty table or fields in update method")

    def test_update_empty_fields(self):
        result = self.qb.update('params', {})

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), True)
        self.assertEqual(result.get_error_message(), "Empty table or fields in update method")

    def test_update_empty_table_and_fields(self):
        result = self.qb.update('', {})

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), True)
        self.assertEqual(result.get_error_message(), "Empty table or fields in update method")

    def test_update_table_as_str(self):
        result = self.qb.update('posts', {'status': 'published'}).where([['YEAR(`updated_at`)', '>', 2020]])

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "UPDATE `posts` SET `status` = 'published' WHERE (YEAR(`updated_at`) > 2020)")
        self.assertEqual(self.qb.get_params(), ('published', 2020))

    def test_update_table_as_dict(self):
        result = self.qb.update({'p': 'posts'}, {'status': 'published'}).where([['YEAR(`updated_at`)', '>', 2020]])

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "UPDATE `posts` AS `p` SET `status` = 'published' WHERE (YEAR(`updated_at`) > 2020)")
        self.assertEqual(self.qb.get_params(), ('published', 2020))

    def test_update_where_eq(self):
        result = self.qb.update('posts', {'status': 'draft'}).where([['user_id', '=', 10]])

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "UPDATE `posts` SET `status` = 'draft' WHERE (`user_id` = 10)")
        self.assertEqual(self.qb.get_params(), ('draft', 10))

    def test_update_where_no_eq(self):
        result = self.qb.update('posts', {'status': 'draft'}).where([['user_id', 10]])

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "UPDATE `posts` SET `status` = 'draft' WHERE (`user_id` = 10)")
        self.assertEqual(self.qb.get_params(), ('draft', 10))

    def test_update_where_eq_limit(self):
        result = self.qb.update('users', {'username': 'John Doe', 'status': 'new status'})\
                    .where([['id', '=', 7]]).limit()

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "UPDATE `users` SET `username` = 'John Doe', `status` = 'new status' WHERE (`id` = 7) LIMIT 1")
        self.assertEqual(self.qb.get_params(), ('John Doe', 'new status', 7))

    def test_update_where_no_eq_limit(self):
        result = self.qb.update('users', {'username': 'John Doe', 'status': 'new status'})\
                    .where([['id', 7]]).limit()

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "UPDATE `users` SET `username` = 'John Doe', `status` = 'new status' WHERE (`id` = 7) LIMIT 1")
        self.assertEqual(self.qb.get_params(), ('John Doe', 'new status', 7))
    
    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
