import mariadb, sys, os
from dotenv import load_dotenv

load_dotenv()


def db_config():
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT')),
            database=os.getenv('DB_DATABASE'))
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    # Disable Auto-Commit
    conn.autocommit = False
    return conn


"""this function gets table's name and saves its infos.
 it's necessary that  info dictionary keys , equals to table columns."""


def table_insert(table_name, info):
    connection = db_config()
    try:

        cursor = connection.cursor()
        columns_string = '(' + ','.join(info.keys()) + ')'
        values_string = '("' + '","'.join(map(str, info.values())) + '")'
        sql = """INSERT INTO %s %s VALUES %s""" % (table_name, columns_string, values_string)
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception:
        raise Exception


def table_read(table_name, columns, where):
    try:
        connection = db_config()
        cursor = connection.cursor()
        sql = """SELECT %s FROM %s WHERE %s""" % (columns, table_name, where)
        cursor.execute(sql)
        connection.commit()
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result
    except Exception:
        raise Exception

def table_update(table_name,column,where):
    try:
        connection = db_config()
        cursor = connection.cursor()
        sql = """UPDATE %s SET %s WHERE %s""" % (table_name,column, where)
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception:
        raise Exception


