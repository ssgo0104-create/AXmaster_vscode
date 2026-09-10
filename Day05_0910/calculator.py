import os
from pathlib import Path
import requests
import streamlit as st
from dotenv import load_dotenv

current_dir = Path(__file__).resolve().parent
load_dotenv(dotenv_path=current_dir / ".env")
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")

st.set_page_config(page_title="Global Forex Dashboard", page_icon="💱", layout="wide")

# 세션 상태 기본값 초기화
if "in_val_1" not in st.session_state:
    st.session_state.in_val_1 = 100.0
if "in_val_2" not in st.session_state:
    st.session_state.in_val_2 = 1000000.0

st.markdown("""
<style>
    .stApp {
        background-color: #f1f5f9;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1050px;
    }

    /* 상단 요약 미니 카드 */
    .rate-summary-badge {
        background: #ffffff;
        border-radius: 12px;
        padding: 16px 20px;
        border: 1px solid #cbd5e1;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
    }
    .rate-country {
        font-size: 0.8rem;
        font-weight: 700;
        color: #64748b;
        letter-spacing: -0.02em;
    }
    .rate-price {
        font-size: 1.55rem;
        font-weight: 800;
        color: #0f172a;
        margin-top: 4px;
    }

    /* 시인성 극대화 결과 디스플레이 박스 */
    .result-hero-box {
        background: #ffffff;
        border: 2px solid #2563eb;
        border-radius: 14px;
        padding: 22px 24px;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.08);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .result-hero-label {
        font-size: 0.88rem;
        font-weight: 700;
        color: #2563eb;
    }
    .result-hero-value {
        font-size: 2.2rem;
        font-weight: 900;
        color: #0f172a;
        letter-spacing: -0.03em;
        margin: 6px 0;
    }
    .result-hero-sub {
        font-size: 0.82rem;
        color: #64748b;
        font-weight: 500;
    }

    /* 상단 가로형 프리셋 선택 바 */
    .preset-header {
        font-size: 0.85rem;
        color: #334155;
        font-weight: 700;
        margin-top: 14px;
        margin-bottom: 6px;
    }

    /* 프리셋 버튼 디자인 */
    div.row-widget.stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        color: #1e293b !important;
        padding: 6px 0 !important;
    }
    div.row-widget.stButton > button:hover {
        border-color: #2563eb !important;
        color: #2563eb !important;
        background-color: #eff6ff !important;
    }

    button[data-baseweb="tab"] {
        font-size: 1rem !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("💱 Global Forex Dashboard")
st.caption("주요 4대 통화 실시간 환율 및 맞춤 양방향 계산기")

if not EXCHANGE_API_KEY:
    st.error(".env 파일에 EXCHANGE_API_KEY가 설정되어 있지 않습니다.")
    st.stop()

try:
    ex_url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/USD"
    ex_res = requests.get(ex_url, timeout=10).json()

    if ex_res.get("result") == "success":
        rates = ex_res["conversion_rates"]
        krw_rate = rates.get("KRW", 1350.0)
        jpy_rate = rates.get("JPY", 150.0)
        eur_rate = rates.get("EUR", 0.92)
        cny_rate = rates.get("CNY", 7.2)

        update_time = ex_res.get("time_last_update_utc", "")[:16]

        st.markdown(f"**🕒 기준 환율 정보** &nbsp;`{update_time} UTC` &nbsp;·&nbsp; 기준통화: **1 USD**")

        # 상단 실시간 환율 카드
        col1, col2, col3, col4 = st.columns(4)
        cards = [
            (col1, "🇰🇷 대한민국 KRW", f"₩ {krw_rate:,.1f}"),
            (col2, "🇯🇵 일본 JPY", f"¥ {jpy_rate:,.1f}"),
            (col3, "🇪🇺 유로존 EUR", f"€ {eur_rate:,.2f}"),
            (col4, "🇨🇳 중국 CNY", f"¥ {cny_rate:,.2f}"),
        ]
        for col, title, val in cards:
            with col:
                st.markdown(f"""
                <div class="rate-summary-badge">
                    <div class="rate-country">{title}</div>
                    <div class="rate-price">{val}</div>
                </div>
                """, unsafe_allow_html=True)

        st.write("")
        st.write("")

        st.subheader("🖩 환율 계산기")

        currency_map = {
            "USD (미국 달러)": (krw_rate, "$", "USD", 1),
            "JPY (일본 100엔)": ((krw_rate / jpy_rate) * 100, "¥", "JPY", 100),
            "EUR (유럽 유로)": (krw_rate / eur_rate, "€", "EUR", 1),
            "CNY (중국 위안)": (krw_rate / cny_rate, "元", "CNY", 1),
        }

        preset_by_currency = {
            "USD": [50, 100, 500, 1000],
            "JPY": [1000, 5000, 10000, 50000],
            "EUR": [50, 100, 300, 500],
            "CNY": [100, 500, 1000, 5000],
        }

        tab1, tab2 = st.tabs(["➡️  외화 ➔ 원화(KRW) 계산", "⬅️  원화(KRW) ➔ 외화 계산"])

        # 탭 1: 외화 -> 원화
        with tab1:
            # 1. 최상단 빠른 금액 선택 영역
            def set_preset_val_1(amount):
                st.session_state.in_val_1 = float(amount)

            curr_1 = st.session_state.get("sel_curr_1", "USD (미국 달러)")
            curr_code_1 = curr_1.split()[0]
            curr_presets_1 = preset_by_currency.get(curr_code_1, [50, 100, 500, 1000])

            st.markdown('<div class="preset-header">⚡ 빠른 금액 선택</div>', unsafe_allow_html=True)
            p_cols1 = st.columns(4)
            for idx, p_val in enumerate(curr_presets_1):
                with p_cols1[idx]:
                    btn_label = f"{curr_code_1} {p_val:,}"
                    st.button(btn_label, key=f"btn_p1_{curr_code_1}_{idx}", on_click=set_preset_val_1, args=(p_val,), use_container_width=True)

            st.write("")

            # 2. 본문 입력 및 계산 결과 영역
            c_input, c_rate, c_result = st.columns([1.2, 1.2, 1.4], gap="medium")

            with c_input:
                curr_choice_1 = st.selectbox("외화 통화", list(currency_map.keys()), key="sel_curr_1")
                base_1, sym_1, code_1, scale_1 = currency_map[curr_choice_1]
                val_1 = st.number_input(f"외화 금액 ({code_1})", min_value=0.0, step=10.0, key="in_val_1")

            with c_rate:
                custom_1 = st.checkbox("환율 직접 지정", key="chk_custom_1")
                lbl_1 = f"적용 환율 ({'100엔' if code_1 == 'JPY' else '1 ' + code_1}당 KRW)"
                if custom_1:
                    applied_1 = st.number_input(lbl_1, value=float(round(base_1, 2)), step=1.0, key="rate_inp_1")
                else:
                    applied_1 = base_1
                    st.text_input(lbl_1, value=f"{applied_1:,.2f} 원", disabled=True, key="dis_rate_1")

            with c_result:
                if applied_1 > 0:
                    final_krw = (val_1 / scale_1) * applied_1
                    st.markdown(f"""
                    <div class="result-hero-box">
                        <div class="result-hero-label">최종 환산 원화(KRW)</div>
                        <div class="result-hero-value">₩ {final_krw:,.0f}</div>
                        <div class="result-hero-sub">계산식: {sym_1}{val_1:,.2f} × {applied_1:,.2f}원</div>
                    </div>
                    """, unsafe_allow_html=True)

        # 탭 2: 원화 -> 외화
        with tab2:
            # 1. 최상단 빠른 금액 선택 영역
            def set_preset_val_2(amount):
                st.session_state.in_val_2 = float(amount)

            krw_presets = [
                (50000, "KRW 50,000 (5만)"),
                (100000, "KRW 100,000 (10만)"),
                (500000, "KRW 500,000 (50만)"),
                (1000000, "KRW 1,000,000 (100만)"),
            ]

            st.markdown('<div class="preset-header">⚡ 빠른 금액 선택</div>', unsafe_allow_html=True)
            p_cols2 = st.columns(4)
            for idx, (p_val, p_text) in enumerate(krw_presets):
                with p_cols2[idx]:
                    st.button(p_text, key=f"btn_p2_{idx}", on_click=set_preset_val_2, args=(p_val,), use_container_width=True)

            st.write("")

            # 2. 본문 입력 및 계산 결과 영역
            c_input, c_rate, c_result = st.columns([1.2, 1.2, 1.4], gap="medium")

            with c_input:
                curr_choice_2 = st.selectbox("외화 통화", list(currency_map.keys()), key="sel_curr_2")
                base_2, sym_2, code_2, scale_2 = currency_map[curr_choice_2]
                val_2 = st.number_input("원화 금액 (KRW)", min_value=0.0, step=10000.0, key="in_val_2")

            with c_rate:
                custom_2 = st.checkbox("환율 직접 지정", key="chk_custom_2")
                lbl_2 = f"적용 환율 ({'100엔' if code_2 == 'JPY' else '1 ' + code_2}당 KRW)"
                if custom_2:
                    applied_2 = st.number_input(lbl_2, value=float(round(base_2, 2)), step=1.0, key="rate_inp_2")
                else:
                    applied_2 = base_2
                    st.text_input(lbl_2, value=f"{applied_2:,.2f} 원", disabled=True, key="dis_rate_2")

            with c_result:
                if applied_2 > 0:
                    final_foreign = (val_2 / applied_2) * scale_2
                    st.markdown(f"""
                    <div class="result-hero-box">
                        <div class="result-hero-label">최종 환산 {code_2}</div>
                        <div class="result-hero-value">{sym_2} {final_foreign:,.2f}</div>
                        <div class="result-hero-sub">계산식: ₩{val_2:,.0f} ÷ {applied_2:,.2f}원</div>
                    </div>
                    """, unsafe_allow_html=True)

    else:
        st.error("환율 API 데이터를 받아오지 못했습니다.")
except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")