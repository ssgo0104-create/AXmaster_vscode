# 인코딩 자동 감지 + 한글 폰트 막대그래프
# 여러 인코딩 방법("utf-8-sig", "cp949", "euc-kr") 순서대로 시도
# 내가 쓸 폰트 같은 경로에 있어야 함
# 객실등급별 생존율 막대그래프 생성 후 그림으로 저장 chart.png
# 실행 streamlit run 9-7-4.py

import os
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from matplotlib import font_manager

st.title("📊인코딩 자동 감지 + 한글 폰트 막대 그래프(Titanic 연습)")
st.caption("여러 인코딩을 순서대로 시도해서 파일을 읽고, 객실등급별 생존율을 그래프로 그립니다")

CSV_PATH = os.path.join(os.path.dirname(__file__),"titanic_cleaned.csv") # 파일명 대/소문자 구분해야함
FONT_PATH = os.path.join(os.path.dirname(__file__),"KoPubWorld Dotum Medium.ttf")

def read_csv_with_auto_encoding(file_path, **kwargs):
    """지정된 인코딩 순서('utf-8-sig', 'cp949', 'euc-kr')대로

    CSV 파일을 읽어 Pandas DataFrame으로 반환합니다.
    """
    encodings = ["utf-8-sig", "cp949", "euc-kr"]

    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding, **kwargs)
            st.success(f"✅성공: '{encoding}' 인코딩으로 파일을 읽었습니다.")
            return df
        except UnicodeDecodeError:
            continue
        except Exception as e:
            # 인코딩 오류가 아닌 파일 경로 없음, 문법 오류 등 다른 예외 발생 시 처리
            raise e

    raise ValueError(
        f"지원하는 인코딩({', '.join(encodings)})으로 파일을 읽을 수 없습니다: {file_path}"
    )

# 인코딩 자동 감지로 csv읽기
st.subheader("1) 인코딩 자동 감지")
df = read_csv_with_auto_encoding(CSV_PATH) # 함수 호출에 CSV_PATH 파일을 넣어서 불러라

st.markdown("---")

# 객실 등급(Pclass) 별 생존율 집계
# Survived 사망 0 / 생존 1 등급별 평균을 내면
# 그대로가 등급의 생존 비율이 된다
# 10명 남3 여자7
# 1000 생존 300 300/1000 30%


pclass_survival_rate = df.groupby("Pclass")["Survived"].mean().sort_index()
st.dataframe( (pclass_survival_rate * 100 ).round(1).rename("생존율(%)") )

# df_df = st.dataframe( (pclass_survival_rate * 100 ).round(1).rename("생존율(%)") )
# st.write(df_df)

# 차트 그리기

st.markdown("---")
st.header("3) 객실등급별 생존율 막대그래프")
try :
    # 폰트 파일이 없으면 FileNotFoundError 가 발생 / try는 폰트가 있을 때 실행
    font_prop = font_manager.FontProperties(fname=FONT_PATH)
    # matplotlib font_manager에 폰트를 등록하고, 전역 폰트로 설정
    font_manager.fontManager.addfont(FONT_PATH)

    plt.rcParams["font.family"] = font_prop.get_name()

    st.write("KoPubWorld Dotum 폰트를 적용했습니다")
except FileNotFoundError :
    st.warning("폰트 파일을 찾을 수 없습니다")



fig, ax = plt.subplots(figsize=(8,5)) # fig(차트 영역), ax(그림 영역) / 아직은 사이즈만 걸어준 거고 어떤 데이터를 가지고 차트를 만들지 지정하지 않음
(pclass_survival_rate * 100 ).plot(kind="bar", color="blue", ax=ax)
ax.set_title("객실 등급별 생존율")
ax.set_xlabel("객실 등급")
ax.set_ylabel("생존율(%)")

st.pyplot(fig) #streamlit으로 g 차트 띄울 때 해당 함수를 써야함

output_png = output_path = os.path.join(os.path.dirname(__file__),"chart.png")
fig.savefig(output_png)
st.success("chart.png로 파일이 저장되었습니다")