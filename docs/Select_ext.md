# SELECT extensions
## `JOIN`
SQLite supports `INNER`, `LEFT OUTER` and `CROSS` joins (`INNER` is by default)
### `INNER JOIN`
```python
results = qb.select({'u': 'users'}, [
        'u.id',
        'u.email',
        'u.username',
        {'perms': 'groups.permissions'}
    ])\
    .join('groups', ['u.group_id', 'groups.id'])\
    .limit(5)\
    .all()
```
Result query
```sql
SELECT `u`.`id`, `u`.`email`, `u`.`username`, `groups`.`permissions` AS `perms`
FROM `users` AS `u`
INNER JOIN `groups` ON `u`.`group_id` = `groups`.`id`
LIMIT 5;
```
More complicated examples
```python
results = qb.select({'cp': 'cabs_printers'}, [
        'cp.id',
        'cp.cab_id',
        {'cab_name': 'cb.name'},
        'cp.printer_id',
        {'printer_name': 'p.name'},
        {'cartridge_type': 'c.name'},
        'cp.comment'
    ])\
    .join({'cb': 'cabs'}, ['cp.cab_id', 'cb.id'])\
    .join({'p': 'printer_models'}, ['cp.printer_id', 'p.id'])\
    .join({'c': 'cartridge_types'}, 'p.cartridge_id=c.id')\
    .where([['cp.cab_id', 'in', [11, 12, 13]], 'or', ['cp.cab_id', '=', 5], 'and', ['p.id', '>', 'c.id']])\
    .all()
```
Result query
```sql
SELECT `cp`.`id`, `cp`.`cab_id`, `cb`.`name` AS `cab_name`, `cp`.`printer_id`,
       `p`.`name` AS `printer_name`, `c`.`name` AS `cartridge_type`, `cp`.`comment`
FROM `cabs_printers` AS `cp`
INNER JOIN `cabs` AS `cb` ON `cp`.`cab_id` = `cb`.`id`
INNER JOIN `printer_models` AS `p` ON `cp`.`printer_id` = `p`.`id`
INNER JOIN `cartridge_types` AS `c` ON p.cartridge_id=c.id
WHERE (`cp`.`cab_id` IN (11, 12, 13)) OR (`cp`.`cab_id` = 5) AND (`p`.`id` > `c`.`id`);
```
It's able not using equals `=` in `JOIN` conditions since [v0.3.4](https://github.com/co0lc0der/simple-query-builder-python/releases/tag/v0.3.4) 
```python
results = qb.select({'cp': 'cabs_printers'}, [
        'cp.id',
        'cp.cab_id',
        {'cab_name': 'cb.name'},
        'cp.printer_id',
        {'cartridge_id': 'c.id'},
        {'printer_name': 'p.name'},
        {'cartridge_type': 'c.name'},
        'cp.comment'
    ])\
    .join({'cb': 'cabs'}, ['cp.cab_id', 'cb.id'])\
    .join({'p': 'printer_models'}, ['cp.printer_id', 'p.id'])\
    .join({'c': 'cartridge_types'}, ['p.cartridge_id', 'c.id'])\
    .group_by(['cp.printer_id', 'cartridge_id'])\
    .order_by(['cp.cab_id', 'cp.printer_id desc'])\
    .all()
```
Result query
```sql
SELECT `cp`.`id`, `cp`.`cab_id`, `cb`.`name` AS `cab_name`, `cp`.`printer_id`, `c`.`id` AS `cartridge_id`,
    `p`.`name` AS `printer_name`, `c`.`name` AS `cartridge_type`, `cp`.`comment`
FROM `cabs_printers` AS `cp`
INNER JOIN `cabs` AS `cb` ON `cp`.`cab_id` = `cb`.`id`
INNER JOIN `printer_models` AS `p` ON `cp`.`printer_id` = `p`.`id`
INNER JOIN `cartridge_types` AS `c` ON `p`.`cartridge_id` = `c`.`id`
GROUP BY `cp`.`printer_id`, `cartridge_id`
ORDER BY `cp`.`cab_id` ASC, `cp`.`printer_id` DESC;
```
### `LEFT [OUTER] JOIN`
```python
# LEFT JOIN
results = qb.select('employees', ['employees.employee_id', 'employees.last_name', 'positions.title'])\
            .join('positions', ['employees.position_id', 'positions.position_id'], join_type="left")\
            .all()

# or LEFT OUTER JOIN
results = qb.select('employees', ['employees.employee_id', 'employees.last_name', 'positions.title'])\
            .join('positions', ['employees.position_id', 'positions.position_id'], join_type="left outer")\
            .all()
```
Result query
```sql
SELECT `employees`.`employee_id`, `employees`.`last_name`, `positions`.`title` FROM `employees`
LEFT [OUTER] JOIN `positions` ON `employees`.`position_id` = `positions`.`position_id`;
```
## `INTERSECT`
Since [v0.4](https://github.com/co0lc0der/simple-query-builder-python/releases/tag/v0.4)
```python
results = qb.select('departments', ['department_id']).intersect_select('employees').all()
```
Result query
```sql
SELECT `department_id` FROM `departments`
INTERSECT
SELECT `department_id` FROM `employees`;
```
One more example
```python
results = qb.select('contacts', ['contact_id', 'last_name', 'first_name']).where([['contact_id', '>', 50]])\
            .intersect()\
            .select('customers', ['customer_id', 'last_name', 'first_name']).where([['last_name', '<>', 'Zagoskin']])\
            .all()
```
Result query
```sql
SELECT `contact_id`, `last_name`, `first_name` FROM `contacts` WHERE (`contact_id` > 50)
INTERSECT
SELECT `customer_id`, `last_name`, `first_name` FROM `customers` WHERE (`last_name` <> 'Zagoskin');
```
## `EXCEPT`
Since [v0.4](https://github.com/co0lc0der/simple-query-builder-python/releases/tag/v0.4)
```python
results = qb.select('departments', ['department_id']).except_select('employees').all()
```
Result query
```sql
SELECT `department_id` FROM `departments`
EXCEPT
SELECT `department_id` FROM `employees`;
```
One more example
```python
results = qb.select('suppliers', ['supplier_id', 'state']).where([['state', 'Nevada']])\
            .excepts()\
            .select('companies', ['company_id', 'state']).where([['company_id', '<', 2000]])\
            .order_by('1 desc').all()
```
Result query
```sql
SELECT `supplier_id`, `state` FROM `suppliers` WHERE (`state` = 'Nevada')
EXCEPT
SELECT `company_id`, `state` FROM `companies` WHERE (`company_id` < 2000) ORDER BY `1` DESC;
```
## `UNION` and `UNION ALL`
Since [v0.4](https://github.com/co0lc0der/simple-query-builder-python/releases/tag/v0.4)
### `UNION`
```python
results = qb.select('clients', ['name', 'age'])\
        .union()\
        .select('employees', ['name', 'age'])\
        .all()

# or
results = qb.select('clients', ['name', 'age'])\
        .union_select('employees')\
        .all()
```
Result query
```sql
SELECT `name`, `age` FROM `clients`
UNION
SELECT `name`, `age` FROM `employees`;
```
### `UNION ALL`
```python
results = qb.select('clients', ['name', 'age'])\
        .union(True)\
        .select('employees', ['name', 'age'])\
        .all()

# or
results = qb.select('clients', ['name', 'age'])\
        .union_select('employees', True)\
        .all()
```
Result query
```sql
SELECT `name`, `age` FROM `clients`
UNION ALL
SELECT `name`, `age` FROM `employees`;
```

To the [INSERT section](Insert.md)

Back to [doc index](index.md) or [readme](../README.md)
