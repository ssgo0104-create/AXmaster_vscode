import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io
import os
import urllib.request
from PIL import Image, ImageDraw, ImageFont

# -------------------------------------------------------------
# 1. 페이지 기본 설정
# -------------------------------------------------------------
st.set_page_config(
    page_title="무역 직무 MBTI 진단 테스트",
    page_icon="🚢",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------------------
# 2. 전체 UI 스타일
# -------------------------------------------------------------
st.markdown("""<style>
.stApp {
    background: #F6F7F9 !important;
    color: #172033 !important;
}

.block-container {
    padding-top: 2.8rem;
    padding-bottom: 5rem;
    max-width: 720px;
    width: 100%;
    margin: 0 auto;
}

p, span, div, label {
    font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
}

.main-title {
    font-size: 2.25rem;
    font-weight: 900;
    color: #172033;
    text-align: center;
    letter-spacing: -0.04em;
    margin-bottom: 0.45rem;
    line-height: 1.3;
}

.sub-title {
    font-size: 0.98rem;
    color: #667085;
    text-align: center;
    margin-bottom: 2rem;
    font-weight: 500;
    line-height: 1.55;
}

.intro-box {
    background: #FFFFFF;
    border: 1px solid #E4E7EC;
    border-radius: 18px;
    padding: 28px 30px;
    margin-bottom: 24px;
    box-shadow: 0 5px 18px rgba(16, 24, 40, 0.035);
}

.feature-tag {
    display: inline-block;
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: #244A7C;
    background: #F1F6FC;
    border: 1px solid #D8E5F3;
    padding: 5px 11px;
    border-radius: 999px;
    margin-bottom: 12px;
}

.dim-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    margin-top: 14px;
}

.dim-card {
    padding: 18px;
    border-radius: 14px;
    background: #FFFFFF;
    border: 1px solid #E4E7EC;
    box-shadow: 0 3px 10px rgba(16, 24, 40, 0.025);
}

.dim-blue { border-top: 3px solid #4778B8; }
.dim-sky { border-top: 3px solid #5B9BD5; }
.dim-indigo { border-top: 3px solid #6573C3; }
.dim-cyan { border-top: 3px solid #5A9A9A; }

.single-q-card {
    background: #FFFFFF !important;
    border-radius: 18px;
    padding: 30px 28px;
    margin-top: 14px;
    margin-bottom: 20px;
    border: 1px solid #E4E7EC;
    box-shadow: 0 6px 20px rgba(16, 24, 40, 0.045);
}

.q-step-badge {
    font-size: 0.76rem;
    font-weight: 800;
    color: #FFFFFF;
    background: #243B5A;
    padding: 5px 12px;
    border-radius: 999px;
    display: inline-block;
    margin-bottom: 11px;
}

.q-dim-text {
    font-size: 0.84rem;
    font-weight: 700;
    color: #667085;
    margin-left: 7px;
}

.q-main-scenario {
    font-size: 1.18rem;
    font-weight: 800;
    color: #172033;
    line-height: 1.65;
    letter-spacing: -0.025em;
    margin-bottom: 4px;
}

/* 일반 버튼 및 다운로드 버튼 공통 스타일 */
.stButton > button, .stDownloadButton > button {
    border-radius: 12px !important;
    font-weight: 700 !important;
    padding: 13px 18px !important;
    transition: all 0.16s ease !important;
    white-space: normal !important;
    height: auto !important;
    min-height: 48px !important;
    line-height: 1.5 !important;
}

.stButton > button[kind="primary"], .stDownloadButton > button {
    background: #243B5A !important;
    color: #FFFFFF !important;
    border: 1px solid #243B5A !important;
    box-shadow: 0 4px 12px rgba(36, 59, 90, 0.16) !important;
    text-align: center !important;
    width: 100% !important;
}

.stButton > button[kind="primary"]:hover, .stDownloadButton > button:hover {
    background: #1C304A !important;
    border-color: #1C304A !important;
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(36, 59, 90, 0.2) !important;
}

.stButton > button[kind="secondary"] {
    background: #FFFFFF !important;
    color: #273142 !important;
    border: 1px solid #D5D9E0 !important;
    text-align: left !important;
}

.stButton > button[kind="secondary"]:hover {
    background: #F7FAFD !important;
    border-color: #4A6F9F !important;
    color: #243B5A !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(36, 59, 90, 0.06) !important;
}

/* 🧭 문항 건너뛰기 전용 버튼 스타일 */
.nav-grid-container .stButton > button {
    padding: 7px 0 !important;
    min-height: 38px !important;
    text-align: center !important;
    font-size: 0.88rem !important;
    font-weight: 800 !important;
    border-radius: 8px !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    margin-bottom: 6px !important;
}

.stProgress > div > div > div > div {
    background: #4A6F9F !important;
}

.result-section-title {
    color: #172033;
    font-weight: 900;
    letter-spacing: -0.025em;
    margin-top: 5px;
    margin-bottom: 14px;
}

.result-card {
    background: #FFFFFF;
    border: 1px solid #E4E7EC;
    border-radius: 18px;
    box-shadow: 0 5px 18px rgba(16, 24, 40, 0.035);
}

.axis-card {
    background: #FFFFFF;
    border: 1px solid #E4E7EC;
    border-radius: 14px;
    padding: 17px 18px;
    margin-bottom: 11px;
}

.axis-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 9px;
}

.axis-name {
    font-size: 0.94rem;
    font-weight: 800;
    color: #344054;
}

.axis-bar {
    display: flex;
    width: 100%;
    height: 11px;
    border-radius: 999px;
    overflow: hidden;
    background: #EAECF0;
}

.axis-left { background: #5A7394; }
.axis-right { background: #B8C6D6; }

.axis-caption {
    display: flex;
    justify-content: space-between;
    margin-top: 7px;
    font-size: 0.76rem;
    color: #667085;
}

.detail-card {
    background: #FFFFFF;
    border: 1px solid #E4E7EC;
    border-radius: 18px;
    padding: 25px;
    box-shadow: 0 5px 18px rgba(16, 24, 40, 0.035);
    margin-bottom: 24px;
}

@media (max-width: 640px) {
    .block-container {
        padding-top: 1.8rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .main-title { font-size: 1.7rem; }
    .sub-title { font-size: 0.9rem; margin-bottom: 1.4rem; }
    .dim-grid { grid-template-columns: 1fr; }
    .single-q-card { padding: 22px 20px; }
    .q-main-scenario { font-size: 1.05rem; }
}
</style>""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 3. 질문 데이터
# -------------------------------------------------------------
QUESTIONS = [
    {
        "id": 1, "dim": "F/B", "dim_name": "업무 반경 (Front vs Back)",
        "scenario": "해외 유명 무역 전시회 참가 기회가 주어졌을 때, 당신이 더 몰입하고 싶은 역할은?",
        "choice_a": "부스 전면에 서서 각국 바이어를 맞이하고 상담하며 명함을 적극적으로 교환한다.",
        "choice_b": "부스 백오피스에서 바이어별 상담 일지를 체계적으로 기록하고 카탈로그/샘플 재고를 챙긴다.",
        "trait_a": "F", "trait_b": "B"
    },
    {
        "id": 2, "dim": "A/D", "dim_name": "판단 기준 (Action vs Data)",
        "scenario": "유력 바이어가 신제품의 대략적인 견적(Target Price)을 당장 현장에서 묻는다면?",
        "choice_a": "시장 감각과 경쟁사 가격 수준을 떠올려 즉시 적정 가격 범위를 제시하고 반응을 살핀다.",
        "choice_b": "원자재비, 물류비, 마진율이 계산된 정밀 원가 스프레드시트를 검토한 후 공식 회신한다.",
        "trait_a": "A", "trait_b": "D"
    },
    {
        "id": 3, "dim": "C/R", "dim_name": "업무 태도 (Compliance vs Risk)",
        "scenario": "출항 마감 직전, 선적 서류의 품명 철자에 사소한 오타 1글자를 발견했다면?",
        "choice_a": "도착지 통관 보류나 네고 하자 위험이 있으므로, 시간이 걸리더라도 원칙대로 정정 후 발행한다.",
        "choice_b": "사소한 표기이고 일정 지연 페널티가 더 크므로, 일단 진행시키고 사후 보완 방법을 찾는다.",
        "trait_a": "C", "trait_b": "R"
    },
    {
        "id": 4, "dim": "M/S", "dim_name": "시야 범위 (Macro vs Micro)",
        "scenario": "연간 수출 실적 리뷰 회의를 준비할 때, 가장 먼저 눈길이 가고 분석하고 싶은 데이터는?",
        "choice_a": "글로벌 거시경제 추이, 주요 권역별 시장 점유율 성장률, 공급망 전체의 리드타임 흐름",
        "choice_b": "개별 품목별 HS코드별 수출 단가 변동(센트 단위), 품목별 부대비용 및 오발송 발생 내역",
        "trait_a": "M", "trait_b": "S"
    },
    {
        "id": 5, "dim": "F/B", "dim_name": "업무 반경 (Front vs Back)",
        "scenario": "선적 공간(Space) 캔슬 등 돌발 물류 이슈가 터졌을 때, 당신의 본능적인 대처 방식은?",
        "choice_a": "선사 담당자나 포워더에게 즉시 다이렉트 전화를 걸어 목소리로 상황을 파악하고 네고한다.",
        "choice_b": "사건 경위와 책임 소재를 이메일과 메신저로 텍스트/공문 기록으로 명확히 남기며 대응한다.",
        "trait_a": "F", "trait_b": "B"
    },
    {
        "id": 6, "dim": "A/D", "dim_name": "판단 기준 (Action vs Data)",
        "scenario": "아직 검증되지 않은 신흥국(남미/동남아 등) 시장 개척 여부를 결정할 때 우선순위는?",
        "choice_a": "현지 소비 트렌드의 폭발성과 선점 효과, 직관적인 비즈니스 잠재 기회",
        "choice_b": "관세청 HS코드 수출입 통계, 1인당 GDP 추이, 수입 규제 데이터의 철저한 검증",
        "trait_a": "A", "trait_b": "D"
    },
    {
        "id": 7, "dim": "C/R", "dim_name": "업무 태도 (Compliance vs Risk)",
        "scenario": "신규 바이어가 결제 조건을 신용장(L/C)이 아닌 외상 결제(O/A 60일)로 요구해 왔다면?",
        "choice_a": "수출보험 한도 승인이나 확실한 담보가 확보되지 않는 한 결코 원칙을 양보할 수 없다.",
        "choice_b": "바이어의 향후 오더 규모와 잠재력을 감안해, 리스크를 감수하고 초기 물량을 수용해 본다.",
        "trait_a": "C", "trait_b": "R"
    },
    {
        "id": 8, "dim": "M/S", "dim_name": "시야 범위 (Macro vs Micro)",
        "scenario": "물류 프로세스 개선 태스크포스(TF)에 참여했을 때, 당신이 집중하고 싶은 과제는?",
        "choice_a": "공장 출하부터 해외 현지 배송까지의 엔드투엔드(End-to-End) 글로벌 SCM 동선 최적화",
        "choice_b": "파렛트당 컨테이너 적재 효율(CBM) 극대화 및 패킹 포장재 단가 1원 절감 기법",
        "trait_a": "M", "trait_b": "S"
    },
    {
        "id": 9, "dim": "F/B", "dim_name": "업무 반경 (Front vs Back)",
        "scenario": "하루 일과 중 더 에너지를 얻고 몰입도가 높은 업무 환경은?",
        "choice_a": "국내외 거래처와의 끊임없는 미팅, 전화 통화, 슬랙 대화로 북적이는 다이내믹한 환경",
        "choice_b": "방해받지 않고 모니터 2대에 ERP, 엑셀, 규정집을 띄워놓고 홀로 집중하는 정적 환경",
        "trait_a": "F", "trait_b": "B"
    },
    {
        "id": 10, "dim": "A/D", "dim_name": "판단 기준 (Action vs Data)",
        "scenario": "글로벌 해상 운임 지수가 가파르게 상승하기 시작했다는 속보를 접했을 때?",
        "choice_a": "'더 오르면 선복도 못 잡는다!' 즉각적인 판단으로 이번 분기 선복을 선제 부킹한다.",
        "choice_b": "'일시적 급등인지 구조적인지 봐야 한다.' 최근 6개월 SCFI 추이와 유가 지표를 교차 검증한다.",
        "trait_a": "A", "trait_b": "D"
    },
    {
        "id": 11, "dim": "C/R", "dim_name": "업무 태도 (Compliance vs Risk)",
        "scenario": "선적 마감 1시간 전, 포워더가 규정상 모호한 방식으로 선적을 처리해 주겠다고 제안한다면?",
        "choice_a": "법적·규정상 하자가 생기면 더 큰 화가 되므로, 다음 항차로 미루더라도 정석대로 간다.",
        "choice_b": "바이어와의 납기 약속을 지키는 게 최우선이므로, 각서(L/I)를 작성하고 신속히 밀어붙인다.",
        "trait_a": "C", "trait_b": "R"
    },
    {
        "id": 12, "dim": "M/S", "dim_name": "시야 범위 (Macro vs Micro)",
        "scenario": "주요 결제 통화(달러/엔화) 환율이 급격히 요동치기 시작했다는 소식을 들었을 때?",
        "choice_a": "통화 가치 변동이 회사 연간 수익성과 글로벌 거점 공급망 전략에 미칠 영향을 내다본다.",
        "choice_b": "당장 금주 결제 예정인 수출 대금 인보이스 건별 환차손익을 센트 단위까지 재계산한다.",
        "trait_a": "M", "trait_b": "S"
    },
    {
        "id": 13, "dim": "F/B", "dim_name": "업무 반경 (Front vs Back)",
        "scenario": "거래처(바이어 또는 벤더)와의 장기적 신뢰를 구축할 때 더 중요하다고 믿는 것은?",
        "choice_a": "정기적인 안부, 티타임, 식사, 전시회 만남 등 인간적인 유대감과 라포(Rapport) 형성",
        "choice_b": "오류 없는 서류 발송, 납기 준수, 명문화된 계약 조건 이행 등 빈틈없는 업무적 완결성",
        "trait_a": "F", "trait_b": "B"
    },
    {
        "id": 14, "dim": "A/D", "dim_name": "판단 기준 (Action vs Data)",
        "scenario": "해외 신규 원자재 공급업체(Vendor)를 최종 낙점할 때 당신의 주된 결정 기준은?",
        "choice_a": "화상 미팅에서 느낀 대표의 추진력과 비즈니스 태도, 현물 샘플의 실물 촉감과 인상",
        "choice_b": "공급사의 공인 시험성적서, 지난 3년간의 공장 불량률 수치, 단가 비교 원가 분석표",
        "trait_a": "A", "trait_b": "D"
    },
    {
        "id": 15, "dim": "C/R", "dim_name": "업무 태도 (Compliance vs Risk)",
        "scenario": "경쟁사의 저가 공세로 오랫동안 거래해 온 주요 바이어를 경쟁사에 뺏길 위기라면?",
        "choice_a": "마진 마지노선 원칙을 고수하며, 원산지 증명과 품질 신뢰도 및 사후관리로 설득한다.",
        "choice_b": "노마진을 감수하더라도 출혈 가격 경쟁에 즉시 베팅하여 일단 바이어를 뺏기지 않는다.",
        "trait_a": "C", "trait_b": "R"
    },
    {
        "id": 16, "dim": "M/S", "dim_name": "시야 범위 (Macro vs Micro)",
        "scenario": "영문 무역 매매계약서를 검토할 때 당신의 시선이 가장 먼저 머무는 곳은?",
        "choice_a": "계약의 전반적인 준거법, 분쟁 해결 조항, 인코텀즈 조건에 따른 양사의 위험 분담 구조",
        "choice_b": "부대비용(THC, Demurrage) 귀속 주체, 결제일 오기재 여부, 세부 면책 조항의 단어 뉘앙스",
        "trait_a": "M", "trait_b": "S"
    },
    {
        "id": 17, "dim": "F/B", "dim_name": "업무 반경 (Front vs Back)",
        "scenario": "팀에서 대규모 수출 프로젝트를 수행할 때, 가장 기여하고 싶은 포지션은?",
        "choice_a": "화주사, 선사, 해외 파트너 등 이해관계자들의 갈등을 조율하고 협상하는 대외 메신저",
        "choice_b": "진행 단계별 서류 현황을 트래킹하고, ERP 전산 데이터 및 예산을 종합 관리하는 컨트롤 타워",
        "trait_a": "F", "trait_b": "B"
    },
    {
        "id": 18, "dim": "A/D", "dim_name": "판단 기준 (Action vs Data)",
        "scenario": "해외 바이어로부터 선적된 제품에 결함이 있다는 긴급 클레임이 들어왔다면?",
        "choice_a": "바이어 분노를 가라앉히기 위해 즉시 유선 사과 후 대체품 긴급 항공 발송 등 실행 조치",
        "choice_b": "생산 로트 번호와 검수 로그 데이터, 선적 당시 온습도 기록을 분석해 원인과 귀책 규명",
        "trait_a": "A", "trait_b": "D"
    },
    {
        "id": 19, "dim": "C/R", "dim_name": "업무 태도 (Compliance vs Risk)",
        "scenario": "EU 탄소국경조정제도(CBAM) 등 까다로운 신규 통상 규제가 도입되었을 때?",
        "choice_a": "정부와 공공기관의 공식 가이드라인이 명확해질 때까지 철저히 보수적으로 대응한다.",
        "choice_b": "규제의 틈새와 기회를 선제적으로 파악해 경쟁사보다 먼저 친환경 인증을 마케팅에 활용한다.",
        "trait_a": "C", "trait_b": "R"
    },
    {
        "id": 20, "dim": "M/S", "dim_name": "시야 범위 (Macro vs Micro)",
        "scenario": "해외 현지 물류 허브 거점을 새롭게 선정해야 하는 프로젝트를 맡았다면?",
        "choice_a": "인접 국가들과의 FTA 체결망, 대륙 간 해상 항로 연결성, 장기적 통상 환경 조망",
        "choice_b": "현지 창고 일일 보관료, 보세운송 구간별 셔틀 비용, 현지 지게차 인건비 시세 분석",
        "trait_a": "M", "trait_b": "S"
    },
    {
        "id": 21, "dim": "F/B", "dim_name": "업무 반경 (Front vs Back)",
        "scenario": "해외 출장지에서 저녁 일정이 비었을 때, 당신이 자연스럽게 선택할 행동은?",
        "choice_a": "현지 에이전트나 유관 바이어들과 가벼운 맥주 미팅을 하며 현지 인맥 네트워크를 넓힌다.",
        "choice_b": "호텔 룸에서 오늘 미팅 내용을 리포트로 정리하고 내일 있을 본 상담 자료를 꼼꼼히 점검한다.",
        "trait_a": "F", "trait_b": "B"
    },
    {
        "id": 22, "dim": "A/D", "dim_name": "판단 기준 (Action vs Data)",
        "scenario": "해외 창고에 특정 모델의 재고가 예상보다 빠르게 쌓여가고 있을 때?",
        "choice_a": "기존 바이어들에게 번들 번외 할인 프로모션을 제안하여 현장 재고를 빠르게 소진시킨다.",
        "choice_b": "주차별 출고량 추세선과 리드타임을 통계적으로 재분석하여 안전재고 발주 로직을 수정한다.",
        "trait_a": "A", "trait_b": "D"
    },
    {
        "id": 23, "dim": "C/R", "dim_name": "업무 태도 (Compliance vs Risk)",
        "scenario": "바이어가 개설해 준 신용장(L/C)에 까다로운 단서 조항(Special Condition)이 붙어 있다면?",
        "choice_a": "수출 대금 부도 위험을 원천 차단하기 위해, 선적을 늦추더라도 즉각 Amendment(조건변경)를 요청한다.",
        "choice_b": "오더 규모가 크고 오랜 거래처라면, 은행 매입 시 디스쿱(하자수수료)을 감수하고 선적을 진행한다.",
        "trait_a": "C", "trait_b": "R"
    },
    {
        "id": 24, "dim": "M/S", "dim_name": "시야 범위 (Macro vs Micro)",
        "scenario": "무역 업무 중 당신에게 가장 짜릿한 직무적 성취감을 주는 순간은?",
        "choice_a": "'우리 회사가 이번에 중동-유럽을 잇는 새로운 글로벌 공급 루트를 완벽하게 개척했다!'",
        "choice_b": "'수십 장의 복잡한 통관 서류 속에서 관세 추징을 유발할 뻔한 결정적 오타 1개를 잡아냈다!'",
        "trait_a": "M", "trait_b": "S"
    }
]

# -------------------------------------------------------------
# 4. JOBS
# -------------------------------------------------------------
JOBS = {
    "FARM": {
        "title": "해외영업 (신시장 개척형)",
        "subtitle": "글로벌 프런티어",
        "char_name": "불꽃 개척자 레오",
        "char_icon": "🦁",
        "char_color": "#EA580C",
        "traits": "대외 협상(F) + 빠른 실행(A) + 도전 정신(R) + 거시적 안목(M)",
        "strengths": [
            "불확실성을 두려워하지 않는 과감한 추진력과 개척 정신",
            "글로벌 바이어의 마음을 여는 강력한 친화력과 협상 감각",
            "새로운 해외 트렌드와 비즈니스 기회를 포착하는 거시적 안목"
        ],
        "summary": "새로운 해외 바이어를 발굴하고 가격과 계약을 네고하여 영토를 확장하는 무역의 공격수입니다.",
        "description": "탁월한 친화력과 회복 탄력성으로 전 세계를 누빕니다. 불확실성 속에서도 기회를 포착하며, 바이어와의 라포(Rapport)를 형성하고 수출 판로를 뚫어내는 무역 전선의 개척자입니다.",
        "kpi": "신규 바이어 발굴 건수, 수출 수주액, 신시장 매출 성장률",
        "certs": "국제무역사, 비즈니스 영어 회화, 무역영어 1급",
        "best_match": "해외영업관리 (FDCM) - 공격과 수비의 조화",
        "worst_match": "무역사무 (BDCS) - 서류 규정 vs 빠른 실행"
    },
    "FDCM": {
        "title": "해외영업관리 (어카운트 케어형)",
        "subtitle": "파트너십 가디언",
        "char_name": "철벽 수호자 베어",
        "char_icon": "🐻",
        "char_color": "#0284C7",
        "traits": "대외 조율(F) + 데이터 분석(D) + 규정 준수(C) + 거시적 안목(M)",
        "strengths": [
            "바이어와 생산 공장 사이의 이해관계를 푸는 뛰어난 조율력",
            "오더 접수부터 선적·수금까지 빈틈없이 챙기는 체계적 프로세스 관리력",
            "숫자와 일정 약속을 칼같이 지켜내는 높은 신뢰도"
        ],
        "summary": "확보된 핵심 고객사와의 장기적 신뢰를 유지하고 수금 및 납기 전반을 책임지는 수비 사령관입니다.",
        "description": "바이어의 까다로운 요구와 공장 생산 일정 사이에서 완벽한 밸런스를 잡습니다. 숫자에 밝고 약속을 칼같이 지켜 클라이언트 이탈을 방어하고 채권을 안전하게 회수합니다.",
        "kpi": "기존 바이어 유지율, 납기 준수율(OTD), 미수금 회수율",
        "certs": "무역영어 1급, ERP 정보관리사, 외환전문역",
        "best_match": "해외영업 (FARM) - 딜을 안전하게 매출로 전환",
        "worst_match": "포워딩 운영 (FARS) - 원칙주의 vs 돌발 대처"
    },
    "FARS": {
        "title": "포워딩 운영 (국제물류 조율)",
        "subtitle": "글로벌 트래픽 컨트롤러",
        "char_name": "음속의 물류 여우 폭스",
        "char_icon": "🦊",
        "char_color": "#D97706",
        "traits": "대외 소통(F) + 순발력(A) + 위기 돌파(R) + 일정 디테일(S)",
        "strengths": [
            "물류 딜레이와 결항 등 돌발 위기에 당황하지 않는 실시간 순발력",
            "선사·항공사와의 줄다리기에서 최적의 운임과 공간을 따내는 협상력",
            "복잡한 물류 일정 속에서 작은 시차와 디테일을 놓치지 않는 기민함"
        ],
        "summary": "해상·항공 선복을 확보하고 운임을 네고하며, 딜레이 등 돌발 변수를 실시간 해결하는 물류 해결사입니다.",
        "description": "변수가 일상인 국제물류 현장에서 가장 빛나는 순발력을 자랑합니다. 선사, 항공사, 화주 사이에서 최적의 루트를 번개처럼 짜내고 긴급 상황에서도 선적을 기필코 완수합니다.",
        "kpi": "선복(Space) 매칭률, 운임 마진율, 긴급 대처 속도",
        "certs": "물류관리사, 국제무역사, 위험물운송자격",
        "best_match": "글로벌 SCM (BACM) - 실행과 스케줄링의 융합",
        "worst_match": "FTA 원산지 관리 (BDCM) - 융통성 vs 엄격한 법률"
    },
    "BACM": {
        "title": "글로벌 SCM / 선적 스케줄러",
        "subtitle": "서플라이 체인 지휘관",
        "char_name": "체스 마스터 이글",
        "char_icon": "🦅",
        "char_color": "#4F46E5",
        "traits": "내부 조율(B) + 빠른 실행(A) + 규정 준수(C) + 공급망 거시 시야(M)",
        "strengths": [
            "원자재 조달부터 최종 납품까지 공급망 전체를 조망하는 시스템적 사고",
            "재고 낭비를 줄이고 총물류비를 아끼는 구조적 프로세스 최적화 능력",
            "예상되는 물류 병목 구간을 선제적으로 예측하고 대응하는 리드타임 제어력"
        ],
        "summary": "공장-창고-항만으로 이어지는 글로벌 공급망의 병목을 없애고 리드타임을 최적화하는 물류 전략가입니다.",
        "description": "전 세계 거점 창고의 재고 회전율과 운송 리드타임을 한눈에 조망합니다. 납기 지연을 사전에 방지하고 최적 운송 모드를 설계하여 기업의 총물류비를 혁신적으로 절감합니다.",
        "kpi": "재고 회전일수, 총물류비 절감률, 리드타임 단축",
        "certs": "CPIM, 물류관리사, 유통관리사 1급",
        "best_match": "포워딩 운영 (FARS) - 전략과 현장 조달의 합작",
        "worst_match": "해외영업 (FARM) - 시스템 계획 vs 즉흥적 약속"
    },
    "FDCS": {
        "title": "해외소싱 / 글로벌 구매",
        "subtitle": "원가 핀셋 분석가",
        "char_name": "예리한 올빼미 아울",
        "char_icon": "🦉",
        "char_color": "#0D9488",
        "traits": "대외 네고(F) + 원가 분석(D) + 규정 준수(C) + 센트 단위 디테일(S)",
        "strengths": [
            "제품 원가 명세서와 부품 단가를 센트 단위까지 파헤치는 정밀 분석력",
            "해외 공급사의 숨은 리스크와 제품 결함을 짚어내는 날카로운 검수 안목",
            "마진율을 원천적으로 끌어올리는 끈질긴 가격 협상력"
        ],
        "summary": "전 세계 공급선을 뒤져 최상의 품질과 최저 단가를 협상해 내는 글로벌 원가 파수꾼입니다.",
        "description": "제품의 나사 하나, 포장재 한 장까지 원가를 집요하게 파헤칩니다. 해외 벤더와의 끈질긴 단가 협상력과 현물 검수 감각으로 회사의 마진을 근본적으로 지켜냅니다.",
        "kpi": "구매 원가 절감률(CR), 공급업체 품질 불량률, 적기 납품률",
        "certs": "CPSM, 국제무역사, 원가분석사",
        "best_match": "무역사무 (BDCS) - 소싱 계약의 완벽한 서류화",
        "worst_match": "무역 데이터 분석가 (BDRM) - 실물 협상 vs 데이터 예측"
    },
    "BDCS": {
        "title": "무역사무 / 수출입 통관 지원",
        "subtitle": "서류 무결점 마스터",
        "char_name": "완벽주의 비버",
        "char_icon": "🦫",
        "char_color": "#2563EB",
        "traits": "내부 집중(B) + 데이터 검증(D) + 규정 준수(C) + 오탈자 디테일(S)",
        "strengths": [
            "오탈자 1글자도 허용하지 않는 결벽에 가까운 꼼꼼함과 집중력",
            "인코텀즈, L/C 통일규칙 등 복잡한 무역 법규를 정확히 이행하는 규정 준수력",
            "통관 보류 및 매입 부도를 원천 차단하여 회사의 자산을 지키는 리스크 방어력"
        ],
        "summary": "L/C, B/L, 인보이스 등 무역 서류의 하자 0%를 추구하여 안전한 통관과 외환 네고를 보장하는 행정 스페셜리스트입니다.",
        "description": "단 1글자의 오탈자도 허용하지 않는 결벽에 가까운 철저함을 가졌습니다. 인코텀즈와 은행 신용장 통일규칙(UCP600)을 바탕으로 회사를 무역 사기와 금융 하자로부터 방어합니다.",
        "kpi": "서류 하자율 0건, 통관 지연율 0%, 매입(Nego) 지연 방지",
        "certs": "무역영어 1급, 국제무역사, 보세사",
        "best_match": "해외영업 (FARM) - 오더를 무결점으로 매듭",
        "worst_match": "포워딩 운영 (FARS) - 융통성 처리 vs 철저한 서류주의"
    },
    "BDRM": {
        "title": "무역 데이터 분석가",
        "subtitle": "수출입 빅데이터 나침반",
        "char_name": "알고리즘 돌고래 핀",
        "char_icon": "🐬",
        "char_color": "#7C3AED",
        "traits": "내부 분석(B) + 데이터 논리(D) + 혁신 시도(R) + 거시 시장 통찰(M)",
        "strengths": [
            "수많은 통계와 숫자 속에서 유의미한 비즈니스 패턴을 찾아내는 데이터 통찰력",
            "글로벌 운임과 환율 변동을 예측해 비용을 절감하는 계량적 모델링 감각",
            "복잡한 무역 현황을 명쾌한 시각화 대시보드로 전환하는 전달력"
        ],
        "summary": "HS코드 수출입 통계와 글로벌 운임 빅데이터를 분석해 미래 수요와 새로운 기회를 발굴하는 데이터 항해사입니다.",
        "description": "무역 실무 감각과 데이터 사이언스 역량을 겸비했습니다. 관세청 통계와 선사 API 데이터를 연결하여 환율과 운임 변동을 모델링하고 경영진에게 확실한 데이터 근거를 제시합니다.",
        "kpi": "수요 예측 정확도, 운임 예측 오차율, 대시보드 활용도",
        "certs": "SQLD, 데이터분석준전문가(ADsP), 빅데이터분석기사",
        "best_match": "FTA 원산지 관리 (BDCM) - HS코드와 통상 데이터 시너지",
        "worst_match": "해외소싱 (FDCS) - 현물 감각 vs 정량 알고리즘"
    },
    "BDCM": {
        "title": "FTA 원산지 관리 / 통상 규제 대응",
        "subtitle": "무역 법률·규제 방패",
        "char_name": "철통 방패 판다",
        "char_icon": "🐼",
        "char_color": "#059669",
        "traits": "내부 연구(B) + 법률 데이터(D) + 규정 준수(C) + 통상 정책 거시 시야(M)",
        "strengths": [
            "까다로운 통상 협정과 법령을 정밀하게 해석하는 법률적 논리력",
            "원산지 판정 원칙을 완벽히 소명하여 세관 사후검증을 막아내는 증빙 관리력",
            "글로벌 통상 제재와 친환경 규제(CBAM 등)에 선제 대비하는 컴플라이언스 감각"
        ],
        "summary": "FTA 특혜 관세와 글로벌 통상 제재를 방어하여 관세 추징을 막아내는 무역 규제 수호자입니다.",
        "description": "국제 협정과 관세 법령을 면밀히 분석합니다. 원산지 판정 원칙을 완벽히 수호하여 합법적인 관세 절감 혜택을 챙기고 복잡해지는 무역 규제 리스크로부터 기업을 보호합니다.",
        "kpi": "FTA 활용률, 원산지 사후검증 추징 0건, 규제 위반 0건",
        "certs": "원산지관리사, 보세사, 관세사 1차",
        "best_match": "무역 데이터 분석가 (BDRM) - 규제 데이터 분석 시너지",
        "worst_match": "포워딩 운영 (FARS) - 원칙주의 vs 현장 스케줄 우선"
    }
}

# -------------------------------------------------------------
# 5. 이미지 생성 함수 (Pillow & 한글 폰트 자동 다운로드)
# -------------------------------------------------------------
def get_korean_font(size):
    font_filename = "NanumGothic.ttf"
    # Streamlit Cloud 서버에 폰트가 없으면 구글 폰트 레포에서 자동 다운로드
    if not os.path.exists(font_filename):
        font_url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
        try:
            urllib.request.urlretrieve(font_url, font_filename)
        except Exception:
            pass

    # 다운받은 폰트 파일 열기
    try:
        return ImageFont.truetype(font_filename, size)
    except Exception:
        # 윈도우/맥 기본 폰트 시도
        for local_font in ["malgun.ttf", "AppleGothic.ttf"]:
            try:
                return ImageFont.truetype(local_font, size)
            except Exception:
                continue
        return ImageFont.load_default()

def generate_result_image(job_info, user_code, match_score, f_pct, b_pct, a_pct, d_pct, c_pct, r_pct, m_pct, s_pct):
    width, height = 700, 880
    image = Image.new("RGB", (width, height), color="#F6F7F9")
    draw = ImageDraw.Draw(image)

    font_title = get_korean_font(28)
    font_sub = get_korean_font(18)
    font_body = get_korean_font(15)
    font_small = get_korean_font(13)

    accent_color = job_info.get("char_color", "#243B5A")

    # 1. 상단 카드
    draw.rounded_rectangle([30, 30, 670, 310], radius=18, fill="#FFFFFF", outline="#E4E7EC", width=2)
    draw.rounded_rectangle([30, 30, 670, 42], radius=6, fill=accent_color)

    draw.text((350, 75), "MY TRADE PERSONA", font=font_small, fill="#667085", anchor="mm")
    draw.text((350, 125), str(job_info["char_name"]), font=font_title, fill="#172033", anchor="mm")
    draw.text((350, 175), str(job_info["title"]), font=font_sub, fill=accent_color, anchor="mm")
    draw.text((350, 225), f"성향 코드: {user_code}   |   매칭률: {match_score}%", font=font_body, fill="#475467", anchor="mm")
    
    summary_text = f"\"{job_info['summary']}\""
    if len(summary_text) > 42:
        summary_text = summary_text[:40] + "...\""
    draw.text((350, 265), summary_text, font=font_small, fill="#667085", anchor="mm")

    # 2. DNA 카드
    draw.rounded_rectangle([30, 330, 670, 420], radius=12, fill="#FFFFFF", outline="#E4E7EC", width=1)
    draw.rectangle([30, 330, 38, 420], fill=accent_color)
    draw.text((50, 348), "MY TRADE DNA", font=font_small, fill="#667085")
    draw.text((50, 375), str(job_info["traits"]), font=font_body, fill="#172033")

    # 3. 4대 축 분석 카드
    draw.rounded_rectangle([30, 440, 670, 840], radius=18, fill="#FFFFFF", outline="#E4E7EC", width=2)
    draw.text((50, 465), "나의 무역 성향 4대 축 분석", font=font_sub, fill="#172033")

    axes = [
        ("Front", f_pct, "Back", b_pct, 520),
        ("Action", a_pct, "Data", d_pct, 600),
        ("Compliance", c_pct, "Risk", r_pct, 680),
        ("Macro", m_pct, "Micro", s_pct, 760)
    ]

    for left_label, left_v, right_label, right_v, y in axes:
        draw.text((50, y), f"{left_label} {left_v}%", font=font_body, fill="#344054")
        draw.text((650, y), f"{right_v}% {right_label}", font=font_body, fill="#344054", anchor="ra")

        bar_y = y + 25
        draw.rounded_rectangle([50, bar_y, 650, bar_y + 12], radius=6, fill="#EAECF0")
        split_x = 50 + int((left_v / 100.0) * 600)
        if split_x > 50:
            draw.rounded_rectangle([50, bar_y, split_x, bar_y + 12], radius=6, fill="#5A7394")
        if split_x < 650:
            draw.rounded_rectangle([split_x, bar_y, 650, bar_y + 12], radius=6, fill="#B8C6D6")

    buf = io.BytesIO()
    image.save(buf, format="PNG", optimize=True)
    buf.seek(0)
    return buf.getvalue()

# -------------------------------------------------------------
# 6. 세션 상태
# -------------------------------------------------------------
if "current_idx" not in st.session_state:
    st.session_state.current_idx = 0

if "answers" not in st.session_state:
    st.session_state.answers = {}

# -------------------------------------------------------------
# 7. 공통 헤더
# -------------------------------------------------------------
st.markdown(
    '<div class="main-title">🚢 무역 직무 MBTI 진단 테스트</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">24개 실무 시나리오로 찾는 나의 무역 페르소나 & 맞춤 직무 리포트</div>',
    unsafe_allow_html=True
)

# =============================================================
# 8. INTRO
# =============================================================
if st.session_state.current_idx == 0:

    intro_html = """<div class="intro-box">
<span class="feature-tag">TRADE CAREER MATCHER</span>
<h3 style="color:#172033; margin:4px 0 12px 0; font-size:1.4rem; font-weight:800;">
"무역 분야, 나는 어디서 가장 빛날 수 있을까?"
</h3>
<p style="color:#475467; font-size:0.96rem; line-height:1.75; margin-bottom:12px;">
무역은 단순히 물건을 사고파는 것을 넘어
<strong>영업, 서류 행정, 국제물류, 데이터 분석, 통상 규제</strong>까지
영역별 성격이 매우 뚜렷한 전문 분야입니다.
</p>
<p style="color:#475467; font-size:0.96rem; line-height:1.75; margin-bottom:0;">
실제 무역 실무에서 마주하는 24가지 의사결정 시나리오를 통해
<strong>나의 실무 DNA와 최적의 무역 세부 직무, 그리고 나만의 페르소나 캐릭터</strong>를
진단해 보세요.
</p>
</div>"""
    st.markdown(intro_html, unsafe_allow_html=True)

    st.markdown(
        "<h4 style='color:#172033; font-weight:800;'>🧭 무역 직무 MBTI의 4대 핵심 축</h4>",
        unsafe_allow_html=True
    )

    st.caption(
        "실제 무역 실무에서 자주 마주하는 네 가지 판단 기준을 측정합니다."
    )

    dim_grid_html = """<div class="dim-grid">
<div class="dim-card dim-blue">
<div style="font-size:.94rem;font-weight:800;color:#4778B8;margin-bottom:6px;">
🤝 [F vs B] 업무 반경
</div>
<div style="font-size:.85rem;color:#475467;line-height:1.55;">
• <strong>F (Front)</strong>: 바이어 상담, 운임 네고 등 <strong>대외 협상</strong><br>
• <strong>B (Back)</strong>: 서류 검수, ERP 등록 등 <strong>내부 집중</strong>
</div>
</div>
<div class="dim-card dim-sky">
<div style="font-size:.94rem;font-weight:800;color:#4C8BC5;margin-bottom:6px;">
🎯 [A vs D] 판단 기준
</div>
<div style="font-size:.85rem;color:#475467;line-height:1.55;">
• <strong>A (Action)</strong>: 직관적 기회 포착 및 <strong>현장 감각</strong><br>
• <strong>D (Data)</strong>: 관세율, 원가 분석 등 <strong>정밀 데이터</strong>
</div>
</div>
<div class="dim-card dim-indigo">
<div style="font-size:.94rem;font-weight:800;color:#6573C3;margin-bottom:6px;">
⚖️ [C vs R] 업무 태도
</div>
<div style="font-size:.85rem;color:#475467;line-height:1.55;">
• <strong>C (Compliance)</strong>: 법령 및 규정 <strong>원칙 준수</strong><br>
• <strong>R (Risk-taking)</strong>: 신시장 개척, 유연한 <strong>위기 돌파</strong>
</div>
</div>
<div class="dim-card dim-cyan">
<div style="font-size:.94rem;font-weight:800;color:#5A9A9A;margin-bottom:6px;">
🔭 [M vs S] 시야 범위
</div>
<div style="font-size:.85rem;color:#475467;line-height:1.55;">
• <strong>M (Macro)</strong>: 글로벌 SCM 전체 <strong>거시적 조망</strong><br>
• <strong>S (Micro)</strong>: 원가, B/L 등 <strong>세부 디테일</strong>
</div>
</div>
</div>"""
    st.markdown(dim_grid_html, unsafe_allow_html=True)

    st.write("")

    notice_html = """<div style="background:#FFFFFF; border:1px solid #E4E7EC; border-radius:13px; padding:15px 18px; margin-top:15px; margin-bottom:24px;">
<span style="font-weight:800;color:#172033;">
⏱️ 소요 시간: 약 3분 · 총 24문항
</span><br>
<span style="font-size:.86rem;color:#667085;">
정답은 없습니다. 실제 실무에서 내가 더 편안하게 느낄 선택지를 골라주세요.
</span>
</div>"""
    st.markdown(notice_html, unsafe_allow_html=True)

    if st.button(
        "🚀 나의 무역 직무 MBTI 진단 시작하기",
        use_container_width=True,
        type="primary"
    ):
        st.session_state.answers = {}
        st.session_state.current_idx = 1
        st.rerun()

# =============================================================
# 9. QUESTION
# =============================================================
elif 1 <= st.session_state.current_idx <= 24:

    idx = st.session_state.current_idx
    q = QUESTIONS[idx - 1]

    progress = idx / 24.0
    st.progress(progress)

    st.caption(
        f"📌 **Question {idx:02d} / 24**  ·  진행률 **{int(progress * 100)}%**"
    )

    # 🧭 문항 건너뛰기 전용 네비게이터
    with st.expander("🧭 문항 건너뛰기", expanded=False):
        st.markdown('<div class="nav-grid-container">', unsafe_allow_html=True)
        nav_cols = st.columns(8)
        for i in range(1, 25):
            col_target = nav_cols[(i - 1) % 8]
            with col_target:
                is_curr = (i == idx)
                if st.button(
                    str(i),
                    key=f"nav_q_{i}",
                    use_container_width=True,
                    type="primary" if is_curr else "secondary"
                ):
                    st.session_state.current_idx = i
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # 질문 내용 카드
    q_card_html = f"""<div class="single-q-card">
<div>
<span class="q-step-badge">Question {idx:02d}</span>
<span class="q-dim-text">· {q['dim_name']}</span>
</div>
<div class="q-main-scenario">
{q['scenario']}
</div>
</div>"""
    st.markdown(q_card_html, unsafe_allow_html=True)

    # 선택지 클릭 시 즉시 다음 문항 이동
    if st.button(q["choice_a"], key=f"btn_choice_a_{idx}", use_container_width=True):
        st.session_state.answers[q["id"]] = "A"
        st.session_state.current_idx = idx + 1
        st.rerun()

    if st.button(q["choice_b"], key=f"btn_choice_b_{idx}", use_container_width=True):
        st.session_state.answers[q["id"]] = "B"
        st.session_state.current_idx = idx + 1
        st.rerun()

    st.write("")

    # 이전 문항 이동 버튼
    prev_label = "🏠 처음으로" if idx == 1 else "⬅️ 이전 문항"
    if st.button(prev_label, use_container_width=True):
        st.session_state.current_idx -= 1
        st.rerun()

# =============================================================
# 10. RESULT
# =============================================================
elif st.session_state.current_idx == 25:

    st.balloons()

    # ---------------------------------------------------------
    # 점수 계산
    # ---------------------------------------------------------
    counts = {
        "F": 0, "B": 0,
        "A": 0, "D": 0,
        "C": 0, "R": 0,
        "M": 0, "S": 0
    }

    for q in QUESTIONS:
        ans = st.session_state.answers.get(q["id"])
        if ans == "A":
            counts[q["trait_a"]] += 1
        elif ans == "B":
            counts[q["trait_b"]] += 1

    dim1 = "F" if counts["F"] >= counts["B"] else "B"
    dim2 = "A" if counts["A"] >= counts["D"] else "D"
    dim3 = "C" if counts["C"] >= counts["R"] else "R"
    dim4 = "M" if counts["M"] >= counts["S"] else "S"

    user_code = f"{dim1}{dim2}{dim3}{dim4}"

    # ---------------------------------------------------------
    # 직무 점수
    # ---------------------------------------------------------
    job_scores = {}

    for j_code, info in JOBS.items():
        score = 0
        score += (counts[j_code[0]] / 6.0) * 25
        score += (counts[j_code[1]] / 6.0) * 25
        score += (counts[j_code[2]] / 6.0) * 25
        score += (counts[j_code[3]] / 6.0) * 25
        job_scores[j_code] = round(score, 1)

    best_job_code = max(job_scores, key=job_scores.get)
    best_job = JOBS[best_job_code]

    # ---------------------------------------------------------
    # 4대 축 비율
    # ---------------------------------------------------------
    f_pct = int((counts["F"] / 6) * 100)
    b_pct = 100 - f_pct

    a_pct = int((counts["A"] / 6) * 100)
    d_pct = 100 - a_pct

    c_pct = int((counts["C"] / 6) * 100)
    r_pct = 100 - c_pct

    m_pct = int((counts["M"] / 6) * 100)
    s_pct = 100 - m_pct

    # ---------------------------------------------------------
    # RESULT HERO (캐릭터 카드)
    # ---------------------------------------------------------
    hero_html = f"""<div style="background:#FFFFFF; border:1px solid #E4E7EC; border-radius:22px; overflow:hidden; margin-bottom:14px; box-shadow:0 8px 25px rgba(16,24,40,.06);">
<div style="height:7px; background:{best_job['char_color']};"></div>
<div style="text-align:center; padding:35px 22px 30px;">
<div style="font-size:4.2rem; line-height:1; margin-bottom:14px;">{best_job['char_icon']}</div>
<div style="display:inline-block; font-size:.72rem; font-weight:800; letter-spacing:.1em; color:{best_job['char_color']}; background:#F7F8FA; border:1px solid #E4E7EC; padding:5px 12px; border-radius:999px;">MY TRADE PERSONA</div>
<h1 style="font-size:2.05rem; margin:12px 0 6px; font-weight:900; letter-spacing:-.035em; color:#172033;">{best_job['char_name']}</h1>
<div style="font-size:1.18rem; font-weight:800; color:{best_job['char_color']}; margin-bottom:10px;">{best_job['title']}</div>
<div style="font-size:.9rem; color:#667085;">
성향 코드 <strong style="color:#172033;">{user_code}</strong>
<span style="margin:0 5px;">·</span>
매칭률 <strong style="color:#172033;">{job_scores[best_job_code]}%</strong>
</div>
</div>
</div>"""
    st.markdown(hero_html, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # 결과지 이미지 생성 및 다운로드 버튼 (Pillow 기반)
    # ---------------------------------------------------------
    img_bytes = generate_result_image(
        best_job, user_code, job_scores[best_job_code],
        f_pct, b_pct, a_pct, d_pct, c_pct, r_pct, m_pct, s_pct
    )

    st.download_button(
        label="🖼️ 결과지 이미지로 저장",
        data=img_bytes,
        file_name=f"trade_mbti_{best_job_code}.png",
        mime="image/png",
        use_container_width=True
    )

    st.write("")

    # ---------------------------------------------------------
    # DNA
    # ---------------------------------------------------------
    dna_html = f"""<div style="background:#F9FAFB; border:1px solid #E4E7EC; border-left:4px solid {best_job['char_color']}; border-radius:13px; padding:15px 17px; margin-bottom:26px;">
<div style="font-size:.76rem; font-weight:800; color:#667085; margin-bottom:5px; letter-spacing:.04em;">MY TRADE DNA</div>
<div style="font-size:.94rem; font-weight:700; color:#344054; line-height:1.55;">{best_job['traits']}</div>
</div>"""
    st.markdown(dna_html, unsafe_allow_html=True)

    # =========================================================
    # 4대 축
    # =========================================================
    st.markdown(
        "<h3 class='result-section-title'>📊 나의 무역 성향 4대 축 분석</h3>",
        unsafe_allow_html=True
    )

    def render_axis(left_name, left_val, right_name, right_val, sub_left, sub_right):
        return f"""<div class="axis-card">
<div class="axis-header">
<span class="axis-name">{left_name} <span style="color:#172033;">{left_val}%</span></span>
<span class="axis-name"><span style="color:#172033;">{right_val}%</span> {right_name}</span>
</div>
<div class="axis-bar">
<div class="axis-left" style="width:{left_val}%;"></div>
<div class="axis-right" style="width:{right_val}%;"></div>
</div>
<div class="axis-caption">
<span>{sub_left}</span>
<span>{sub_right}</span>
</div>
</div>"""

    axis_cols = st.columns(2)

    with axis_cols[0]:
        st.markdown(
            render_axis(
                "Front", f_pct,
                "Back", b_pct,
                "대외 미팅 · 바이어 협상",
                "내부 서류 · ERP 시스템"
            ),
            unsafe_allow_html=True
        )

        st.markdown(
            render_axis(
                "Compliance", c_pct,
                "Risk", r_pct,
                "규정 준수 · 원칙 중심",
                "도전 · 위기 돌파"
            ),
            unsafe_allow_html=True
        )

    with axis_cols[1]:
        st.markdown(
            render_axis(
                "Action", a_pct,
                "Data", d_pct,
                "직관적 실행 · 기회 포착",
                "정밀 수치 · 데이터 분석"
            ),
            unsafe_allow_html=True
        )

        st.markdown(
            render_axis(
                "Macro", m_pct,
                "Micro", s_pct,
                "글로벌 구조 · 전체 조망",
                "세부 수치 · 디테일"
            ),
            unsafe_allow_html=True
        )

    st.write("")
    st.divider()

    # =========================================================
    # 8대 직무 레이더
    # =========================================================
    st.markdown(
        "<h3 class='result-section-title'>🎯 8대 무역 직무 적합도</h3>",
        unsafe_allow_html=True
    )

    categories = [
        JOBS[code]["title"].split(" (")[0]
        for code in job_scores.keys()
    ]

    values = list(job_scores.values())

    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]

    fig = go.Figure(
        data=go.Scatterpolar(
            r=values_closed,
            theta=categories_closed,
            fill="toself",
            fillcolor="rgba(74,111,159,0.10)",
            line=dict(
                color="#4A6F9F",
                width=2
            ),
            marker=dict(
                size=6,
                color="#344E6F"
            )
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(
                    size=10,
                    color="#98A2B3"
                ),
                linecolor="#EAECF0",
                gridcolor="#EAECF0"
            ),
            angularaxis=dict(
                tickfont=dict(
                    size=10,
                    color="#344054",
                    family="sans-serif"
                ),
                linecolor="#EAECF0",
                gridcolor="#EAECF0"
            ),
            bgcolor="#FFFFFF"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(l=35, r=35, t=25, b=25),
        height=380
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =========================================================
    # 1순위 직무
    # =========================================================
    st.markdown(
        "<h3 class='result-section-title'>🏆 1순위 추천 직무 심층 분석</h3>",
        unsafe_allow_html=True
    )

    strength_items_html = "".join(
        [
            f"<li style='margin-bottom:7px; color:#344054;'>{s}</li>"
            for s in best_job["strengths"]
        ]
    )

    detail_card_html = f"""<div class="detail-card">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px; flex-wrap:wrap; gap:8px;">
<span style="font-size:1.3rem; font-weight:900; color:#172033;">{best_job['title']}</span>
<span style="background:#F7F8FA; border:1px solid #E4E7EC; color:{best_job['char_color']}; font-weight:800; font-size:.86rem; padding:5px 12px; border-radius:999px;">매칭률 {job_scores[best_job_code]}%</span>
</div>
<p style="font-size:1rem; font-weight:700; color:#344054; margin-bottom:18px; line-height:1.65; border-left:4px solid {best_job['char_color']}; padding-left:12px;">"{best_job['summary']}"</p>
<div style="padding:16px 18px; background:#F8F9FB; border:1px solid #EAECF0; border-radius:13px; margin-bottom:18px;">
<div style="font-size:.94rem; font-weight:800; color:{best_job['char_color']}; margin-bottom:8px;">🌟 나의 무역 핵심 강점 3가지</div>
<ul style="font-size:.9rem; line-height:1.65; margin-bottom:0; padding-left:20px;">{strength_items_html}</ul>
</div>
<div style="font-size:.91rem; line-height:1.75; color:#475467;">
<p style="margin-bottom:7px;">💡 <strong style="color:#172033;">업무 성향 매칭:</strong> {best_job['traits']}</p>
<p style="margin-bottom:7px;">📌 <strong style="color:#172033;">업무 스타일:</strong> {best_job['description']}</p>
<p style="margin-bottom:7px;">🎯 <strong style="color:#172033;">핵심 관리 KPI:</strong> {best_job['kpi']}</p>
<p style="margin-bottom:0;">📜 <strong style="color:#172033;">추천 자격증 & 핵심 역량:</strong> {best_job['certs']}</p>
</div>
<div style="margin-top:18px; padding:15px 16px; background:#FAFBFC; border:1px solid #E4E7EC; border-radius:13px; font-size:.88rem; line-height:1.6;">
<div style="color:#344054; font-weight:700;">🤝 <strong>찰떡 파트너 직무:</strong> {best_job['best_match']}</div>
<div style="margin-top:9px; color:#B42318; font-weight:700;">⚠️ <strong>주의가 필요한 상극 직무:</strong> {best_job['worst_match']}</div>
</div>
</div>"""

    st.markdown(detail_card_html, unsafe_allow_html=True)

    # =========================================================
    # 전체 순위
    # =========================================================
    with st.expander("📊 전체 8개 직무 적합도 순위표"):

        ranking_data = []

        for code, score in sorted(
            job_scores.items(),
            key=lambda x: x[1],
            reverse=True
        ):
            ranking_data.append({
                "순위": len(ranking_data) + 1,
                "직무명": JOBS[code]["title"],
                "캐릭터": JOBS[code]["char_name"],
                "적합도(%)": f"{score}%",
                "매칭 코드": code
            })

        st.dataframe(
            pd.DataFrame(ranking_data),
            use_container_width=True,
            hide_index=True
        )

    # =========================================================
    # 다시 하기
    # =========================================================
    st.write("")

    if st.button(
        "🔄 테스트 다시 하기",
        use_container_width=True
    ):
        st.session_state.current_idx = 0
        st.session_state.answers = {}
        st.rerun()