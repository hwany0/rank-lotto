# main.py
import streamlit as st
from load import update_lotto_db
import os

# 로또 데이터 로드
@st.cache_data(ttl=86400)
def get_db():
    return update_lotto_db()

lotto_db = get_db()

# 세션 상태
if "selected" not in st.session_state:
    st.session_state.selected = []

# 진짜 로또 공 디자인 + 깜빡임 없이 부드럽게!
st.set_page_config(page_title="로또 6/45 당첨 확인기", page_icon="https://www.dhlottery.co.kr/images/common/favicon.ico")
st.markdown("""
<style>
    .main {background: linear-gradient(to bottom, #003087, #001f5a); padding: 20px; min-height: 100vh;}
    .title {font-size: 3rem; color: #ffd700; text-align: center; margin: 20px 0; text-shadow: 3px 3px 8px #000;}
    
    /* 진짜 로또 공 */
    .ball {
        width: 60px; height: 60px; border-radius: 50%; display: inline-flex;
        align-items: center; justify-content: center; font-size: 24px; font-weight: bold;
        color: white; margin: 6px; box-shadow: inset 0 4px 8px rgba(255,255,255,0.3), 0 4px 10px rgba(0,0,0,0.5);
        transition: all 0.15s ease;
    }
    .ball-1 {background: #fbc400;}  /* 1~10 */
    .ball-2 {background: #69c8f2;}  /* 11~20 */
    .ball-3 {background: #ff7272;}  /* 21~30 */
    .ball-4 {background: #aaa;}      /* 31~40 */
    .ball-5 {background: #b0d840;}  /* 41~45 */
    
    .selected {transform: scale(1.2); box-shadow: 0 0 25px gold, 0 8px 20px rgba(0,0,0,0.8) !important;}
    .bonus {background: #ffcc00 !important; color: black !important;}
    
    .grid {display: grid; grid-template-columns: repeat(9, 1fr); gap: 12px; justify-items: center; padding: 20px;}
    @media (max-width: 600px) {
        .grid {grid-template-columns: repeat(6, 1fr); gap: 10px;}
        .ball {width: 50px; height: 50px; font-size: 20px;}
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown('<h1 class="title">로또 6/45 당첨 확인기</h1>', unsafe_allow_html=True)

# 선택된 번호 표시 (진짜 로또처럼!)
if st.session_state.selected:
    balls = ""
    for n in sorted(st.session_state.selected):
        color = f"ball-{(n-1)//10 + 1}"
        balls += f'<span class="ball {color} selected">{n}</span>'
    st.markdown(f"<div style='text-align:center; padding:20px; background:rgba(255,255,255,0.1); border-radius:20px;'>{balls}</div>", unsafe_allow_html=True)
else:
    st.markdown("<div style='text-align:center; padding:20px; color:#ccc; font-size:1.5rem;'>번호를 선택하세요!</div>", unsafe_allow_html=True)

# 번호 그리드 (9열 고정, 모바일은 6열)
st.markdown("<div class='grid'>", unsafe_allow_html=True)
for num in range(1, 46):
    color_class = f"ball-{(num-1)//10 + 1}"
    is_selected = num in st.session_state.selected
    ball_style = f"ball {color_class} {'selected' if is_selected else ''}"
    
    if st.button(str(num), key=f"n{num}"):
        if is_selected:
            st.session_state.selected.remove(num)
        elif len(st.session_state.selected) < 6:
            st.session_state.selected.append(num)
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# 초기화
if st.button("번호 초기화", use_container_width=True):
    st.session_state.selected = []
    st.rerun()

# 6개 다 선택하면 자동 확인 (깜빡임 없이!)
if len(st.session_state.selected) == 6:
    my_set = set(st.session_state.selected)
    found = False
    result = ""
    
    for no, info in lotto_db.items():
        match = len(my_set & set(info["numbers"]))
        if match >= 4:
            rank = "1등" if match==6 else "2등" if match==5 and info["bonus"] in my_set else "3등" if match==5 else "4등"
            win_balls = " ".join([f"<span class='ball ball-{(n-1)//10 + 1}'>{n}</span>" for n in info["numbers"]])
            result += f"<div style='background:rgba(255,255,255,0.2); padding:20px; margin:15px 0; border-radius:15px; text-align:center;'>"
            result += f"<h3 style='color:gold; margin:0;'>제 {no}회 → {rank} 당첨!!!</h3>"
            result += f"<p style='margin:10px 0; font-size:1.3rem;'>{win_balls} + <span class='ball bonus'>{info['bonus']}</span></p>"
            result += f"<small style='color:#ccc;'>{info['date']}</small></div>"
            found = True
    
    if found:
        st.success("축하합니다!!! 당첨된 회차가 있어요!!!")
        st.balloons()
    else:
        st.info("4등 이상 당첨된 적 없네요... 다음 기회에!")
    
    st.markdown(result, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.caption("")
