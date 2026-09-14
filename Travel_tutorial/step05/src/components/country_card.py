import os
import streamlit as st

def render_country_page(flag: str, country_name: str, country_description: str, country_url: str, image_path: str = None):
    # 상단 제목
    st.title(country_name)
    st.divider()

    # 1. 이미지 먼저 출력
    if image_path and os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
    elif image_path:
        st.info(f"이미지 준비 중입니다. (`{image_path}`에 사진을 추가하세요)")

    # 2. 설명 글씨 출력
    st.write(country_description)
    st.write("")

    # 3. 공식 여행 사이트 링크 버튼
    st.link_button(
        label=f"{country_name} 공식 여행 사이트 방문",
        url=country_url
    )