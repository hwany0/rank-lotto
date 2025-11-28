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

# 완전히 깨끗한 화면 (네모, 헤더, 푸터 전부 제거 + 배경 깔끔하게)
st.set_page_config(
    page_title="로또 6/45",
    page_icon="four_leaf_clover",
    layout="centered"
)

st.markdown(
    """
<style>
    /* Streamlit 기본 요소 완전 제거 */
    #MainMenu, header, footer {visibility: hidden !important;}
    .stApp > div:first-child {background: none !important;}
    .block-container {padding-top: 0rem !important; padding-bottom: 0rem !important;}
    
    /* 진짜 로또 배경 */
    body {
        background: linear-gradient(to bottom, #003087, #001f5a);
        color: white;
        font-family: 'Malgun Gothic', sans-serif;
        margin: 0;
        min-height: 100vh;
    }

    /* 로또 공 디자인 (선택된 번호 표시용) */
    .ball {
        width: 72px; height: 72px; border-radius: 50%; display: inline-flex;
        align-items: center; justify-content: center; font-size: 28px; font-weight: bold;
        color: white; margin: 10px; box-shadow: 0 6px 15px rgba(0,0,0,0.6);
        transition: all 0.2s ease; border: 4px solid #fff;
    }
    .ball-1 {background: #fbc400;} 
    .ball-2 {background: #69c8f2;} 
    .ball-3 {background: #ff7272;} 
    .ball-4 {background: #aaa;} 
    .ball-5 {background: #b0d840;}
    .selected {transform: scale(1.25); box-shadow: 0 0 30px gold !important; z-index: 10;}

    /* Streamlit 버튼들을 공 모양으로 */
    div.stButton > button {
        width: 72px;
        height: 72px;
        border-radius: 50%;
        font-size: 22px;
        font-weight: bold;
        margin: 6px;
        border: 3px solid #ffffffaa;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        background: #004aad;
        color: #fff;
    }

    /* 타이틀 */
    .title {
        font-size: 3.5rem; 
        color: #ffd700; 
        text-align: center; 
        margin: 30px 0; 
        text-shadow: 3px 3px 12px #000;
    }
</style>
""",
    unsafe_allow_html=True,
)

# 타이틀
st.markdown('<h1 class="title">로또 6/45 당첨 확인기</h1>', unsafe_allow_html=True)

# 선택된 번호 표시 (위에 예쁘게 공으로)
if st.session_state.selected:
    balls = "".join(
        [
            f"<span class='ball ball-{(n-1)//10 + 1} selected'>{n}</span>"
            for n in sorted(st.session_state.selected)
        ]
    )
    st.markdown(
        f"<div style='text-align:center; padding:30px;'>{balls}</div>",
        unsafe_allow_html=True,
    )

st.markdown("### 번호를 선택하세요 (최대 6개)")

# 🔹 여기서부터: 9열 그리드 (st.columns 사용)
cols = st.columns(9)

for num in range(1, 46):
    col = cols[(num - 1) % 9]
    with col:
        # 버튼에 선택 여부 반영 (색 조금 바꾸고 싶으면 여기에서 조건 분기해서 CSS 더 줄 수 있음)
        if st.button(str(num), key=f"n{num}"):
            if num in st.session_state.selected:
                st.session_state.selected.remove(num)
            elif len(st.session_state.selected) < 6:
                st.session_state.selected.append(num)
            st.rerun()

st.write("")  # 살짝 아래 여백

# 초기화 버튼
if st.button("번호 초기화", use_container_width=True):
    st.session_state.selected = []
    st.rerun()

# 결과
if len(st.session_state.selected) == 6:
    my_set = set(st.session_state.selected)
    found = False
    result = ""

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
                [
                    f"<span class='ball ball-{(n-1)//10 + 1}'>{n}</span>"
                    for n in info["numbers"]
                ]
            )

            result += (
                "<div style='background:rgba(255,255,255,0.15); "
                "padding:30px; margin:20px auto; border-radius:20px; "
                "max-width:700px; text-align:center;'>"
            )
            result += f"<h3 style='color:gold; margin:10px;'>제 {no}회 → {rank} 당첨!!!</h3>"
            result += (
                f"<p style='margin:15px 0; font-size:1.5rem;'>{win_balls} + "
                f"<span class='ball bonus'>{info['bonus']}</span></p>"
            )
            result += f"<small style='color:#ccc;'>{info['date']}</small></div>"
            found = True

    if found:
        st.balloons()
        st.success("축하합니다!!! 당첨됐어요!!!")
    else:
        st.info("4등 이상 없네요... 다음 기회에!")

    st.markdown(result, unsafe_allow_html=True)
