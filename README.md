# QueryBuilder python module

[![Latest Version](https://img.shields.io/github/release/co0lc0der/simple-query-builder-python?color=orange&style=flat-square)](https://github.com/co0lc0der/simple-query-builder-python/release)
![GitHub repo size](https://img.shields.io/github/repo-size/co0lc0der/simple-query-builder-python?label=size&style=flat-square)
[![GitHub license](https://img.shields.io/github/license/co0lc0der/simple-query-builder-python?style=flat-square)](https://github.com/co0lc0der/simple-query-builder-python/blob/main/LICENSE.md)
![Python 3.7, 3.8, 3.9, 3.10, 3.11, 3.12](https://img.shields.io/pypi/pyversions/simple-query-builder?color=blueviolet&style=flat-square)
![PyPI](https://img.shields.io/pypi/v/simple-query-builder?color=yellow&style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/simple-query-builder?color=darkgreen&style=flat-square)

This is a small easy-to-use module for working with a database. It provides some public methods to compose SQL queries and manipulate data. Each SQL query is prepared and safe. QueryBuilder fetches data to _dictionary_ by default. At present time the component supports SQLite (file or memory).

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
### Import the module and init `QueryBuilder` with `Database()`
```python
from simple_query_builder import *

qb = QueryBuilder(DataBase(), 'my_db.db')

# or DB in memory
qb = QueryBuilder(DataBase(), ':memory:')
```
### Usage examples
#### Select all rows from a table
```python
results = qb.select('users').all()
```
Result query
```sql
SELECT * FROM `users`;
```
#### Select rows with two conditions
```python
results = qb.select('users').where([['id', '>', 1], 'and', ['group_id', '=', 2]]).all()
```
Result query
```sql
SELECT * FROM `users` WHERE (`id` > 1) AND (`group_id` = 2);
```
#### Update a row
```python
qb.update('users', {
        'username': 'John Doe',
        'status': 'new status'
    })\
    .where([['id', '=', 7]])\
    .limit()\
    .go()
```
Result query
```sql
UPDATE `users` SET `username` = 'John Doe', `status` = 'new status'
WHERE `id` = 7 LIMIT 1;
```
More examples you can find in [documentation](https://github.com/co0lc0der/simple-query-builder-python/blob/main/docs/index.md)

## ToDo
I'm going to add the next features into future versions
- write more unit testes
- add subqueries for QueryBuilder
- add `BETWEEN`
- add `WHERE EXISTS`
- add TableBuilder class (for beginning `CREATE TABLE`, move `qb.drop()` and `qb.truncate()` into it)
- add MySQL support
- add PostgreSQL support
- add `WITH`
- and probably something more
