import os
import random
import requests
import streamlit as st
import folium
from streamlit_folium import st_folium
from dotenv import load_dotenv

# -------------------------------------------------------------
# 1. 페이지 설정
# -------------------------------------------------------------
st.set_page_config(
    page_title="여행 준비 도우미🍀",
    page_icon="🍀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# 2. 소프트 연초록 & 네잎클로버 미니멀 스타일링
# -------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

    *:not([class*="material-icons"]):not([class*="MaterialSymbols"]):not([data-testid*="Icon"]) {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        letter-spacing: -0.02em;
        box-sizing: border-box;
    }

    .stApp {
        background-color: #F1F7F3;
        color: #1F2937;
    }

    [data-testid="stSidebar"] {
        background-color: #E6EFEA !important;
        border-right: 1px solid #D1E0D7 !important;
    }

    /* 상단 배너 */
    .clover-banner {
        background: linear-gradient(135deg, #FFFFFF 0%, #F5FAF7 100%);
        border: 1px solid #D5E5DB;
        border-radius: 20px;
        padding: 1.4rem 2rem;
        margin-bottom: 1.4rem;
        box-shadow: 0 4px 18px rgba(34, 112, 68, 0.05);
    }
    .clover-badge {
        background: #E8F5EE;
        color: #2D6A4F;
        border: 1px solid #B7DFCA;
        font-size: 11px;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 9999px;
        display: inline-block;
        margin-bottom: 6px;
    }
    .clover-title {
        font-size: 2rem;
        font-weight: 800;
        color: #1B4332;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .clover-desc {
        color: #52796F;
        font-size: 0.95rem;
        margin-top: 5px;
        font-weight: 500;
    }

    /* 카드 컨테이너 */
    [data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E0ECE4 !important;
        border-radius: 20px !important;
        padding: 1.4rem 1.4rem 1.7rem 1.4rem !important;
        box-shadow: 0 2px 12px rgba(45, 106, 79, 0.035) !important;
        margin-bottom: 1.3rem !important;
    }

    .card-label {
        font-size: 11px;
        font-weight: 800;
        color: #40916C;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 3px;
    }
    .card-title {
        font-size: 1.15rem;
        font-weight: 750;
        color: #1B4332;
        margin-bottom: 1rem;
    }

    /* 날씨 박스 */
    .weather-box {
        background: #F4F9F6;
        border: 1px solid #D5E5DB;
        border-radius: 14px;
        padding: 1.1rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.9rem;
    }
    .weather-temp {
        font-size: 2.3rem;
        font-weight: 800;
        color: #1B4332;
        line-height: 1;
    }

    .weather-stat-grid {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 8px;
        text-align: center;
        margin-bottom: 0.5rem;
    }

    /* 환율 결과 박스 */
    .rate-box {
        background: #F4F9F6;
        border: 1px solid #D5E5DB;
        border-radius: 14px;
        padding: 1.2rem 1rem;
        text-align: center;
        margin-top: 1.1rem;
        margin-bottom: 0.4rem;
    }
    .rate-val {
        font-size: 1.6rem;
        font-weight: 800;
        color: #2D6A4F;
        margin: 4px 0;
    }

    /* 장소 리스트 아이템 */
    .place-item {
        background: #FFFFFF;
        border: 1px solid #E5EBE7;
        border-radius: 12px;
        padding: 11px 14px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.2s ease;
    }
    .place-item:hover {
        border-color: #52B788;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(82, 183, 136, 0.1);
    }
    .place-title {
        font-size: 13.5px;
        font-weight: 700;
        color: #1F2937;
    }
    .place-category {
        font-size: 10.5px;
        font-weight: 700;
        color: #2D6A4F;
        background: #E8F5EE;
        padding: 2px 7px;
        border-radius: 6px;
        margin-left: 6px;
    }
    .place-addr {
        font-size: 11.5px;
        color: #6B7280;
        margin-top: 2px;
    }

    /* 행운 결과 박스 */
    .fortune-inner-box {
        background: linear-gradient(135deg, #F0F8F3 0%, #E3F2E9 100%);
        border: 1px solid #B7DFCA;
        border-radius: 14px;
        padding: 1.1rem 1rem;
        text-align: center;
        margin-top: 14px;
        margin-bottom: 0.4rem;
        animation: fadeIn 0.3s ease-in-out;
    }
    .fortune-title {
        font-size: 15px;
        font-weight: 800;
        color: #1B4332;
    }
    .fortune-desc {
        font-size: 12.5px;
        color: #2D6A4F;
        margin-top: 5px;
        line-height: 1.45;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(4px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* 인풋 & 버튼 */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
        border: 1px solid #D1DFD6 !important;
        border-radius: 12px !important;
        background-color: #FFFFFF !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #52B788 !important;
        box-shadow: 0 0 0 2px rgba(82, 183, 136, 0.2) !important;
    }
    .stButton > button {
        background: #FFFFFF !important;
        color: #2D6A4F !important;
        border: 1px solid #B7DFCA !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background: #E8F5EE !important;
        border-color: #74C69D !important;
        color: #1B4332 !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 3. 환경 변수 로드
# -------------------------------------------------------------
env_path = r"C:\Users\user\AXmaster_vscode\.env"
load_dotenv(dotenv_path=env_path)

kakao_key = (os.getenv("MY_KAKAO_API_KEY") or "").strip().strip('"').strip("'")
exchange_key = (os.getenv("EXCHANGE_API_KEY") or "").strip().strip('"').strip("'")
weather_key = (os.getenv("OPENWEATHER_API_KEY") or "").strip().strip('"').strip("'")

# -------------------------------------------------------------
# 4. 세션 상태 관리
# -------------------------------------------------------------
if "city_input" not in st.session_state:
    st.session_state["city_input"] = "성수"

if "last_synced_city" not in st.session_state:
    st.session_state["last_synced_city"] = ""

if "search_query" not in st.session_state or not st.session_state["search_query"]:
    st.session_state["search_query"] = "성수"

if "fortune_result" not in st.session_state:
    st.session_state["fortune_result"] = None

# 장소 더보기 펼침 상태 (기본 5개 표시)
if "show_all_places" not in st.session_state:
    st.session_state["show_all_places"] = False

def toggle_show_places():
    st.session_state["show_all_places"] = not st.session_state["show_all_places"]

def set_query(new_query):
    st.session_state["search_query"] = new_query

# -------------------------------------------------------------
# 5. 풍부한 20가지 여행 행운 풀 & 완전 랜덤 추첨
# -------------------------------------------------------------
EXPANDED_FORTUNES = [
    ("✨ 대박 숨은 맛집 발견", "우연히 들어간 골목 식당에서 인생 최고의 맛과 정을 경험하게 됩니다!"),
    ("📸 인생샷 무한 생성", "자연광과 배경이 완벽히 어우러져 어디서 찍어도 A컷 인생 사진을 건질 운세입니다."),
    ("🌤️ 화창한 맑은 하늘", "구름 한 점 없는 청명한 날씨 덕분에 여행 내내 발걸음이 한결 가볍고 상쾌합니다."),
    ("🎁 따뜻한 친절과 환대", "현지인이나 동행자로부터 예상치 못한 따스한 배려와 도움을 받게 됩니다."),
    ("☕ 완벽한 여유의 티타임", "조용하고 감각적인 카페에서 음악과 함께 온전한 재충전의 시간을 보냅니다."),
    ("🚶 발길 닿는 곳이 명소", "계획 없이 우연히 꺾은 골목길에서 보물 같은 풍경과 감성을 마주칩니다."),
    ("🛍️ 득템의 찬스", "오랫동안 찾아 헤매던 특별한 소품이나 기념품을 기분 좋은 가격에 만나게 됩니다."),
    ("🌅 황홀한 일몰 감상", "하루의 끝자락, 하늘을 붉게 물들이는 잊지 못할 환상적인 노을을 마주합니다."),
    ("🎵 여행 BGM과의 조화", "이어폰에서 흘러나오는 노래가 지금 걷는 풍경과 소름 돋게 어울리는 순간을 만납니다."),
    ("🍧 달콤한 디저트의 축복", "한 입 베어 무는 순간 피로가 눈 녹듯 사라지는 환상적인 달콤함을 맛봅니다."),
    ("🚦 이동 요정 강림", "대중교통 환승 타이밍이 척척 맞아떨어지고 대기 시간 없이 매끄럽게 이동합니다."),
    ("🔋 넘치는 활력과 에너지", "하루 종일 걸어 다녀도 발걸음이 지치지 않는 기분 좋은 컨디션을 유지합니다."),
    ("🌊 가슴이 뻥 뚫리는 시야", "가장 높은 전망대나 탁 트인 스팟에서 시원한 바람과 장관을 한눈에 담습니다."),
    ("🌙 로맨틱한 밤 산책", "은은한 야경 조명 아래를 산책하며 오래도록 기억될 낭만적인 밤을 보냅니다."),
    ("🧭 길 찾기의 달인", "복잡한 골목에서도 헤매지 않고 한 번에 원하는 목적지를 쏙쏙 찾아냅니다."),
    ("🍀 기분 좋은 깜짝 서비스", "방문한 매장에서 친절한 미소와 함께 달콤한 덤이나 서비스를 받게 됩니다."),
    ("📖 잊지 못할 한 페이지", "훗날 꺼내보며 미소 지을 수 있는 소중한 추억과 이야기를 가슴에 남깁니다."),
    ("🛋️ 극강의 편안함", "하루 일정을 마치고 돌아온 숙소가 더없이 아늑하여 꿀잠을 선물합니다."),
    ("🎟️ 웨이팅 프리 패스", "평소 대기가 긴 핫플레이스인데도 도착하자마자 기적처럼 바로 자리가 납니다."),
    ("🌈 뜻밖의 행운 모먼트", "사소하게 지나칠 수 있었던 순간들이 모여 하루 전체를 반짝이게 만들어 줍니다.")
]

def draw_random_fortune():
    current = st.session_state.get("fortune_result")
    candidates = [f for f in EXPANDED_FORTUNES if f != current]
    st.session_state["fortune_result"] = random.choice(candidates if candidates else EXPANDED_FORTUNES)

# -------------------------------------------------------------
# 6. 글로벌 도시 맵 & API 함수
# -------------------------------------------------------------
GLOBAL_CITY_MAP = {
    "서울": ("Seoul", 37.5665, 126.9780),
    "부산": ("Busan", 35.1796, 129.0756),
    "제주": ("Jeju", 33.4996, 126.5312),
    "제주도": ("Jeju", 33.4996, 126.5312),
    "인천": ("Incheon", 37.4563, 126.7052),
    "대구": ("Daegu", 35.8714, 128.6014),
    "대전": ("Daejeon", 36.3504, 127.3845),
    "광주": ("Gwangju", 35.1595, 126.8526),
    "울산": ("Ulsan", 35.5384, 129.3114),
    "수원": ("Suwon", 37.2636, 127.0286),
    "강릉": ("Gangneung", 37.7519, 128.8761),
    "경주": ("Gyeongju", 35.8562, 129.2247),
    "전주": ("Jeonju", 35.8242, 127.1480),
    "속초": ("Sokcho", 38.2070, 128.5918),
    "여수": ("Yeosu", 34.7604, 127.6622),
    "도쿄": ("Tokyo", 35.6762, 139.6503),
    "오사카": ("Osaka", 34.6937, 135.5023),
    "교토": ("Kyoto", 35.0116, 135.7681),
    "후쿠오카": ("Fukuoka", 33.5904, 130.4017),
    "삿포로": ("Sapporo", 43.0618, 141.3545),
    "오키나와": ("Okinawa", 26.2124, 127.6809),
    "방콕": ("Bangkok", 13.7563, 100.5018),
    "다낭": ("Danang", 16.0544, 108.2022),
    "파리": ("Paris", 48.8566, 2.3522),
    "런던": ("London", 51.5074, -0.1278),
    "뉴욕": ("New York", 40.7128, -74.0060)
}

def get_exchange_rates(api_key, base="USD"):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base}"
    try:
        res = requests.get(url, timeout=4)
        if res.status_code == 200:
            data = res.json()
            if data.get("result") == "success":
                return data.get("conversion_rates", {}), True
        return {}, False
    except:
        return {}, False

def get_current_weather_smart(query, weather_api_key, kakao_api_key):
    clean_q = query.strip()
    if not clean_q:
        return None, (None, None), False

    if clean_q in GLOBAL_CITY_MAP:
        eng_name, lat, lon = GLOBAL_CITY_MAP[clean_q]
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": eng_name, "appid": weather_api_key, "units": "metric", "lang": "kr"}
        try:
            res = requests.get(url, params=params, timeout=4)
            if res.status_code == 200:
                data = res.json()
                data["display_name"] = clean_q
                return data, (lat, lon), True
        except:
            pass

    if kakao_api_key:
        headers = {
            "Authorization": f"KakaoAK {kakao_api_key}",
            "KA": "sdk/1.0.0 os/python lang/ko-KR origin/http://localhost:8501"
        }
        for api_type in ["keyword", "address"]:
            try:
                res_k = requests.get(f"https://dapi.kakao.com/v2/local/search/{api_type}.json", headers=headers, params={"query": clean_q, "size": 1}, timeout=3)
                if res_k.status_code == 200:
                    docs = res_k.json().get("documents", [])
                    if docs:
                        lat = float(docs[0]["y"])
                        lon = float(docs[0]["x"])
                        place_nm = docs[0].get("place_name") or docs[0].get("address_name", clean_q)

                        url_w = "https://api.openweathermap.org/data/2.5/weather"
                        params_w = {"lat": lat, "lon": lon, "appid": weather_api_key, "units": "metric", "lang": "kr"}
                        res_w = requests.get(url_w, params=params_w, timeout=4)
                        if res_w.status_code == 200:
                            w_data = res_w.json()
                            w_data["display_name"] = f"{clean_q} ({place_nm.split()[0]})"
                            return w_data, (lat, lon), True
            except:
                pass

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": clean_q, "appid": weather_api_key, "units": "metric", "lang": "kr"}
    try:
        res = requests.get(url, params=params, timeout=4)
        if res.status_code == 200:
            data = res.json()
            data["display_name"] = clean_q
            c_lat = data.get("coord", {}).get("lat")
            c_lon = data.get("coord", {}).get("lon")
            return data, (c_lat, c_lon), True
    except:
        pass

    return None, (None, None), False

# [핵심] size=15로 대폭 확대하여 풍부한 검색 결과 획득
def search_kakao_smart(query, api_key):
    headers = {
        "Authorization": f"KakaoAK {api_key}",
        "KA": "sdk/1.0.0 os/python lang/ko-KR origin/http://localhost:8501"
    }

    try:
        res = requests.get("https://dapi.kakao.com/v2/local/search/keyword.json", headers=headers, params={"query": query, "size": 15}, timeout=4)
        if res.status_code == 200:
            docs = res.json().get("documents", [])
            if docs:
                return docs, True
    except:
        pass

    try:
        res_addr = requests.get("https://dapi.kakao.com/v2/local/search/address.json", headers=headers, params={"query": query, "size": 10}, timeout=4)
        if res_addr.status_code == 200:
            addr_docs = res_addr.json().get("documents", [])
            if addr_docs:
                converted = []
                for item in addr_docs:
                    name = item.get("address_name")
                    converted.append({
                        "place_name": name,
                        "category_name": "지역 > 행정구역",
                        "road_address_name": name,
                        "address_name": name,
                        "phone": "",
                        "place_url": f"https://map.kakao.com/link/search/{name}",
                        "x": item.get("x"),
                        "y": item.get("y")
                    })
                return converted, True
    except:
        pass

    return [], False

# -------------------------------------------------------------
# 7. 사이드바
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="background:#FFFFFF; border:1px solid #D5E5DB; border-radius:14px; padding:14px; box-shadow:0 2px 8px rgba(0,0,0,0.02); margin-bottom:15px;">
        <div style="font-size:11px; font-weight:800; color:#40916C; text-transform:uppercase;">SYSTEM MONITOR</div>
        <h3 style="margin:2px 0 4px 0; font-size:16px; color:#1B4332;">🍀 API 연결 상태</h3>
        <span style="font-size:11.5px; color:#6B7280;">실시간 키 인증 및 통신 점검</span>
    </div>
    """, unsafe_allow_html=True)

    if not kakao_key:
        st.error("❌ 카카오맵 API: 키 누락")
    else:
        _, kakao_ok = search_kakao_smart("성수", kakao_key)
        if kakao_ok:
            st.success("✅ 카카오 로컬 API: 정상 연결")
        else:
            st.error("❌ 카카오 로컬 API: 통신 실패")

    if not exchange_key:
        st.error("❌ 환율 API: 키 누락")
    else:
        _, ex_ok = get_exchange_rates(exchange_key, "USD")
        if ex_ok:
            st.success("✅ 환율 API: 정상 연결")
        else:
            st.error("❌ 환율 API: 통신 실패")

    if not weather_key:
        st.error("❌ 날씨 API: 키 누락")
    else:
        _, _, w_ok = get_current_weather_smart("성수", weather_key, kakao_key)
        if w_ok:
            st.success("✅ 날씨 API: 정상 연결")
        else:
            st.error("❌ 날씨 API: 통신 실패")

    st.markdown("---")
    st.markdown("""
    <div style="font-size:11.5px; color:#52796F; line-height:1.5; background:#FFFFFF; padding:10px; border-radius:10px; border:1px solid #E0ECE4;">
        🍀 <b>스마트 동네 연동</b><br>
        날씨 칸에 원하는 동네를 입력하면 <b>오른쪽 지도도 자동으로 해당 지역으로 이동</b>합니다!
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# 8. 상단 헤더 배너
# -------------------------------------------------------------
st.markdown("""
<div class="clover-banner">
    <div>
        <span class="clover-badge">🍀 TRIP ASSISTANT NOTE</span>
        <h1 class="clover-title">여행 준비 도우미🍀</h1>
        <div class="clover-desc">행운이 가득한 여행의 시작! 실시간 날씨, 환율 계산, 핫플레이스 탐색까지 한눈에.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 9. 본문 레이아웃 (좌: 날씨/환율/행운, 우: 지도)
# -------------------------------------------------------------
col_left, col_right = st.columns([1, 1.15], gap="large")

# =======================
# [LEFT COLUMN] 날씨 & 환율 & 일체형 행운 뽑기
# =======================
with col_left:
    # 1. 날씨 섹션
    with st.container(border=True):
        st.markdown('<div class="card-label">Weather Forecast</div><div class="card-title">🌤️ 여행지 실시간 날씨</div>', unsafe_allow_html=True)
        city_input = st.text_input(
            "도시 또는 동네 입력 (한글/영문)",
            value=st.session_state["city_input"],
            key="city_input_field",
            placeholder="예: 성수, 서면, 홍대, 강남, 제주, 도쿄, 파리",
            label_visibility="collapsed"
        )

        weather_coords = (None, None)
        if weather_key and city_input:
            w, weather_coords, is_ok = get_current_weather_smart(city_input, weather_key, kakao_key)
            if is_ok and w:
                temp = w["main"]["temp"]
                feels = w["main"]["feels_like"]
                desc = w["weather"][0]["description"].title()
                icon = w["weather"][0]["icon"]
                humidity = w["main"]["humidity"]
                wind = w["wind"]["speed"]
                display_name = w.get("display_name", city_input)

                if st.session_state["last_synced_city"] != city_input:
                    st.session_state["last_synced_city"] = city_input
                    st.session_state["city_input"] = city_input
                    st.session_state["search_query"] = city_input

                st.markdown(f"""
                <div class="weather-box">
                    <div>
                        <div class="weather-temp">{temp:.1f}°C</div>
                        <div style="font-size: 13px; font-weight: 700; color: #2D6A4F; margin-top: 4px;">
                            {display_name} · <span style="color: #52796F;">{desc}</span>
                        </div>
                    </div>
                    <img src="https://openweathermap.org/img/wn/{icon}@2x.png" width="55" style="background:#FFFFFF; border-radius:50%; border:1px solid #D5E5DB;"/>
                </div>
                <div class="weather-stat-grid">
                    <div style="background:#F9FBFA; padding:9px; border-radius:10px; border:1px solid #E5EBE7;">
                        <div style="font-size:10.5px; color:#6B7280; font-weight:600;">체감</div>
                        <div style="font-weight:750; font-size:13px; color:#1B4332;">{feels:.1f}°C</div>
                    </div>
                    <div style="background:#F9FBFA; padding:9px; border-radius:10px; border:1px solid #E5EBE7;">
                        <div style="font-size:10.5px; color:#6B7280; font-weight:600;">습도</div>
                        <div style="font-weight:750; font-size:13px; color:#1B4332;">{humidity}%</div>
                    </div>
                    <div style="background:#F9FBFA; padding:9px; border-radius:10px; border:1px solid #E5EBE7;">
                        <div style="font-size:10.5px; color:#6B7280; font-weight:600;">바람</div>
                        <div style="font-weight:750; font-size:13px; color:#1B4332;">{wind}m/s</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.caption("⚠️ 위치를 찾지 못했습니다. 주요 지역명(예: 성수, 서면, 홍대, 강남, 도쿄)으로 적어주세요.")

    # 2. 환율 섹션
    with st.container(border=True):
        st.markdown('<div class="card-label">Exchange Rate</div><div class="card-title">💱 스마트 환율 계산기</div>', unsafe_allow_html=True)
        if exchange_key:
            currencies = ["KRW", "USD", "JPY", "EUR", "CNY", "VND"]
            c1, c2 = st.columns(2)
            base_c = c1.selectbox("보유 통화", currencies, index=1)
            target_c = c2.selectbox("환전 통화", currencies, index=0)
                
            amt = st.number_input("환전할 금액", min_value=1.0, value=100.0, step=10.0)
            
            rates, _ = get_exchange_rates(exchange_key, base_c)
            if rates and target_c in rates:
                r = rates[target_c]
                total = amt * r
                st.markdown(f"""
                <div class="rate-box">
                    <div style="font-size:11px; font-weight:700; color:#52796F; text-transform:uppercase;">Estimated Value</div>
                    <div class="rate-val">{total:,.2f} {target_c}</div>
                    <div style="font-size:11px; color:#6B7280;">1 {base_c} = {r:,.2f} {target_c} 기준</div>
                </div>
                """, unsafe_allow_html=True)

    # 3. 네잎클로버 완전 랜덤 행운 뽑기
    with st.container(border=True):
        st.markdown("""
        <div class="card-label">Daily Fortune</div>
        <div class="card-title" style="margin-bottom:4px;">🍀 오늘의 여행 행운 뽑기</div>
        <div style="font-size:12px; color:#6B7280; margin-bottom:14px;">어떤 클로버를 선택해도 완전 무작위로 오늘의 행운이 열립니다!</div>
        """, unsafe_allow_html=True)

        clover_cols = st.columns(5)
        for i in range(5):
            clover_cols[i].button(
                "🍀",
                key=f"clover_btn_{i}",
                on_click=draw_random_fortune,
                use_container_width=True
            )

        if st.session_state["fortune_result"]:
            f_title, f_desc = st.session_state["fortune_result"]
            st.markdown(f"""
            <div class="fortune-inner-box">
                <div class="fortune-title">{f_title}</div>
                <div class="fortune-desc">{f_desc}</div>
            </div>
            """, unsafe_allow_html=True)


# =======================
# [RIGHT COLUMN] 카카오맵 장소 및 동네 탐색 (최대 15개 표시)
# =======================
with col_right:
    with st.container(border=True):
        st.markdown('<div class="card-label">Map & Places</div><div class="card-title">🗺️ 목적지 및 핫플레이스 탐색</div>', unsafe_allow_html=True)

        base_region = city_input.strip() if city_input.strip() else "성수"

        btn_cols = st.columns(4)
        btn_cols[0].button("☕ 카페", on_click=set_query, args=(f"{base_region} 카페",), use_container_width=True)
        btn_cols[1].button("🍽️ 맛집", on_click=set_query, args=(f"{base_region} 맛집",), use_container_width=True)
        btn_cols[2].button("🍮 푸딩", on_click=set_query, args=(f"{base_region} 푸딩",), use_container_width=True)
        btn_cols[3].button("🍢 이자카야", on_click=set_query, args=(f"{base_region} 이자카야",), use_container_width=True)

        current_search = st.text_input(
            "검색어 입력",
            key="search_query",
            placeholder="동네(성수, 서면, 홍대) 또는 장소 검색",
            label_visibility="collapsed"
        )

        default_lat = weather_coords[0] if weather_coords[0] else 37.5446
        default_lng = weather_coords[1] if weather_coords[1] else 127.0560
        center_lat, center_lng = default_lat, default_lng
        zoom_level = 14
        places = []

        # 최대 15개 장소 조회
        if kakao_key and current_search.strip():
            places, _ = search_kakao_smart(current_search.strip(), kakao_key)
            if places:
                first = places[0]
                center_lat, center_lng = float(first["y"]), float(first["x"])
                zoom_level = 14 if "행정구역" in first.get("category_name", "") else 15

        fig = folium.Figure(height=410)
        m = folium.Map(location=[center_lat, center_lng], zoom_start=zoom_level, control_scale=True)
        fig.add_child(m)

        # 검색된 모든 장소(최대 15개) 지도에 마커 등록
        if places:
            for idx, p in enumerate(places, 1):
                p_lat, p_lng = float(p["y"]), float(p["x"])
                name = p["place_name"]
                cat = p.get("category_name", "").split(">")[-1].strip()
                addr = p.get("road_address_name") or p.get("address_name")
                url = p.get("place_url", f"https://map.kakao.com/link/search/{name}")
                phone = p.get("phone") or "연락처 미등록"

                popup_content = f"""
                <div style="font-family:'Pretendard', sans-serif; min-width:170px; padding:3px;">
                    <div style="font-size:10.5px; color:#2D6A4F; font-weight:700;">#{cat}</div>
                    <div style="font-size:13.5px; font-weight:750; color:#1F2937; margin:2px 0;">{idx}. {name}</div>
                    <div style="font-size:11px; color:#6B7280;">{addr}</div>
                    <div style="font-size:11px; color:#6B7280; margin-top:2px;">📞 {phone}</div>
                    <a href="{url}" target="_blank" style="display:inline-block; margin-top:5px; font-size:11px; color:#40916C; font-weight:700; text-decoration:none;">카카오맵 열기 ↗</a>
                </div>
                """

                folium.Marker(
                    location=[p_lat, p_lng],
                    popup=folium.Popup(popup_content, max_width=280),
                    tooltip=f"{idx}. {name}",
                    icon=folium.Icon(color="green", icon="info-sign")
                ).add_to(m)

        st_folium(fig, use_container_width=True, height=410, returned_objects=[])

        # 장소 리스트 출력 (기본 5개, 더보기 클릭 시 전체 최대 15개)
        if places:
            total_count = len(places)
            display_limit = total_count if st.session_state["show_all_places"] else 5
            displayed_places = places[:display_limit]

            st.markdown(f"""
            <div style='display:flex; justify-content:space-between; align-items:center; margin-top:14px; margin-bottom:8px;'>
                <span style='font-size:12px; font-weight:700; color:#2D6A4F;'>검색 결과 ({len(displayed_places)} / {total_count}개)</span>
            </div>
            """, unsafe_allow_html=True)

            for idx, item in enumerate(displayed_places, 1):
                cat_tag = item.get("category_name", "").split(">")[-1].strip()
                road_addr = item.get("road_address_name") or item.get("address_name")
                st.markdown(f"""
                <div class="place-item">
                    <div style="max-width: 78%;">
                        <span style="font-size:12px; font-weight:800; color:#40916C; margin-right:4px;">{idx}.</span>
                        <span class="place-title">{item['place_name']}</span>
                        <span class="place-category">{cat_tag}</span>
                        <div class="place-addr">{road_addr} · 📞 {item.get('phone') or '번호 없음'}</div>
                    </div>
                    <a href="{item.get('place_url')}" target="_blank" style="text-decoration:none; font-size:11px; font-weight:700; color:#2D6A4F; padding:5px 12px; background:#E8F5EE; border:1px solid #B7DFCA; border-radius:7px; white-space:nowrap;">
                        상세보기 ↗
                    </a>
                </div>
                """, unsafe_allow_html=True)

            # 5개 이상일 때 '더보기 / 접기' 토글 버튼
            if total_count > 5:
                toggle_btn_label = "▲ 접기 (기본 5개만 보기)" if st.session_state["show_all_places"] else f"▼ 더보기 (총 {total_count}개 전체 보기)"
                st.button(toggle_btn_label, on_click=toggle_show_places, use_container_width=True)

        elif current_search.strip():
            st.info("검색된 장소가 없습니다. 다른 키워드로 검색해 보세요.")#여행프로그램