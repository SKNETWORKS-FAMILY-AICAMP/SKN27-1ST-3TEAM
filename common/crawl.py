import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import pymysql
from common.db import DB

## 페이지에서 원하는 데이터를 크롤링함
def crawl_faq():

    driver = webdriver.Chrome()
    driver.get("https://www.hyundai.com/kr/ko/faq.html")

    wait = WebDriverWait(driver, 10)

    data = []

    while True:

        # FAQ 로딩 대기
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.ui_accordion.acc_01 dl")
            )
        )

        time.sleep(10)

        faq_list = driver.find_elements(
            By.CSS_SELECTOR,
            "div.ui_accordion.acc_01 dl"
        )

        for faq in faq_list:
            try:
                dt = faq.find_element(By.CSS_SELECTOR, "dt")

                category = dt.find_element(By.CSS_SELECTOR, "b i").text
                title = dt.find_element(By.CSS_SELECTOR, "b span").text

                # 내용 열기 (JS 클릭이 안전)
                driver.execute_script("arguments[0].click();", dt)
                time.sleep(0.3)

                content = faq.find_element(By.CSS_SELECTOR, "dd div.exp").text

                data.append({
                    "title": title,
                    "content": content,
                    "category": category
                })

            except:
                continue

        # 🔥 다음 페이지 숫자 버튼 찾기
        try:
            current_page = driver.find_element(By.CSS_SELECTOR, "div.pagination strong")
            next_page = current_page.find_element(By.XPATH, "following-sibling::a[1]")

            driver.execute_script("arguments[0].click();", next_page)
            time.sleep(2)

        except:
            # 다음 페이지 없으면 종료
            break

    driver.quit()

    df = pd.DataFrame(data)

    return df

## 크롤링한 데이터를 DB에 저장
def save_to_mysql(func):
    db = DB("FAQ_table", "FAQ_id")
    conn = db.conn
    cursor = conn.cursor()

    sql = """
        INSERT INTO FAQ_table (title, content, category)
        VALUES (%s, %s, %s)
    """

    for _, row in func.iterrows():
        cursor.execute(sql, (row["title"], row["content"], row["category"]))

    conn.commit()
    conn.close()

    print("DB 저장 완료")


@st.cache_data
def load_faq():
    return crawl_faq()

#크롤링 실행
if __name__=="__main__":
    save_to_mysql(crawl_faq())