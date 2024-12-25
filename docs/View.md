# VIEW
Since [v0.4](https://github.com/co0lc0der/simple-query-builder-python/releases/tag/v0.4)
## CREATE
Create a view from SELECT query
```python
qb.select('users')\
    .where([['email', 'is null'], 'or', ['email', '']])\
    .create_view('users_no_email')\
    .go()
```
Result query
```sql
CREATE VIEW IF NOT EXISTS `users_no_email` AS SELECT * FROM `users` WHERE (`email` IS NULL) OR (`email` = '');
```
One more example
```python
qb.select('users')\
    .is_null('email')\
    .create_view('users_no_email')\
    .go()
```
Result query
```sql
CREATE VIEW IF NOT EXISTS `users_no_email` AS SELECT * FROM `users` WHERE (`email` IS NULL);
```
- Without `IF EXISTS`
```python
qb.select('users')\
    .is_null('email')\
    .create_view('users_no_email', False)\
    .go()
```
Result query
```sql
CREATE VIEW `users_no_email` AS SELECT * FROM `users` WHERE (`email` IS NULL);
```
## DROP
- Drop a view
```python
qb.drop_view('users_no_email').go()
```
Result query
```sql
DROP VIEW IF EXISTS `users_no_email`;
```
- Without `IF EXISTS`
```python
qb.drop_view('users_no_email', False).go()
```
Result query
```sql
DROP VIEW `users_no_email`;
```

Back to [doc index](index.md) or [readme](../README.md)
