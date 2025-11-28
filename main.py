# main.py
import streamlit as st
from load import update_lotto_db
import os

lotto_db = update_lotto_db()

# 세션 상태
if "selected" not in st.session_state:
    st.session_state.selected = []

# 진짜 동행복권 디자인 CSS (모바일 완벽 지원!)
st.set_page_config(page_title="로또 당첨 확인기", page_icon="four_leaf_clover", layout="centered")
st.markdown("""
<style>
    .main {background: #003366; padding: 20px; min-height: 100vh; font-family: 'Malgun Gothic', sans-serif;}
    .title {font-size: 2.8rem; color: #ffd700; text-align: center; margin: 20px 0; text-shadow: 3px 3px 8px #000;}
    .subtitle {color: #fff; text-align: center; font-size: 1.2rem; margin-bottom: 30px;}
    
    /* 진짜 로또 공 스타일 */
    .lotto-ball {
        width: 60px; height: 60px; border-radius: 50%; display: flex; 
        align-items: center; justify-content: center; font-size: 24px; 
        font-weight: bold; color: white; margin: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        transition: all 0.2s ease;
    }
    .ball-1 {background: #fbc400;}   /* 1~10 */
    .ball-2 {background: #69c8f2;}   /* 11~20 */
    .ball-3 {background: #ff7272;}   /* 21~30 */
    .ball-4 {background: #aaa;}      /* 31~40 */
    .ball-5 {background: #b0d840;}   /* 41~45 */
    
    .selected-ball {transform: scale(1.15); box-shadow: 0 0 20px gold, 0 8px 20px rgba(0,0,0,0.7) !important;}
    .bonus {background: #ffcc00 !important; color: black !important;}
    
    .number-grid {display: grid; grid-template-columns: repeat(auto-fit, minmax(70px, 1fr)); gap: 12px; padding: 20px;}
    .selected-display {background: rgba(255,255,255,0.2); padding: 20px; border-radius: 20px; text-align: center; margin: 20px 0;}
    
    @media (max-width: 600px) {
        .lotto-ball {width: 50px; height: 50px; font-size: 20px;}
        .title {font-size: 2.2rem;}
    }
</style>
""", unsafe_allow_html=True)

# 메인 UI
st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown('<h1 class="title">로또 당첨 확인기</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">진짜 로또 공을 클릭해서 6개 선택하세요!</p>', unsafe_allow_html=True)

# 선택된 번호 표시
selected_sorted = sorted(st.session_state.selected)
if selected_sorted:
    bonus = "" if len(selected_sorted) < 7 else f" + <span class='lotto-ball bonus'>{selected_sorted[6]}</span>"
    balls = " ".join([f"<span class='lotto-ball ball-{(n-1)//10 + 1} selected-ball'>{n}</span>" for n in selected_sorted[:6]])
    st.markdown(f"<div class='selected-display'><h2>내 번호: {balls}{bonus}</h2></div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='selected-display'><h2>아직 선택되지 않음</h2></div>", unsafe_allow_html=True)

# 번호 선택 그리드
st.markdown("<div class='number-grid'>", unsafe_allow_html=True)
for num in range(1, 46):
    color_class = f"ball-{(num-1)//10 + 1}"
    is_selected = num in st.session_state.selected
    ball_class = f"lotto-ball {color_class} {'selected-ball' if is_selected else ''}"
    
    if st.button(str(num), key=f"ball_{num}", help=f"{num}번"):
        if is_selected:
            st.session_state.selected.remove(num)
        elif len(st.session_state.selected) < 6:
            st.session_state.selected.append(num)
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# 초기화
col1, col2, col3 = st.columns(3)
with col2:
    if st.button("번호 초기화", use_container_width=True):
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
            result += f"<div style='background:rgba(255,255,255,0.2);padding:20px;margin:10px 0;border-radius:15px;'>"
            result += f"<h3 style='color:gold; margin:0;'>제 {no}회 ({info['date']}) → {rank} 당첨!!!</h3>"
            balls = " ".join([f"<span class='lotto-ball ball-{(n-1)//10 + 1}'>{n}</span>" for n in info["numbers"]])
            result += f"<p>당첨번호: {balls} + <span class='lotto-ball bonus'>{info['bonus']}</span></p></div>"
            found = True
    
    if found:
        st.success("축하합니다!!! 당첨된 회차가 있어요!!!")
        st.balloons()
    else:
        st.info("4등 이상 당첨된 적 없네요... 다음 기회에!")
    
    if result:
        st.markdown(result, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.caption("진짜 로또 디자인 with ❤️ by Grok + 당신")
