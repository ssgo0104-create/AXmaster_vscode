"""
Most Streamed Spotify Songs 2025 데이터셋 기초 탐색
pandas   head / tail / shape / info / columns 를 사용해서 데이터셋의 기본 정보를
화면에 순서대로 보여주는 streamlit 앱이다
실행방법 streamlit run 9-7-2.py
"""

import pandas as pd
import streamlit as st

st.title("Most Streamed Spotify Songs 2025🎵")

CSV_PATH = "most_streamed_spotify_2025.csv"

upload_file = st.file_uploader("most_streamed_spotify_2025.csv 파일을 직접 업로드 할 수 있습니다(선택사항)", type="csv")

if upload_file is not None:
    df = pd.read_csv(upload_file)
else:
    try:
        df = pd.read_csv(CSV_PATH)
    except FileNotFoundError :
        st.error("❌ 파일을 찾을 수가 없습니다.")
        st.info("같은 경로에 파일을 업로드 하거나 csv 파일을 폴더에 넣고 새로고침 하세요.")
        df = None


if df is not None :
    st.subheader("1) 상위 30곡 ")
    st.dataframe(df.head(30), use_container_width=True)

    st.subheader("2) 하위 30곡")
    st.dataframe(df.tail(30), use_container_width=True)

    st.subheader("3) 전체 곡 개수, 열개수")
    col1, col2 = st.columns(2)
    with col1 :
        st.metric("전체 곡 개수", f"{df.shape[0]}개")
    with col2 :
        st.metric("열개수", f"{df.shape[1]}개")

    st.subheader("4) 전체 열 이름 목록")
    st.write(df.columns)

    st.subheader("5) 각 열의 자료형과 결측치(Nan 여부 요약)")
    info_df = pd.DataFrame({
        "타입" : df.dtypes,
        "결측치 아닌 개수" : df.notna().sum(),
        "결측치 개수" : df.isna().sum(),
    })
    st.dataframe(info_df, use_container_width=True)