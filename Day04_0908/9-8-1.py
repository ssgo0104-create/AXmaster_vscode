# raw_trade_data.csv 파일 활용
# HS코드가 
# 85로 시작하는 (반도체류) + 국가명 미국 또는 베트남 + 수출금액 0보다 큰 수(실제 수출 실적이 있는) 행만
# 다중 조건으로 필터링 한 뒤, 수출 금액 상위 10건을 화면에 보여주고 report.csv 로 저장
# streamlit 사용 streamlit run 9-8-1.py
#dsgag

import os
import pandas as pd
import streamlit as st

# 1. 페이지 기본 설정 및 디자인 테마 적용
st.set_page_config(
    page_title="반도체류(HS Code 85) 수출 분석 보고서",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 제목 및 헤더 영역
st.title("📈 반도체류(HS Code 85) 수출 데이터 분석")
st.markdown("""
이 애플리케이션은 **raw_trade_data.csv** 파일을 분석하여 특정 조건에 부합하는 수출 실적을 필터링하고 시각화합니다.
""")

# 3. 경로 설정 (스크립트 위치 기준 동적 경로)
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, 'raw_trade_data.csv')
report_path = os.path.join(current_dir, 'report.csv')

# 4. 파일 존재 여부 및 데이터 로드/처리
if not os.path.exists(csv_path):
    st.error(f"❌ 데이터 파일을 찾을 수 없습니다: `{csv_path}`")
else:
    # 데이터 불러오기
    df = pd.read_csv(csv_path)
    
    # 5. 다중 조건 필터링
    # - HS코드가 '85'로 시작하는 행 (반도체류)
    # - 국가명이 '미국' 또는 '베트남'인 행
    # - 수출금액이 0보다 큰 행 (실제 수출 실적이 존재하는 행)
    filtered_df = df[
        (df['hs_code'].astype(str).str.startswith('85')) &
        (df['국가명'].isin(['미국', '베트남'])) &
        (df['수출금액'] > 0)
    ]
    
    # 수출금액 내림차순 정렬 후 상위 10건 추출
    top_10_df = filtered_df.sort_values(by='수출금액', ascending=False).head(10).reset_index(drop=True)
    
    # 6. report.csv로 저장 (Excel 한글 깨짐 방지를 위해 utf-8-sig 인코딩 사용)
    top_10_df.to_csv(report_path, index=False, encoding='utf-8-sig')
    
    # 성공 메시지 출력
    st.success(f"💾 필터링된 상위 10건의 데이터를 성공적으로 `{os.path.basename(report_path)}` 파일로 저장했습니다!")
    
    # 7. 주요 지표 요약 (Metric Card)
    st.markdown("### 📊 주요 지표 요약")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="필터링된 전체 수출 건수", 
            value=f"{len(filtered_df):,} 건",
            help="HS코드 85로 시작 + 미국/베트남 + 수출금액 > 0에 부합하는 전체 행 수"
        )
        
    with col2:
        total_top_10_export = top_10_df['수출금액'].sum()
        st.metric(
            label="상위 10건 총 수출 금액", 
            value=f"${total_top_10_export:,.0f}",
            help="상위 10건의 수출 금액 합계"
        )
        
    with col3:
        max_export = top_10_df['수출금액'].max()
        st.metric(
            label="최대 단일 수출 금액", 
            value=f"${max_export:,.0f}",
            help="필터링된 전체 건 중 단일 행 최대 수출 금액"
        )
        
    st.markdown("---")
    
    # 8. 상위 10건 데이터프레임 시각화
    st.markdown("### 🏆 수출 금액 상위 10건 목록")
    
    # 화면 표시를 위해 금액 및 중량 컬럼 포맷팅 적용
    display_df = top_10_df.copy()
    display_df['수출금액'] = display_df['수출금액'].apply(lambda x: f"${x:,.0f}")
    display_df['중량'] = display_df['중량'].apply(lambda x: f"{x:,.2f} kg" if pd.notnull(x) else "-")
    
    # Streamlit 데이터프레임으로 출력
    st.dataframe(display_df, use_container_width=True)
    
    st.markdown("---")
    
    # 9. 상위 10건 시각화 차트
    st.markdown("### 📊 상위 10건 수출 금액 시각화")
    
    # 차트 범례 가독성을 위해 '날짜 (국가)' 형식의 새 컬럼 생성
    chart_df = top_10_df.copy()
    chart_df['날짜_국가'] = chart_df['날짜'] + " (" + chart_df['국가명'] + ")"
    
    # Streamlit 내장 막대 그래프 사용
    st.bar_chart(
        data=chart_df, 
        x='날짜_국가', 
        y='수출금액', 
        use_container_width=True
    )
    
    st.markdown("---")
    
    # 10. 사이드바 및 다운로드 링크 제공
    st.sidebar.markdown("### 🛠️ 데이터 분석 조건")
    st.sidebar.info("""
    - **품목 코드 (HS Code):** 85... (반도체류)
    - **대상 국가:** 미국, 베트남
    - **수출 실적:** 수출금액 > $0
    """)
    
    st.sidebar.markdown("### 📥 보고서 다운로드")
    
    # 다운로드용 이진 데이터 생성
    csv_bytes = top_10_df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
    st.sidebar.download_button(
        label="📥 report.csv 다운로드",
        data=csv_bytes,
        file_name='report.csv',
        mime='text/csv'
    )
    
    st.sidebar.markdown("---")
    st.sidebar.caption("제작: Gemini CLI Assistant (2026)")
