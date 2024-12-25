import unittest
from querybuilder import *

# test run
# python .\qb_select_unittest.py -v


class QBSelectTestCase(unittest.TestCase):
    def setUp(self):
        self.qb = QueryBuilder(DataBase(), ":memory:")

    def test_sql_select_all(self):
        sql = self.qb.select('users').get_sql()
        self.assertEqual(sql, 'SELECT * FROM `users`')
        self.assertEqual(self.qb.get_params(), ())

    def test_sql_select_where_eq(self):
        sql = self.qb.select('users').where([['id', '=', 10]]).get_sql()
        self.assertEqual(sql, 'SELECT * FROM `users` WHERE (`id` = 10)')
        self.assertEqual(self.qb.get_params(), (10,))

    def test_sql_select_where_no_eq(self):
        sql = self.qb.select('users').where([['id', 10]]).get_sql()
        self.assertEqual(sql, 'SELECT * FROM `users` WHERE (`id` = 10)')
        self.assertEqual(self.qb.get_params(), (10, ))

    def test_sql_select_where_and_eq(self):
        sql = self.qb.select('users').where([['id', '>', 1], 'and', ['group_id', '=', 2]]).get_sql()
        self.assertEqual(sql, 'SELECT * FROM `users` WHERE (`id` > 1) AND (`group_id` = 2)')
        self.assertEqual(self.qb.get_params(), (1, 2))

    def test_sql_select_where_and_no_eq(self):
        sql = self.qb.select('users').where([['id', '>', 1], 'and', ['group_id', 2]]).get_sql()
        self.assertEqual(sql, 'SELECT * FROM `users` WHERE (`id` > 1) AND (`group_id` = 2)')
        self.assertEqual(self.qb.get_params(), (1, 2))

    def test_sql_select_where_or_eq(self):
        sql = self.qb.select('users').where([['id', '>', 1], 'or', ['group_id', '=', 2]]).get_sql()
        self.assertEqual(sql, 'SELECT * FROM `users` WHERE (`id` > 1) OR (`group_id` = 2)')
        self.assertEqual(self.qb.get_params(), (1, 2))

    def test_sql_select_where_or_no_eq(self):
        sql = self.qb.select('users').where([['id', '>', 1], 'or', ['group_id', 2]]).get_sql()
        self.assertEqual(sql, 'SELECT * FROM `users` WHERE (`id` > 1) OR (`group_id` = 2)')
        self.assertEqual(self.qb.get_params(), (1, 2))

    def test_sql_select_where_like(self):
        sql = self.qb.select('users').where([['name', 'LIKE', '%John%']]).get_sql()
        self.assertEqual(sql, "SELECT * FROM `users` WHERE (`name` LIKE '%John%')")
        self.assertEqual(self.qb.get_params(), ('%John%',))

    def test_sql_select_like_list(self):
        sql = self.qb.select('users').like(['name', '%John%']).get_sql()
        self.assertEqual(sql, "SELECT * FROM `users` WHERE (`name` LIKE '%John%')")
        self.assertEqual(self.qb.get_params(), ('%John%',))

    def test_sql_select_like_str(self):
        sql = self.qb.select('users').like('name', '%John%').get_sql()
        self.assertEqual(sql, "SELECT * FROM `users` WHERE (`name` LIKE '%John%')")
        self.assertEqual(self.qb.get_params(), ('%John%',))

    def test_sql_select_where_not_like(self):
        sql = self.qb.select('users').where([['name', 'NOT LIKE', '%John%']]).get_sql()
        self.assertEqual(sql, "SELECT * FROM `users` WHERE (`name` NOT LIKE '%John%')")
        self.assertEqual(self.qb.get_params(), ('%John%',))

    def test_sql_select_not_like_list(self):
        sql = self.qb.select('users').not_like(['name', '%John%']).get_sql()
        self.assertEqual(sql, "SELECT * FROM `users` WHERE (`name` NOT LIKE '%John%')")
        self.assertEqual(self.qb.get_params(), ('%John%',))

    def test_sql_select_not_like_str(self):
        sql = self.qb.select('users').not_like('name', '%John%').get_sql()
        self.assertEqual(sql, "SELECT * FROM `users` WHERE (`name` NOT LIKE '%John%')")
        self.assertEqual(self.qb.get_params(), ('%John%',))

    def test_sql_select_where_is_null(self):
        sql = self.qb.select('users').where([['phone', 'is null']]).get_sql()
        self.assertEqual(sql, "SELECT * FROM `users` WHERE (`phone` IS NULL)")
        self.assertEqual(self.qb.get_params(), ())

    def test_sql_select_is_null(self):
        sql = self.qb.select('users').is_null('phone').get_sql()
        self.assertEqual(sql, "SELECT * FROM `users` WHERE (`phone` IS NULL)")
        self.assertEqual(self.qb.get_params(), ())

    def test_sql_select_where_is_not_null(self):
        sql = self.qb.select('customers').where([['address', 'is not null']]).get_sql()
        self.assertEqual(sql, "SELECT * FROM `customers` WHERE (`address` IS NOT NULL)")
        self.assertEqual(self.qb.get_params(), ())

    def test_sql_select_not_null(self):
        sql = self.qb.select('customers').not_null('address').get_sql()
        self.assertEqual(sql, "SELECT * FROM `customers` WHERE (`address` IS NOT NULL)")
        self.assertEqual(self.qb.get_params(), ())

    def test_sql_select_is_not_null(self):
        sql = self.qb.select('customers').is_not_null('address').get_sql()
        self.assertEqual(sql, "SELECT * FROM `customers` WHERE (`address` IS NOT NULL)")
        self.assertEqual(self.qb.get_params(), ())

    def test_sql_select_offset(self):
        sql = self.qb.select('posts').where([['user_id', 3]]).offset(14).get_sql()
        self.assertEqual(sql, "SELECT * FROM `posts` WHERE (`user_id` = 3) OFFSET 14")
        self.assertEqual(self.qb.get_params(), (3,))

    def test_sql_select_limit(self):
        sql = self.qb.select('posts').where([['id', '>', 42]]).limit(7).get_sql()
        self.assertEqual(sql, "SELECT * FROM `posts` WHERE (`id` > 42) LIMIT 7")
        self.assertEqual(self.qb.get_params(), (42, ))

    def test_sql_select_counter(self):
        sql = self.qb.select('users', {'counter': 'COUNT(*)'}).get_sql()
        self.assertEqual(sql, "SELECT COUNT(*) AS `counter` FROM `users`")
        self.assertEqual(self.qb.get_params(), ())

    def test_sql_select_distinct_order_by(self):
        sql = self.qb.select('customers', ['city'], True).order_by('city').get_sql()
        self.assertEqual(sql, "SELECT DISTINCT `city` FROM `customers` ORDER BY `city` ASC")
        self.assertEqual(self.qb.get_params(), ())

    def test_sql_select_distinct_order_by_2col(self):
        sql = self.qb.select('customers', ['city', 'country'], True).order_by('country desc').get_sql()
        self.assertEqual(sql, "SELECT DISTINCT `city`, `country` FROM `customers` ORDER BY `country` DESC")
        self.assertEqual(self.qb.get_params(), ())

    def test_sql_select_order_by_two_param(self):
        sql = self.qb.select({'b': 'branches'}, ['b.id', 'b.name'])\
                    .where([['b.id', '>', 1], 'and', ['b.parent_id', 1]]).order_by('b.id', 'desc').get_sql()
        self.assertEqual(sql, "SELECT `b`.`id`, `b`.`name` FROM `branches` AS `b` WHERE (`b`.`id` > 1) AND (`b`.`parent_id` = 1) ORDER BY `b`.`id` DESC")
        self.assertEqual(self.qb.get_params(), (1, 1))

    def test_sql_select_order_by_one_param(self):
        sql = self.qb.select({'b': 'branches'}, ['b.id', 'b.name'])\
                    .where([['b.id', '>', 1], 'and', ['b.parent_id', 1]]).order_by('b.id desc').get_sql()
        self.assertEqual(sql, "SELECT `b`.`id`, `b`.`name` FROM `branches` AS `b` WHERE (`b`.`id` > 1) AND (`b`.`parent_id` = 1) ORDER BY `b`.`id` DESC")
        self.assertEqual(self.qb.get_params(), (1, 1))

    def test_sql_select_group_by(self):
        sql = self.qb.select('posts', ['id', 'category', 'title'])\
                    .where([['views', '>=', 1000]]).group_by('category').get_sql()
        self.assertEqual(sql, "SELECT `id`, `category`, `title` FROM `posts` WHERE (`views` >= 1000) GROUP BY `category`")
        self.assertEqual(self.qb.get_params(), (1000, ))

    def test_sql_select_group_by_having_eq(self):
        sql = self.qb.select('orders', {'month_num': 'MONTH(`created_at`)', 'total': 'SUM(`total`)'})\
                        .where([['YEAR(`created_at`)', 2020]]).group_by('month_num')\
                        .having([['total', '=', 20000]]).get_sql()
        self.assertEqual(sql, "SELECT MONTH(`created_at`) AS `month_num`, SUM(`total`) AS `total` FROM `orders` WHERE (YEAR(`created_at`) = 2020) GROUP BY `month_num` HAVING (`total` = 20000)")
        self.assertEqual(self.qb.get_params(), (2020, 20000))

    def test_sql_select_group_by_having_no_eq_sum(self):
        sql = self.qb.select('orders', {'month_num': 'MONTH(`created_at`)', 'total': 'SUM(`total`)'})\
                        .where([['YEAR(`created_at`)', 2020]]).group_by('month_num')\
                        .having([['total', 20000]]).get_sql()
        self.assertEqual(sql, "SELECT MONTH(`created_at`) AS `month_num`, SUM(`total`) AS `total` FROM `orders` WHERE (YEAR(`created_at`) = 2020) GROUP BY `month_num` HAVING (`total` = 20000)")
        self.assertEqual(self.qb.get_params(), (2020, 20000))

    def test_sql_select_group_by_having_max(self):
        sql = self.qb.select('employees', ['department', {'Highest salary': 'MAX(`salary`)'}])\
                    .where([['favorite_website', 'Google.com']]).group_by('department')\
                    .having([['MAX(`salary`)', '>=', 30000]]).get_sql()
        self.assertEqual(sql, "SELECT `department`, MAX(`salary`) AS `Highest salary` FROM `employees` WHERE (`favorite_website` = 'Google.com') GROUP BY `department` HAVING (MAX(`salary`) >= 30000)")
        self.assertEqual(self.qb.get_params(), ('Google.com', 30000))

    def test_sql_select_group_by_having_count(self):
        sql = self.qb.select('employees', ['department', {'Number of employees': 'COUNT(*)'}])\
                    .where([['state', 'Nevada']]).group_by('department')\
                    .having([['COUNT(*)', '>', 20]]).get_sql()
        self.assertEqual(sql, "SELECT `department`, COUNT(*) AS `Number of employees` FROM `employees` WHERE (`state` = 'Nevada') GROUP BY `department` HAVING (COUNT(*) > 20)")
        self.assertEqual(self.qb.get_params(), ('Nevada', 20))

    def test_sql_select_summ(self):
        sql = self.qb.select("1+5 as 'res'").get_sql()
        self.assertEqual(sql, "SELECT 1+5 as 'res'")
        self.assertEqual(self.qb.get_params(), ())

    def test_sql_select_sub(self):
        sql = self.qb.select("10 - 3 as 'res'").get_sql()
        self.assertEqual(sql, "SELECT 10 - 3 as 'res'")
        self.assertEqual(self.qb.get_params(), ())

    def test_sql_select_substr(self):
        sql = self.qb.select("substr('Hello world!', 1, 5) as 'str'").get_sql()
        self.assertEqual(sql, "SELECT substr('Hello world!', 1, 5) as 'str'")
        self.assertEqual(self.qb.get_params(), ())

    def test_sql_select_sqlite_version(self):
        sql = self.qb.select("sqlite_version() as ver").get_sql()
        self.assertEqual(sql, "SELECT sqlite_version() as ver")
        self.assertEqual(self.qb.get_params(), ())

    def test_sql_select_time(self):
        sql = self.qb.select("strftime('%Y-%m-%d %H:%M', 'now')").get_sql()
        self.assertEqual(sql, "SELECT strftime('%Y-%m-%d %H:%M', 'now')")
        self.assertEqual(self.qb.get_params(), ())

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
