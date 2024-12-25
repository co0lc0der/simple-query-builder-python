# SELECT
## Simple queries
### Select all rows from a table
```python
results = qb.select('users').all()
```
Result query
```sql
SELECT * FROM `users`;
```
### Select a row with a condition
```python
results = qb.select('users').where([['id', '=', 10]]).one()
```
It's able not using equals `=` in `WHERE` conditions since [v0.3.4](https://github.com/co0lc0der/simple-query-builder-python/releases/tag/v0.3.4) 
```python
results = qb.select('users').where([['id', 10]]).one()
```
Result query
```sql
SELECT * FROM `users` WHERE `id` = 10;
```
### Select rows with two conditions
```python
results = qb.select('users').where([['id', '>', 1], 'and', ['group_id', '=', 2]]).all()
```
or since [v0.3.4](https://github.com/co0lc0der/simple-query-builder-python/releases/tag/v0.3.4)
```python
results = qb.select('users').where([['id', '>', 1], 'and', ['group_id', 2]]).all()
```
Result query
```sql
SELECT * FROM `users` WHERE (`id` > 1) AND (`group_id` = 2);
```
### Select a row with a `LIKE` and `NOT LIKE` condition
```python
results = qb.select('users').like(['name', '%John%']).all()

# or
results = qb.select('users').where([['name', 'LIKE', '%John%']]).all()
```
or it's able to use two strings in parameters since [v0.3.5](https://github.com/co0lc0der/simple-query-builder-python/releases/tag/v0.3.5)
```python
results = qb.select('users').like('name', '%John%').all()
```
Result query
```sql
SELECT * FROM `users` WHERE (`name` LIKE '%John%');
```
```python
results = qb.select('users').not_like(['name', '%John%']).all()

# or
results = qb.select('users').where([['name', 'NOT LIKE', '%John%']]).all()
```
or it's able to use two strings in parameters since [v0.3.5](https://github.com/co0lc0der/simple-query-builder-python/releases/tag/v0.3.5)
```python
results = qb.select('users').not_like('name', '%John%').all()
```
Result query
```sql
SELECT * FROM `users` WHERE (`name` NOT LIKE '%John%');
```
### Select a row with a `IS NULL` and `IS NOT NULL` condition
since [v0.3.5](https://github.com/co0lc0der/simple-query-builder-python/releases/tag/v0.3.5)
```python
results = qb.select('users').is_null('phone').all()

# or
results = qb.select('users').where([['phone', 'is null']]).all()
```
Result query
```sql
SELECT * FROM `users` WHERE (`phone` IS NULL);
```
```python
results = qb.select('customers').is_not_null('address').all()

# or
results = qb.select('customers').not_null('address').all()

# or
results = qb.select('customers').where([['address', 'is not null']]).all()
```
Result query
```sql
SELECT * FROM `customers` WHERE (`address` IS NOT NULL);
```
### Select rows with `OFFSET` and `LIMIT`
```python
results = qb.select('posts')\
    .where([['user_id', '=', 3]])\
    .offset(14)\
    .limit(7)\
    .all()
```
It's able not using equals `=` in `WHERE` conditions since [v0.3.4](https://github.com/co0lc0der/simple-query-builder-python/releases/tag/v0.3.4) 
```python
results = qb.select('posts')\
    .where([['user_id', 3]])\
    .offset(14)\
    .limit(7)\
    .all()
```
Result query
```sql
SELECT * FROM `posts` WHERE (`user_id` = 3) OFFSET 14 LIMIT 7;
```
### Select custom fields with additional SQL
#### `COUNT()`
```python
results = qb.select('users', {'counter': 'COUNT(*)'}).one()

# or
results = qb.count('users').one()
```
Result query
```sql
SELECT COUNT(*) AS `counter` FROM `users`;
```
#### `ORDER BY`
```python
results = qb.select({'b': 'branches'}, ['b.id', 'b.name'])\
    .where([['b.id', '>', 1], 'and', ['b.parent_id', 1]])\
    .order_by('b.id', 'desc')\
    .all()
```
It's able not using equals `=` in `WHERE` conditions since [v0.3.4](https://github.com/co0lc0der/simple-query-builder-python/releases/tag/v0.3.4) 
```python
results = qb.select({'b': 'branches'}, ['b.id', 'b.name'])\
    .where([['b.id', '>', 1], 'and', ['b.parent_id', 1]])\
    .order_by('b.id desc')\
    .all()
```
Result query
```sql
SELECT `b`.`id`, `b`.`name` FROM `branches` AS `b`
WHERE (`b`.`id` > 1) AND (`b`.`parent_id` = 1)
ORDER BY `b`.`id` DESC;
```
#### `DISTINCT`
```python
results = qb.select('customers', ['city', 'country'], True).order_by('country desc').all()
```
Result query
```sql
SELECT DISTINCT `city`, `country` FROM `customers` ORDER BY `country` DESC;
```
#### `GROUP BY` and `HAVING`
```python
results = qb.select('posts', ['id', 'category', 'title'])\
    .where([['views', '>=', 1000]])\
    .group_by('category')\
    .all()
```
Result query
```sql
SELECT `id`, `category`, `title` FROM `posts`
WHERE (`views` >= 1000) GROUP BY `category`;
```
More complicated example
```python
groups = qb.select('orders', {'month_num': 'MONTH(`created_at`)', 'total': 'SUM(`total`)'})\
    .where([['YEAR(`created_at`)', '=', 2020]])\
    .group_by('month_num')\
    .having([['total', '=', 20000]])\
    .all()
```
It's able not using equals `=` in `HAVING` conditions since [v0.3.4](https://github.com/co0lc0der/simple-query-builder-python/releases/tag/v0.3.4) 
```python
groups = qb.select('orders', {'month_num': 'MONTH(`created_at`)', 'total': 'SUM(`total`)'})\
    .where([['YEAR(`created_at`)', 2020]])\
    .group_by('month_num')\
    .having([['total', 20000]])\
    .all()
```
Result query
```sql
SELECT MONTH(`created_at`) AS `month_num`, SUM(`total`) AS `total`
FROM `orders` WHERE (YEAR(`created_at`) = 2020)
GROUP BY `month_num` HAVING (`total` = 20000);
```

To the [SELECT extensions section](Select_ext.md)

Back to [doc index](index.md) or [readme](../README.md)
