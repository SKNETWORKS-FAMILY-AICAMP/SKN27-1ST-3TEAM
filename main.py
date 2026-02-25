import streamlit as st
from common.crawl import crawl_faq
from common.db import DB

st.set_page_config(page_title="전기차 대시보드", layout="wide")

st.title("🚗 대한민국 친환경차 대시보드")
st.markdown("""
---
### 📖 스토리텔링 구성

| 챕터 | 제목 | 내용 |
|------|------|------|
| 🌍 Prologue | 지구가 뜨거워지고 있다 | 기온 상승, 수송 CO2 |
| 📊 Ch.1 | 대한민국 도로의 현실 | 전체 자동차 vs 친환경차 비율 |
| 📈 Ch.2 | 그래도 변하고 있다 | 전기차·수소차·충전소 성장 |
| 🗺️ Ch.3 | 지금 어디까지 왔나 | 지역별 현황, 보조금, 인구 대비 |
| 🔮 Ch.4 | 앞으로의 10년 | 성장 예측, CO2 감축 효과 |

---
왼쪽 사이드바에서 챕터를 선택하세요.
""")
st.code(code, language=None)
