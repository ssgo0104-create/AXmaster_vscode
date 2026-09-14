# import streamlit as st

# st.set_page_config(page_title="세계 여행 포털", page_icon="🌏")


# # 사이드 바
# menu = st.sidebar.radio("메뉴", ["홈","미국","중국","일본"])

# if menu == "홈":
#     대한민국
#     대한민국 설명

# elif menu == "미국":
#     미국
#     미국 설명
#     링크 버튼(미국공식사이트방문)



import streamlit as st

# 1. 브라우저 탭 설정
st.set_page_config(page_title="세계 여행 포털", page_icon="🌏")

# 2. 사이드바 메뉴 생성
menu = st.sidebar.radio("메뉴", ["홈", "미국", "중국", "일본"])

# 3. 메뉴별 화면 출력
if menu == "홈":
    st.title("KR 대한민국")
    st.write("대한민국은 동아시아에 위치한 나라로, 한반도의 남쪽에 자리잡고 있습니다.")
    st.link_button("대한민국 관광 공식 사이트 방문", "https://korean.visitkorea.or.kr")

elif menu == "미국":
    st.title("US 미국")
    st.write("미국은 북아메리카에 위치한 나라로, 50개 주와 다양한 자연경관 및 대도시가 공존하는 곳입니다.")
    st.link_button("미국 관광청 공식 사이트 방문", "https://www.gousa.or.kr")

elif menu == "중국":
    st.title("CN 중국")
    st.write("중국은 동아시아에 위치한 나라로, 유구한 역사와 광활한 대륙, 풍부한 문화유산을 지니고 있습니다.")
    st.link_button("중국 관광청 공식 사이트 방문", "https://www.ctrip.com/")

elif menu == "일본":
    st.title("JP 일본")
    st.write("일본은 동아시아 열도에 위치한 나라로, 전통 문화와 현대 도시의 매력이 어우러진 여행지입니다.")
    st.link_button("일본 관광청(JNTO) 공식 사이트 방문", "https://www.japan.travel/ko/kr/")