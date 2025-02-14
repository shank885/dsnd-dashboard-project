from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd

# Using pathlib, create a `db_path` variable
# that points to the absolute path for the `employee_events.db` file
db_path = Path(__file__).parent.resolve() / "employee_events.db"


# OPTION 1: MIXIN
# Define a class called `QueryMixin`
class QueryMixin:
    
    # Define a method named `pandas_query`
    # that receives an sql query as a string
    # and returns the query's result
    # as a pandas dataframe
    def pandas_query(self, query):
        try:
            db_conn = connect(db_path)
            df = pd.read_sql_query(query, db_conn)
        except sqlite3.Error as sq_error:
            print(f"Error connecting to database: {sq_error}")
        
        if db_conn:
            db_conn.close()
            return df
        else:
            return pd.DataFrame()

    # Define a method named `query`
    # that receives an sql_query as a string
    # and returns the query's result as
    # a list of tuples. (You will need
    # to use an sqlite3 cursor)
    def query(self, query):
        try:
            db_conn = connect(db_path)
            cursor = connection.cursor()
            result = cursor.execute(query).fetchall()
        except sqlite3.Error as sq_error:
            print(f"Error connecting to database: {sq_error}")
        
        if db_conn:
            db_conn.close()
            return result
        else:
            return []
 
 
 # Leave this code unchanged
def query(func):
    """
    Decorator that runs a standard sql execution
    and returns a list of tuples
    """

    @wraps(func)
    def run_query(*args, **kwargs):
        query_string = func(*args, **kwargs)
        connection = connect(db_path)
        cursor = connection.cursor()
        result = cursor.execute(query_string).fetchall()
        connection.close()
        return result
    
    return run_query
