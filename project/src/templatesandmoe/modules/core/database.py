from sqlalchemy.sql import text

# Database utility functions


def insert(session, table, parameters):
    fields = [field for field, _ in parameters]
    fields_string = ','.join(fields)
    param_fields = [':' + field for field,_ in parameters]
    param_fields_string = ','.join(param_fields)
    values = [value for _, value in parameters]
    bind_parameters = dict(list(zip(fields, values)))

    query = 'INSERT INTO ' + table + '(' + fields_string + ') VALUES (' + param_fields_string + ')'
    insert = session.execute(text(query), bind_parameters)

    return insert
