import pymysql
import pandas as pd
import streamlit as st


class DB:

    def __init__(self,p_table, p_col):

        #DB 연결
        self.conn = pymysql.connect(
            host = "localhost",
            user = "root",
            password = "root1234",
            charset = "utf8mb4",
            database = "car_insert"
        )
        self.table = p_table
        self.col = p_col


    #쿼리문을 통해서 DB명령
    def select_table(self):
        try:
            query = "SELECT * FROM "+self.table
            with self.conn.cursor() as cursor:
                df = pd.read_sql(query, self.conn)
                return df
        except Exception as e:
            st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
            return None

    ## 특정 컬럼만 가져오기 (DB에 저장된 컬럼명)    
    def get_col(self):
        try:
            query = "SELECT " + self.col + " FROM " + self.table
            with self.conn.cursor() as cursor:
                df = pd.read_sql(query, self.conn)
                return df
        except Exception as e:
            st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
            return None


    ## DB에 데이터 삽입 
    def insert_data(self, query):
        try:
            query = "INSERT INTO "+ self.table + query
            for idx in range(len(df)):
                with self.conn.cursor() as cursor:
                    cursor.execute(query)
                    self.conn.commit()
            return True
        except Exception as e:
            st.error(f"데이터를 저장하는 중 오류가 발생했습니다: {e}")
            return False
        
    
    ## DB에 저장된 데이터 출력 
    def write_data(self):
        table = self.select_table()
        col = self.get_col()
        ta_df = st.dataframe(table)
        co_df = st.dataframe(col)

        return ta_df, co_df

    



