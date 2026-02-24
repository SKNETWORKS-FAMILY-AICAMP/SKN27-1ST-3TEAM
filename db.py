import pandas as pd
import sqlalchemy

DB_URL = 'mysql+mysqlconnector://car_insert:car1234@localhost:3306/car_insert'

engine = sqlalchemy.create_engine(DB_URL)

def query(sql):
    with engine.connect() as conn:
        df = pd.read_sql(sql, conn)
    return df

print(query("select * from region"))



