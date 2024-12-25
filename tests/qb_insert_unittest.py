import unittest
from querybuilder import *

# test run
# python .\qb_insert_unittest.py -v


class QBInsertTestCase(unittest.TestCase):
    def setUp(self):
        self.qb = QueryBuilder(DataBase(), ":memory:")

    def test_sql_insert(self):
        sql = self.qb.insert('groups', {'name': 'Moderator', 'permissions': 'moderator'}).get_sql()
        self.assertEqual(sql, "INSERT INTO `groups` (`name`, `permissions`) VALUES ('Moderator','moderator')")
        self.assertEqual(self.qb.get_params(), ('Moderator', 'moderator'))

    def test_sql_insert_multiple(self):
        sql = self.qb.insert('groups', [
                            ['name', 'role'],
                            ['Moderator', 'moderator'], ['Moderator2', 'moderator'],
                            ['User', 'user'], ['User2', 'user']
                        ]).get_sql()
        self.assertEqual(sql, "INSERT INTO `groups` (`name`, `role`) VALUES ('Moderator','moderator'),('Moderator2','moderator'),('User','user'),('User2','user')")
        self.assertEqual(self.qb.get_params(), ('Moderator', 'moderator', 'Moderator2', 'moderator', 'User', 'user', 'User2', 'user'))


if __name__ == "__main__":
    unittest.main()
