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
# 2. 기본 세팅 및 레이아웃 CSS
# ==============================================================================
st.set_page_config(page_title="Global Weather & Forex", page_icon="✈️", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    .main-header {
        font-size: 2.1rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 0.95rem;
        color: #64748b;
        margin-bottom: 1.5rem;
    }

    /* 위치 선택 영역 강조 */
    .selector-title {
        font-size: 1rem;
        font-weight: 800;
        color: #1e3a8a;
        margin-bottom: 8px;
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
        font-size: 1.05rem;
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
        font-size: 0.82rem;
        font-weight: 700;
        color: #64748b;
    }
    .fx-rate {
        font-size: 1.5rem;
        font-weight: 800;
        color: #0f172a;
        margin-top: 4px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">✈️ Global Travel Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">실시간 기상 상태에 따른 컬러 테마와 옷차림 추천, 실시간 통화 환율을 제공합니다.</div>', unsafe_allow_html=True)

if not WEATHER_API_KEY or not EXCHANGE_API_KEY:
    st.error(".env 파일에서 API 키 설정을 확인하세요.")
    st.stop()

# ==============================================================================
# 3. 날씨별 동적 테마 (맑음: 밝은 화사한 톤 / 흐림: 어두운 톤)
# ==============================================================================
def get_weather_theme(weather_main, icon_code):
    weather_main = weather_main.lower()
    is_night = icon_code.endswith('n')
    
    # 1) 맑은 날: 밝고 화사한 웜 옐로우/오렌지 베이지톤 (낮) / 밤은 세련된 딥 네이비
    if "clear" in weather_main:
        if is_night:
            # 밤 맑음: 어두운 인디고
            return {
                "bg": "linear-gradient(135deg, #1e1b4b 0%, #312e81 100%)",
                "emoji": "🌙",
                "title_color": "#e0e7ff",
                "temp_color": "#ffffff",
                "desc_color": "#c7d2fe",
                "chip_bg": "rgba(255, 255, 255, 0.15)",
                "chip_text": "#ffffff"
            }
        else:
            # 낮 맑음: 화사하고 밝은 샴페인 선셋톤
            return {
                "bg": "linear-gradient(135deg, #ffedd5 0%, #fed7aa 100%)",
                "emoji": "☀️",
                "title_color": "#9a3412",
                "temp_color": "#7c2d12",
                "desc_color": "#c2410c",
                "chip_bg": "rgba(255, 255, 255, 0.65)",
                "chip_text": "#7c2d12"
            }

    # 2) 흐림/구름: 확실하게 어둡고 차분한 다크 슬레이트 톤
    elif "cloud" in weather_main:
        return {
            "bg": "linear-gradient(135deg, #334155 0%, #1e293b 100%)",
            "emoji": "☁️",
            "title_color": "#cbd5e1",
            "temp_color": "#f8fafc",
            "desc_color": "#94a3b8",
            "chip_bg": "rgba(255, 255, 255, 0.12)",
            "chip_text": "#f1f5f9"
        }

    # 3) 비/소나기: 톤다운된 차분한 딥 블루
    elif any(k in weather_main for k in ["rain", "drizzle"]):
        return {
            "bg": "linear-gradient(135deg, #1e3a8a 0%, #172554 100%)",
            "emoji": "🌧️",
            "title_color": "#bfdbfe",
            "temp_color": "#ffffff",
            "desc_color": "#93c5fd",
            "chip_bg": "rgba(255, 255, 255, 0.15)",
            "chip_text": "#ffffff"
        }

    # 4) 눈: 맑고 뽀얀 화이트-스카이블루 밝은 톤
    elif "snow" in weather_main:
        return {
            "bg": "linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%)",
            "emoji": "❄️",
            "title_color": "#0369a1",
            "temp_color": "#0c4a6e",
            "desc_color": "#0284c7",
            "chip_bg": "rgba(255, 255, 255, 0.7)",
            "chip_text": "#0c4a6e"
        }

    # 5) 천둥번개 / 기타 안개
    elif "thunderstorm" in weather_main:
        return {
            "bg": "linear-gradient(135deg, #312e81 0%, #0f172a 100%)",
            "emoji": "⚡",
            "title_color": "#e0e7ff",
            "temp_color": "#ffffff",
            "desc_color": "#c7d2fe",
            "chip_bg": "rgba(255, 255, 255, 0.15)",
            "chip_text": "#ffffff"
        }
    else:
        # 안개 등
        return {
            "bg": "linear-gradient(135deg, #475569 0%, #334155 100%)",
            "emoji": "🌫️",
            "title_color": "#e2e8f0",
            "temp_color": "#ffffff",
            "desc_color": "#cbd5e1",
            "chip_bg": "rgba(255, 255, 255, 0.12)",
            "chip_text": "#f8fafc"
        }

def get_outfit_recommendation(temp, weather_desc):
    rain_or_snow = any(k in weather_desc for k in ["비", "소나기", "눈", "천둥"])
    
    if temp >= 28:
        outfit, icon = "민소매, 얇은 린넨 셔츠, 반바지, 자외선 차단 선글라스", "🕶️"
    elif 23 <= temp < 28:
        outfit, icon = "반팔 티셔츠, 얇은 셔츠, 슬랙스 또는 통풍 면바지", "👕"
    elif 20 <= temp < 23:
        outfit, icon = "긴팔 티셔츠, 가벼운 가디건, 셔츠, 청바지", "👔"
    elif 17 <= temp < 20:
        outfit, icon = "니트, 얇은 맨투맨, 가디건, 바람막이, 슬랙스", "🧶"
    elif 12 <= temp < 17:
        outfit, icon = "자켓, 야상, 셔츠 레이어드, 도톰한 맨투맨", "🧥"
    elif 9 <= temp < 12:
        outfit, icon = "트렌치코트, 도톰한 점퍼, 기모 바지", "🧣"
    elif 5 <= temp < 9:
        outfit, icon = "울 코트, 히트텍, 도톰한 니트, 가죽 자켓, 머플러", "🧤"
    else:
        outfit, icon = "패딩, 두꺼운 울 코트, 기모 의류, 목도리, 장갑 필수", "❄️"
        
    if rain_or_snow:
        outfit += " (⚠️ 우산 필수 지참)"
        
    return icon, outfit

# ==============================================================================
# 4. 상단 도시 선택 드롭다운 + 검색창
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
# 5. 동적 컬러 날씨 카드 & 옷차림
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

            # 날씨 상태별 색상 및 이모지 가져오기
            theme = get_weather_theme(main_state, icon_code)
            outfit_icon, recommended_outfit = get_outfit_recommendation(temp, desc)

            # 날씨 카드 (밝은 날은 밝게, 흐린 날은 어둡게 자동 렌더링)
            st.markdown(f"""
            <div style="background: {theme['bg']}; border-radius: 20px; padding: 24px 28px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.12); margin-top: 10px; margin-bottom: 18px; border: 1px solid rgba(0,0,0,0.04);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 1.25rem; font-weight: 700; color: {theme['title_color']};">
                            {theme['emoji']} {city_name}, {country}
                        </div>
                        <div style="font-size: 3.4rem; font-weight: 800; line-height: 1.05; margin: 4px 0; color: {theme['temp_color']};">
                            {temp}°C
                        </div>
                        <div style="font-size: 1rem; font-weight: 600; color: {theme['desc_color']};">
                            {desc} · 체감 {feels_like}°C
                        </div>
                    </div>
                    <div>
                        <img src="https://openweathermap.org/img/wn/{icon_code}@4x.png" width="115" style="filter: drop-shadow(0 4px 10px rgba(0,0,0,0.18));">
                    </div>
                </div>
                <div style="display: flex; gap: 10px; margin-top: 16px;">
                    <div style="background: {theme['chip_bg']}; color: {theme['chip_text']}; border-radius: 10px; padding: 6px 14px; font-size: 0.85rem; font-weight: 700;">💧 습도 {humidity}%</div>
                    <div style="background: {theme['chip_bg']}; color: {theme['chip_text']}; border-radius: 10px; padding: 6px 14px; font-size: 0.85rem; font-weight: 700;">💨 풍속 {wind} m/s</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # 옷차림 카드
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