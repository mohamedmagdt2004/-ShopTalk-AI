from sqlalchemy import create_engine
import pandas as pd

engine = create_engine(
    "mssql+pyodbc://@localhost\\SQLEXPRESS/retail_db?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

def run_query(sql):
    return pd.read_sql(sql, engine)