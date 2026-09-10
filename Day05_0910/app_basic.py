import os
from pathlib import Path
import requests
import streamlit as st
from dotenv import load_dotenv

# ==============================================================================
# 1. API 키 로드
# ==============================================================================
current_dir = Path(__file__).resolve().parent
env_path = current_dir / ".env"
load_dotenv(dotenv_path=env_path)

WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")

# ==============================================================================
# 2. 스타일링 (선택창 강조 및 기본 UI)
# ==============================================================================
st.set_page_config(page_title="Global Weather & Forex", page_icon="✈️", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    .main-header {
        font-size: 2rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 0.95rem;
        color: #64748b;
        margin-bottom: 1.5rem;
    }

    /* 위치 선택 영역 강조 컨테이너 */
    .location-selector-box {
        background: #ffffff;
        border: 2px solid #3b82f6;
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 6px 15px -3px rgba(59, 130, 246, 0.15);
        margin-bottom: 24px;
    }
    .selector-title {
        font-size: 0.95rem;
        font-weight: 800;
        color: #1e40af;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* 추천 옷차림 카드 */
    .outfit-card {
        background: white;
        border-radius: 16px;
        padding: 16px 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .outfit-icon {
        font-size: 2rem;
        background: #f8fafc;
        padding: 10px 14px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }
    .outfit-title {
        font-size: 0.8rem;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .outfit-desc {
        font-size: 1rem;
        font-weight: 600;
        color: #1e293b;
        margin-top: 2px;
    }

    /* 환율 카드 */
    .fx-card {
        background: white;
        border-radius: 14px;
        padding: 16px 18px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 3px 5px -1px rgba(0, 0, 0, 0.03);
    }
    .fx-currency {
        font-size: 0.8rem;
        font-weight: 700;
        color: #64748b;
    }
    .fx-rate {
        font-size: 1.45rem;
        font-weight: 800;
        color: #0f172a;
        margin-top: 4px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">✈️ Global Travel Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">실시간 도시 기상 맞춤 테마와 옷차림 정보, 실시간 환율을 제공합니다.</div>', unsafe_allow_html=True)

if not WEATHER_API_KEY or not EXCHANGE_API_KEY:
    st.error(".env 파일에서 API 키 설정을 확인하세요.")
    st.stop()

# ==============================================================================
# 3. 날씨별 동적 테마(배경색 & 이모지) 및 옷차림 로직
# ==============================================================================
def get_weather_theme(weather_main, icon_code):
    weather_main = weather_main.lower()
    is_night = icon_code.endswith('n')
    
    # 맑음
    if "clear" in weather_main:
        if is_night:
            return "linear-gradient(135deg, #1e1b4b 0%, #312e81 100%)", "🌙", "#c7d2fe", "#a5b4fc"
        return "linear-gradient(135deg, #f59e0b 0%, #ea580c 100%)", "☀️", "#fef3c7", "#fed7aa"
    # 구름/흐림
    elif "cloud" in weather_main:
        return "linear-gradient(135deg, #475569 0%, #334155 100%)", "☁️", "#cbd5e1", "#94a3b8"
    # 비
    elif any(k in weather_main for k in ["rain", "drizzle"]):
        return "linear-gradient(135deg, #2563eb 0%, #1e3a8a 100%)", "🌧️", "#bfdbfe", "#93c5fd"
    # 천둥번개
    elif "thunderstorm" in weather_main:
        return "linear-gradient(135deg, #3730a3 0%, #1e1b4b 100%)", "⚡", "#e0e7ff", "#c7d2fe"
    # 눈
    elif "snow" in weather_main:
        return "linear-gradient(135deg, #0284c7 0%, #0369a1 100%)", "❄️", "#e0f2fe", "#bae6fd"
    # 안개/먼지 등
    else:
        return "linear-gradient(135deg, #64748b 0%, #475569 100%)", "🌫️", "#e2e8f0", "#cbd5e1"

def get_outfit_recommendation(temp, weather_desc):
    rain_or_snow = any(k in weather_desc for k in ["비", "소나기", "눈", "천둥"])
    
    if temp >= 28:
        outfit, icon = "민소매, 얇은 린넨 셔츠, 반바지, 선글라스", "🕶️"
    elif 23 <= temp < 28:
        outfit, icon = "반팔 티셔츠, 얇은 셔츠, 슬랙스 또는 면바지", "👕"
    elif 20 <= temp < 23:
        outfit, icon = "긴팔 티셔츠, 가벼운 가디건, 셔츠, 청바지", "👔"
    elif 17 <= temp < 20:
        outfit, icon = "니트, 맨투맨, 가디건, 바람막이, 슬랙스", "🧶"
    elif 12 <= temp < 17:
        outfit, icon = "자켓, 야상, 셔츠 레이어드, 도톰한 맨투맨", "🧥"
    elif 9 <= temp < 12:
        outfit, icon = "트렌치코트, 도톰한 점퍼, 기모 바지", "🧣"
    elif 5 <= temp < 9:
        outfit, icon = "울 코트, 히트텍, 도톰한 니트, 가죽 자켓, 머플러", "🧤"
    else:
        outfit, icon = "패딩, 두꺼운 울 코트, 기모 제품, 목도리, 장갑 필수", "❄️"
        
    if rain_or_snow:
        outfit += " (⚠️ 우산 챙기세요)"
        
    return icon, outfit

# ==============================================================================
# 4. 강조된 위치 선택창 (드롭다운 + 직접 검색)
# ==============================================================================
st.markdown('<div class="selector-title">📍 여행지 및 도시 선택</div>', unsafe_allow_html=True)

city_presets = {
    "🇰🇷 서울 (Seoul)": "Seoul",
    "🇯🇵 도쿄 (Tokyo)": "Tokyo",
    "🇯🇵 오사카 (Osaka)": "Osaka",
    "🇻🇳 다낭 (Da Nang)": "Da Nang",
    "🇹🇭 방콕 (Bangkok)": "Bangkok",
    "🇨🇳 상하이 (Shanghai)": "Shanghai",
    "🇬🇧 런던 (London)": "London",
    "🇫🇷 파리 (Paris)": "Paris",
    "🇺🇸 뉴욕 (New York)": "New York",
    "🔍 직접 도시 검색하기": "custom"
}

select_col, input_col = st.columns([1.3, 1.7])
with select_col:
    selected_option = st.selectbox("도시 목록", list(city_presets.keys()), label_visibility="collapsed")

target_city = city_presets[selected_option]
if selected_option == "🔍 직접 도시 검색하기":
    with input_col:
        custom_input = st.text_input("도시 이름 입력", placeholder="영문 도시명을 입력하세요 (예: Sydney, Roma, Madrid)", label_visibility="collapsed")
        target_city = custom_input.strip()

# ==============================================================================
# 5. 동적 날씨 카드 렌더링
# ==============================================================================
if target_city:
    weather_url = "https://api.openweathermap.org/data/2.5/weather"
    weather_params = {
        "q": target_city,
        "appid": WEATHER_API_KEY,
        "units": "metric",
        "lang": "kr"
    }

    try:
        res = requests.get(weather_url, params=weather_params, timeout=10)
        w_data = res.json()

        if res.status_code == 200:
            temp = round(w_data["main"]["temp"], 1)
            feels_like = round(w_data["main"]["feels_like"], 1)
            desc = w_data["weather"][0]["description"]
            main_state = w_data["weather"][0]["main"]
            humidity = w_data["main"]["humidity"]
            wind = w_data["wind"]["speed"]
            city_name = w_data["name"]
            country = w_data["sys"]["country"]
            icon_code = w_data["weather"][0]["icon"]

            # 날씨 상태 기반 테마(배경 그라디언트, 이모지, 폰트 색) 가져오기
            card_bg, weather_emoji, text_sub_color, chip_color = get_weather_theme(main_state, icon_code)
            outfit_icon, recommended_outfit = get_outfit_recommendation(temp, desc)

            # 동적 색상과 이모지가 적용된 메인 날씨 카드
            st.markdown(f"""
            <div style="background: {card_bg}; border-radius: 20px; padding: 24px 28px; color: white; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.18); margin-top: 10px; margin-bottom: 18px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 1.25rem; font-weight: 700; color: {text_sub_color};">
                            {weather_emoji} {city_name}, {country}
                        </div>
                        <div style="font-size: 3.4rem; font-weight: 800; line-height: 1.05; margin: 4px 0;">
                            {temp}°C
                        </div>
                        <div style="font-size: 1rem; color: {text_sub_color};">
                            {desc} · 체감 {feels_like}°C
                        </div>
                    </div>
                    <div>
                        <img src="https://openweathermap.org/img/wn/{icon_code}@4x.png" width="115" style="filter: drop-shadow(0 4px 10px rgba(0,0,0,0.25));">
                    </div>
                </div>
                <div style="display: flex; gap: 10px; margin-top: 16px;">
                    <div style="background: rgba(255, 255, 255, 0.18); border-radius: 10px; padding: 6px 14px; font-size: 0.85rem; font-weight: 600;">💧 습도 {humidity}%</div>
                    <div style="background: rgba(255, 255, 255, 0.18); border-radius: 10px; padding: 6px 14px; font-size: 0.85rem; font-weight: 600;">💨 풍속 {wind} m/s</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # 날씨 맞춤 옷차림 카드
            st.markdown(f"""
            <div class="outfit-card">
                <div class="outfit-icon">{outfit_icon}</div>
                <div>
                    <div class="outfit-title">Today's Recommended Outfit</div>
                    <div class="outfit-desc">{recommended_outfit}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        elif res.status_code == 404:
            st.warning("일치하는 도시를 찾을 수 없습니다. 철자를 확인해 주세요.")
    except Exception as e:
        st.error(f"날씨 데이터를 불러오지 못했습니다: {e}")

# ==============================================================================
# 6. 실시간 환율 그리드
# ==============================================================================
st.markdown("<h4 style='color: #1e293b; margin: 25px 0 12px 0; font-size: 1.1rem; font-weight: 700;'>💵 실시간 기준 환율 (Base: $1 USD)</h4>", unsafe_allow_html=True)

try:
    ex_url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/USD"
    ex_res = requests.get(ex_url, timeout=10)
    ex_data = ex_res.json()

    if ex_res.status_code == 200 and ex_data.get("result") == "success":
        rates = ex_data["conversion_rates"]
        
        krw = rates.get("KRW", 0)
        jpy = rates.get("JPY", 0)
        eur = rates.get("EUR", 0)
        cny = rates.get("CNY", 0)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f'<div class="fx-card"><div class="fx-currency">🇰🇷 KRW</div><div class="fx-rate">₩ {krw:,.1f}</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="fx-card"><div class="fx-currency">🇯🇵 JPY</div><div class="fx-rate">¥ {jpy:,.1f}</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="fx-card"><div class="fx-currency">🇪🇺 EUR</div><div class="fx-rate">€ {eur:,.2f}</div></div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div class="fx-card"><div class="fx-currency">🇨🇳 CNY</div><div class="fx-rate">¥ {cny:,.2f}</div></div>', unsafe_allow_html=True)

        st.caption(f"<div style='text-align: right; margin-top: 8px; color: #94a3b8; font-size: 0.8rem;'>기준 시각: {ex_data.get('time_last_update_utc', '')[:16]} UTC</div>", unsafe_allow_html=True)
    else:
        st.error("환율 정보를 불러오지 못했습니다.")
except Exception as e:
    st.error(f"환율 통신 오류: {e}")