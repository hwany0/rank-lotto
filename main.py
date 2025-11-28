# main.py
import streamlit as st
from load import update_lotto_db
import os

# 로또 데이터 로드
@st.cache_data(ttl=86400)
def get_db():
    return update_lotto_db()

lotto_db = get_db()

if "selected" not in st.session_state:
    st.session_state.selected = []

# 완전히 깨끗한 화면 (네모, 헤더, 푸터 전부 제거 + 배경 깔끔하게!)
st.set_page_config(page_title="로또 6/45", page_icon="four_leaf_clover", layout="centered")
st.markdown("""
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
    
    /* 로또 공 디자인 */
    .ball {
        width: 72px; height: 72px; border-radius: 50%; display: inline-flex;
        align-items: center; justify-content: center; font-size: 28px; font-weight: bold;
        color: white; margin: 10px; box-shadow: 0 6px 15px rgba(0,0,0,0.6);
        transition: all 0.2s ease; border: 4px solid #fff;
    }
    .ball-1 {background: #fbc400;} .ball-2 {background: #69c8f2;} 
    .ball-3 {background: #ff7272;} .ball-4 {background: #aaa;} 
    .ball-5 {background: #b0d840;}
    .selected {transform: scale(1.25); box-shadow: 0 0 30px gold !important; z-index: 10;}
    
    /* 9열 완벽 그리드 */
    .number-grid {
        display: grid; grid-template-columns: repeat(9, 1fr);
        gap: 20px; justify-items: center; max-width: 900px; margin: 40px auto;
    }
    @media (max-width: 600px) {
        .number-grid {grid-template-columns: repeat(6, 1fr); gap: 15px;}
        .ball {width: 58px; height: 58px; font-size: 22px;}
    }
    
    .title {font-size: 3.5rem; color: #ffd700; text-align: center; margin: 30px 0; text-shadow: 3px 3px 12px #000;}
</style>
""", unsafe_allow_html=True)

# 타이틀
st.markdown('<h1 class="title">로또 6/45 당첨 확인기</h1>', unsafe_allow_html=True)

# 선택된 번호 표시
if st.session_state.selected:
    balls = "".join([f'<span class="ball ball-{(n-1)//10 + 1} selected">{n}</span>' 
                     for n in sorted(st.session_state.selected)])
    st.markdown(f"<div style='text-align:center; padding:30px;'>{balls}</div>", unsafe_allow_html=True)

# 번호 그리드
st.markdown('<div class="number-grid">', unsafe_allow_html=True)
for num in range(1, 46):
    color = f"ball-{(num-1)//10 + 1}"
    selected = "selected" if num in st.session_state.selected else ""
    
    if st.button(str(num), key=f"n{num}"):
        if num in st.session_state.selected:
            st.session_state.selected.remove(num)
        elif len(st.session_state.selected) < 6:
            st.session_state.selected.append(num)
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# 초기화
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
            rank = "1등" if match==6 else "2등" if match==5 and info["bonus"] in my_set else "3등" if match==5 else "4등"
            win_balls = " ".join([f"<span class='ball ball-{(n-1)//10 + 1}'>{n}</span>" for n in info["numbers"]])
            result += f"<div style='background:rgba(255,255,255,0.15); padding:30px; margin:20px auto; border-radius:20px; max-width:700px; text-align:center;'>"
            result += f"<h3 style='color:gold; margin:10px;'>제 {no}회 → {rank} 당첨!!!</h3>"
            result += f"<p style='margin:15px 0; font-size:1.5rem;'>{win_balls} + <span class='ball bonus'>{info['bonus']}</span></p>"
            result += f"<small style='color:#ccc;'>{info['date']}</small></div>"
            found = True
    
    if found:
        st.balloons()
        st.success("축하합니다!!! 당첨됐어요!!!")
    else:
        st.info("4등 이상 없네요... 다음 기회에!")
    
    st.markdown(result, unsafe_allow_html=True)
