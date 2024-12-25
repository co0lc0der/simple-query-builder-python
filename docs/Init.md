# Initialization
## Import the module and init `QueryBuilder` with `Database()`
```python
from simple_query_builder import *

# if you want to get results as a list of dictionaries (by default since 0.3.5)
qb = QueryBuilder(DataBase(), 'my_db.db') # result_dict=True, print_errors=False

# or if you want to get results as a list of tuples (since 0.3.5)
qb = QueryBuilder(DataBase(), 'my_db.db', result_dict=False)

# for printing errors into terminal (since 0.3.5)
qb = QueryBuilder(DataBase(), 'my_db.db', print_errors=True)

# DB in memory
qb = QueryBuilder(DataBase(), ':memory:')
```

To the [Methods section](Methods.md)

Back to [doc index](index.md) or [readme](../README.md)
