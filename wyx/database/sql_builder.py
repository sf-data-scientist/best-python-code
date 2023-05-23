import copy
from pymysql import escape_string


class SQLBuilder(object):

    @classmethod
    def translate_value(cls, input):
        output = copy.deepcopy(input)
        for k, v in output.items():
            try:
                str_tuple = (str, unicode)
            except:
                str_tuple = (str)
            if isinstance(v, str_tuple):
                new_v = escape_string(v.replace('%', '%%').replace(':', '\\:'))
                output[k] = "'{new_v}'".format(new_v=new_v)
            elif v is None:
                output[k] = 'null'
        return output

    @classmethod
    def insert_into_on_duplicate_update(cls, table, insert_columns, update_columns, values):
        # 1. check
        if isinstance(insert_columns, (list, tuple)):
            insert_columns = tuple(insert_columns)
        else:
            raise Exception('insert_columns only support list or tuple')
        if not isinstance(update_columns, (list, tuple)):
            raise Exception('update_columns only support list or tuple')

        # 2. build columns & assignment_list
        columns_s = str(insert_columns).replace('\'', '').replace("\"", "")
        update_columns_list = ['{column}=VALUES({column})'.format(column=i) for i in update_columns]
        assignment_list_s = ','.join(update_columns_list)

        # 3. build values
        values = copy.deepcopy(values)
        value_template = '(' + ','.join(['{' + i + '}' for i in insert_columns]) + ')'
        values = [cls.translate_value(i) for i in values]
        values = [value_template.format(**i) for i in values]
        values_s = ','.join(values)

        sql = """
        INSERT INTO {table} {columns}
        VALUES {values}
        ON DUPLICATE KEY UPDATE {assignment_list};""".format(table=table, columns=columns_s, values=values_s,
                                                             assignment_list=assignment_list_s)
        return sql
