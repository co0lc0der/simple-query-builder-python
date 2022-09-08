from simple_query_builder import *

qb = QueryBuilder(DataBase(), 'my_db.db')

res = qb.select('users').all()
# SELECT * FROM `users`
print(res)
