# main.py
import streamlit as st
from load import update_lotto_db
import os

@st.cache_data(ttl=86400)
def get_db():
    return update_lotto_db()

lotto_db = get_db()

if "selected" not in st.session_state:
    st.session_state.selected = []

st.set_page_config(
    page_title="로또 6/45",
    page_icon="four_leaf_clover",
    layout="centered",
)

# ===================== CSS =====================
st.markdown(
    """
<style>
    /* 기본 스트림릿 요소 제거 */
    #MainMenu, header, footer {visibility: hidden !important;}
    .stApp > div:first-child {background: none !important;}
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }

    /* 전체 배경 */
    body {
        background: linear-gradient(to bottom, #003087, #001f5a);
        color: white;
        font-family: 'Malgun Gothic', sans-serif;
        margin: 0;
        min-height: 100vh;
    }

    /* 타이틀 */
    .title {
        font-size: 3.5rem;
        color: #ffd700;
        text-align: center;
        margin: 30px 0 10px 0;
        text-shadow: 3px 3px 12px #000;
    }

    /* 선택된 번호 표시 공 */
    .ball {
        width: 72px; height: 72px; border-radius: 50%;
        display: inline-flex; align-items: center; justify-content: center;
        font-size: 28px; font-weight: bold;
        color: white; margin: 10px;
        box-shadow: 0 6px 15px rgba(0,0,0,0.6);
        transition: all 0.2s ease; border: 4px solid #fff;
    }
    .ball-1 {background: #fbc400;}  /* 1~10 노랑 */
    .ball-2 {background: #69c8f2;}  /* 11~20 파랑 */
    .ball-3 {background: #ff7272;}  /* 21~30 빨강 */
    .ball-4 {background: #aaaaaa;}  /* 31~40 회색 */
    .ball-5 {background: #b0d840;}  /* 41~45 초록 */
    .selected {
        transform: scale(1.25);
        box-shadow: 0 0 30px gold !important;
    }

    /* 상단 기능 버튼(번호 초기화) */
    button[aria-label="번호 초기화"] {
        width: 200px !important;
        height: 42px !important;
        border-radius: 999px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        margin: 10px auto 20px auto !important;
        display: block !important;
        background: rgba(255,255,255,0.15) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255,255,255,0.5) !important;
    }
    button[aria-label="번호 초기화"]:hover {
        background: rgba(255,255,255,0.3) !important;
    }

    /* 번호 선택 버튼 공 모양 기본 스타일 */
    div.stButton > button {
        width: 72px;
        height: 72px;
        border-radius: 50%;
        font-size: 22px;
        font-weight: bold;
        margin: 6px;
        border: 3px solid #ffffffaa;
        color: #fff;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        transition: 0.1s ease;
        background: #004aad;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        filter: brightness(1.05);
    }

    /* 번호별 실제 로또 공 색상 적용 */
    /* 1~10: 노랑 */
    button[aria-label="1"],
    button[aria-label="2"],
    button[aria-label="3"],
    button[aria-label="4"],
    button[aria-label="5"],
    button[aria-label="6"],
    button[aria-label="7"],
    button[aria-label="8"],
    button[aria-label="9"],
    button[aria-label="10"] {
        background: #fbc400 !important;
    }

    /* 11~20: 파랑 */
    button[aria-label="11"],
    button[aria-label="12"],
    button[aria-label="13"],
    button[aria-label="14"],
    button[aria-label="15"],
    button[aria-label="16"],
    button[aria-label="17"],
    button[aria-label="18"],
    button[aria-label="19"],
    button[aria-label="20"] {
        background: #69c8f2 !important;
    }

    /* 21~30: 빨강 */
    button[aria-label="21"],
    button[aria-label="22"],
    button[aria-label="23"],
    button[aria-label="24"],
    button[aria-label="25"],
    button[aria-label="26"],
    button[aria-label="27"],
    button[aria-label="28"],
    button[aria-label="29"],
    button[aria-label="30"] {
        background: #ff7272 !important;
    }

    /* 31~40: 회색 */
    button[aria-label="31"],
    button[aria-label="32"],
    button[aria-label="33"],
    button[aria-label="34"],
    button[aria-label="35"],
    button[aria-label="36"],
    button[aria-label="37"],
    button[aria-label="38"],
    button[aria-label="39"],
    button[aria-label="40"] {
        background: #aaaaaa !important;
    }

    /* 41~45: 초록 */
    button[aria-label="41"],
    button[aria-label="42"],
    button[aria-label="43"],
    button[aria-label="44"],
    button[aria-label="45"] {
        background: #b0d840 !important;
    }

</style>
""",
    unsafe_allow_html=True,
)

# ===================== UI =====================

# 타이틀
st.markdown('<h1 class="title">로또 6/45 당첨 확인기</h1>', unsafe_allow_html=True)

# 상단 기능 버튼 (번호 초기화)
if st.button("번호 초기화", key="reset_btn"):
    st.session_state.selected = []
    st.experimental_rerun()

# 선택된 번호 표시
if st.session_state.selected:
    balls = "".join(
        f"<span class='ball ball-{(n-1)//10 + 1} selected'>{n}</span>"
        for n in sorted(st.session_state.selected)
    )
    st.markdown(
        f"<div style='text-align:center;'>{balls}</div>",
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        "<p style='text-align:center;'>6개의 번호를 선택하세요.</p>",
        unsafe_allow_html=True,
    )

st.markdown("")

# 번호 선택 그리드 (9열 고정)
cols = st.columns(9)
for num in range(1, 46):
    col = cols[(num - 1) % 9]
    with col:
        if st.button(str(num), key=f"n{num}"):
            if num in st.session_state.selected:
                st.session_state.selected.remove(num)
            elif len(st.session_state.selected) < 6:
                st.session_state.selected.append(num)
            st.experimental_rerun()

# ===================== 결과 =====================
if len(st.session_state.selected) == 6:
    my_set = set(st.session_state.selected)
    result_html = ""
    found = False

    for no, info in lotto_db.items():
        match = len(my_set & set(info["numbers"]))

        if match >= 4:
            if match == 6:
                rank = "1등"
            elif match == 5 and info["bonus"] in my_set:
                rank = "2등"
            elif match == 5:
                rank = "3등"
            else:
                rank = "4등"

            win_balls = " ".join(
                f"<span class='ball ball-{(n-1)//10 + 1}'>{n}</span>"
                for n in info["numbers"]
            )

            result_html += f"""
            <div style='background:rgba(255,255,255,0.15);
                        padding:30px; margin:20px auto; border-radius:20px;
                        max-width:700px; text-align:center;'>
                <h3 style='color:gold;'>제 {no}회 → {rank} 당첨!!!</h3>
                <p style='font-size:1.5rem;'>{win_balls}
                    + <span class='ball ball-5'>{info['bonus']}</span>
                </p>
                <small style='color:#ccc;'>{info['date']}</small>
            </div>
            """
            found = True

    if found:
        st.balloons()
        st.success("축하합니다! 당첨입니다!")
    else:
        st.info("4등 이상 당첨 없음. 다음 기회에!")

    st.markdown(result_html, unsafe_allow_html=True)
