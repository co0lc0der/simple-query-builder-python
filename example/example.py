from simple_query_builder import *

qb = QueryBuilder(DataBase(), 'my_db.db')

res = qb.select('cabs')
print(res)
