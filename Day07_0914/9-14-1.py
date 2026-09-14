# folium으로 지도에 마커를 표시하는 예제 코드
# import folium     pip install folium
# 서울 시내 명소 4곳의 좌표(위도/경도)와 이름을 리스트로 받아 folium 지도를 만들고 
# 각 좌표에 이름표가 붙은 마커를 찍은 다음, basic_map.html 파일로 저장하는 예제 코드입니다.
# 저장된 basic_map.html을 웹브라우저로 열어서 확인
# python 9-14-1.py

import folium
import webbrowser


# 서울 시내 명소 4곳의 이름, 위도, 경도, 샘플데이터
places = [
    {"name": "여의도한강공원", "lat": 37.5284, "lng": 126.9328},
    {"name": "경복궁", "lat": 37.579617, "lng": 126.977041},
    {"name": "N서울타워(남산타워)", "lat": 37.551169, "lng": 126.988227},
    {"name": "강남역", "lat": 37.497952, "lng": 127.027619}
]


# 지도의 시작 중심 좌표 (N서울타워(남산타워)) 지정해서 folium 지도 객체 생성
# 숫자가 클수록 더 가깝게 보여준다
seoul_center = [37.551169, 126.988227]
map = folium.Map(location=seoul_center, zoom_start=13)

# CartoDB 타일 URL을 직접 입력 (차단 우회)
map = folium.Map(
    location=seoul_center,
    zoom_start=12,
    tiles="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",
    attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
)

# 리스트에 담긴 장소들을 하나씩 꺼내며 지도 위 마커 추가
for place in places:
    folium.Marker(
        location=[place["lat"], place["lng"]],
        popup=folium.Popup(place["name"], max_width=200),
        tooltip=place["name"],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(map)

# basic_map.html 파일로 저장
map.save("basic_map.html")
print("basic_map.html 파일이 성공적으로 저장되었습니다.")

# 저장된 basic_map.html을 웹브라우저로 열어서 확인
webbrowser.open("basic_map.html")