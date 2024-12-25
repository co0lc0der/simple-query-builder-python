import unittest
from querybuilder import *

# test run
# python .\qb_select_ext_unittest.py -v


class QBSelectExtensionsTestCase(unittest.TestCase):
    def setUp(self):
        self.qb = QueryBuilder(DataBase(), ":memory:")

    def test_sql_select_inner_join_list(self):
        sql = self.qb.select({'u': 'users'}, ['u.id', 'u.email', 'u.username', {'perms': 'groups.permissions'}])\
                        .join('groups', ['u.group_id', 'groups.id']).get_sql()
        self.assertEqual(sql, "SELECT `u`.`id`, `u`.`email`, `u`.`username`, `groups`.`permissions` AS `perms` FROM `users` AS `u` INNER JOIN `groups` ON `u`.`group_id` = `groups`.`id`")
        self.assertEqual(self.qb.get_params(), ())

    def test_sql_select_inner_join3_str(self):
        sql = self.qb.select({'cp': 'cabs_printers'}, [
                'cp.id', 'cp.cab_id', {'cab_name': 'cb.name'}, 'cp.printer_id',
                {'printer_name': 'p.name'}, {'cartridge_type': 'c.name'}, 'cp.comment'
            ])\
            .join({'cb': 'cabs'}, ['cp.cab_id', 'cb.id'])\
            .join({'p': 'printer_models'}, ['cp.printer_id', 'p.id'])\
            .join({'c': 'cartridge_types'}, 'p.cartridge_id=c.id')\
            .where([['cp.cab_id', 'in', [11, 12, 13]], 'or', ['cp.cab_id', 5], 'and', ['p.id', '>', 'c.id']]).get_sql()
        self.assertEqual(sql, "SELECT `cp`.`id`, `cp`.`cab_id`, `cb`.`name` AS `cab_name`, `cp`.`printer_id`, `p`.`name` AS `printer_name`, `c`.`name` AS `cartridge_type`, `cp`.`comment` FROM `cabs_printers` AS `cp` INNER JOIN `cabs` AS `cb` ON `cp`.`cab_id` = `cb`.`id` INNER JOIN `printer_models` AS `p` ON `cp`.`printer_id` = `p`.`id` INNER JOIN `cartridge_types` AS `c` ON p.cartridge_id=c.id WHERE (`cp`.`cab_id` IN (11,12,13)) OR (`cp`.`cab_id` = 5) AND (`p`.`id` > 'c.id')")
        self.assertEqual(self.qb.get_params(), (11, 12, 13, 5, 'c.id'))

    def test_sql_select_inner_join3_groupby_orederby(self):
        sql = self.qb.select({'cp': 'cabs_printers'}, [
                    'cp.id', 'cp.cab_id', {'cab_name': 'cb.name'},
                    'cp.printer_id', {'cartridge_id': 'c.id'},
                    {'printer_name': 'p.name'}, {'cartridge_type': 'c.name'}, 'cp.comment'
                ])\
                .join({'cb': 'cabs'}, ['cp.cab_id', 'cb.id'])\
                .join({'p': 'printer_models'}, ['cp.printer_id', 'p.id'])\
                .join({'c': 'cartridge_types'}, ['p.cartridge_id', 'c.id'])\
                .group_by(['cp.printer_id', 'cartridge_id'])\
                .order_by(['cp.cab_id', 'cp.printer_id desc']).get_sql()
        self.assertEqual(sql, "SELECT `cp`.`id`, `cp`.`cab_id`, `cb`.`name` AS `cab_name`, `cp`.`printer_id`, `c`.`id` AS `cartridge_id`, `p`.`name` AS `printer_name`, `c`.`name` AS `cartridge_type`, `cp`.`comment` FROM `cabs_printers` AS `cp` INNER JOIN `cabs` AS `cb` ON `cp`.`cab_id` = `cb`.`id` INNER JOIN `printer_models` AS `p` ON `cp`.`printer_id` = `p`.`id` INNER JOIN `cartridge_types` AS `c` ON `p`.`cartridge_id` = `c`.`id` GROUP BY `cp`.`printer_id`, `cartridge_id` ORDER BY `cp`.`cab_id` ASC, `cp`.`printer_id` DESC")
        self.assertEqual(self.qb.get_params(), ())

    def test_sql_select_left_join(self):
        sql = self.qb.select('employees', ['employees.employee_id', 'employees.last_name', 'positions.title'])\
            .join('positions', ['employees.position_id', 'positions.position_id'], join_type="left").get_sql()
        self.assertEqual(sql, "SELECT `employees`.`employee_id`, `employees`.`last_name`, `positions`.`title` FROM `employees` LEFT JOIN `positions` ON `employees`.`position_id` = `positions`.`position_id`")
        self.assertEqual(self.qb.get_params(), ())

    def test_sql_select_left_outer_join(self):
        sql = self.qb.select({'e': 'employees'}, ['e.employee_id', 'e.last_name', 'p.title'])\
            .join({'p': 'positions'}, ['e.position_id', 'p.position_id'], join_type="left outer").get_sql()
        self.assertEqual(sql, "SELECT `e`.`employee_id`, `e`.`last_name`, `p`.`title` FROM `employees` AS `e` LEFT OUTER JOIN `positions` AS `p` ON `e`.`position_id` = `p`.`position_id`")
        self.assertEqual(self.qb.get_params(), ())

    def test_sql_select_cross_join(self):
        sql = self.qb.select('positions').join('departments', join_type="cross").get_sql()
        self.assertEqual(sql, "SELECT * FROM `positions` CROSS JOIN `departments`")
        self.assertEqual(self.qb.get_params(), ())

    def test_sql_except_select(self):
        sql = self.qb.select('departments', ['department_id']).except_select('employees').get_sql()
        self.assertEqual(sql, "SELECT `department_id` FROM `departments` EXCEPT SELECT `department_id` FROM `employees`")
        self.assertEqual(self.qb.get_params(), ())

    def test_sql_select_excepts_where(self):
        sql = self.qb.select('contacts', ['contact_id', 'last_name', 'first_name']).where([['contact_id', '>=', 74]])\
                .excepts()\
                .select('employees', ['employee_id', 'last_name', 'first_name']).where([['first_name', 'Sandra']])\
                .get_sql()
        self.assertEqual(sql, "SELECT `contact_id`, `last_name`, `first_name` FROM `contacts` WHERE (`contact_id` >= 74) EXCEPT SELECT `employee_id`, `last_name`, `first_name` FROM `employees` WHERE (`first_name` = 'Sandra')")
        self.assertEqual(self.qb.get_params(), (74, 'Sandra'))

    def test_sql_select_excepts_where_order_by(self):
        sql = self.qb.select('suppliers', ['supplier_id', 'state']).where([['state', 'Nevada']]) \
            .excepts()\
            .select('companies', ['company_id', 'state']).where([['company_id', '<', 2000]]).order_by('1 desc')\
            .get_sql()
        self.assertEqual(sql, "SELECT `supplier_id`, `state` FROM `suppliers` WHERE (`state` = 'Nevada') EXCEPT SELECT `company_id`, `state` FROM `companies` WHERE (`company_id` < 2000) ORDER BY `1` DESC")
        self.assertEqual(self.qb.get_params(), ('Nevada', 2000))

    def test_sql_intersect_select(self):
        sql = self.qb.select('departments', ['department_id']).intersect_select('employees').get_sql()
        self.assertEqual(sql, "SELECT `department_id` FROM `departments` INTERSECT SELECT `department_id` FROM `employees`")
        self.assertEqual(self.qb.get_params(), ())

    def test_sql_select_intersect_where(self):
        sql = self.qb.select('departments', 'department_id').where([['department_id', '>=', 25]])\
                .intersect()\
                .select('employees', 'department_id').where([['last_name', '<>', 'Petrov']])\
                .get_sql()
        self.assertEqual(sql, "SELECT `department_id` FROM `departments` WHERE (`department_id` >= 25) INTERSECT SELECT `department_id` FROM `employees` WHERE (`last_name` <> 'Petrov')")
        self.assertEqual(self.qb.get_params(), (25, 'Petrov'))

    def test_sql_select_intersect_where2(self):
        sql = self.qb.select('contacts', ['contact_id', 'last_name', 'first_name']).where([['contact_id', '>', 50]])\
            .intersect()\
            .select('customers', ['customer_id', 'last_name', 'first_name']).where([['last_name', '<>', 'Zagoskin']])\
            .get_sql()
        self.assertEqual(sql, "SELECT `contact_id`, `last_name`, `first_name` FROM `contacts` WHERE (`contact_id` > 50) INTERSECT SELECT `customer_id`, `last_name`, `first_name` FROM `customers` WHERE (`last_name` <> 'Zagoskin')")
        self.assertEqual(self.qb.get_params(), (50, 'Zagoskin'))

    def test_sql_select_intersect_where_orderby(self):
        sql = self.qb.select('departments', ['department_id', 'state']).where([['department_id', '>=', 25]]) \
            .intersect()\
            .select('companies', ['company_id', 'state']).like('company_name', 'G%').order_by('1')\
            .get_sql()
        self.assertEqual(sql, "SELECT `department_id`, `state` FROM `departments` WHERE (`department_id` >= 25) INTERSECT SELECT `company_id`, `state` FROM `companies` WHERE (`company_name` LIKE 'G%') ORDER BY `1` ASC")
        self.assertEqual(self.qb.get_params(), (25, 'G%'))

    def test_sql_select_union_where(self):
        sql = self.qb.select('clients', ['name', 'age', {'total_sum': 'account_sum + account_sum * 0.1'}])\
            .where([['account_sum', '<', 3000]])\
            .union()\
            .select('clients', ['name', 'age', {'total_sum': 'account_sum + account_sum * 0.3'}])\
            .where([['account_sum', '>=', 3000]]).get_sql()
        self.assertEqual(sql, "SELECT `name`, `age`, account_sum + account_sum * 0.1 AS `total_sum` FROM `clients` WHERE (`account_sum` < 3000) UNION SELECT `name`, `age`, account_sum + account_sum * 0.3 AS `total_sum` FROM `clients` WHERE (`account_sum` >= 3000)")
        self.assertEqual(self.qb.get_params(), (3000, 3000))

    def test_sql_union_select_where(self):
        sql = self.qb.select('clients', ['name', 'age']).where([['id', '<', 10]])\
                    .union_select('employees').where([['id', 1]]).get_sql()
        self.assertEqual(sql, "SELECT `name`, `age` FROM `clients` WHERE (`id` < 10) UNION SELECT `name`, `age` FROM `employees` WHERE (`id` = 1)")
        self.assertEqual(self.qb.get_params(), (10, 1))

    def test_sql_select_union_where_orderby(self):
        sql = self.qb.select('departments', ['department_id', 'department_name']).where([['department_id', 'in', [1, 2]]])\
            .union()\
            .select('employees', ['employee_id', 'last_name']).where([['hire_date', '2024-02-08']]).order_by('2')\
            .get_sql()
        self.assertEqual(sql, "SELECT `department_id`, `department_name` FROM `departments` WHERE (`department_id` IN (1,2)) UNION SELECT `employee_id`, `last_name` FROM `employees` WHERE (`hire_date` = '2024-02-08') ORDER BY `2` ASC")
        self.assertEqual(self.qb.get_params(), (1, 2, '2024-02-08'))

    def test_sql_select_union_all(self):
        sql = self.qb.select('clients', ['name', 'age', {'total_sum': 'account_sum + account_sum * 0.1'}])\
            .where([['account_sum', '<', 3000]])\
            .union(True)\
            .select('clients', ['name', 'age', {'total_sum': 'account_sum + account_sum * 0.3'}])\
            .where([['account_sum', '>=', 3000]]).get_sql()
        self.assertEqual(sql, "SELECT `name`, `age`, account_sum + account_sum * 0.1 AS `total_sum` FROM `clients` WHERE (`account_sum` < 3000) UNION ALL SELECT `name`, `age`, account_sum + account_sum * 0.3 AS `total_sum` FROM `clients` WHERE (`account_sum` >= 3000)")
        self.assertEqual(self.qb.get_params(), (3000, 3000))

    def test_sql_union_select_all_where(self):
        sql = self.qb.select('cabs', ['id', 'name']) \
            .union_select('printer_models', True).where([['id', '<', 10]]) \
            .get_sql()
        self.assertEqual(sql, "SELECT `id`, `name` FROM `cabs` UNION ALL SELECT `id`, `name` FROM `printer_models` WHERE (`id` < 10)")
        self.assertEqual(self.qb.get_params(), (10, ))

    def test_sql_select_union_all_where_orderby(self):
        sql = self.qb.select('departments', ['department_id', 'department_name']).where([['department_id', '>=', 10]])\
            .union(True)\
            .select('employees', ['employee_id', 'last_name']).where([['last_name', 'Rassohin']]).order_by('2')\
            .get_sql()
        self.assertEqual(sql, "SELECT `department_id`, `department_name` FROM `departments` WHERE (`department_id` >= 10) UNION ALL SELECT `employee_id`, `last_name` FROM `employees` WHERE (`last_name` = 'Rassohin') ORDER BY `2` ASC")
        self.assertEqual(self.qb.get_params(), (10, 'Rassohin'))

    # def test_sql_select_in_select_str_one_param(self):
    #     sql = self.qb.select(self.qb.select('categories').get_sql(), ['id', 'name']).where([['id', '<=', 5]]).get_sql()
    #     self.assertEqual(sql, "SELECT `id`, `name` FROM (SELECT * FROM `categories`) WHERE (`id` <= 5)")
    #     self.assertEqual(self.qb.get_params(), (5, ))
    #
    # def test_sql_select_in_select_str_two_params(self):
    #     sql = self.qb.select(self.qb.select('categories').where([['parent_id', 0]]).get_sql(), ['id', 'name']).where([['id', '<=', 5]]).get_sql()
    #     self.assertEqual(sql, "SELECT `id`, `name` FROM (SELECT * FROM `categories` WHERE (`parent_id` = 0)) WHERE (`id` <= 5)")
    #     self.assertEqual(self.qb.get_params(), (0, 5))
    #
    # def test_sql_select_in_select_add_query(self):
    #     q1 = self.qb.select('categories').where([['parent_id', 0]]).get_sql()
    #     sql = self.qb.select(q1, ['id', 'name']).where([['id', '<=', 5]]).get_sql()
    #     self.assertEqual(sql, "SELECT `id`, `name` FROM (SELECT * FROM `categories` WHERE (`parent_id` = 0)) WHERE (`id` <= 5)")
    #     self.assertEqual(self.qb.get_params(), (0, 5))
    #
    # def test_sql_select_in_select_add_query_format(self):
    #     q1 = self.qb.select('categories').where([['parent_id', 0]])
    #     sql = self.qb.select(f'{q1}', ['id', 'name']).where([['id', '<=', 5]]).get_sql()
    #     self.assertEqual(sql, "SELECT `id`, `name` FROM (SELECT * FROM `categories` WHERE (`parent_id` = 0)) WHERE (`id` <= 5)")
    #     self.assertEqual(self.qb.get_params(), (0, 5))

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
