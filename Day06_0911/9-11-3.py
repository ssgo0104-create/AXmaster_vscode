# 대화 기록을 기억하는 멀티턴 챗봇(스트리밍 응답)
# st.session_state에 대화 기록을 저장해서, 이전 대화 맥락을 기억하는 챗봇
# st.chat_message / st.chat_input 같은 Streamlit 채팅 전용 위젯을 사용합니다.
# stream=True 옵션으로 답변이 실시간으로 타이핑되듯 출력됩니다.
# streamlit run 9-11-3.py

# 시스템 메시지를 사용자가 설정하도록
# 대화 기록 초기화 버튼 



import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="🤖AI 비서 서비스", layout="centered")

st.title("🤖 무엇이든 물어보세요")

# ----------사이드바 설정----------
with st.sidebar:
    st.header("설정")
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
    st.markdown("[API 발급 받기](https://platform.openai.com/api-keys)")

    st.divider()

    # 1. 사용자가 직접 설정하는 시스템 메시지
    default_system_prompt = (
        "당신은 예의 바르고 헌신적인 AI 비서입니다. "
        "모든 답변은 반드시 '주인님'으로 시작하여 매우 친절하고 상냥한 어조로 작성하세요."
    )
    system_prompt = st.text_area(
        "시스템 프롬프트 설정",
        value=default_system_prompt,
        help="AI의 성격과 역할을 지정합니다.",
        height=130,
    )

    # 2. 대화 기록 초기화 버튼
    if st.button("대화 기록 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ----------세션 상태(대화 기록) 초기화----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------이전 대화 기록 화면 렌더링----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------채팅 입력 및 응답 처리----------
if question := st.chat_input("메시지를 입력하세요..."):
    # 1. API 키 확인
    if not api_key:
        st.error("사이드바에서 OpenAI API Key를 먼저 입력하세요.")
    else:
        # 2. 사용자 질문 화면 표시 및 세션 저장
        st.chat_message("user").markdown(question)
        st.session_state.messages.append({"role": "user", "content": question})

        # 3. 모델에 전송할 메시지 배열 조립 (시스템 메시지 + 이전 대화 기록)
        messages_payload = [{"role": "system", "content": system_prompt}] + [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]

        # 4. 스트리밍 응답 생성
        try:
            client = OpenAI(api_key=api_key)

            with st.chat_message("assistant"):
                # stream=True로 스트리밍 호출
                stream = client.chat.completions.create(
                    model=model,
                    messages=messages_payload,
                    stream=True,
                )
                # Streamlit의 st.write_stream을 활용해 글자가 실시간으로 타이핑되듯 렌더링
                response_content = st.write_stream(stream)

            # 5. 완성된 AI 답변을 대화 기록에 저장
            st.session_state.messages.append(
                {"role": "assistant", "content": response_content}
            )

        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")