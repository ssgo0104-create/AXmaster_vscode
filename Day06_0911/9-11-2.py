# # OpenAI API key
# # 질문 하나 입력하면 OpenAI chat  Completions API 한 번 호출
# # 답변을 받아오는 가장 단순한 방법
# # 대화 기록을 기억하지 않는 단발성 질문-답변
# # streamlit run 9-11-2.py

# import streamlit as st
# from openai import OpenAI

# st.set_page_config(page_title="나의 첫번째 챗봇", page_icon="🤖")
# st.title("예제 1) 나의 첫번째 챗봇")
# st.caption("질문 하나 입력하면 OpenAi chat Completions API 한 번 호출, 답변을 받아오는 가장 단순한 방법")

# # ----------사이드바 API 모델----------

# with st.sidebar: 
#     st.header("설정")
#     api_key = st.text_input("OpenAI API Key", type="password", help="sk-로 시작하는 OpenAI API Key를 입력하세요") # 타입이 그냥 문자이면 다 표시가 됨. 타입을 패스워드로 설정해서 ●●● 의 형태로 입력됨
#     model = st.selectbox("모델 선택", ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini"], index=0)
#     st.markdown("[api 발급 받기](https://platform.openai.com/api-keys)")

# # ----------메인화면----------

# question = st.text_input("질문을 입력하세요", placeholder="예) 오늘 날씨가 어떤가요?")

# if st.button("질문하기"):
#     if not api_key:
#         st.error("OpenAI API Key를 입력하세요")
#     elif not question:
#         st.warning("질문을 입력하세요.")
#     else:
#         client = OpenAI(api_key=api_key)
#         답변을 생각하는 중..
#         주인님으로 시작하는 친절한 답변가

#     사용한 토큰수 표기(비용감을 잡는데 유용하게...
#         입력 토큰, 출력 토큰, 총 토큰수)

#     오류가 있으면 있다고 메시지 출력




import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI 비서 서비스", layout="centered")

st.title("🤖 무엇이든 물어보세요")

# ----------사이드바 API 모델----------
with st.sidebar:
    st.header("설정")
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        help="sk-로 시작하는 OpenAI API Key를 입력하세요",  # 타입이 그냥 문자이면 다 표시가 됨. 타입을 패스워드로 설정해서 ●●● 의 형태로 입력됨
    )
    model = st.selectbox(
        "모델 선택",
        ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini"],
        index=0,
    )
    st.markdown("[api 발급 받기](https://platform.openai.com/api-keys)")

# ----------메인 영역----------
question = st.text_input("질문을 입력하세요", placeholder="예) 오늘 날씨가 어떤가요?")

if st.button("질문하기", type="primary"):
    if not api_key:
        st.error("OpenAI API Key를 입력하세요.")
    elif not question:
        st.warning("질문을 입력하세요.")
    else:
        try:
            client = OpenAI(api_key=api_key)

            # 로딩 상태 표시
            with st.spinner("답변을 생각하는 중..."):
                response = client.chat.completions.create(
                    model=model,  # 사이드바에서 선택한 모델 변수 적용
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "당신은 예의 바르고 헌신적인 AI 비서입니다. "
                                "모든 답변은 반드시 '주인님'으로 시작하여 매우 친절하고 상냥한 어조로 작성하세요."
                            ),
                        },
                        {"role": "user", "content": question},
                    ],
                )

            # 답변 출력
            answer = response.choices[0].message.content
            st.success("답변이 완료되었습니다.")
            st.markdown(f"### 💬 답변 ({model})\n\n{answer}")

            # 사용 토큰 수 지표 표시
            usage = response.usage
            if usage:
                st.divider()
                st.subheader("📊 사용한 토큰 수")
                col1, col2, col3 = st.columns(3)
                col1.metric("입력 토큰 (Prompt)", f"{usage.prompt_tokens:,}개")
                col2.metric("출력 토큰 (Completion)", f"{usage.completion_tokens:,}개")
                col3.metric("총 토큰 (Total)", f"{usage.total_tokens:,}개")

        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")