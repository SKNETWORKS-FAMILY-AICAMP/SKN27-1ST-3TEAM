import streamlit as st
import pandas as pd
from common.db2 import DB

class FAQ:
    def __init__(self):
        #DB에서 데이터 가져오기
        #FAQ_table
        
        self.db = DB("FAQ_table", "FAQ_id")
        self.df = self.db.select_table()
        self.df_ = pd.DataFrame(self.df)
        self.ca =  [
            "전체", 
            "차량구매", 
            "차량정비",  
            "홈페이지", 
            "모젠서비스", 
            "블루링크", 
            "현대 디지털 키"
            ]
    
    
    #확인
    def show_category(self, category_name, search_text=None):

        filtered_df = self.df_.copy()

        # 카테고리 필터
        if category_name != "전체":
            filtered_df = filtered_df[
                filtered_df["category"].str.contains(category_name, na=False)
            ]

        # 검색 필터 (제목 OR 내용)
        if search_text:
            filtered_df = filtered_df[
                filtered_df["title"].str.contains(search_text, case=False, na=False) |
                filtered_df["content"].str.contains(search_text, case=False, na=False)
            ]

        # 출력
        if filtered_df.empty:
            st.warning("검색 결과가 없습니다.")
            return

        for _, row in filtered_df.iterrows():
            with st.expander(f"{row['title']}"):
                st.markdown(f"**카테고리:** {row['category']}")
                st.markdown("---")
                st.write(row["content"])
    

    def main(self):

        container = st.container(border=True)
        container.header("🤔 자주 묻는 질문(FAQ)")
        container.text("현대 전기차 관련 궁금증을 해결해 드립니다.")

        # 검색창
        search_text = st.text_input("🔎 질문을 검색하세요")

        # 탭 생성
        tabs = st.tabs(self.ca)

        print(self.df_.head())  

        for tab, category in zip(tabs, self.ca):
            with tab:
                self.show_category(category, search_text)
    

if __name__ == "__main__":
    faq = FAQ()
    faq.main()

