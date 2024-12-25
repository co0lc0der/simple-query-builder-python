# UPDATE
## Update a row
```python
qb.update('users', {
        'username': 'John Doe',
        'status': 'new status'
    })\
    .where([['id', '=', 7]])\
    .limit()\
    .go()
```
or since [v0.3.4](https://github.com/co0lc0der/simple-query-builder-python/releases/tag/v0.3.4)
```python
qb.update('users', {
        'username': 'John Doe',
        'status': 'new status'
    })\
    .where([['id', 7]])\
    .limit()\
    .go()
```
Result query
```sql
UPDATE `users` SET `username` = 'John Doe', `status` = 'new status'
WHERE `id` = 7 LIMIT 1;
```
## Update rows
```python
qb.update('posts', {'status': 'published'})\
    .where([['YEAR(`updated_at`)', '>', 2020]])\
    .go()
```
Result query
```sql
UPDATE `posts` SET `status` = 'published'
WHERE (YEAR(`updated_at`) > 2020);
```

To the [DELETE section](Delete.md)

Back to [doc index](index.md) or [readme](../README.md)
