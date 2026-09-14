import streamlit as st

# 브라우저 탭 및 기본 레이아웃 설정
st.set_page_config(
    page_title="세계 여행 포털",
    page_icon="🌏",
    layout="wide"
)

# 네비게이션에 연결할 페이지 정의 (src/views 경로 지정)
home_page = st.Page("src/views/home.py", title="홈 (대한민국)", icon="🏠", default=True)
china = st.Page("src/views/china.py", title="중국", icon="🇨🇳")
japan = st.Page("src/views/japan.py", title="일본", icon="🇯🇵")
usa = st.Page("src/views/usa.py", title="미국", icon="🇺🇸")

# 네비게이션 메뉴 생성 및 실행
pg = st.navigation([home_page, china, japan, usa])
pg.run()