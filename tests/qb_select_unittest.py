import unittest
from querybuilder import *

# test run
# python .\qb_select_unittest.py -v


class QBSelectTestCase(unittest.TestCase):
    def setUp(self):
        self.qb = QueryBuilder(DataBase(), ":memory:")
        self.maxDiff = None

    def test_select_empty_table(self):
        result = self.qb.select('', 'param')

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), True)
        self.assertEqual(result.get_error_message(), "Empty table or fields in select method")

    def test_select_empty_fields(self):
        result = self.qb.select('users', [])

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), True)
        self.assertEqual(result.get_error_message(), "Empty table or fields in select method")

    def test_select_empty_table_and_fields(self):
        result = self.qb.select('', '')

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), True)
        self.assertEqual(result.get_error_message(), "Empty table or fields in select method")

    def test_get_sql(self):
        result = self.qb.select('users').where([['id', 1]])

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), 'SELECT * FROM `users` WHERE (`id` = 1)')
        self.assertEqual(result.get_params(), (1, ))

    def test_get_sql_no_values(self):
        result = self.qb.select('users').where([['id', 1]])

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(False), 'SELECT * FROM `users` WHERE (`id` = ?)')
        self.assertEqual(result.get_params(), (1, ))

    def test_select_no_fields(self):
        result = self.qb.select('users')

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), 'SELECT * FROM `users`')
        self.assertEqual(result.get_params(), ())

    def test_select_alias_all(self):
        result = self.qb.select({'u': 'users'}, 'u.*')

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), 'SELECT u.* FROM `users` AS `u`')
        self.assertEqual(result.get_params(), ())

    def test_select_where_eq(self):
        result = self.qb.select('users').where([['id', '=', 10]])

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), 'SELECT * FROM `users` WHERE (`id` = 10)')
        self.assertEqual(result.get_params(), (10,))

    def test_select_where_no_eq(self):
        result = self.qb.select('users').where([['id', 10]])

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), 'SELECT * FROM `users` WHERE (`id` = 10)')
        self.assertEqual(result.get_params(), (10, ))

    def test_select_where_and_eq(self):
        result = self.qb.select('users').where([['id', '>', 1], 'and', ['group_id', '=', 2]])

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), 'SELECT * FROM `users` WHERE (`id` > 1) AND (`group_id` = 2)')
        self.assertEqual(result.get_params(), (1, 2))

    def test_select_where_and_no_eq(self):
        result = self.qb.select('users').where([['id', '>', 1], 'and', ['group_id', 2]])

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), 'SELECT * FROM `users` WHERE (`id` > 1) AND (`group_id` = 2)')
        self.assertEqual(result.get_params(), (1, 2))

    def test_select_where_or_eq(self):
        result = self.qb.select('users').where([['id', '>', 1], 'or', ['group_id', '=', 2]])

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), 'SELECT * FROM `users` WHERE (`id` > 1) OR (`group_id` = 2)')
        self.assertEqual(result.get_params(), (1, 2))

    def test_select_where_or_no_eq(self):
        result = self.qb.select('users').where([['id', '>', 1], 'or', ['group_id', 2]])

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), 'SELECT * FROM `users` WHERE (`id` > 1) OR (`group_id` = 2)')
        self.assertEqual(result.get_params(), (1, 2))

    def test_select_where_like(self):
        result = self.qb.select('users').where([['name', 'LIKE', '%John%']])

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "SELECT * FROM `users` WHERE (`name` LIKE '%John%')")
        self.assertEqual(result.get_params(), ('%John%',))

    def test_select_like_list(self):
        result = self.qb.select('users').like(['name', '%John%'])

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "SELECT * FROM `users` WHERE (`name` LIKE '%John%')")
        self.assertEqual(result.get_params(), ('%John%',))

    def test_select_like_str(self):
        result = self.qb.select('users').like('name', '%John%')

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "SELECT * FROM `users` WHERE (`name` LIKE '%John%')")
        self.assertEqual(result.get_params(), ('%John%',))

    def test_select_where_not_like(self):
        result = self.qb.select('users').where([['name', 'NOT LIKE', '%John%']])

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "SELECT * FROM `users` WHERE (`name` NOT LIKE '%John%')")
        self.assertEqual(result.get_params(), ('%John%',))

    def test_select_not_like_list(self):
        result = self.qb.select('users').not_like(['name', '%John%'])

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "SELECT * FROM `users` WHERE (`name` NOT LIKE '%John%')")
        self.assertEqual(result.get_params(), ('%John%',))

    def test_select_not_like_str(self):
        result = self.qb.select('users').not_like('name', '%John%')

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "SELECT * FROM `users` WHERE (`name` NOT LIKE '%John%')")
        self.assertEqual(result.get_params(), ('%John%',))

    def test_select_where_is_null(self):
        result = self.qb.select('users').where([['phone', 'is null']])

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "SELECT * FROM `users` WHERE (`phone` IS NULL)")
        self.assertEqual(result.get_params(), ())

    def test_select_is_null(self):
        result = self.qb.select('users').is_null('phone')

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "SELECT * FROM `users` WHERE (`phone` IS NULL)")
        self.assertEqual(result.get_params(), ())

    def test_select_where_is_not_null(self):
        result = self.qb.select('customers').where([['address', 'is not null']])

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "SELECT * FROM `customers` WHERE (`address` IS NOT NULL)")
        self.assertEqual(result.get_params(), ())

    def test_select_not_null(self):
        result = self.qb.select('customers').not_null('address')

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "SELECT * FROM `customers` WHERE (`address` IS NOT NULL)")
        self.assertEqual(result.get_params(), ())

    def test_select_is_not_null(self):
        result = self.qb.select('customers').is_not_null('address')

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "SELECT * FROM `customers` WHERE (`address` IS NOT NULL)")
        self.assertEqual(result.get_params(), ())

    def test_select_offset(self):
        result = self.qb.select('posts').where([['user_id', 3]]).offset(14)

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "SELECT * FROM `posts` WHERE (`user_id` = 3) OFFSET 14")
        self.assertEqual(result.get_params(), (3,))

    def test_select_limit(self):
        result = self.qb.select('posts').where([['id', '>', 42]]).limit(7)

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "SELECT * FROM `posts` WHERE (`id` > 42) LIMIT 7")
        self.assertEqual(result.get_params(), (42, ))

    def test_select_counter(self):
        result = self.qb.select('users', {'counter': 'COUNT(*)'})

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "SELECT COUNT(*) AS `counter` FROM `users`")
        self.assertEqual(result.get_params(), ())

    def test_select_distinct_method_empty_table(self):
        result = self.qb.select_distinct('', 'param')

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), True)
        self.assertEqual(result.get_error_message(), "Empty table or fields in select_distinct method")

    def test_select_distinct_method_empty_fields(self):
        result = self.qb.select_distinct('users', [])

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), True)
        self.assertEqual(result.get_error_message(), "Empty table or fields in select_distinct method")

    def test_select_distinct_method_empty_table_and_fields(self):
        result = self.qb.select_distinct('', '')

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), True)
        self.assertEqual(result.get_error_message(), "Empty table or fields in select_distinct method")

    def test_select_distinct_order_by(self):
        result = self.qb.select('customers', ['city'], True).order_by('city')

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "SELECT DISTINCT `city` FROM `customers` ORDER BY `city` ASC")
        self.assertEqual(result.get_params(), ())

    def test_select_distinct_method_order_by(self):
        result = self.qb.select_distinct('customers', ['city']).order_by('city')

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "SELECT DISTINCT `city` FROM `customers` ORDER BY `city` ASC")
        self.assertEqual(result.get_params(), ())

    def test_select_distinct_order_by_2col(self):
        result = self.qb.select('customers', ['city', 'country'], True).order_by('country desc')

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "SELECT DISTINCT `city`, `country` FROM `customers` ORDER BY `country` DESC")
        self.assertEqual(result.get_params(), ())

    def test_select_distinct_method_order_by_2col(self):
        result = self.qb.select_distinct('customers', ['city', 'country']).order_by('country desc')

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "SELECT DISTINCT `city`, `country` FROM `customers` ORDER BY `country` DESC")
        self.assertEqual(result.get_params(), ())

    def test_select_order_by_two_params(self):
        result = self.qb.select({'b': 'branches'}, ['b.id', 'b.name'])\
                    .where([['b.id', '>', 1], 'and', ['b.parent_id', 1]]).order_by('b.id', 'desc')

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "SELECT `b`.`id`, `b`.`name` FROM `branches` AS `b` WHERE (`b`.`id` > 1) AND (`b`.`parent_id` = 1) ORDER BY `b`.`id` DESC")
        self.assertEqual(result.get_params(), (1, 1))

    def test_select_order_by_one_param(self):
        result = self.qb.select({'b': 'branches'}, ['b.id', 'b.name'])\
                    .where([['b.id', '>', 1], 'and', ['b.parent_id', 1]]).order_by('b.id desc')

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "SELECT `b`.`id`, `b`.`name` FROM `branches` AS `b` WHERE (`b`.`id` > 1) AND (`b`.`parent_id` = 1) ORDER BY `b`.`id` DESC")
        self.assertEqual(result.get_params(), (1, 1))

    def test_select_group_by(self):
        result = self.qb.select('posts', ['id', 'category', 'title'])\
                    .where([['views', '>=', 1000]]).group_by('category')

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "SELECT `id`, `category`, `title` FROM `posts` WHERE (`views` >= 1000) GROUP BY `category`")
        self.assertEqual(result.get_params(), (1000, ))

    def test_select_group_by_having_eq(self):
        result = self.qb.select('orders', {'month_num': 'MONTH(`created_at`)', 'total': 'SUM(`total`)'})\
                        .where([['YEAR(`created_at`)', 2020]]).group_by('month_num')\
                        .having([['total', '=', 20000]])
        self.assertEqual(result.get_sql(), "SELECT MONTH(`created_at`) AS `month_num`, SUM(`total`) AS `total` FROM `orders` WHERE (YEAR(`created_at`) = 2020) GROUP BY `month_num` HAVING (`total` = 20000)")
        self.assertEqual(result.get_params(), (2020, 20000))

    def test_select_group_by_having_no_eq_sum(self):
        result = self.qb.select('orders', {'month_num': 'MONTH(`created_at`)', 'total': 'SUM(`total`)'})\
                        .where([['YEAR(`created_at`)', 2020]]).group_by('month_num')\
                        .having([['total', 20000]])
        self.assertEqual(result.get_sql(), "SELECT MONTH(`created_at`) AS `month_num`, SUM(`total`) AS `total` FROM `orders` WHERE (YEAR(`created_at`) = 2020) GROUP BY `month_num` HAVING (`total` = 20000)")
        self.assertEqual(result.get_params(), (2020, 20000))

    def test_select_group_by_having_max(self):
        result = self.qb.select('employees', ['department', {'Highest salary': 'MAX(`salary`)'}])\
                    .where([['favorite_website', 'Google.com']]).group_by('department')\
                    .having([['MAX(`salary`)', '>=', 30000]])

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "SELECT `department`, MAX(`salary`) AS `Highest salary` FROM `employees` WHERE (`favorite_website` = 'Google.com') GROUP BY `department` HAVING (MAX(`salary`) >= 30000)")
        self.assertEqual(result.get_params(), ('Google.com', 30000))

    def test_select_group_by_having_count(self):
        result = self.qb.select('employees', ['department', {'Number of employees': 'COUNT(*)'}])\
                    .where([['state', 'Nevada']]).group_by('department')\
                    .having([['COUNT(*)', '>', 20]])

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "SELECT `department`, COUNT(*) AS `Number of employees` FROM `employees` WHERE (`state` = 'Nevada') GROUP BY `department` HAVING (COUNT(*) > 20)")
        self.assertEqual(result.get_params(), ('Nevada', 20))

    def test_select_sum(self):
        result = self.qb.select("1+5 as 'res'")

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "SELECT 1+5 as 'res'")
        self.assertEqual(result.get_params(), ())

    def test_select_sub(self):
        result = self.qb.select("10 - 3 as 'res'")

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "SELECT 10 - 3 as 'res'")
        self.assertEqual(result.get_params(), ())

    def test_select_substr(self):
        result = self.qb.select("substr('Hello world!', 1, 5) as 'str'")

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "SELECT substr('Hello world!', 1, 5) as 'str'")
        self.assertEqual(result.get_params(), ())

    def test_select_concat_str(self):
        result = self.qb.select("'Hello' || ' world!' as 'str'")

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "SELECT 'Hello' || ' world!' as 'str'")
        self.assertEqual(result.get_params(), ())

    def test_select_sqlite_version(self):
        result = self.qb.select("sqlite_version() as ver")

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "SELECT sqlite_version() as ver")
        self.assertEqual(result.get_params(), ())

    def test_select_time(self):
        result = self.qb.select("strftime('%Y-%m-%d %H:%M', 'now')")

        self.assertEqual(result, self.qb)
        self.assertEqual(result.has_error(), False)
        self.assertEqual(result.get_sql(), "SELECT strftime('%Y-%m-%d %H:%M', 'now')")
        self.assertEqual(result.get_params(), ())

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
