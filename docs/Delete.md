# DELETE
## Delete a row
```python
qb.delete('users')\
    .where([['name', '=', 'John']])\
    .go()
```
or since [v0.3.4](https://github.com/co0lc0der/simple-query-builder-python/releases/tag/v0.3.4)
```python
qb.delete('users')\
    .where([['name', 'John']])\
    .go()
```
Result query
```sql
DELETE FROM `users` WHERE `name` = 'John';
```
## Delete rows
```python
qb.delete('comments')\
    .where([['user_id', '=', 10]])\
    .go()
```
or since [v0.3.4](https://github.com/co0lc0der/simple-query-builder-python/releases/tag/v0.3.4)
```python
qb.delete('comments')\
    .where([['user_id', 10]])\
    .go()
```
Result query
```sql
DELETE FROM `comments` WHERE `user_id` = 10;
```

To the [TABLE section](Table.md)

Back to [doc index](index.md) or [readme](../README.md)
