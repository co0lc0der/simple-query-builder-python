# Main public methods
## QueryBuilder class
- `query(sql, params, fetch_type, col_index)` executes prepared `sql` with `params`, it can be used for custom queries
- `get_sql()` returns SQL query string which will be executed
- `__str__()` works the same as `get_sql()`
- `get_params()` returns a tuple of parameters for a query
- `get_result()` returns query's result
- `get_count()` returns result's rows count
- `has_error()` returns `True` if an error is had
- `get_error()` returns `True` if an error is had, ***this method will be changed in the next version!***
- `get_error_message()` returns an error message if an error is had
- `set_error(message)` sets `_error` to `True` and `_error_message`
- `get_first()` returns the first item of results
- `get_last()` returns the last item of results
- `reset()` resets state to default values
- `all()` executes SQL query and returns **all rows** of result (`fetchall()`)
- `one()` executes SQL query and returns **the first row** of result (`fetchone()`)
- `column(col)` executes SQL query and returns the needed column of result by its index or name, `col` is `0` by default
- `pluck(key, col)` executes SQL query and returns a list of tuples/dicts (the key (usually ID) and the needed column of result) by its indexes or names, `key` is `0` and `col` is `1` by default
- `go()` this method is for non `SELECT` queries. it executes SQL query and returns nothing (but returns the last inserted row ID for `INSERT` method)
- `exists()` returns `True` if SQL query has at least one row and `False` if it hasn't
- `count()` prepares a query with SQL `COUNT(*)` function and _executes it_

'SQL' methods are presented in the [next section](Select.md)

Back to [doc index](index.md) or [readme](../README.md)
