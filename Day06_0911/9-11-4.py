import pandas as pd
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="파일 업로드 문서 요약 앱", layout="wide")

st.title("📄 파일 업로드 문서 요약 앱")

# ---------- 사이드바 설정 ----------
with st.sidebar:
    st.header("⚙️ 설정")

    # 4) 개인 OpenAI Key 및 모델 선택
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        help="sk-로 시작하는 OpenAI API Key를 입력하세요",
    )
    model = st.selectbox(
        "모델 선택",
        ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini"],
        index=0,
    )
    st.markdown("[🔑 API Key 발급받기](https://platform.openai.com/api-keys)")

    st.divider()

    # 5) 요약 옵션 (분량)
    length_option = st.selectbox(
        "요약 분량",
        ["짧게 (3줄)", "보통 (5-7줄)", "자세히 (Bullet Point)"],
        index=1,
    )

    # 6) 요약 스타일 드롭다운
    style_option = st.selectbox(
        "요약 스타일",
        [
            "일반/전문적 (격식 있는 보고서 톤)",
            "핵심 위주 (군더더기 없는 개조식 요약)",
            "친절하고 쉬운 설명 (비전문가/초보자 맞춤형)",
            "회의록/액션아이템 중심 (주요 안건 및 조치사항)",
        ],
        index=0,
    )

# ---------- 메인 영역: 1) 파일 업로드 ----------
uploaded_file = st.file_uploader(
    "요약할 파일을 업로드하세요 (지원 형식: TXT, CSV, MD)",
    type=["txt", "csv", "md"],
)

file_content = ""

# 1) 확장자 검증 및 파일 내용 읽기
if uploaded_file is not None:
    file_name = uploaded_file.name
    file_extension = file_name.split(".")[-1].lower()

    if file_extension not in ["txt", "csv", "md"]:
        st.error(
            "⚠️ 올바른 확장자가 아니라 업로드가 불가능합니다. (TXT, CSV, MD 파일만 지원됩니다)"
        )
    else:
        st.success(f"'{file_name}' 파일이 성공적으로 업로드되었습니다.")

        try:
            if file_extension == "csv":
                # CSV 파일 처리
                df = pd.read_csv(uploaded_file)
                file_content = df.to_csv(index=False)

                # 2) 문서 미리보기 (데이터프레임 형태)
                st.subheader("👀 업로드한 문서 미리보기")
                st.dataframe(df.head(20), use_container_width=True)
                st.caption(f"* 총 {len(df):,}개의 행 중 상위 20개 행만 미리 표시합니다.")

            else:
                # TXT, MD 파일 처리
                bytes_data = uploaded_file.getvalue()
                try:
                    file_content = bytes_data.decode("utf-8")
                except UnicodeDecodeError:
                    file_content = bytes_data.decode("cp949")  # 한글 인코딩 대응

                # 2) 문서 미리보기 (텍스트/마크다운 렌더링)
                st.subheader("👀 업로드한 문서 미리보기")
                with st.expander("문서 내용 펼치기 / 접기", expanded=True):
                    if file_extension == "md":
                        st.markdown(file_content)
                    else:
                        st.text_area(
                            "원문 내용",
                            value=file_content,
                            height=250,
                            disabled=True,
                        )

        except Exception as e:
            st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")

# ---------- 3) 요약하기 버튼 및 요약 수행 ----------
st.divider()

if st.button("✨ 요약하기", type="primary"):
    if not api_key:
        st.error("사이드바에 OpenAI API Key를 입력해 주세요.")
    elif uploaded_file is None or not file_content.strip():
        st.warning("먼저 요약할 파일을 업로드해 주세요.")
    else:
        # 프롬프트 조립
        system_instruction = f"""
당신은 뛰어난 문서 요약 전문가입니다.
사용자가 제공한 문서를 다음 지침에 맞춰 완벽히 요약하세요:

[요약 분량 지침]
- {length_option} 기준에 철저히 맞춰 작성하세요.
  * '짧게 (3줄)': 정확히 3줄 문장으로 핵심만 작성.
  * '보통 (5-7줄)': 5~7줄 분량으로 주요 문맥을 살려 작성.
  * '자세히 (Bullet Point)': 항목별 기호(•, -)를 사용해 세부 사항까지 체계적으로 정리.

[요약 스타일 지침]
- 스타일: {style_option}
- 원문의 사실을 왜곡하거나 없는 내용을 지어내지 말고, 원문 내용에 기반해 작성하세요.
"""

        user_prompt = f"""
다음 문서를 위의 지침에 맞게 요약해 주세요.

[문서 내용]
\"\"\"
{file_content}
\"\"\"
"""

        try:
            client = OpenAI(api_key=api_key)

            # 요약 중 로딩 메시지 출력
            with st.spinner("⏳ 문서를 꼼꼼히 분석하여 요약 중입니다... 잠시만 기다려 주세요."):
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_prompt},
                    ],
                )

            summary_result = response.choices[0].message.content

            # 결과 출력
            st.success("요약이 완료되었습니다!")
            st.subheader("📋 문서 요약 결과")
            st.info(f"적용 옵션: **{length_option}** | 스타일: **{style_option}** | 모델: **{model}**")
            st.markdown(summary_result)

        except Exception as e:
            st.error(f"요약 중 오류가 발생했습니다: {e}")