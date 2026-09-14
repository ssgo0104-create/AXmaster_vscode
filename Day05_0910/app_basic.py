import os
from pathlib import Path
import requests
import streamlit as st
from dotenv import load_dotenv

current_dir = Path(__file__).resolve().parent
load_dotenv(dotenv_path=current_dir / ".env")
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

st.set_page_config(page_title="Global Weather Dashboard", page_icon="🌤️", layout="centered")

# ==============================================================================
# 모바일/태블릿 맞춤 미디어 쿼리 반응형 CSS
# ==============================================================================
st.markdown("""
<style>
    .stApp {
        background-color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .main-header {
        font-size: clamp(1.6rem, 5vw, 2.1rem);
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: clamp(0.85rem, 2.5vw, 0.95rem);
        color: #64748b;
        margin-bottom: 1.5rem;
    }

    /* 날씨 메인 카드 반응형 */
    .weather-main-card {
        border-radius: 20px;
        padding: clamp(18px, 4vw, 26px);
        box-shadow: 0 10px 25px -5px rgba(0,0,0,0.12);
        margin-top: 6px;
        margin-bottom: 12px;
        border: 1px solid rgba(0,0,0,0.04);
    }
    .weather-temp {
        font-size: clamp(2.4rem, 8vw, 3.4rem);
        font-weight: 800;
        line-height: 1.05;
        margin: 4px 0;
    }
    .weather-city {
        font-size: clamp(1.05rem, 3.5vw, 1.25rem);
        font-weight: 700;
    }
    .weather-desc {
        font-size: clamp(0.85rem, 2.8vw, 0.95rem);
        font-weight: 600;
    }

    /* 옷차림 카드 반응형 */
    .outfit-card {
        background: white;
        border-radius: 16px;
        padding: clamp(14px, 3.5vw, 18px);
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
        margin-top: 14px;
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .outfit-icon {
        font-size: clamp(1.6rem, 5vw, 2rem);
        background: #f8fafc;
        padding: 8px 12px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        flex-shrink: 0;
    }
    .outfit-desc {
        font-size: clamp(0.9rem, 3vw, 1.05rem);
        font-weight: 600;
        color: #1e293b;
    }

    /* 현지 표현 카드 반응형 그리드 */
    .phrases-unified-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        padding: clamp(16px, 4vw, 24px);
        box-shadow: 0 6px 16px -3px rgba(15, 23, 42, 0.05);
        margin-top: 14px;
    }
    .phrases-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
    }
    .phrase-item {
        background: #f8fafc;
        border: 1px solid #edf2f7;
        border-radius: 12px;
        padding: 12px 14px;
        display: flex;
        flex-direction: column;
        gap: 3px;
    }

    /* [반응형 핵심] 가로 640px 이하 모바일 화면일 때 레이아웃 변경 */
    @media (max-width: 640px) {
        .phrases-grid {
            grid-template-columns: 1fr; /* 3줄 가로배열 -> 1열 세로배열로 자동 전환 */
            gap: 10px;
        }
        .weather-content-row {
            flex-direction: column-reverse; /* 모바일에서 아이콘이 텍스트 위나 정돈되게 */
            align-items: flex-start !important;
            gap: 10px;
        }
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🌤️ Global Weather Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">실시간 여행지 기상 상태, 추천 옷차림, 현지 필수 회화 표현을 제공합니다.</div>', unsafe_allow_html=True)

if not WEATHER_API_KEY:
    st.error(".env 파일에서 OPENWEATHER_API_KEY를 확인하세요.")
    st.stop()

CITY_DB = {
    "🇰🇷 서울 (Seoul)": {
        "query": "Seoul",
        "phrases": [
            ("안녕하세요", "Annyeonghaseyo", "기본 인사"),
            ("감사합니다", "Gamsahamnida", "감사 표현"),
            ("얼마예요?", "Eolmayeyo?", "가격 문의")
        ]
    },
    "🇯🇵 도쿄 (Tokyo)": {
        "query": "Tokyo",
        "phrases": [
            ("こんにちは", "곤니치와", "안녕하세요"),
            ("ありがとうございます", "아리가토고자이마스", "감사합니다"),
            ("これ、いくらですか？", "고레 이쿠라데스카?", "이거 얼마예요?")
        ]
    },
    "🇯🇵 오사카 (Osaka)": {
        "query": "Osaka",
        "phrases": [
            ("こんにちは", "곤니치와", "안녕하세요"),
            ("ありがとうございます", "아리가토고자이마스", "감사합니다"),
            ("これ、なんぼ？", "고레 난보?", "이거 얼마예요? (방언)")
        ]
    },
    "🇻🇳 다낭 (Da Nang)": {
        "query": "Da Nang",
        "phrases": [
            ("Xin chào", "씬 짜오", "안녕하세요"),
            ("Cảm ơn", "깜 온", "감사합니다"),
            ("Bao nhiêu tiền?", "바오 니에우 띠엔?", "얼마예요?")
        ]
    },
    "🇹🇭 방콕 (Bangkok)": {
        "query": "Bangkok",
        "phrases": [
            ("สวัสดี", "싸왓디-캅/카", "안녕하세요"),
            ("ขอบคุณ", "컵쿤-캅/카", "감사합니다"),
            ("อันนี้เท่าไหร่", "안니 타오라이?", "이거 얼마예요?")
        ]
    },
    "🇨🇳 상하이 (Shanghai)": {
        "query": "Shanghai",
        "phrases": [
            ("你好", "니하오", "안녕하세요"),
            ("谢谢", "씨에씨에", "감사합니다"),
            ("多少钱？", "뚜오샤오 치엔?", "얼마예요?")
        ]
    },
    "🇬🇧 런던 (London)": {
        "query": "London",
        "phrases": [
            ("Hello / Cheers", "헬로우 / 치어스", "인사 / 고마워요"),
            ("Thank you", "땡큐", "감사합니다"),
            ("How much is this?", "하우 머치 이즈 디스?", "얼마예요?")
        ]
    },
    "🇫🇷 파리 (Paris)": {
        "query": "Paris",
        "phrases": [
            ("Bonjour", "봉주르", "안녕하세요"),
            ("Merci", "메르시", "감사합니다"),
            ("C'est combien ?", "쎄 꽁비앙?", "얼마예요?")
        ]
    },
    "🇺🇸 뉴욕 (New York)": {
        "query": "New York",
        "phrases": [
            ("Hi, How's it going?", "하이, 하우짓 고잉?", "안녕하세요, 어때요?"),
            ("Thanks a lot", "땡스 어 랏", "정말 감사합니다"),
            ("Check, please", "체크 플리즈", "계산서 주세요")
        ]
    },
    "🇦🇺 시드니 (Sydney)": {
        "query": "Sydney",
        "phrases": [
            ("G'day, mate!", "그다이, 마이트!", "안녕하세요, 친구!"),
            ("No worries", "노 워리스", "천만에요 / 괜찮아요"),
            ("Can I get the bill?", "캔 아이 겟 더 빌?", "계산서 주세요")
        ]
    }
}

DEFAULT_PHRASES = [
    ("Hello", "헬로우", "안녕하세요"),
    ("Thank you", "땡큐", "감사합니다"),
    ("Excuse me", "익스큐즈 미", "실례합니다 / 저기요")
]

def get_weather_theme(weather_main, icon_code):
    weather_main = weather_main.lower()
    is_night = icon_code.endswith('n')
    if "clear" in weather_main:
        if is_night:
            return {"bg": "linear-gradient(135deg, #1e1b4b 0%, #312e81 100%)", "emoji": "🌙", "title": "#e0e7ff", "temp": "#ffffff", "desc": "#c7d2fe", "chip_bg": "rgba(255, 255, 255, 0.15)", "chip_tx": "#ffffff"}
        return {"bg": "linear-gradient(135deg, #ffedd5 0%, #fed7aa 100%)", "emoji": "☀️", "title": "#9a3412", "temp": "#7c2d12", "desc": "#c2410c", "chip_bg": "rgba(255, 255, 255, 0.65)", "chip_tx": "#7c2d12"}
    elif "cloud" in weather_main:
        return {"bg": "linear-gradient(135deg, #334155 0%, #1e293b 100%)", "emoji": "☁️", "title": "#cbd5e1", "temp": "#f8fafc", "desc": "#94a3b8", "chip_bg": "rgba(255, 255, 255, 0.12)", "chip_tx": "#f1f5f9"}
    elif any(k in weather_main for k in ["rain", "drizzle"]):
        return {"bg": "linear-gradient(135deg, #1e3a8a 0%, #172554 100%)", "emoji": "🌧️", "title": "#bfdbfe", "temp": "#ffffff", "desc": "#93c5fd", "chip_bg": "rgba(255, 255, 255, 0.15)", "chip_tx": "#ffffff"}
    elif "snow" in weather_main:
        return {"bg": "linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%)", "emoji": "❄️", "title": "#0369a1", "temp": "#0c4a6e", "desc": "#0284c7", "chip_bg": "rgba(255, 255, 255, 0.7)", "chip_tx": "#0c4a6e"}
    else:
        return {"bg": "linear-gradient(135deg, #475569 0%, #334155 100%)", "emoji": "🌫️", "title": "#e2e8f0", "temp": "#ffffff", "desc": "#cbd5e1", "chip_bg": "rgba(255, 255, 255, 0.12)", "chip_tx": "#f8fafc"}

def get_outfit_recommendation(temp, weather_desc):
    rain_or_snow = any(k in weather_desc for k in ["비", "소나기", "눈", "천둥"])
    if temp >= 28:
        outfit, icon = "민소매, 얇은 린넨 셔츠, 반바지, 선글라스", "🕶️"
    elif 23 <= temp < 28:
        outfit, icon = "반팔 티셔츠, 얇은 셔츠, 통풍 면바지", "👕"
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

st.markdown("<div style='font-size: 1rem; font-weight: 800; color: #1e3a8a; margin-bottom: 8px;'>📍 여행지 및 도시 선택</div>", unsafe_allow_html=True)

all_options = list(CITY_DB.keys()) + ["🔍 직접 도시 검색 (한글/영문)"]
col_sel, col_inp = st.columns([1.3, 1.7])

with col_sel:
    selected_option = st.selectbox(
        "도시 목록", 
        all_options, 
        index=0, 
        label_visibility="collapsed", 
        key="city_select_box"
    )

target_query = ""
if selected_option == "🔍 직접 도시 검색 (한글/영문)":
    with col_inp:
        custom_input = st.text_input("도시 입력", placeholder="한글 또는 영문 입력 (예: 부산, 제주, 로마)", label_visibility="collapsed")
        if custom_input.strip():
            target_query = custom_input.strip()
else:
    target_query = CITY_DB[selected_option]["query"]

if target_query:
    weather_data = None
    card_city_title = ""

    try:
        geo_url = "http://api.openweathermap.org/geo/1.0/direct"
        geo_res = requests.get(geo_url, params={"q": target_query, "limit": 1, "appid": WEATHER_API_KEY}, timeout=5).json()
        if geo_res and len(geo_res) > 0:
            target_lat = geo_res[0]["lat"]
            target_lon = geo_res[0]["lon"]
            display_name = geo_res[0].get("local_names", {}).get("ko", geo_res[0]["name"])
            card_city_title = f"{display_name}, {geo_res[0].get('country', '')}"
            
            w_res = requests.get("https://api.openweathermap.org/data/2.5/weather", 
                                 params={"lat": target_lat, "lon": target_lon, "appid": WEATHER_API_KEY, "units": "metric", "lang": "kr"}, timeout=10)
            if w_res.status_code == 200:
                weather_data = w_res.json()
    except Exception:
        pass

    if not weather_data:
        try:
            fallback = requests.get("https://api.openweathermap.org/data/2.5/weather", 
                                    params={"q": target_query, "appid": WEATHER_API_KEY, "units": "metric", "lang": "kr"}, timeout=10)
            if fallback.status_code == 200:
                weather_data = fallback.json()
                card_city_title = f"{weather_data['name']}, {weather_data['sys']['country']}"
        except Exception:
            pass

    if weather_data:
        temp = round(weather_data["main"]["temp"], 1)
        feels_like = round(weather_data["main"]["feels_like"], 1)
        desc = weather_data["weather"][0]["description"]
        main_state = weather_data["weather"][0]["main"]
        humidity = weather_data["main"]["humidity"]
        wind = weather_data["wind"]["speed"]
        icon_code = weather_data["weather"][0]["icon"]

        theme = get_weather_theme(main_state, icon_code)
        outfit_icon, outfit_text = get_outfit_recommendation(temp, desc)

        # 1) 반응형 날씨 카드
        st.markdown(f"""
        <div class="weather-main-card" style="background: {theme['bg']};">
            <div class="weather-content-row" style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div class="weather-city" style="color: {theme['title']};">
                        {theme['emoji']} {card_city_title}
                    </div>
                    <div class="weather-temp" style="color: {theme['temp']};">
                        {temp}°C
                    </div>
                    <div class="weather-desc" style="color: {theme['desc']};">
                        {desc} · 체감 {feels_like}°C
                    </div>
                </div>
                <div>
                    <img src="https://openweathermap.org/img/wn/{icon_code}@4x.png" width="100" style="filter: drop-shadow(0 4px 8px rgba(0,0,0,0.18));">
                </div>
            </div>
            <div style="display: flex; gap: 8px; margin-top: 14px; flex-wrap: wrap;">
                <div style="background: {theme['chip_bg']}; color: {theme['chip_tx']}; border-radius: 10px; padding: 6px 12px; font-size: 0.85rem; font-weight: 700;">💧 습도 {humidity}%</div>
                <div style="background: {theme['chip_bg']}; color: {theme['chip_tx']}; border-radius: 10px; padding: 6px 12px; font-size: 0.85rem; font-weight: 700;">💨 풍속 {wind} m/s</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2) 반응형 옷차림 카드
        st.markdown(f"""
        <div class="outfit-card">
            <div class="outfit-icon">{outfit_icon}</div>
            <div>
                <div style="font-size: 0.8rem; font-weight: 700; color: #64748b; text-transform: uppercase;">Today's Recommended Outfit</div>
                <div class="outfit-desc">{outfit_text}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 3) 반응형 필수 표현 카드 (모바일에서는 세로 1열로 자동 변환)
        phrases = CITY_DB[selected_option]["phrases"] if selected_option in CITY_DB else DEFAULT_PHRASES

        st.markdown(f"""
        <div class="phrases-unified-card">
            <div style="font-size: 0.95rem; font-weight: 800; color: #1e293b; margin-bottom: 14px;">💬 현지 여행 필수 표현 (TOP 3)</div>
            <div class="phrases-grid">
                <div class="phrase-item">
                    <div style="font-size: 1.05rem; font-weight: 800; color: #1e40af;">{phrases[0][0]}</div>
                    <div style="font-size: 0.8rem; color: #64748b; font-weight: 600;">[{phrases[0][1]}]</div>
                    <div style="font-size: 0.88rem; color: #0f172a; font-weight: 700; margin-top: 2px;">{phrases[0][2]}</div>
                </div>
                <div class="phrase-item">
                    <div style="font-size: 1.05rem; font-weight: 800; color: #1e40af;">{phrases[1][0]}</div>
                    <div style="font-size: 0.8rem; color: #64748b; font-weight: 600;">[{phrases[1][1]}]</div>
                    <div style="font-size: 0.88rem; color: #0f172a; font-weight: 700; margin-top: 2px;">{phrases[1][2]}</div>
                </div>
                <div class="phrase-item">
                    <div style="font-size: 1.05rem; font-weight: 800; color: #1e40af;">{phrases[2][0]}</div>
                    <div style="font-size: 0.8rem; color: #64748b; font-weight: 600;">[{phrases[2][1]}]</div>
                    <div style="font-size: 0.88rem; color: #0f172a; font-weight: 700; margin-top: 2px;">{phrases[2][2]}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.info("도시를 선택하거나 입력해 주세요.")