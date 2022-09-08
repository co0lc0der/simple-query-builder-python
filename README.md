# QueryBuilder python module

![PyPI](https://img.shields.io/pypi/v/simple-query-builder?color=yellow&style=flat-square)
[![Latest Version](https://img.shields.io/github/release/co0lc0der/simple-query-builder-python?color=orange&style=flat-square)](https://github.com/co0lc0der/simple-query-builder-python/release)
![GitHub repo size](https://img.shields.io/github/repo-size/co0lc0der/simple-query-builder-python?label=size&style=flat-square)
![Python 3.7, 3.8, 3.9, 3.10](https://img.shields.io/pypi/pyversions/simple-query-builder?color=blueviolet&style=flat-square)
[![GitHub license](https://img.shields.io/github/license/co0lc0der/simple-query-builder-python?style=flat-square)](https://github.com/co0lc0der/simple-query-builder-python/blob/main/LICENSE.md)

This is a small easy-to-use component for working with a database. It provides some public methods to compose SQL queries and manipulate data. Each SQL query is prepared and safe. QueryBuilder fetches data to _list_ by default. At present time the component supports SQLite (file or memory).

## Contributing

Bug reports and/or pull requests are welcome

## License

The module is available as open source under the terms of the [MIT license](https://github.com/co0lc0der/simple-query-builder-python/blob/main/LICENSE.md)

## Installation

Install the current version with [PyPI](https://pypi.org/project/simple-query-builder):

```bash
pip install simple-query-builder
```

Or from Github:
```bash
pip install https://github.com/co0lc0der/simple-query-builder-python/archive/main.zip
```
## How to use
### Main public methods
- `get_sql()` returns SQL query string which will be executed
- `get_params()` returns an array of parameters for a query
- `get_result()` returns query's results
- `get_count()` returns results' rows count
- `get_error()` returns `True` if an error is had
- `get_error_message()` returns an error message if an error is had
- `set_error(message)` sets `_error` to `True` and `_error_essage`
- `get_first()` returns the first item of results
- `get_last()` returns the last item of results
- `reset()` resets state to default values (except PDO property)
- `all()` executes SQL query and return all rows of result (`fetchall()`)
- `one()` executes SQL query and return the first row of result (`fetchone()`)
- `column(col_index)` executes SQL query and return the first column of result, `col_index` is `0` by default
- `go()` this method is for non `SELECT` queries. it executes SQL query and return nothing (but returns the last inserted row ID for `INSERT` method)
- `count()` prepares a query with SQL `COUNT()` function
- `query(sql, params, fetch_type, col_index)` executes prepared `sql` with `params`, it can be used for custom queries
- 'SQL' methods are presented in [Usage section](#usage-examples)

### Import the module and init `QueryBuilder` with `Database()`
```python
from querybuilder import *

qb = QueryBuilder(DataBase(), 'my_db.db')
```
### Usage examples
- Select all rows from a table
```python
results = qb.select('users').all()
```
```sql
SELECT * FROM `users`;
```
- Select a row with a condition
```python
results = qb.select('users').where([['id', '=', 10]]).one()
```
```sql
SELECT * FROM `users` WHERE `id` = 10;
```
- Select rows with two conditions
```python
results = qb.select('users')\
    .where([['id', '>', 1], 'and', ['group_id', '=', 2]])\
    .all()
```
```sql
SELECT * FROM `users` WHERE (`id` > 1) AND (`group_id` = 2)
```
- Select a row with a `LIKE` and `NOT LIKE` condition
```python
results = qb.select('users').like(['name', '%John%']).all()
# or
results = qb.select('users').where([['name', 'LIKE', '%John%']]).all()
```
```sql
SELECT * FROM `users` WHERE (`name` LIKE '%John%')
```
```python
results = qb.select('users').notLike(['name', '%John%']).all()
# or
results = qb.select('users').where([['name', 'NOT LIKE', '%John%']]).all()
```
```sql
SELECT * FROM `users` WHERE (`name` NOT LIKE '%John%')
```
- Select rows with `OFFSET` and `LIMIT`
```python
results = qb.select('posts')\
    .where([['user_id', '=', 3]])\
    .offset(14)\
    .limit(7)\
    .all()
```
```sql
SELECT * FROM `posts` WHERE (`user_id` = 3) OFFSET 14 LIMIT 7;
```
- Select custom fields with additional SQL
1. `COUNT()`
```python
results = qb.select('users', {'counter': 'COUNT(*)'}).one()
# or
results = qb.count('users').one()
```
```sql
SELECT COUNT(*) AS `counter` FROM `users`;
```
2. `ORDER BY`
```python
results = qb.select({'b': 'branches'}, ['b.id', 'b.name'])\
    .where([['b.id', '>', 1], 'and', ['b.parent_id', '=', 1]])\
    .orderBy('b.id', 'desc')\
    .all()
```
```sql
SELECT `b`.`id`, `b`.`name` FROM `branches` AS `b`
WHERE (`b`.`id` > 1) AND (`b`.`parent_id` = 1)
ORDER BY `b`.`id` DESC;
``` 
3. `GROUP BY` and `HAVING`
```python
results = qb.select('posts', ['id', 'category', 'title'])\
    .where([['views', '>=', 1000]])\
    .groupBy('category')\
    .all()
```
```sql
SELECT `id`, `category`, `title` FROM `posts`
WHERE (`views` >= 1000) GROUP BY `category`;
```
```python
groups = qb.select('orders', {'month_num': 'MONTH(`created_at`)', 'total': 'SUM(`total`)'})\
    .where([['YEAR(`created_at`)', '=', 2020]])\
    .groupBy('month_num')\
    .having([['total', '>', 20000]])\
    .all()
```
```sql
SELECT MONTH(`created_at`) AS `month_num`, SUM(`total`) AS `total`
FROM `orders` WHERE (YEAR(`created_at`) = 2020)
GROUP BY `month_num` HAVING (`total` > 20000)
```
4. `JOIN`. Supports `INNER`, `LEFT OUTER`, `RIGHT OUTER`, `FULL OUTER` and `CROSS` joins (`INNER` is by default)
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
```sql
SELECT `u`.`id`, `u`.`email`, `u`.`username`, `groups`.`permissions` AS `perms`
FROM `users` AS `u`
INNER JOIN `groups` ON `u`.`group_id` = `groups`.`id`
LIMIT 5;
```
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
```sql
SELECT `cp`.`id`, `cp`.`cab_id`, `cb`.`name` AS `cab_name`, `cp`.`printer_id`,
       `p`.`name` AS `printer_name`, `c`.`name` AS `cartridge_type`, `cp`.`comment`
FROM `cabs_printers` AS `cp`
INNER JOIN `cabs` AS `cb` ON `cp`.`cab_id` = `cb`.`id`
INNER JOIN `printer_models` AS `p` ON `cp`.`printer_id` = `p`.`id`
INNER JOIN `cartridge_types` AS `c` ON p.cartridge_id=c.id
WHERE (`cp`.`cab_id` IN (11,12,13)) OR (`cp`.`cab_id` = 5) AND (`p`.`id` > `c`.`id`)
```
- Insert a row
```python
new_id = qb.insert('groups', {
    'name': 'Moderator',
    'permissions': 'moderator'
}).go()
```
```sql
INSERT INTO `groups` (`name`, `permissions`) VALUES ('Moderator', 'moderator')
```
- Insert many rows
```python
qb.insert('groups', [['name', 'role'],
    ['Moderator', 'moderator'],
    ['Moderator2', 'moderator'],
    ['User', 'user'],
    ['User2', 'user']
]).go()
```
```sql
INSERT INTO `groups` (`name`, `role`)
VALUES ('Moderator', 'moderator'),
       ('Moderator2', 'moderator'),
       ('User', 'user'),
       ('User2', 'user')
```
- Update a row
```python
qb.update('users', {
        'username': 'John Doe',
        'status': 'new status'
    })\
    .where([['id', '=', 7]])\
    .limit()\
    .go()
```
```sql
UPDATE `users` SET `username` = 'John Doe', `status` = 'new status'
WHERE `id` = 7 LIMIT 1;
```
- Update rows
```python
qb.update('posts', {'status': 'published'})\
    .where([['YEAR(`updated_at`)', '>', 2020]])\
    .go()
```
```sql
UPDATE `posts` SET `status` = 'published'
WHERE (YEAR(`updated_at`) > 2020)
```
- Delete a row
```python
qb.delete('users')\
    .where([['name', '=', 'John']])\
    .limit()\
    .go()
```
```sql
DELETE FROM `users` WHERE `name` = 'John' LIMIT 1;
```
- Delete rows
```python
qb.delete('comments')\
    .where([['user_id', '=', 10]])\
    .go()
```
```sql
DELETE FROM `comments` WHERE `user_id` = 10;
```
- Truncate a table
```python
qb.truncate('users').go()
```
```sql
TRUNCATE TABLE `users`;
```
- Drop a table
```python
qb.drop('temporary').go()
```
```sql
DROP TABLE IF EXISTS `temporary`;
```
