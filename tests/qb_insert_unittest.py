import unittest
from querybuilder import *

# test run
# python .\qb_insert_unittest.py -v


class QBInsertTestCase(unittest.TestCase):
    def setUp(self):
        self.qb = QueryBuilder(DataBase(), ":memory:")

    def test_insert_empty_table(self):
        result = self.qb.insert('', {'param': 'new_value'})

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), True)
        self.assertEqual(result.get_error_message(), "Empty table or fields in insert method")

    def test_insert_empty_fields(self):
        result = self.qb.insert('params', {})

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), True)
        self.assertEqual(result.get_error_message(), "Empty table or fields in insert method")

    def test_insert_empty_table_and_fields(self):
        result = self.qb.insert('', {})

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), True)
        self.assertEqual(result.get_error_message(), "Empty table or fields in insert method")

    def test_insert_table_as_str(self):
        result = self.qb.insert('groups', {'name': 'Moderator', 'permissions': 'moderator'})

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "INSERT INTO `groups` (`name`, `permissions`) VALUES ('Moderator','moderator')")
        self.assertEqual(result.get_params(), ('Moderator', 'moderator'))

    def test_insert_table_as_dict(self):
        result = self.qb.insert({'g': 'groups'}, {'name': 'Moderator', 'permissions': 'moderator'})

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "INSERT INTO `groups` AS `g` (`name`, `permissions`) VALUES ('Moderator','moderator')")
        self.assertEqual(result.get_params(), ('Moderator', 'moderator'))

    def test_insert_multiple_as_str(self):
        result = self.qb.insert('groups', [
                            ['name', 'role'],
                            ['Moderator', 'moderator'], ['Moderator2', 'moderator'],
                            ['User', 'user'], ['User2', 'user']
                        ])

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "INSERT INTO `groups` (`name`, `role`) VALUES ('Moderator','moderator'),('Moderator2','moderator'),('User','user'),('User2','user')")
        self.assertEqual(result.get_params(), ('Moderator', 'moderator', 'Moderator2', 'moderator', 'User', 'user', 'User2', 'user'))

    def test_insert_multiple_as_dict(self):
        result = self.qb.insert({'g': 'groups'}, [
                            ['name', 'role'],
                            ['Moderator', 'moderator'], ['Moderator2', 'moderator'],
                            ['User', 'user'], ['User2', 'user']
                        ])

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "INSERT INTO `groups` AS `g` (`name`, `role`) VALUES ('Moderator','moderator'),('Moderator2','moderator'),('User','user'),('User2','user')")
        self.assertEqual(result.get_params(), ('Moderator', 'moderator', 'Moderator2', 'moderator', 'User', 'user', 'User2', 'user'))

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
