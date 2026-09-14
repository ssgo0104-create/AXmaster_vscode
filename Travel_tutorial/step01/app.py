# import streamlit as st

# st.set_page_config(page_title="세계 여행 포털", page_icon="🌏")

# st.title("KR 대한민국")
# st.write("대한민국은 동아시아에 위치한 나라로, 한반도의 남쪽에 자리잡고 있습니다.")



import streamlit as st

# 브라우저 탭 설정
st.set_page_config(page_title="세계 여행 포털", page_icon="🌏")

# 국가 선택 라디오 버튼 (가로 정렬)
country = st.radio(
    "국가를 선택하세요",
    ["대한민국", "미국", "중국", "일본"],
    horizontal=True
)

# 선택한 국가에 따라 제목과 설명 출력
if country == "대한민국":
    st.title("KR 대한민국")
    st.write("대한민국은 동아시아에 위치한 나라로, 한반도의 남쪽에 자리잡고 있습니다.")

elif country == "미국":
    st.title("US 미국")
    st.write("미합중국은 북아메리카에 위치한 세계 최대 경제 대국이자 다양한 문화와 광활한 자연을 품고 있는 나라입니다.")

elif country == "중국":
    st.title("CN 중국")
    st.write("중국은 동아시아에 위치한 나라로, 유구한 역사와 넓은 영토, 풍부한 문화유산을 보유하고 있습니다.")

elif country == "일본":
    st.title("JP 일본")
    st.write("일본은 동아시아 태평양 연안에 위치한 열도 국가로, 전통과 첨단 기술이 공존하는 여행지입니다.")