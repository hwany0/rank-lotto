# main.py
import streamlit as st
from load import update_lotto_db
import os

# 로또 데이터 로드 (최초 1회만 다운로드)
@st.cache_data(ttl=86400)
def get_db():
    return update_lotto_db()

lotto_db = get_db()

# 세션 상태 초기화
if "selected" not in st.session_state:
    st.session_state.selected = []

# 진짜 동행복권 디자인 + 모바일 완벽
st.set_page_config(page_title="로또 6/45 당첨 확인기", page_icon="https://www.dhlottery.co.kr/images/common/favicon.ico", layout="centered")
st.markdown("""
<style>
    .main {background: linear-gradient(to bottom, #003087, #001f5a); color: white; min-height: 100vh; padding: 20px; font-family: 'Malgun Gothic', sans-serif;}
    .title {font-size: 3.2rem; color: #ffd700; text-align: center; margin: 20px 0; text-shadow: 3px 3px 10px #000;}
    .subtitle {text-align: center; font-size: 1.4rem; color: #ccc; margin-bottom: 30px;}
    
    .ball {width: 70px; height: 70px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center;
           font-size: 28px; font-weight: bold; color: white; margin: 8px; box-shadow: 0 6px 15px rgba(0,0,0,0.6);
           transition: all 0.2s ease;}
    .ball-1 {background: #fbc400;} .ball-2 {background: #69c8f2;} .ball-3 {background: #ff7272;}
    .ball-4 {background: #aaa;} .ball-5 {background: #b0d840;}
    .selected {transform: scale(1.25); box-shadow: 0 0 30px gold, 0 10px 30px rgba(0,0,0,0.8) !important;}
    .bonus {background: #ffcc00 !important; color: black !important;}
    
    .grid {display: grid; grid-template-columns: repeat(9, 1fr); gap: 15px; justify-items: center; padding: 20px;}
    @media (max-width: 600px) {.grid {grid-template-columns: repeat(6, 1fr); gap: 12px;}}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown('<h1 class="title">로또 6/45 당첨 확인기</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">진짜 로또 공을 클릭해서 6개 선택하세요!</p>', unsafe_allow_html=True)

# 선택된 번호 표시
if st.session_state.selected:
    balls = "".join([f'<span class="ball ball-{(n-1)//10 + 1} selected">{n}</span>' 
                     for n in sorted(st.session_state.selected)])
    st.markdown(f"<div style='text-align:center; padding:30px; background:rgba(255,255,255,0.1); border-radius:20px;'>{balls}</div>", 
                unsafe_allow_html=True)
else:
    st.markdown("<div style='text-align:center; padding:30px; color:#666; font-size:1.5rem;'>번호를 선택하세요!</div>", unsafe_allow_html=True)

# 진짜 로또 공 그리드 (줄바꿈 완전 없음!)
st.markdown("<div class='grid'>", unsafe_allow_html=True)
for num in range(1, 46):
    color = f"ball-{(num-1)//10 + 1}"
    selected = "selected" if num in st.session_state.selected else ""
    
    if st.button(str(num), key=f"ball_{num}"):
        if num in st.session_state.selected:
            st.session_state.selected.remove(num)
        elif len(st.session_state.selected) < 6:
            st.session_state.selected.append(num)
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# 초기화 버튼
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("번호 초기화", type="secondary", use_container_width=True):
        st.session_state.selected = []
        st.rerun()

# 6개 다 선택하면 자동 확인
if len(st.session_state.selected) == 6:
    my_set = set(st.session_state.selected)
    found = False
    result = ""
    
    for no, info in lotto_db.items():
        match = len(my_set & set(info["numbers"]))
        if match >= 4:
            rank = "1등" if match==6 else "2등" if match==5 and info["bonus"] in my_set else "3등" if match==5 else "4등"
            win_balls = " ".join([f"<span class='ball ball-{(n-1)//10 + 1}'>{n}</span>" for n in info["numbers"]])
            result += f"<div style='background:rgba(255,255,255,0.15); padding:25px; margin:15px 0; border-radius:20px; text-align:center;'>"
            result += f"<h3 style='color:gold; margin:0;'>제 {no}회 → {rank} 당첨!!!</h3>"
            result += f"<p style='margin:15px 0; font-size:1.3rem;'>{win_balls} + <span class='ball bonus'>{info['bonus']}</span></p>"
            result += f"<small style='color:#aaa;'>{info['date']}</small></div>"
            found = True
    
    if found:
        st.success("축하합니다!!! 당첨된 회차가 있어요!!!")
        st.balloons()
    else:
        st.info("4등 이상 당첨된 적 없네요... 다음 기회에!")
    
    st.markdown(result, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.caption("")
